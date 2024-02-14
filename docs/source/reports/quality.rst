Reports: Data Profiling
=======================

**Data profiling** is the process of analyzing and examining data from various sources to understand
its structure, content, quality, and completeness. It involves collecting descriptive statistics
and metadata to gain insights into data elements, such as data types, length, format, patterns,
and relationships. Data profiling helps organizations identify potential issues with their data,
such as missing orin consistent values, duplicates, outliers, and data quality problems. By analyzing
data profiles, organizations can gain a better understanding of their data, detect data quality issues,
and take corrective actions to improve data accuracy, completeness, and consistency. Data profiling
can be used in a variety of contexts, including data migration, data integration, data warehousing,
and data governance. It is a crucial step in the data preparation process, which helps organizations
ensure that their data is reliable, consistent, and of high quality.

Each capability has a common set of reports that provide this Data Quality insights

Quality Summary Report
----------------------

Our first view of data is through the quality summary report, giving an overview of
our dataset. It provides insight to the overall data set including data types and
their distribution, along with an opinion on overall quality and usability.

.. code-block:: python

    capability.quality_report(canonical)


Data Dictionary Report
----------------------

The Data dictionary provides more of an insight into the quality, quantity and veracity
of the dataset. It provides the attributes, their types, nulls, uniqueness and
observable values in order of count.

.. code-block:: python

    capability.canonical_report(canonical)

Data Schema Report
------------------

The Data schema drills down further into the dataset, listing characteristics of
each attribute individually. It looks at interval, pattern frequency and measure
as well as relevant statistics pertaining to the attribute type.

.. code-block:: python

    capability.schema_report(canonical)


Data Profiling as an Action
---------------------------

To this point we have seen data profiling through the capability reports as
part of discovery or information gathering. As part of FeatureBuild capability
data profiling can also be used as an intent action and thus part of a
pipeline throughput

.. code-block:: python

    capability.tools.build_profiling(canonical, profiling='quality')
    capability.tools.build_profiling(canonical, profiling='dictionary')
    capability.tools.build_profiling(canonical, profiling='schema')

Profiling API
-------------

.. toctree::
   :maxdepth: 1

   quality_reports
   quality_actions
