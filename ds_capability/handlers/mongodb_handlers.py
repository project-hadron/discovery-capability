# Developing Mongo Persist Handler
import ast
import pyarrow as pa
from ds_core.handlers.abstract_handlers import AbstractSourceHandler, AbstractPersistHandler
from ds_core.handlers.abstract_handlers import HandlerFactory, ConnectorContract
from ds_capability.components.commons import Commons


class MongodbSourceHandler(AbstractSourceHandler):
    """ A mongoDB source handler"""

    def __init__(self, connector_contract: ConnectorContract):
        """ initialise the Handler passing the source_contract dictionary """
        # required module import
        self.mongo = HandlerFactory.get_module('pymongo')
        super().__init__(connector_contract)

        _kwargs = {**self.connector_contract.kwargs, **self.connector_contract.query}
        database = connector_contract.path[1:]

        self.collection_name = _kwargs.pop('collection', "hadron_default")
        self._mongo_find = ast.literal_eval(_kwargs.pop('find')) if _kwargs.get('find') else {}
        self._mongo_aggregate = ast.literal_eval(_kwargs.pop('aggregate')) if _kwargs.get('aggregate') else None
        self._mongo_project = ast.literal_eval(_kwargs.pop('project')) if _kwargs.get('project') else None
        self._mongo_limit = _kwargs.pop('limit') if _kwargs.get('limit') else None
        self._mongo_skip = _kwargs.pop('skip') if _kwargs.get('skip') else None

        self._if_exists = _kwargs.pop('if_exists', 'replace')
        self._file_state = 0
        self._changed_flag = True

        self._mongo_database = self.mongo.MongoClient(self.connector_contract.address)[database]
        self._mongo_collection = self._mongo_database[self.collection_name]

    def supported_types(self) -> list:
        """ The source types supported with this module"""
        return ['mongodb']

    def load_canonical(self, **kwargs) -> pa.Table:
        """ returns the canonical dataset based on the source contract
            The canonical in this instance is a dictionary that has the headers as the key and then
            the ordered list of values for that header
        """
        if not isinstance(self.connector_contract, ConnectorContract):
            raise ValueError("The PandasSource Connector Contract has not been set")

        if self._mongo_aggregate is not None:
            _ = list(self._mongo_collection.aggregate(self._mongo_aggregate))
            return Commons.table_flatten(pa.Table.from_pylist(_))
        cursor = self._mongo_collection.find(self._mongo_find, self._mongo_project)
        if self._mongo_limit is not None:
            cursor.limit(self._mongo_limit)
        if self._mongo_skip is not None:
            cursor.skip(self._mongo_skip)
        return Commons.table_flatten(pa.Table.from_pylist(list(cursor)))

    def exists(self) -> bool:
        """ returns True if the collection exists """
        return self.collection_name in self._mongo_database.list_collection_names()

    def has_changed(self) -> bool:
        """ returns the amount of documents in the collection
            ... if the counts change ... then the collection was probably modified ...
            ... this assumes that records are never edited/updated ... nor deleted ...
        """
        _cc = self.connector_contract
        state = self._mongo_collection.count_documents(self._mongo_find)
        if state != self._file_state:
            self._changed_flag = True
            self._file_state = state
        return self._changed_flag

    def reset_changed(self, changed: bool = False):
        """ manual reset to say the file has been seen. This is automatically called if the file is loaded"""
        changed = changed if isinstance(changed, bool) else False
        self._changed_flag = changed


class MongodbPersistHandler(MongodbSourceHandler, AbstractPersistHandler):
    # a mongoDB persist handler

    def persist_canonical(self, canonical: pa.Table, **kwargs) -> bool:
        """ persists the canonical dataset
        """
        if not isinstance(self.connector_contract, ConnectorContract):
            return False
        _uri = self.connector_contract.uri
        return self.backup_canonical(canonical=canonical, collection_name=self.collection_name, **kwargs)

    def backup_canonical(self, canonical: pa.Table, collection_name: str, **kwargs) -> bool:
        """  creates a backup of the canonical to an alternative table """
        if not isinstance(self.connector_contract, ConnectorContract):
            return False
        _collection = self._mongo_database[collection_name]
        resp = _collection.insert_many(Commons.table_nest(canonical))
        return resp.acknowledged

    def remove_canonical(self) -> bool:
        if not isinstance(self.connector_contract, ConnectorContract):
            return False
        if self.exists():
            return self._mongo_database.drop_collection(self.collection_name).acknowledged
        return False
