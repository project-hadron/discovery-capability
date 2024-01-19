Reports: data lineage
=====================

Each capability has a common set of reports that provide Data lineage, identifying where the
data originated, how it has changed, and its ultimate destination.

.. code:: python

    from ds_capability import FeatureSelect
    from ds_core.handlers.abstract_handlers import ConnectorContract

Dataset Citation
----------------

As part of the set-up process and as best practice, the component is
cited through added knowledge from the component’s creator or SME
feedback. In addition the data location of the source and persist is
also captured.

This is extended with the Project Hadron transition component,
considered the data entry point reporting tool, which includes a special
method call to add provenance. Provenance sites a number of origin
indicators that guide the user to the data’s provenance, its
restrictions such as cost and license, its provider and the data’s
author.

Additional knowledge can be added beyond the set provenance (see other
sections).

.. code:: python

    fs = FeatureSelect.from_env('demo_citation', has_contract=False)

Adding Citation
---------------

As part of the set-up process, or at anytime during the component
development cycle, information can be gathered and added to the
component as part of its information store.

It is worth noting, method calls allow partial completion with
additional information added at a later date as knowledge is gained or
changed.

.. code:: python

    fs.set_description("Every arrest effected in NYC by the NYPD from 2006 to the end of the previous calendar year")
    fs.set_version('0.0.1')
    fs.set_status('discovery')
    fs.set_source_uri(uri="https://data.cityofnewyork.us/api/views/8h9b-rp9u/rows.csv")
    fs.set_persist(uri_file='NYPD_Arrest_Historic.parquet')

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

Reports
-------

Once information is added it can easily be accessed, either visually
through reporting or remotely through predefined connector contracts. In
our case we are visually displaying the reports for the purpose of
demonstration but would normally be connected to a reporting tool for
information capture.

Component Reporting
^^^^^^^^^^^^^^^^^^^

Our initial report shows information capture about our component.

.. code:: python

    fs.report_task()

.. image:: /source/_images/reports/rpt_cit_01.png
  :align: center
  :width: 300

Connectivity Reporting
^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^^^^^

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
