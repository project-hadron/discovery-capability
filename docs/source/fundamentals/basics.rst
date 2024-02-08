Introducing Capabilities
========================

Project Hadron is designed using Microservices. Microservices are an
architectural patterns that structures an application as a collection
of services, which, themselves are a component or collection of components.

Fundamentals
------------

Capabilities and their separation of concern are fundamental principles
in the design of Project Hadron. Capabilities can be thought of as
specialist components that refer to the range of functionalities and
features a software solution possesses, in our case, to handle and
process data for a downstream objective.

Each capability class, at it is root, is defined as a concrete implementation
of a shared abstract parent class. This means that all capability instances
share common behavior in initialization, connectivity management, reporting
and running the component.

Through initialization capabilities are also responsible for the capture and up
keep of **recipe**. A recipe can be thought of as a runbook of instruction
of the lineage of that instance. The recipe  By referencing the name of the instance, the
recipe can be re-loaded and re-run creating a referencable and reusable capability.


Capability Setup
----------------

For this example we are going to use the FeatureSelect capability class.
Other capability classes include FeatureEngineer, FeatureTransform,
FeatureBuild and AutoML

This set up process can be applied to any of the capability classes
as each class is built upon a common abstract class. The difference comes
when we consider actions for each capability component.

import
^^^^^^

Initially we import the capability class, all of which can be found
in the root package tree.

.. code-block:: python

    from ds_capability import FeatureSelect

initialise
^^^^^^^^^^

We can now create the instance of our FeatureSelect capability, but it is
important to note we don't instantiate the class directly, but years one
of the factory class methods, in this case ``from_env`` to look in the
:ref:`environment<Environment Variables>` for any special settings. This
is the most common way to start any of the capability components.

.. code-block:: python

    fs = FeatureSelect.from_env('my_select', has_contract=False)

The first parameter is a named identifier for this instance and used to create and
retrieve the capabilities recipe containing the current state of the capability.

The final parameter `has_contract` is a fail-safe, only used on first creation
of a capability instance to validate the recipe should be empty.

connectivity
^^^^^^^^^^^^

A key component of our capability is to be able to get data in and out. This
is achieved through the capabilities connectivity methods. In order to retrieve
data, we initially set up a connector contract which contains the information
for a data source, be it a database, file or cloud storage. This does not
retrieve the data but sets up the parameters needed to retrieve the data.

The base methods call is:

* add_connector_uri('<connector_name>', '<uri>')

where `connector_name` is the connector reference name and the`uri` is a
fully qualified URI reference to the data or feature set.

For ease of coding this method has been extended to mirror the source
and the persist, where source is a read-only sub-class of the persist class.
Though you can use persist for all your connectivity, it is good practice
to use the read-only source calls when reference in downstream data to
protected from accidental overwrite.

The methods `set_source(...)` and `set_persist()` use the environment variable
`HADRON_DEFAULT_PATH`, which, by default, is set to point to a local path.
You can find more on this at `Environment Variables`_. With `set_persist()`
there is the option to be able to set the name of the target file otherwise
a default name is used.

All the `set_` methods automatically set a standard name reference for ease,
more of which is in the next section. While the `add_connector_` still use a
reference name to allow new connect pipelines bot to restrict those pipelines
according to the connector method been used.

**source**

* set_source('<file_name.ext>')
* set_source_uri('<uri>')
* add_connector_source('<connector_name>', '<uri>')

**persist**

* set_persist()
* set_persist_uri('<uri>')
* add_connector_persist('<connector_name>', '<uri>')

An example of using these connectivity methods might be:

.. code-block:: python

    fs.set_source_uri('https://www.openml.org/data/get_csv/16826755/phpMYEkMl.csv')
    fs.set_persist()

where the source is pointing to a remote URL data source and the persist is using
default settings.

load and save
^^^^^^^^^^^^^

Once we have created our connector contract it is ready to use. We have three
options to load the data or feature set, returning a canonical, and two options
to persist, passing a canonical. As a mirror of the set methods the core methods
are `load_canonical` and `save_canonical`, passing through the `connector_name`
as reference. The other method calls are shortcuts read the connector name is
assumed from the call.

**load**

* load_canonical('<connector_name>')
* load_source_canonical()
* load_persist_canonical()

**save**

* save_canonical('<connector_name>', canonical)
* save_persist_canonical(canonical)

For ease, the add and set connectivity methods return the class instance
allowing you to chain the set with the load for example:

