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


The review of a dataset by an expert with similar credentials and
subject knowledge as the data creator to validate the accuracy of the
data and gain insight into its content and form.

.. code-block:: python

    from ds_discovery import Transition

Quality Assurance
-----------------

Quality assurance provides an immediate insight into the quality,
quantity, veracity and availability of the dataset being provided. This
is a critical step to the success of any machine learning or product
outcome.

Observational immediacy to the content of the dataset allows quick
decision making at the earliest stage of the process. It also provides
output for discussion for SME’s and data architects to share common
reports that are based on best practice and familiar to both parties.

Finially it provides observational tools presenting a broad-set of
information in a compacted and common display format.

.. code-block:: python

    tr = Transition.from_env('demo_quality', has_contract=False)

Set File Source
^^^^^^^^^^^^^^^

Initially we set the file source for our data of interest and run the
component.

.. code-block:: python

    ## Set the file source location
    data = 'https://www.openml.org/data/get_csv/16826755/phpMYEkMl.csv'
    fs.set_source_uri(data)
    fs.set_persist()
    fs.set_description("Original Titanic Dataset")

Data Dictionary
---------------

The data dictionary is a go to tool that gives both a visual and
shareable summary of the dataset provided. In this case one looks at the
raw source so as to assess its visual suitability.

In this instance, taking the original Titanic dataset, data elements
such as nulls have been masked and in some cases inappropriately ‘typed’
the data. There are also multiple features that are not required, all of
which need to be dealt with before one can get a better view of the data
presented.

.. code-block:: python

    df = fs.load_source_canonical()
    fs.canonical_report (df)

.. image:: /images/reports/qua_img01.png
  :align: center
  :width: 700

Engineering Selection
^^^^^^^^^^^^^^^^^^^^^

The canonical is tidied up through engineering selection where one
adjusts the features of interest, whilst removing the data columns that
are of no interest and making sure the data is correctly typed.

.. code-block:: python

    df = fs.tools.auto_reinstate_nulls(df, nulls_list=['?'])
    df = fs.tools.to_remove(df, headers=['body', 'name', 'ticket', 'boat', 'home.dest'])
    df = fs.tools.auto_to_category(df)
    df = fs.tools.to_numeric_type(df, headers=['age', 'fare'])
    df = fs.tools.to_int_type(df, headers='survived')
    
    fs.run_component_pipeline()

Validation
----------

Now our selection engineering has been applied to the dataset one has a
clearer view of the value of the data provided.

The canonical report provides an enhancement of already existing data
science tools to give a clear single view of our data set that is
familiar to a broader audience.

.. code-block:: python

    fs.canonical_report(df)

.. image:: /images/reports/qua_img02.png
  :align: center
  :width: 550

Add Bulk Notes
--------------

In addition to adding individual notes one also has the ability to
upload bulk notes from an external data source. In our next example we
take an order book and from an already existing description catalogue
extract that knowledge and add it to our attributes.

.. code-block:: python

    tr = Transition.from_env('cs_orders', has_contract=False)

Set file source
~~~~~~~~~~~~~~~

Initially set the file source for the data of interest and run the
component.

.. code-block:: python

    fs.set_source_uri(uri='data/CS_ORDERS.txt', sep='\t', error_bad_lines=False, low_memory=True, encoding='Latin1')
    fs.set_persist()
    fs.set_description("Consumer Notebook Orders for Q4 FY20")

Connect the bulk upload
~~~~~~~~~~~~~~~~~~~~~~~

First create a connector to the information source.

.. code-block:: python

    fs.add_connector_uri(connector_name='bulk_notes', uri='data/cs_orders_dictionary.csv')

Upload the descriptions
~~~~~~~~~~~~~~~~~~~~~~~

With our connector in place one can now load that data and specify the
columns of interest that provide both the label and the text.

Using our reporting tool one can now observe that attribute descriptions
have been uploaded.

.. code-block:: python

    notes = fs.load_canonical(connector_name='bulk_notes')
    fs.upload_notes(canonical=notes, catalog='attributes', label_key='Attribute', text_key='Description')

.. code-block:: python

    fs.report_notes(drop_dates=True)

.. figure:: /images/reports/met_img02.png
  :align: center
  :width: 500

  not all attributes are displayed

Report Filtering
^^^^^^^^^^^^^^^^

Sometimes bulk uploads can result in a large amount of added
information. Our reporting tool has the ability to filter what we
visualize giving us a clean summery of items of interest. In our example
we are filtering on ‘label’ across all sections, or catalogues.

.. code-block:: python

    fs.report_notes(labels=['ORD_DTS', 'INV_DTS', 'HOLD_DTS'], drop_dates=True)

.. image:: /images/reports/met_img03.png
  :align: center
  :width: 250






----







Schema
------

A Schema is a representation of our dataset as a set of statistical and
probabilistic values that are semantically common across all schemas. The
schema separates each data element into four parts:

-  Intent: shows how the data content is being discretionized and its
   type.
-  Params: the parameters used to specialise the Intent such as
   granularity, value limits etc.
