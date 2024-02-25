import os
import pyarrow as pa
import pyarrow.compute as pc
from ds_core.handlers.abstract_handlers import AbstractSourceHandler, AbstractPersistHandler
from ds_core.handlers.abstract_handlers import ConnectorContract, HandlerFactory

class MlflowSourceHandler(AbstractSourceHandler):
    """ A DuckDB source handler"""

    def __init__(self, connector_contract: ConnectorContract):
        """ initialise the Handler passing the source_contract dictionary """
        # required module import
        self.mlflow = HandlerFactory.get_module('mlflow')
        super().__init__(connector_contract)
        # connection
        self.connection = self.mlflow.set_tracking_uri(uri=f"{connector_contract.schema}://{connector_contract.address}")
        # address
        self.experiment = connector_contract.path
        self._changed_flag = True

    def supported_types(self) -> list:
        return ['parquet']

    def exists(self) -> bool:
        _kwargs = self.connector_contract.query
        table = _kwargs.pop('table', 'hadron_table')
        result = self.connection.execute("CALL duckdb_tables()").arrow()
        return pc.is_in(table, result.column('table_name')).as_py()

    def has_changed(self) -> bool:
        return True

    def reset_changed(self, changed: bool=None):
        """ manual reset to say the file has been seen. This is automatically called if the file is loaded"""
        changed = changed if isinstance(changed, bool) else False
        self._changed_flag = changed

    def load_canonical(self, **kwargs) -> pa.Table:
        _kwargs = {**self.connector_contract.query, **kwargs}
        table = _kwargs.pop('table', 'hadron_table')
        if table.startswith("s3://"):
            return self.connection.execute(f"SELECT * FROM read_parquet('{table}')").arrow()
        elif table.startswith('https://'):
            return self.connection.execute(f"SELECT * FROM read_parquet('{table}')").arrow()
        query = _kwargs.pop('sql_query', f"SELECT * FROM {table};")
        query = query.replace('@', table)
        return self.connection.execute(query).arrow()


class MlflowPersistHandler(MlflowSourceHandler, AbstractPersistHandler):

    def persist_canonical(self, canonical: pa.Table, **kwargs) -> bool:
        """ persists the canonical dataset
        """
        if not isinstance(self.connector_contract, ConnectorContract):
            return False
        with self.mlflow.start_run():
            model_info = self.mlflow.sklearn.log_model(sk_model=lr, artifact_path="iris_model")

    def remove_canonical(self, **kwargs) -> bool:
        return True

    def backup_canonical(self, canonical: pa.Table, uri: str, **kwargs) -> bool:
        pass

