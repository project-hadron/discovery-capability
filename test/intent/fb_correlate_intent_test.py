import unittest
import os
from pathlib import Path
import shutil
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from ds_capability import FeatureBuild
from ds_capability.intent.feature_build_intent import FeatureBuildIntentModel
from aistac.properties.property_manager import PropertyManager

# Pandas setup
pd.set_option('max_colwidth', 320)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 99)
pd.set_option('expand_frame_repr', True)


class FeatureBuilderTest(unittest.TestCase):

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
        try:
            shutil.copytree('../_test_data', os.path.join(os.environ['PWD'], 'working/source'))
        except OSError:
            pass
        PropertyManager._remove_all()

    def tearDown(self):
        try:
            shutil.rmtree('working')
        except OSError:
            pass

    def test_for_smoke(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntentModel = fb.tools
        tbl = tools.get_synthetic_data_types(100)
        self.assertEqual((100, 6), tbl.shape)

    def test_correlate_descrete_intervals(self):
        fb = FeatureBuild.from_memory()
        tools: FeatureBuildIntentModel = fb.tools
        tbl = tools.get_synthetic_data_types(100)
        result = tools.correlate_discrete_intervals(tbl, header='num', column_name='num')
        self.assertEqual(3, pc.count(result.column('num').combine_chunks().dictionary).as_py())
        result = tools.correlate_discrete_intervals(tbl, header='num', categories=['low', 'mid', 'high'], column_name='num')
        self.assertCountEqual(['high', 'mid', 'low'], result.column('num').combine_chunks().dictionary.to_pylist())
        result = tools.correlate_discrete_intervals(tbl, header='num', granularity=[0.25,0.5,0.75],
                                                    categories=['0%->25%', '25%->50%', '50%->75%', '75%->100%'], column_name='num')
        self.assertCountEqual(['0%->25%', '25%->50%', '50%->75%', '75%->100%'], result.column('num').combine_chunks().dictionary.to_pylist())

    def test_raise(self):
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
