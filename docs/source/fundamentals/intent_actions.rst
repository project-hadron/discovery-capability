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