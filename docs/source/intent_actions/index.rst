Capability Intent Actions
=========================

Project Hadron is designed using Microservices. Microservices are an
architectural patterns that structures an application as a collection
of services, which, themselves are a component or collection of components.

are components that adhere to the
fundamental concepts
of capability  patterns and separation of concern

Introduction
------------
In Project Hadron these components are known as :ref:`Capabilities<Introducing Capabilities>`

Capabilities, by design, demonstrates the ability to execute a specified set of action
that are coupled with an intention_. These intended actions or
:ref:`intent actions<Capability Intent Actions>` are associated classes that present
a finite set of methods that can be selected and optimized within the capabilities
separation of concerns.




TThough capabilities share common parentage, it is the associative intent that
define the encapsulated actions of that capability.

Capability intent derives from an abstract intent class and associated with a capability
namesake. Intent is therefor accessed through a capability

.. image:: /source/_images/intent_actions/component_intent_class_uml.png
  :align: center
  :width: 700

* component intent class UML

The following capabilities provide accompanying intent actions:

* FeatureSelect: Reduce dimensionality of a dataset through reduction techniques.
* FeatureEngineer:
    * correlate: Modify two value sets into a third value set.
    * model: Remodel a dataset through merge, group and other actions.
    * build: Generate synthetic data through analysis and statistics.
* FeatureTransform: Transformation of data for model optimisation.
* AutoML: Automatically run model predictions.

To give context, the diagram illustrates a typical workflow for Machine Learning looking
to implement business objectives. Highlighted within the diagram are where the capability
action intent apply within the workflow.

.. image:: /source/_images/fundamentals/ml_flow.png
  :align: center
  :width: 800

* UML Machine Learning flow diagram

The rectangles with a dotted outline box, that surround the processes, represent the
action intent used at that point within the workflow. Found within the rectangle is the
name of the component used. This may not fit every workflow but when building a ML
solution, be it for production or as a proof of concept, each of these capabilities are
at the core of any model build.

.. _intention: https://web.archive.org/web/20081123014953/http://www.dtic.mil/doctrine/jel/new_pubs/jp1_02.pdf

Feature Selection
-----------------

This class represents feature selection focusing on dimensionality and specifically
columnar reduction. Its purpose is to disregard irrelevant features to remove, amongst
other things, constants, duplicates and statistically uninteresting columns.

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

This class represents feature engineering intent actions that, depending on its application,
represent data's statistical and distributive characteristics to provide targeted features
of interests. Its focus is around correlate of two value streams to produce a third.

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

This class represents feature engineering intent actions that, depending on its application,
represent data's statistical and distributive characteristics to provide targeted features
of interests. Its focus is modelling the complete dataset to produce a new dataset.

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

This class represents feature transformation intent actions whereby features are converted
from one format or structure to another. This includes, scaling, encoding, discretization
and activation trigger algorithms.

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

This class is for feature builds intent actions which are bespoke to a certain used case
but have broader reuse beyond this use case.

.. toctree::
   :maxdepth: 1

   feature_build

Methods::

    build_difference
    build_profiling

Feature Engineering - synthesis
-------------------------------

This class represents feature engineering intent actions that, depending on its application,
represent data's statistical and distributive characteristics to provide targeted features
of interests. Its focus is around building synthetic data through statistical modelling
and observational logic.

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

This class represents feature engineering intent actions that, depending on its application,
represent data's statistical and distributive characteristics to provide targeted features
of interests. Its focus is around building synthetic data through distributions algorithms
and sampled data.

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

