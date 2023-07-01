import unittest
from timeit import timeit
import os
from pathlib import Path
import shutil
import pandas as pd
import pyarrow as pa
from aistac import ConnectorContract
from ds_discovery import SyntheticBuilder, Transition
from ds_discovery.intent.synthetic_intent import SyntheticIntentModel
from aistac.properties.property_manager import PropertyManager

from ds_capability.handlers.pyarrow_handlers import PyarrowSourceHandler, PyarrowPersistHandler

# Pandas setup
pd.set_option('max_colwidth', 320)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 99)
pd.set_option('expand_frame_repr', True)


class PyarrowHandlerTest(unittest.TestCase):

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
        os.environ['HADRON_PM_PATH'] = Path('working/contracts').as_posix()
        os.environ['HADRON_PM_TYPE'] = 'parquet'
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

    def test_runs(self):
        """Basic smoke test"""
        PyarrowSourceHandler(ConnectorContract('work/data/0_raw/example01.csv', '', '', file_type='csv'))
        PyarrowPersistHandler(ConnectorContract('work/data/2_transition/example01.pq', '', '', file_type='parquet'))

    def test_for_smoke(self):
        print(timeit('10+37', number=10))

    def test_parquet(self):
        pp = PyarrowPersistHandler(ConnectorContract('working/data/test.parquet', '', '', file_type='parquet'))
        ps = PyarrowSourceHandler(ConnectorContract('working/data/test.parquet', '', '', file_type='parquet'))
        tbl = self.tbl(10_000_000)

        pp.persist_canonical(tbl)
        result = ps.load_canonical()
        print(result.schema)




    @staticmethod
    def tbl(size=10, extended=False):
        sb = SyntheticBuilder.from_memory()
        tr = Transition.from_memory()
        df = sb.tools.get_synthetic_data_types(size, extended=extended)
        df = tr.tools.auto_transition(df, inc_category=True)
        return pa.Table.from_pandas(df, preserve_index=False)

    def test_raise(self):
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
