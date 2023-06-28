import unittest
import os
from pathlib import Path
import shutil
import pandas as pd
import pyarrow as pa
from ds_capability import SyntheticBuilder
from ds_capability.intent.synthetic_intent import SyntheticIntentModel
from aistac.properties.property_manager import PropertyManager

# Pandas setup
pd.set_option('max_colwidth', 320)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 99)
pd.set_option('expand_frame_repr', True)


class SyntheticTest(unittest.TestCase):

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

    def test_for_smoke(self):
        sb = SyntheticBuilder.from_memory()
        tools: SyntheticIntentModel = sb.tools
        tbl = tools.model_synthetic_data_types(100)
        self.assertEqual((100, 7), tbl.shape)
        tbl = tools.model_synthetic_data_types(100, inc_nulls=True, p_nulls=0.03)
        self.assertEqual((100, 13), tbl.shape)
        self.assertEqual(3, tbl.column('int_null').null_count)

    def test_model_analysis(self):
        sb = SyntheticBuilder.from_memory()
        tools: SyntheticIntentModel = sb.tools
        sb.add_connector_uri('sample', './working/data.sample.parquet')
        tbl = tools.model_synthetic_data_types(10)
        sb.save_canonical('sample', tbl)
        result = tools.model_analysis(20,'sample')
        print(result.schema)

    def test_model_noise(self):
        sb = SyntheticBuilder.from_memory()
        tools: SyntheticIntentModel = sb.tools
        tbl = tools.model_noise(10, num_columns=3)
        self.assertEqual((10, 3), tbl.shape)
        self.assertEqual(['A', 'B', 'C'], tbl.column_names)
        tbl = tools.model_noise(10, num_columns=3, name_prefix='P_')
        self.assertEqual(['P_A', 'P_B', 'P_C'], tbl.column_names)



    def test_raise(self):
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
