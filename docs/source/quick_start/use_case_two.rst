Use Case Two: Churn
===================

In this second use case we will look at something a little more practical, in this case
customer churn. We are going to work through preprocessing followed by model predict,
then wrap the capabilities as a pipeline :ref:`recipe<How are capabilities reusable?>`
that defines our microservice.

Business Objective
------------------

Churn prediction
~~~~~~~~~~~~~~~~

Predict if a bank’s customers is likely to leave or not

For this use case we are going to use a customer banking dataset for a classification
model. In this use case the emphasis is much more on the transition of the data to
optimize the features for the chosen model.

Setup
~~~~~

Initially import our capability classes, and then any environment variables required. In this
case we are dynamically annotating for the input of the raw data location and the output of the
model prediction.

.. code-block::  python

    import os
    from ds_capability import FeatureSelect, FeatureEngineer,
    from ds_capability import FeatureTransform, AutoML, Controller

.. code-block::  python

    os.environ['HADRON_CHURN_SOURCE_PATH'] = 'https://raw.githubusercontent.com/project-hadron/hadron-asset-bank/master/datasets/toy_sample/churn.csv'
    os.environ['HADRON_CHURN_PERSIST_PATH'] = './hadron/data/hadron_docs_churn_predict.parquet'

Exploratory Data Analysis
-------------------------

With any preprocessing, the initial stages are to do exploratory data analysis, but this
is outside the scope of this lesson and as such is briefly shown as one of the
pre-processing reports on data profiling. This gives us a view of the attributes, the
data quality and observations of its content.

.. image:: /source/_images/quick_start/qs_use_case_2_dictionary.png
  :align: center
  :width: 700

Preprocessing
-------------

In our preprocessing we are going to use FeatureSelect to remove columns of no interest,
and FeatureTransition for feature optimization.

Selection
~~~~~~~~~~~~~~~~~

Common across all capabilities, we initialize our component and use the factory class method
`from_env` to create an instance of our FeatureSelect. The method call looks to the environment
to reference any global variables, in this case `HADRON_PREDICT_SOURCE_DATA`, which is a pointer
to our raw data source.

In the third line we create a pointer to our persistent data, in this case an in-memory event
store, and finally load the data as our canonical, a PyArrow Table.

.. code-block::  python

    fs = FeatureSelect.from_env('churn', has_contract=False)
    fs.set_source_uri('${HADRON_CHURN_SOURCE_PATH}')
    fs.set_persist_uri('event://select')
    tbl = fs.load_source_canonical()

Before we start processing our data, the data contains the Exited labels used to train the data.
This will not be in our production data and as such not preprocessed so we need to set it aside
for the model classification.

Beyond our source and persist pointers we can also create named pointer using `add_connector_uri`,
extract the `Exited` column and save it to the connector uri. In the second line we use
`auto_drop_columns` with the `drop=True`. This reverses the effect of the call and drops
everything except the `Exited` column returning only this column, which we save (in the
next line)

.. code-block::  python

    # label
    fs.add_connector_uri('label', uri='event://label')
    label = fs.tools.auto_drop_columns(tbl, headers=['Exited'], drop=True)
    fs.save_canonical('label', label)

Using the same method we now drop all unwanted columns and return our new reduced canonical.

.. code-block::  python

    tbl = fs.tools.auto_drop_columns(tbl, headers=['Surname', 'RowNumber', 'Exited'])

Finally we run the capability pipeline to ensure everything works.

.. code-block::  python

    fs.run_component_pipeline()

Transformation
~~~~~~~~~~~~~~~~~~~~~~

FeatureTransition capability provides scaling, discretion and encoding but as before
we initialize our component and use the factory class method `from_env` to create an
instance of our class. We create pointers to our source, being a pointer to our previous
FeatureSelect capability output, and set the persist, then load the canonical.

.. code-block::  python

    ft = FeatureTransform.from_env('churn', has_contract=False)
    
    ft.set_source_uri('event://select')
    ft.set_persist_uri('event://transform')
    
    tbl = ft.load_source_canonical()

Encode
^^^^^^

Initial we take our categoricals and encode them as one-hot.

.. code-block::  python

    # robust encode to negate outliers
    tbl = ft.tools.encode_category_one_hot(tbl, headers=['Gender', 'Geography'], drop_first=True)

Discretize
^^^^^^^^^^

Next we use various techniques to build numerically representative discrete categories of
some of our continuous values.

.. code-block::  python

    tbl = ft.tools.discrete_quantiles(tbl, header='CreditScore', interval=6, categories=False, to_header='DiscreteCredit')
    tbl = ft.tools.discrete_quantiles(tbl, header='Age', interval=8, categories=False, to_header='DiscreteAge')
    tbl = ft.tools.discrete_quantiles(tbl, header='EstimatedSalary', interval=10, categories=False, to_header='DiscreteSalary')
    
    # sparse data so rank values to negate predominance of zero's
    tbl = ft.tools.discrete_quantiles(tbl, header='Balance', interval=5, categories=False, duplicates='rank', to_header='DiscreteBalance')

