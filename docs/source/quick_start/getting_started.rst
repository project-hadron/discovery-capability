.. code-block:: python

    # saves you having to use print as all exposed variables are printed in the cell
    from IPython.core.interactiveshell import InteractiveShell
    InteractiveShell.ast_node_interactivity = "all"

First Feature Actions
---------------------

example table
~~~~~~~~~~~~~

.. code-block:: python

    import pyarrow as pa
    
    tbl = pa.table({
        "col1": [0, 2, None, 3, 1, None, 2, 2, 3, 1],
        "col2": [0]*10
    })
    
    tbl




.. parsed-literal::

    pyarrow.Table
    col1: int64
    col2: int64
    ----
    col1: [[0,2,null,3,1,null,2,2,3,1]]
    col2: [[0,0,0,0,0,0,0,0,0,0]]



feature selection
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ds_capability import FeatureSelect
    
    fs = FeatureSelect.from_memory()
    tbl = fs.tools.auto_drop_noise(tbl)
    
    tbl




.. parsed-literal::

    pyarrow.Table
    col1: int64
    ----
    col1: [[0,2,null,3,1,null,2,2,3,1]]



feature Engineering
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ds_capability import FeatureEngineer
    
    fe = FeatureEngineer.from_memory()
    tbl = fe.tools.model_missing(tbl)
    
    tbl




.. parsed-literal::

    pyarrow.Table
    col1: int64
    ----
    col1: [[0,2,2,3,1,1,2,2,3,1]]



feature transformation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ds_capability import FeatureTransform
    
    ft = FeatureTransform.from_memory()
    tbl = ft.tools.scale_normalize(tbl)
    
    tbl




.. parsed-literal::

    pyarrow.Table
    col1: double
    ----
    col1: [[0,0.67,0.67,1,0.33,0.33,0.67,0.67,1,0.33]]



Data Retrieval
--------------

.. code-block:: python

    from ds_capability import FeatureSelect
    
    fs = FeatureSelect.from_memory()

default location
~~~~~~~~~~~~~~~~

.. code-block:: python

    fs.set_source('<file_name.ext>')
    fs.set_persist()

default full path or database uri
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    fs.set_source_uri('<uri>')
    fs.set_persist_uri('<uri>')

named location
~~~~~~~~~~~~~~

.. code-block:: python

    fs.add_connector_source('<name>', '<file_name.ext>')
    fs.add_connector_persist('<name>', '<file_name.ext>')

named full path or database uri
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    fs.add_connector_uri('<name>', '<uri>')

Environment
-----------

When creating the instance of our capability, this time we guide it
towards the environment to set up, providing a reference name to
retrieve this instance settings from a persisted state. This allows us
to run our instance of this capability in changing environments
dynamically.

.. code-block:: python

    from ds_capability import FeatureSelect
    
    fs = FeatureSelect.from_env('task_name', has_contract=False)

example default enironment
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os
    
    os.environ['HADRON_DEFAULT_PATH'] = './default/path'
    os.environ['HADRON_PM_PATH'] = './pm/path'
    os.environ['HADRON_PM_TYPE'] = 'json'

.. code-block:: python

    fs.set_source('file_name.ext')
    fs.set_persist()

example bespoke enironment
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os
    
    os.environ['HADRON_SOURCE_DATA'] = './path/source/raw_data.csv'
    os.environ['HADRON_PERSIST_DATA'] = 's3://<bucket>/<path>/cleaned_data.parquet'

.. code-block:: python

    fs.set_source_uri('${HADRON_SOURCE_DATA}')
    fs.set_persist_uri('${HADRON_PERSIST_DATA}')

Data Cleaner Pipeline
---------------------

.. code-block:: python

    from ds_capability import Controller, FeatureSelect
    import os

dynamic data location
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    os.environ['HADRON_CLEAN_SOURCE_URI'] = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv'
    os.environ['HADRON_CLEAN_PERSIST_URI'] = 'duckdb://getting_started'

data clean receipe
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    fs = FeatureSelect.from_env('auto_clean', has_contract=False)
    fs.set_source_uri('${HADRON_CLEAN_SOURCE_URI}')
    fs.set_persist_uri('${HADRON_CLEAN_PERSIST_URI}')
    
    tbl = fs.load_source_canonical()
    tbl = fs.tools.auto_clean_header(tbl)
    tbl = fs.tools.auto_drop_noise(tbl)
    tbl = fs.tools.auto_drop_correlated(tbl)
    tbl = fs.tools.auto_drop_duplicates(tbl)

controller
~~~~~~~~~~

.. code-block:: python

    ctr = Controller.from_env(has_contract=False)

.. code-block:: python

    ctr.register.feature_select('auto_clean')

Reusing the Pipeline
--------------------

.. code-block:: python

    from ds_capability import Controller
    import os
    
    os.environ['HADRON_CLEAN_SOURCE_URI'] = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv'
    os.environ['HADRON_CLEAN_PERSIST_URI'] = 'duckdb://getting_started'
    
    os.environ['HADRON_PM_REPO'] = './hadron/contracts/'

.. code-block:: python

    ctr = Controller.from_env()
    ctr.run_controller()

Review Results
~~~~~~~~~~~~~~

.. code-block:: python

    ctr.set_persist_uri('duckdb://getting_started')

.. code-block:: python

    ctr.load_persist_canonical().column_names




.. parsed-literal::

    ['total_bill', 'tip', 'sex', 'smoker', 'day', 'time', 'size']



