.. _api:

Capability Intent Actions
=========================

Introduction
------------

The Project Hadron package comes with a number of component capabilities, listed below.
Each capability represents a separation of concerns across the stakeholders and
data science teams model build workflow.

* FeatureSelect: Reduce dimensionality of a dataset through reduction techniques.
* FeatureEngineer:
    * correlate: Modify two value sets into a third value set.
    * model: Remodel a dataset through merge, group and other actions.
    * build: Generate synthetic data through analysis and statistics.
* FeatureTransform: Transformation of data for model optimisation.
* AutoML: Automatically run model predictions.

The diagram illustrates a typical workflow for stakeholders and data science teams looking to
implement business objectives. Highlighted within the diagram are where the capability components
sit within the workflow.

.. image:: /source/_images/fundamentals/ml_flow.png
  :align: center
  :width: 800

The rectangles with a dotted outline box, that surround the processes, represent the components used at that
point within the workflow. Found within the rectangle is the name of the component used.
This may not fit every workflow but when building a model, be it for production or as a proof of concept, each
of these capabilities are at the core of any model build.
Feature Selection
-----------------

This class represents feature selection focusing on dimensionality and specifically columnar
reduction. Its purpose is to disregard irrelevant features to remove, amongst other things,
constants, duplicates and statistically uninteresting columns.

As an early stage data pipeline process, FeatureSelect focuses on data preprocessing, and
as such is a filter step for extracting features of interest.

.. toctree::
   :maxdepth: 1

   feature_select

Methods::

    auto_aggregate
    auto_append_tables
    auto_cast_types
    auto_clean_header
    auto_drop_columns
    auto_drop_correlated
    auto_drop_duplicates
    auto_drop_noise
    auto_projection
    auto_reinstate_nulls
    auto_sample_rows

Feature Engineering - correlate
-------------------------------
.. toctree::
   :maxdepth: 1

   feature_correlate

Methods::

    correlate_column_join
    correlate_date_diff
    correlate_date_element
    correlate_dates
    correlate_missing
    correlate_missing_probability
    correlate_number
    correlate_on_condition
    correlate_on_pandas
    correlate_outliers
    correlate_replace

Feature Engineering - model
---------------------------
.. toctree::
   :maxdepth: 1

   feature_model

Methods::

    model_cat_cast
    model_concat_remote
    model_group
    model_merge
    model_num_cast

Feature Transformation
----------------------

.. toctree::
   :maxdepth: 1

   feature_transform

Methods::

    activate_relu
    activate_sigmoid
    activate_tanh
    discrete_custom
    discrete_intervals
    discrete_quantiles
    encode_category_integer
    encode_category_one_hot
    encode_date_integer
    scale_mapping
    scale_normalize
    scale_standardize
    scale_transform

Feature Build
-------------

.. toctree::
   :maxdepth: 1

   feature_build

Methods::

    build_difference
    build_profiling

Feature Engineering - synthesis
-------------------------------
.. toctree::
   :maxdepth: 1

   feature_synthetic

Methods::

    get_number
    get_category
    get_boolean
    get_datetime
    get_intervals
    get_analysis
    get_analysis_group
    get_string_pattern

Feature Engineering - sample
----------------------------
.. toctree::
   :maxdepth: 1

   feature_sample

Methods::

    get_distribution
    get_dist_normal
    get_dist_choice
    get_dist_bernoulli
    get_dist_bounded_normal
    get_noise
    get_synthetic_data_types
    get_synthetic_persona_usa
    get_sample_list
    get_sample_map
    sample_inspect
    sample_list
    sample_map


Tools
-----