-  Patterns: probabilistic values of how the datas relative frequency is
   distributed, along with a number of other values, related to the data
   type.
-  Stats: a broad set of statistical analysis of the data dependant
   upon the data type including distribution indicators, limits and
   observations.

A schema can be fully or partially stored or represented as a relational
tree, through naming. One can build a semantic and contextualized view of
its data that can be distributed as a machine readable set of
comparatives or as part of some other outcome.

.. code-block:: python

    tr = Transition.from_env('demo_schema', has_contract=False)

Set File Source
^^^^^^^^^^^^^^^

Initially we set the file source for the data of interest and run the
component.

.. code-block:: python

    ## Set the file source location
    fs.set_source_uri('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv')
    fs.set_persist()
    fs.set_description("Titanic Dataset used by Seaborn")

.. code-block:: python

    fs.run_component_pipeline()

Creating and Presenting Schema
------------------------------

By default the primary schema is generated using default values taking a
flat view of the data or feature set and producing a schema that is
either distributable through a given connector contract or, as in our
case, displayed within the notebook.

.. code-block:: python

    fs.save_canonical_schema()

.. code-block:: python

    fs.report_canonical_schema()

.. figure:: /images/reports/sch_img01.png
  :align: center
  :width: 350

  not all attributes are displayed

Report
------

As with all reports one can redistribute our schema to interested
parties or systems where the data can be observed or schematically
examined to produce decision making outcomes. For example with the
observation of concept drift.

.. code-block:: python

    schema = fs.report_canonical_schema(fs.load_persist_canonical(), stylise=False)
    fs.save_report_canonical(reports=fs.REPORT_SCHEMA, report_canonical=schema)

Filter the Schema
-----------------

In the following example we taylor the view of the schema without
changing the underlying schema’s content. In this instance we have
filtered on:

-  root, with our interests in the data features ‘survived’ and ‘fare’
   and
-  section, where our interest is particulary the pattern subset.

This provides quick and easy visualisation of complex schemas and can
help to identify individuals or groups of elements of interest within
that schema.

.. code-block:: python

    fs.report_canonical_schema(roots=['survived', 'fare'], sections='patterns')

.. figure:: /images/reports/sch_img02.png
  :align: center
  :width: 700

  not all attributes are displayed

Semantic Schema
---------------

Beyond the basic schema lies a complex but accessible set of
parametrization that allows for the creation of relational comparisons
between the data type.

In our demonstration below, when creating the schema, we have given it a
name and then provide the relational tree we are interested in. In this
case we take ‘survived’ as our root, being the target feature of
interest. We next relate this to ‘age’ to understand how age is
distributed both by ‘survived’ and ‘gender’.

.. code-block:: python

    fs.save_canonical_schema(schema_name='survived', schema_tree=[
        {'survived': {'dtype': 'bool'}},
        {'age': {'granularity': [(0, 18), (18, 30), (30, 50), (50, 100)]}}])

.. code-block:: python

    fs.report_canonical_schema(schema='survived')

.. figure:: /images/reports/sch_img03.png
  :align: center
  :width: 550

  not all attributes are displayed

Distributable Reporting
-----------------------

With this done one can now further investigate distributions and
discover a view of the data. In this case, as a simple example, one can
see the age range percentage of those that ‘survived’.

From this simple example one can see how schemas can be captured over a
period of time or fixed at a moment in time then distributed and
compared to provide monitoring and insight into data as it flows through
your system.

.. code-block:: python

    result = fs.report_canonical_schema(schema='survived', roots='survived.1.age', elements=['relative_freq'], stylise=False)
    result['value'].to_list()

.. image:: /images/reports/sch_img04.png
  :align: left
  :width: 225




Reporting
---------

As well as its visual display the enhanced dictionary can be distributed
to any connecting service, such as an XL spreadsheet and its graphical
tooling.

.. code-block:: python

    dictionary = fs.canonical_report(fs.load_persist_canonical(), stylise=False)
    fs.save_report_canonical(reports=fs.REPORT_DICTIONARY, report_canonical=dictionary)

Report Tailoring
----------------

By default reports are given their own name and data type, though this
can be tailored to suit a targeted system with options of name,
versioning, timestamp and the data type of the data to be reported.

.. code-block:: python

    reports = [fs.report2dict(report=fs.REPORT_DICTIONARY, prefix='titanic_', file_type='csv', stamped='days')]
    fs.save_report_canonical(reports=reports, report_canonical=dictionary)

Quality Summary
---------------

When looking at the data as well as the detail in the dictionary one can
also produce a summary overview of the dataset as a whole. The quality
report provides a subset view of quality score, data shape, data types,
usability summary and cost, if applicable.

.. code-block:: python

    fs.report_quality_summary()

.. image:: /images/reports/qua_img03.png
  :align: center
  :width: 250

Report Redistribution
---------------------

As with the dictionary the quality report can be saved and redistributed
to interested parties.

.. code-block:: python

    quality = fs.report_quality_summary(stylise=False)
    fs.save_report_canonical(reports=fs.REPORT_SUMMARY, report_canonical=quality)


