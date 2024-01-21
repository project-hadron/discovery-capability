Reports: Data Lineage
=====================
**Data lineage** refers to the data's journey from its origin through its various transformations,
storage locations, and usage. It is a detailed record of the data's origin, how it has been
transformed or processed, and where it has been stored or moved over time. Data lineage helps
organizations understand the data's history, quality, and reliability, which are critical
factors for compliance, auditing, and decision-making purposes. It provides insights into
data sources, transformations, and dependencies that enable organizations to track data's
flow and lineage, understand its impact on various business processes, and ensure its accuracy,
consistency, and security.

*
Each capability has a common set of reports that provide Data lineage, identifying where the
data originated, how it has changed, and its ultimate destination.

.. code:: python

    from ds_capability import FeatureSelect
    from ds_core.handlers.abstract_handlers import ConnectorContract

\

----

Add Knowledge
-------------
As part of the set-up process, or at anytime during the component
development cycle, information can be gathered and added to the
component as part of its information store.

It is worth noting, method calls allow partial completion with
additional information added at a later date as knowledge is gained or
changed.

Firstly we reload the instance we wish to add the knowledge to.

.. code:: python

    fs = FeatureSelect.from_env('demo_citation', has_contract=False)


Add information
~~~~~~~~~~~~~~~

As part of the set-up process and as best practice, the component is
cited through added knowledge from the component’s creator or SME
feedback.


Additional knowledge can be added beyond the set provenance (see other
sections).

.. code:: python

    fs.set_description("Every arrest effected in NYC by the NYPD from 2006 to the end of the previous calendar year")
    fs.set_version('0.0.1')
    fs.set_status('discovery')

Add source citation
~~~~~~~~~~~~~~~~~~~

This is extended with the Project Hadron transition component,
considered the data entry point reporting tool, which includes a special
method call to add provenance. Provenance sites a number of origin
indicators that guide the user to the data’s provenance, its
restrictions such as cost and license, its provider and the data’s
author.

.. code:: python

    fs.set_provenance(title='NYPD Historic Arrest Data',
                      domain='Public Safety',
                      license_type='Public Consumption',
                      description="List of every arrest in NYC going back to 2006 through the end of the previous calendar year.",
                      provider_name='Police Department (NYPD)', 
                      provider_uri="https://data.cityofnewyork.us/Public-Safety/NYPD-Arrests-Data-Historic-/8h9b-rp9u",
                      provider_note="This data is manually extracted every quarter and reviewed by the Office of Management Analysis and Planning before being posted on the NYPD website.",
                      cost_price="$0.00",
                      cost_type="batch")

Add data connectivity
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    fs.set_source_uri(uri="https://data.cityofnewyork.us/api/views/8h9b-rp9u/rows.csv")
    fs.set_persist(uri_file='NYPD_Arrest_Historic.parquet')

----

Add Attributes
--------------

A vital part of understanding one’s dataset is to describe the
attributes provided. In this instance we name our catalogue group
‘attributes’. The attributes are labeled with the name of the attribute
and given a description.

.. code:: python

    ## Add some attribute descriptions
    fs.add_notes(catalog='attributes', label='age', text='The age of the passenger has limited null values')
    fs.add_notes(catalog='attributes', label='deck', text='cabin has already been split into deck from the originals')
    fs.add_notes(catalog='attributes', label='fare', text='the price of the fair')
    fs.add_notes(catalog='attributes', label='pclass', text='The class of the passenger')
    fs.add_notes(catalog='attributes', label='sex', text='The gender of the passenger')
    fs.add_notes(catalog='attributes', label='survived', text='If the passenger survived or not as the target')
    fs.add_notes(catalog='attributes', label='embarked', text='The code for the port the passengered embarked')

----

Adding Observations
-------------------

In addition we can capture feedback from an SME or data owner, for
example. In this case we capture ‘observations’ as our catalogue and
‘describe’ as our label which we maintain for both descriptions.

One can now use the reporting tool to visually present the knowledge
added. It is worth noting that with observations each description has
been captured.

.. code:: python

    fs.add_notes(catalog='observations', label='describe', 
                 text='The original Titanic dataset has been engineered to fit Seaborn functionality')
    fs.add_notes(catalog='observations', label='describe', 
                 text='The age and deck attributes still maintain their null values')


.. code:: python

    fs.report_notes(drop_dates=True)

.. image:: /images/reports/met_img01.png
  :align: center
  :width: 500

----


Transformation Intent
---------------------

Intent is a core concept that transforms a set of intended actions
relating directly to the components core task. In this instance we are
using the Transitioning component that provides selection engineering of
a provided dataset.

As a core concept, Intent and its Parameterization is captured in full
giving it transparency and traceability to an expert observer. It
provides direct editability of each Intent, with each Intent a separate
concern. This means minimal rewrites, adaptability, clarity of change
and reduced testing.

.. code:: ipython3

    tr = Transition.from_env('demo_intent', has_contract=False)

Set File Source
^^^^^^^^^^^^^^^

Initially set the file source for the data of interest and runs the
component.

.. code:: ipython3

    ## Set the file source location
    data = 'https://www.openml.org/data/get_csv/16826755/phpMYEkMl.csv'
    tr.set_source_uri(data)
    tr.set_persist()
    tr.set_description("Original Titanic Dataset")

