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

Each capability has a common set of reports that provide Data lineage, identifying where the
data originated, how it has changed, and its ultimate destination.

Capturing Knowledge
-------------------
As part of the set-up process, or at anytime during the capability
development cycle, information can be gathered and added to the
capability's already existing knowledge.

Add identification
~~~~~~~~~~~~~~~~~~

Primarily giving your capability a description, version and status helps
identify its purpose and placement in a project.

.. code-block:: python

    capability.set_description("Every arrest effected in NYC by the NYPD from 2006 to the end of the previous calendar year")
    capability.set_version('0.0.1')
    capability.set_status('discovery')

Add provenance
~~~~~~~~~~~~~~

The FeatureSelect capability provides a special method to add provenance.
Provenance cites a number of origin indicators that guide the user to the
data’s provenance, its restrictions such as cost and license, its provider
and the data’s author.

.. code-block:: python

    capability.set_provenance(title='NYPD Historic Arrest Data',
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

.. code-block:: python

    ## Add some attribute descriptions
    capability.add_notes(catalog='attributes', label='age', text='The age of the passenger has limited null values')
    capability.add_notes(catalog='attributes', label='deck', text='cabin has already been split into deck from the originals')
    capability.add_notes(catalog='attributes', label='fare', text='the price of the fair')
    capability.add_notes(catalog='attributes', label='pclass', text='The class of the passenger')
    capability.add_notes(catalog='attributes', label='sex', text='The gender of the passenger')
    capability.add_notes(catalog='attributes', label='survived', text='If the passenger survived or not as the target')
    capability.add_notes(catalog='attributes', label='embarked', text='The code for the port the passengered embarked')

Capture observations
~~~~~~~~~~~~~~~~~~~~

As with attributes, we use `add_notes` to capture feedback from an SME or data owner, for
example. In this case we capture ‘observations’ as our catalogue and
‘describe’ as our label which we maintain for both descriptions.

.. code-block:: python

    capability.add_notes(catalog='observations', label='describe',
                 text='The original Titanic dataset has been engineered to fit Seaborn functionality')
    capability.add_notes(catalog='observations', label='describe',
                 text='The age and deck attributes still maintain their null values')

Describe Actions
~~~~~~~~~~~~~~~~

To enhance the readability and understanding of each capabilities actions, we can add notes
to help explain ones thinking for each intent action. This can then extend to the broader team,
and those re-exploring the intended actions to understand why.

.. code-block:: python

    capability.add_intent_description(level='clean_header', text="Tidy headers with spaces and set to lower case")
    capability.add_intent_description(level='reinstate_nulls', text="replace question marks with nulls")

Create Run Books
~~~~~~~~~~~~~~~~

If not provided, the actions of the Intent will be aligned in the order
given but if one wishes to change this order we have the ability to
taylor the sequence using a Run Book. A Run Book provides the facility
to define the run order of a capabilities intent actions to insure those
actions are run appropriate to the sequence they were intended.

.. code-block:: python

    capability.add_run_book(run_levels=['clean_header', 'to_remove', 'reinstate_nulls', 'auto_categorize', 'to_numeric', 'to_int'])


----

Reporting
---------

Once the activities of connectivity and intended actions have been completed, and
information is added it can easily be accessed, either visually
through reporting or remotely through predefined connector contracts. In
our case we are visually displaying the reports for the purpose of
demonstration but would normally be connected to a reporting tool for
information capture.

Capability Reporting
~~~~~~~~~~~~~~~~~~~~

Our initial report shows information capture about our capability.
See `Add identification`_

.. code-block:: python

    capability.report_task()


Connectivity Reporting
~~~~~~~~~~~~~~~~~~~~~~

As part of all capabilities one can also interrogate where data is coming
from and going to, which connector contracts have been set up and what
they look like. In this case we only require our primary source and
persist connectors from which we can identify the data’s location and
how we retrieved it.

.. code-block:: python

    capability.report_connectors()

Provenance Reporting
~~~~~~~~~~~~~~~~~~~~

Specifically to the FeatureSelection capability, we identify
the provider of our data as knowledge gained. see `Add provenance`_

This information not only shows us the domain and description of the
provider but also the providers details, the datas author and
restrictions on that data through license and costs. This information
can easily be passed to a separate capability that could for example
monitor cost/spend on data throughput or collate common provider
sourcing for data reuse.

.. code-block:: python

    capability.report_provenance()

Intent Action Reporting
~~~~~~~~~~~~~~~~~~~~~~~

Each individual capability has their own set of actions associated with that
capability. With the intent actions report we can observe the activities or
actions applied to a dataset by the capability.

.. code-block:: python

    capability.report_intent()


Run Book Reporting
~~~~~~~~~~~~~~~~~~

Once a run book has been defined, we can observe that run book through the run book report.
see `Create Run Books`_

.. code-block:: python

    capability.report_run_book()

Environment Reporting
~~~~~~~~~~~~~~~~~~~~~

Finally we have the environment report report that provides a view of environment
variables starting with HADRON. Specifically the report carries the default location
of the data path, the location of capability recipes and the location of remote read-only
component pipelines.

.. code-block:: python

    report = capability.report_environ()


