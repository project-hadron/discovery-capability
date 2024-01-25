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

Capturing Knowledge
-------------------
As part of the set-up process, or at anytime during the capability
development cycle, information can be gathered and added to the
capability's already existing knowledge.

Firstly we reload the instance we wish to add the knowledge to.

.. code:: python

    fs = FeatureSelect.from_env('demo_citation', has_contract=False)


Add identification
~~~~~~~~~~~~~~~~~~

Primarily giving your capability a description, version and status helps
identify its purpose and placement in a project.

.. code:: python

    fs.set_description("Every arrest effected in NYC by the NYPD from 2006 to the end of the previous calendar year")
    fs.set_version('0.0.1')
    fs.set_status('discovery')

Add provenance
~~~~~~~~~~~~~~

The FeatureSelect capability provides a special method to add provenance.
Provenance cites a number of origin indicators that guide the user to the
data’s provenance, its restrictions such as cost and license, its provider
and the data’s author.

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

Describing attributes
~~~~~~~~~~~~~~~~~~~~~

A vital part of understanding one’s dataset is to describe the attributes provided.
Using `sdd_notes` we set the catalogue group as ‘attributes’, then labeled with the
name of the attribute and description.

.. code:: python

    ## Add some attribute descriptions
    fs.add_notes(catalog='attributes', label='age', text='The age of the passenger has limited null values')
    fs.add_notes(catalog='attributes', label='deck', text='cabin has already been split into deck from the originals')
    fs.add_notes(catalog='attributes', label='fare', text='the price of the fair')
    fs.add_notes(catalog='attributes', label='pclass', text='The class of the passenger')
    fs.add_notes(catalog='attributes', label='sex', text='The gender of the passenger')
    fs.add_notes(catalog='attributes', label='survived', text='If the passenger survived or not as the target')
    fs.add_notes(catalog='attributes', label='embarked', text='The code for the port the passengered embarked')

Capture observations
~~~~~~~~~~~~~~~~~~~~

As with attributes, we use `sdd_notes` to capture feedback from an SME or data owner, for
example. In this case we capture ‘observations’ as our catalogue and
‘describe’ as our label which we maintain for both descriptions.

.. code:: python

    fs.add_notes(catalog='observations', label='describe',
                 text='The original Titanic dataset has been engineered to fit Seaborn functionality')
    fs.add_notes(catalog='observations', label='describe',
                 text='The age and deck attributes still maintain their null values')

Describe Actions
~~~~~~~~~~~~~~~~

To enhance the readability and understanding of each capabilities actions, we can add notes
to help explain ones thinking for each intent action. This can then extend to the broader team,
and those re-exploring the intended actions to understand why.

.. code:: ipython3

    tr.add_intent_description(level='clean_header', text="Tidy headers with spaces and set to lower case")
    tr.add_intent_description(level='reinstate_nulls', text="replace question marks with nulls")

----

Reporting
---------

Once the activities of connectivity and intended actions have been completed, and
information is added it can easily be accessed, either visually
through reporting or remotely through predefined connector contracts. In
our case we are visually displaying the reports for the purpose of
demonstration but would normally be connected to a reporting tool for
information capture.










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

    tr.add_intent_level_description(level='clean_header', text="Tidy headers with spaces and set to lower case")
    tr.add_intent_level_description(level='reinstate_nulls', text="replace question marks with nulls")


.. code:: ipython3

    tr.report_intent_description()

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



Capability Reporting
~~~~~~~~~~~~~~~~~~~~

Our initial report shows information capture about our capability.

.. code:: python

    fs.report_task()

.. image:: /source/_images/reports/rpt_cit_01.png
  :align: center
  :width: 300

Connectivity Reporting
~~~~~~~~~~~~~~~~~~~~~~

As part of all capabilities one can also interrogate where data is coming
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

Finally and specifically to the transitioning capability, we citate
the provider of our data and that citation can be added to as knowledge
is gained.

This information not only shows us the domain and description of the
provider but also the providers details, the datas author and
restrictions on that data through license and costs. This information
can easily be passed to a separate capability that could for example
monitor cost/spend on data throughput or collate common provider
sourcing for data reuse.

.. code:: python

    fs.report_provenance()

.. image:: /source/_images/reports/rpt_cit_03.png
  :align: center
  :width: 650
