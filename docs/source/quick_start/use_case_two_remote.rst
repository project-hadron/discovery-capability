Use Case Two: Churn Pipeline
============================

To this point we have created our project Hadron pipeline and the associated capability
recipes for that pipeline. This next section shows how to build associative synthetic
data and use that through our pre-defined and re-usable pipeline.

The first step is to import the required packages, with FeatureSelect and FeatureEngineer
used for our synthetic data build, and FeaturePredict used to observe the pipeline outcome.
For the purposes of re-running our pipeline only Controller is required.

.. code-block:: python

    import os
    from ds_capability import FeatureSelect, FeatureEngineer, FeaturePredict, Controller

uc2: Synthesize
---------------

Our next step is to build the synthetic data using the sample data. Will initialize our two
classes using the `from_memory()` factory class method. These instantiate the classes in
memory only thus not storing any of the capability recipe. We do this as the creation of
the synthetic data is a one-off activity, not to be repeated.

The synthetic data action calls do not expect a source, just the number of rows
to be produced. We therefore don't need to set the source directly. It does however
expect a named connector contract to provide a sample to be synthesized. Here we
use the method `add_connector_uri` to add to the named connector.

.. code-block:: python

    syn_fe = FeatureEngineer.from_memory()
    syn_ds = FeatureSelect.from_memory()
    
    syn_fe.add_connector_uri('sample', 'https://raw.githubusercontent.com/project-hadron/hadron-asset-bank/master/datasets/toy_sample/churn.csv')
    
    syn_fe.set_persist_uri('./hadron/data/synthetic_churn.parquet')

Once set, we use the FeatureEngineer action intent called `get_analysis_group` to
analyze the passed sample and provide a synthetic data set of row size two thousands.
In this case, to provide us more accuracy in our results, we separate our analysis
by the  `Exited` labels.

In addition we also need to ensure our synthetic data includes a unique identifier,
which would have been compromised in the analysis. We therefore create a new set of
values using the `get_number`.

.. code-block:: python

    tbl = syn_fe.tools.get_analysis_group(size=10_000, other='sample', group_by='Exited')
    tbl = syn_fe.tools.get_number(16_000_000, 19_999_999, at_most=1, size=10_000,
                                  relative_freq=[99, 20, 5, 1],
                                  to_header='CustomerId', canonical=tbl)

Once complete, we then drop the target column `Exited` to drop the labels from the
dataset.

.. code-block:: python

    tbl = syn_ds.tools.auto_drop_columns(tbl, headers=['Exited'])

We then directly save our synthetic dataset for retrieval by our predictive model.

.. code-block:: python

    syn_fe.save_persist_canonical(tbl)


uc2: Remote Run
---------------

With our synthetic data now created, we are ready to run our component pipeline.
In the first instance we set our our predictive source, in this case our synthetic
data, and the location of where to put the results. As you can see the use of
:ref:`environment<Environment>` variables gives us flexibility as we move, or share,
environments.

Having taken our pipeline recipes, including the Controller, and put it into
a repository that is retrievable, we can now point to the location of that
repository.

.. code-block:: python

    os.environ['HADRON_CHURN_SOURCE_PATH'] = './hadron/data/synthetic_churn.parquet'
    os.environ['HADRON_CHURN_PERSIST_PATH'] = './hadron/data/hadron_docs_churn_predict.parquet'

    os.environ['HADRON_PM_REPO'] = 'https://raw.githubusercontent.com/project-hadron/hadron-asset-bank/master/contracts/pyarrow/docs/use_case_two/'

We can now simply create the instance of our controller, using the `from_env` factory
class method, and running the controller.

.. code-block:: python

    ctrl = Controller.from_env('churn')
    ctrl.run_controller()

uc2: View Remote
----------------

We can check our results by loading the canonical at the end of our pipeline. We
do this by creating the instance of our named capability, FeaturePredict, and loading the
persisted canonical. We can then view the resulting table.

.. code-block:: python

    FeaturePredict.from_env('churn').load_persist_canonical()


.. parsed-literal::

    pyarrow.Table
    CustomerId: int64
    predict: int64
    ----
    CustomerId: [[16891877,17196600,18805763,16499576,17418890,...,17097895,17219861,17332523,16025422,16692638]]
    predict: [[0,1,0,0,0,...,1,1,1,0,1]]



