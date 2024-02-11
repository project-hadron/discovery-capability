.. _api:

Intent Actions API
==================

This provides the intent action API documentation for Project Hadron

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

