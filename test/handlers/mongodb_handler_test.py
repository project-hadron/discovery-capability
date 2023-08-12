import unittest
import os
from pathlib import Path
import shutil
import pyarrow as pa
from ds_core.handlers.abstract_handlers import ConnectorContract
from ds_core.properties.property_manager import PropertyManager
from ds_capability import FeatureBuild


class MongodbHandlerTest(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # clean out any old environments
        for key in os.environ.keys():
            if key.startswith('HADRON'):
                del os.environ[key]
        # Local Domain Contract
        os.environ['HADRON_PM_PATH'] = os.path.join('working', 'contracts')
        os.environ['HADRON_PM_TYPE'] = 'json'
        # Local Connectivity
        os.environ['HADRON_DEFAULT_PATH'] = Path('working/data').as_posix()
        # Specialist Component
        try:
            os.makedirs(os.environ['HADRON_PM_PATH'])
        except OSError:
            pass
        try:
            os.makedirs(os.environ['HADRON_DEFAULT_PATH'])
        except OSError:
            pass
        PropertyManager._remove_all()

    def tearDown(self):
        try:
            shutil.rmtree('working')
        except OSError:
            pass

    def test_handler_default(self):
        fb = FeatureBuild.from_memory()
        tbl = fb.tools.get_synthetic_data_types(size=1_000)
        fb.set_persist_uri("mongodb://admin:admin@localhost:27017/synthetic")
        fb.remove_canonical(fb.CONNECTOR_PERSIST)
        self.assertFalse(fb.pm.get_connector_handler(fb.CONNECTOR_PERSIST).exists())
        fb.save_persist_canonical(tbl)
        result = fb.load_persist_canonical()
        self.assertTrue(fb.pm.get_connector_handler(fb.CONNECTOR_PERSIST).exists())
        self.assertEqual((1000, 6), result.shape)
        self.assertEqual(['cat', 'num', 'int', 'bool', 'date', 'string'], result.columns.to_list())
        fb.remove_canonical(fb.CONNECTOR_PERSIST)

    def test_handler_query(self):
        fb = FeatureBuild.from_memory()
        tbl = fb.tools.get_synthetic_data_types(size=1_000)
        os.environ['collection'] = 'hadron_table'
        uri = "mongodb://localhost:27017/test?collection=${collection}&&find={}&&project={'cat':1, 'num':1, 'string':0}"
        fb.set_persist_uri(uri=uri)
        fb.remove_canonical(fb.CONNECTOR_PERSIST)
        fb.save_persist_canonical(tbl)
        result = fb.load_persist_canonical()
        self.assertEqual((1000, 2), result.shape)
        self.assertEqual(['cat', 'num'], result.columns.to_list())
        fb.remove_canonical(fb.CONNECTOR_PERSIST)

    def test_handler_find_limit(self):
        fb = FeatureBuild.from_memory()
        tbl = fb.tools.get_synthetic_data_types(size=1_000)
        os.environ['collection'] = 'hadron_table'
        uri = "mongodb://localhost:27017/synthetic?collection=${collection}&&find={}&&project={'cat':1, 'num':1, '_id':0}&&limit=2&&skip=2&&sort=[('cat', 1)]"
        fb.set_persist_uri(uri=uri)
        fb.remove_canonical(fb.CONNECTOR_PERSIST)
        fb.save_persist_canonical(tbl)
        result = fb.load_persist_canonical()
        self.assertEqual((2, 2), result.shape)
        self.assertEqual(['cat', 'num'], result.columns.to_list())
        fb.remove_canonical(fb.CONNECTOR_PERSIST)

    def test_handler_aggregate(self):
        fb = FeatureBuild.from_memory()
        tbl = fb.tools.get_synthetic_data_types(size=1_000)
        os.environ['collection'] = 'hadron_table'
        uri = "mongodb://localhost:27017/test?collection=${collection}&&aggregate=[{'$count': 'count'}]"
        fb.set_persist_uri(uri=uri)
        fb.remove_canonical(fb.CONNECTOR_PERSIST)
        fb.save_persist_canonical(tbl)
        result = fb.load_persist_canonical()
        self.assertEqual((1, 1), result.shape)
        self.assertEqual(1000, result['count'].iloc[0])
        fb.remove_canonical(fb.CONNECTOR_PERSIST)

    def test_connector_contract(self):
        os.environ['HADRON_ADDITION'] = 'myAddition'
        os.environ['collection'] = 'hadron_table'
        uri = "mongodb://localhost:27017/test?collection=${collection}&&aggregate=[{'$match':{'cat':'ACTIVE'}}, '$count': 'count']"
        cc = ConnectorContract(uri=uri, module_name='', handler='', addition='${HADRON_ADDITION}')
        print(f"raw_uri = {cc.raw_uri}")
        print(f"uri = {cc.uri}")
        print(f"raw_kwargs = {cc.raw_kwargs}")
        print(f"address = {cc.address}")
        print(f"schema = {cc.schema}")
        print(f"hostname = {cc.hostname}")
        print(f"port = {cc.port}")
        print(f"username = {cc.username}")
        print(f"password = {cc.password}")
        print(f"path = {cc.path}")
        print(f"database = {cc.path[1:]}")
        print(f"query")
        extra = cc.query.pop('extra', None)
        print(f" extra = {extra}")
        find = cc.query.pop('find', None)
        print(f" mongo_find = {find}")
        aggregate = cc.query.pop('aggregate', None)
        print(f" mongo_aggregate = {aggregate}")
        collection = cc.query.pop('collection', None)
        print(f" collection = {collection}")
        print(f"kwargs")
        addition = cc.kwargs.get('addition', None)
        print(f" addition = {addition}")

    def test_raise(self):
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