Scale
^^^^^

Finally we scale our continuous values.

.. code-block::  python

    # hypothesis: customers that are older have better tenure
    tbl = ft.tools.scale_mapping(tbl, 'Tenure', 'Age', to_header='TenureAge')
    
    tbl = ft.tools.scale_normalize(tbl, scalar='robust', headers=['CreditScore','Age','Balance','EstimatedSalary','TenureAge'])

As before, we run the capability pipeline to ensure everything works.

.. code-block::  python

    ft.run_component_pipeline()

We ensure our feature set looks how we want it and our features are optimised. Once happy
we can move on to model optimisation.

Model Discovery
---------------

This is a model discovery train and test process optimising a chosen models metadata to
produce a trained model class. It is worth noting but the data carries an identifier
called `CustomerId` that should be omitted from the model training.

The labels can be retrieved loading the data from where it was saved. An example using Project
Hadron.

.. code-block::  python

   a = AutoML.from_memory()
    # set the pointers
    a.set_source_uri('event://transform')
    a.add_connector_uri('label', 'event://label')
    # load the data
    tbl = a.load_source_canonical()
    label = a.load_canonical('label')
    # convert tp numpy arrays
    X = np.asarray(tbl)
    y = np.asarray(label)

Once the model is selected, optimised, trained and tested it is ready to predict. At this point
we pass the trained model to our AutoML capability.

Classifier Predict
------------------
At this point we have our preprocessed feature set and our trained model through discovers.
We can now set up our model predict against new feature sets coming through the pipeline.

.. code-block::  python

    # reset the connectors
    aml.set_source_uri('event://transform')
    aml.set_persist_uri('${HADRON_CHURN_PERSIST_PATH}')
    
    tbl = aml.load_source_canonical()

taking the instance of our model class, we give it a name, so we can retrieve the model
for later interrogation if required, then pass in the trained model instance.

.. code-block::  python

    aml.add_trained_model(model_name='GradientBoost', trained_model=model_GB)

With our model stored, we can now add our action to run our canonical against the model
and return its predictions. Unlike our first use case :ref:`Use Case One: Disaster`, this
time will have an identifier we want to carry alongside our prediction to potentially
align with downstream objectives. The identifier is removed from the model prediction,
then realigned with the prediction outcome.

.. code-block::  python

    predict = aml.tools.label_predict(tbl, model_name='GradientBoost', id_header='CustomerId')

As with the other components, we run the capability pipeline to ensure everything works.

.. code-block::  python

    aml.run_component_pipeline()

Controller
----------

As with or previous capabilities, we initialize our component and use the factory class method
`from_env` to create an instance of our Controller, but this time we don't need to give it a name
as it is assumed there will only ever be one controller in each project Hadron pipeline. We
also don't need source and persist as the pipeline capabilities already have this.

.. code-block::  python

    ctrl = Controller.from_env(has_contract=False)

Once created we simply then register each of the pipeline components referenced by name. With the
Controller recipe complete the project Hadron pipeline is ready to run.

.. code-block::  python

    ctrl.register.feature_select('churn')
    ctrl.register.feature_transform('churn')
    ctrl.register.automl('churn')

To run the pipeline will run the Controller instance using the method call `run_controller`,
which will run the our end-to-end pipeline from raw data to our modules prediction.

.. code-block::  python

    ctrl.run_controller()

Review Run
~~~~~~~~~~

We can review our results by loading the AutoML output canonical. Notice we now include
the `CustomerId` aligned with the prediction result.

.. code-block::  python

    AutoML.from_env('churn').load_persist_canonical()


.. parsed-literal::

    pyarrow.Table
    CustomerId: int64
    predict: int64
    ----
    CustomerId: [[15634602,15647311,15619304,15701354,15737888,...,15606229,15569892,15584532,15682355,15628319]]
    predict: [[0,0,1,0,0,...,0,0,0,0,0]]

Summary
-------

At this point we have

* Performed Exploratory Data Analysis(EDA) to gain more clear insights of the data.
* Completed Data Preprocessing to produce a set of capability recipes to optimize the
  features of interest to a model algorithm.
* Build, train and tested a model to select the best performance for our requirements.
* Save the trained model for prediction retrieval in our AutoML capability.
* Make Predictions using our model, aligned to our chosen identifier.
* Created a capability pipeline of our preprocessing and model predict.

The next step will be to run the re-usable project Hadron pipeline with
representative synthetic data.




