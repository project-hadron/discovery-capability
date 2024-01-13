.. _api:

API
===
**Project Hadron** provides functionalities fundamental to data processing, and as such targets machine
learning preprocessing pipeline

.. image:: /images/introduction/machine_learning_pipeline_v01.png
  :align: center
  :width: 700

\
and a three step data processing pipeline, though its application can be applied far wider.

.. image:: /images/introduction/three_phase_pipeline_v01.png
  :align: center
  :width: 650

\


This provides the intent action API documentation for Project Hadron

Featue Selection
----------------

.. toctree::
   :maxdepth: 1

   feature_select

Methods::

    auto_clean_header
    auto_aggregate
    auto_cast_types
    auto_drop_columns
    auto_drop_correlated
    auto_drop_duplicates
    auto_drop_noise
    auto_projection
    auto_reinstate_nulls
    auto_sample_rows
    auto_append_tables
    auto_to_string

Feature Engineering - correlate
-------------------------------
.. toctree::
   :maxdepth: 1

   feature_correlate

Methods::

    correlate_column_join
    correlate_custom
    correlate_date_diff
    correlate_date_element
    correlate_dates
    correlate_discrete_intervals
    correlate_number
    correlate_on_condition
    correlate_outliers
    correlate_replace

Feature Engineering - model
---------------------------
.. toctree::
   :maxdepth: 1

   feature_model

Methods::

    model_group 
    model_merge 
    model_missing 
    model_concat_remote

Feature Transformation
----------------------

.. toctree::
   :maxdepth: 1

   feature_transform

Methods::

    activate_relu
    activate_sigmoid
    activate_tanh
    encode_category_integer
    encode_category_one_hot
    encode_date_integer
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
    get_sample_list
    get_sample_map
    sample_inspect
    sample_list
    sample_map


Tools
-----