.. code-block:: python

    tbl = fs.set_source('myfile.parquet').load_source_canonical()

Both setting the source and returning the canonical table

run pipeline
^^^^^^^^^^^^
To this point we have we have created our core recipe for this capability.
Though there are no actions associated, using the common method calls
we have created a working capability that ingest data from where we required,
passes it through our component and persists it to a location specified.

But rather than write this each time we want to be able to run our capability,
we use our recipe, created in the background from our activities, to repeat
those activities. We do this through the `run_component_pipeline` method
call.

This call reads the recipe loading the source data, executing the capability
task, of which there are non, then persists the results. As this is a background
process, it expects the source and persist connector contracts to be set.

.. code-block:: python

    fs.run_component_pipeline()

To view the results of the run you're simply load the persisted data.

.. code-block:: python

    tbl = fs.load_persist_canonical()

To view the connectivity of where the data came from and went to use the
connectivity report

.. code-block:: python

    report = fs.report_connectors()

To view the data itself as a readable table, the two following calls might
be useful, and certainly worth of explore for valuable data on your dataset.

.. code-block:: python

    data_dictionary = fs.canonical_report(canonical=tbl)

    data_head = fs.table_report(canonical=tbl, head=5)

Understanding the first order calls in a capability gives you access to understanding
all capabilities at there base methods and create components quickly ready to add
the actions pertinent to each capability.

Environment Variables
---------------------

To this point we have been using the default settings of where to store the
named contract and the persisted dataset. These are set up at initialization
as environment variables for you and are in general local to your working directory.

The current set of environment variables can be viewed with the report

.. code-block:: python

    report = fs.report_environ()

Due to most important environment variables are environment variables are

* HADRON_DEFAULT_PATH
* HADRON_PM_PATH

These point to where the







The use of environment variables
gives flexibility to the list of connector contracts where data can be stored.

Not only this, but environmental variables can be used within actions

Hadron provides an extensive list of environment variables to tailor how
your capabilities retrieve and persist their information, this is beyond
the scope of this tutorial and tends to be for specialist use, therefore
we are going to focus on the two most commonly used for the majority of
projects.

We initially import Python’s ``os`` package.

.. code-block:: python

    import os

In general and as good practice, most notebooks would ``run`` a set up
file that contains imports and environment variables that are common
across all notebooks. In this case, for visibility, because this is a
tutorial, we will import the packages and set up the two environment
variables within each notebook.

The first environment variable we set up is for the location of the
Domain Contract. Domain Contracts are the outcome of named capability
instances and collect together metadata that are pertinent to the
specific capability tasks and actions. Domain Contracts are critical
references of the capabilities and other capabilities that rely on them.

From this point on we use the name 'Domain Contract' to represent the
outcome of the named capability instance which constitute the capabilities
task and used to run the capability.

In this case we are setting the Domain Contract location to be in a
common local directory of our naming.

.. code-block:: python

    os.environ['HADRON_PM_PATH'] = '0_hello_meta/demo/contracts'

The second environment variable is for the location of where the data is
to be persisted. This allows us to place data away from the working
files and have a common directory where data can be sourced or
persisted. This is also used internally within the capability to avoid
having to remember where data is located.

.. code-block:: python

    os.environ['HADRON_DEFAULT_PATH'] = '0_hello_meta/demo/data'

As a tip we can see where the default path environment variable is set
by using ``report_connectors``. By passing the parameter
``inc_template=True`` to the ``report_connectors`` method, showing us
the connector names. By each name is the location path (uri) where, by
default, the capability will source or persist the data set, this is
taken from the environment variable set. Likewise we can see where the
Domain Contract is being persisted by including the parameter ``inc_pm``
giving the location path (uri) given by the environment variable.

.. code-block:: python

    fs.report_connectors(inc_template=True)

Because we have now changed the location of where the Domain Contract
can be found we need to reset things from the start giving the source
location and using the default persist location which we now know has
been set by the environment variable.

.. code-block:: python

    fs = FeatureSelect.from_env('hello_tr,', has_contract=False)

.. code-block:: python

    fs.set_source_uri('https://www.openml.org/data/get_csv/16826755/phpMYEkMl.csv')
    fs.set_persist()

Finally we run the pipeline with the new environment variables in place
and check everything runs okay.

.. code-block:: python

    fs.run_component_pipeline()

And we are there! We now know how to build a capability and set its
environment variables. The next step is to build a real pipeline and
join that with other pipelines to construct the complete master Domain
Contract.