Parameterised Intent
--------------------

Through observations one identifies a number of selection engineering
that needs to be done with the provided dataset. We are therefore
looking to: - automatically clean the header to remove spaces and
hidden characters in the header names. In addition note that ‘home.dest’
is seperated with a dot and best practice is to replace that with an
underscore. - reinstate nulls that have been obfuscated with ‘question
marks’ in order for us to clarify data quality and make better feature
engineering decisions. - identity selected data columns of no interest
and remove them. - apply logic that identifies potential categoricals
and appropriately ‘type’ them. - insure the appropriate’typing’ of
identified numeric features. - turn our target boolean into a 0 and 1
integer type for better feature engineering, observability and decision
making.

Then run the pipeline to apply the Intent to the dataset.

.. code:: ipython3

    df = tr.load_source_canonical()

.. code:: ipython3

    df = tr.tools.auto_clean_header(df, rename_map={'home.dest': 'home_dest'}, intent_level='clean_header')
    df = tr.tools.auto_reinstate_nulls(df, nulls_list=['?'], intent_level='reinstate_nulls')
    df = tr.tools.to_remove(df, headers=['body', 'name', 'ticket', 'boat'], intent_level='to_remove')
    df = tr.tools.auto_to_category(df, intent_level='auto_categorize')
    df = tr.tools.to_numeric_type(df, headers=['age', 'fare'], intent_level='to_numeric')
    df = tr.tools.to_int_type(df, headers='survived', intent_level='to_int')

    tr.run_component_pipeline()

Report
------

The Intent, once applied, can now be observed through the Intent’s
report which outlines each activity which displays each line of the
Intent. So it is worth observing that the Intent report is presented in
alphabetical order and not the order in which it will run.

From the report one can clearly see each Intent and its Parameterization
that can be modified by applying either a new Intent or a replacement of
the already existing line of code.

.. code:: ipython3

    tr.report_intent()

.. image:: /images/reports/int_img01.png
  :align: center
  :width: 450

Intent Metadata
---------------

To enhance the readability and understanding of each intended action one
can also add metadata to help explain ones thinking. This can be used in
conjunction with the Intent report to provided a full picture of the
actions that were taken and their changes and those actions changes to
the outgoing dataset.

.. code:: ipython3

    tr.add_intent_level_description(level='clean_header', text="clean_header")
    tr.add_intent_level_description(level='reinstate_nulls', text="replace in question marks with nulls so its data can be properly typed")
    tr.add_intent_level_description(level='to_remove', text="Selective engineering to remove features of no interest")
    tr.add_intent_level_description(level='auto_categorize', text="categorise feature object types ")
    tr.add_intent_level_description(level='to_numeric', text="with nulls reinstated we can now reset the feature type")
    tr.add_intent_level_description(level='to_int', text="make the target type int rather than bool passing decision making down to the feature engineering")


.. code:: ipython3

    tr.report_column_catalog()

.. image:: /images/reports/int_img02.png
  :align: center
  :width: 500

Run Book
--------

If not provided, the actions of the Intent will be aligned in the order
given but if one wishes to change this order it has the ability to
taylor the sequence using a Run Book. A Run Book provides the facility
to define run order to insure actions are run appropriate to the
Sequence they were intended. This is particulary useful when editing an
existing Intent pipeline or where changes effect other actions.

Run books can also be used to create multiple pipelines whereby a
sequence of Intent is created with multiple outcomes available for a
particular dataset. This is an advanced topic and not covered here.

As usual the Run Book comes with its own reporting tool for easy
visualisation.

.. code:: ipython3

    tr.add_run_book(run_levels=['clean_header', 'to_remove', 'reinstate_nulls', 'auto_categorize', 'to_numeric', 'to_int'])

.. code:: ipython3

    tr.report_run_book()

.. image:: /images/reports/int_img03.png
  :align: center
  :width: 500






Reports
-------

Once information is added it can easily be accessed, either visually
through reporting or remotely through predefined connector contracts. In
our case we are visually displaying the reports for the purpose of
demonstration but would normally be connected to a reporting tool for
information capture.

Component Reporting
~~~~~~~~~~~~~~~~~~~

Our initial report shows information capture about our component.

.. code:: python

    fs.report_task()

.. image:: /source/_images/reports/rpt_cit_01.png
  :align: center
  :width: 300

Connectivity Reporting
~~~~~~~~~~~~~~~~~~~~~~

As part of all components one can also interrogate where data is coming
from and going to, which connector contracts have been set up and what
they look like. In this case we only require our primary source and
persist connectors from which we can identify the data’s location and
how we retrieved it.

.. code:: python

    fs.report_connectors()

.. image:: /source/_images/reports/rpt_cit_02.png
  :align: center
  :width: 700

Provenance Reporting
~~~~~~~~~~~~~~~~~~~~

Finally and specifically to the transitioning component, we citate
the provider of our data and that citation can be added to as knowledge
is gained.

This information not only shows us the domain and description of the
provider but also the providers details, the datas author and
restrictions on that data through license and costs. This information
can easily be passed to a separate component that could for example
monitor cost/spend on data throughput or collate common provider
sourcing for data reuse.

.. code:: python

    fs.report_provenance()

.. image:: /source/_images/reports/rpt_cit_03.png
  :align: center
  :width: 650
