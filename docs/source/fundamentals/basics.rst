Introducing Capabilities
========================

Project Hadron is designed using Microservices. Microservices are an
architectural patterns that structures an application as a collection
of services, which, themselves are a component or collection of components.

Capabilities and their separation of concern are fundamental principles
in the design of Project Hadron. Capabilities can be thought of as
specialist components that refer to the range of functionalities and
features a software solution possesses, in our case, to handle and
process data for a downstream objective.

This tutorial shows the fundamentals of a capability, its ingress
throughput and egress of a dataset.

Capability Setup
----------------

For this example we are going to use the FeatureSelect capability class.
Other capability classes include FeatureEngineer, FeatureTransform,
FeatureBuild and AutoML

This set up process can be applied to any of the capability classes
as each class is built upon a common abstract class. The difference comes
when we consider actions for each capability component.

Initially we import the capability class, all of which can be found
in the root package tree.

.. code-block:: python

    from ds_capability import FeatureSelect

We can now create the instance of our FeatureSelect capability, but it is
important to note we don't instantiate the class directly, but years one
of the factory class methods, in this case ``from_env`` to look in the
environment for any special settings. This is the most common way to start
any of the capability components.

.. code-block:: python

    fs = FeatureSelect.from_env('my_select', has_contract=False)

The first parameter is a named identifier for this instance and used to create and
retrieve the capabilities recipe. A **receipt** can be thought of as a runbook
of instruction of the lineage of that instance. By referencing the name of
the instance, the recipe can be re-loaded and re-run creating the reusable
capability.

The final parameter `has_contract` is a fail-safe, only used on first creation
of a capability instance to validate the receipt should be empty.

---

Connectivity of our capability can be added using the method

* add_connector_uri('<name>', '<uri>')



* set_source('<file_name.ext>')
* set_source_uri('<uri>')
* add_connector_source('<name>', '<file_name.ext>')

* set_persist()
* set_persist_uri('<uri>')
* add_connector_persist('<name>', '<file_name.ext>')


.. code-block:: python

    fs.set_source_uri('https://www.openml.org/data/get_csv/16826755/phpMYEkMl.csv')
    fs.set_persist()

Run Capability
--------------

To run a capability we use the common method ``run_component_pipeline``
which loads the source data, executes the capability task then persists
the results. This is the only method you can use to run the tasks of a
capability and produce its results and should be a familiarized method.

.. code-block:: python

    fs.run_component_pipeline()

This concludes building a capability and though the capability doesn’t
change the throughput, it shows the core steps to building any capability
component.

Retrieval and Reuse
-------------------

Project Hadron came from a desire to improve the availability of objective
relevant data, increase the transparency and traceability of data lineage
and facilitate knowledge transfer, retrieval and reuse.

It was born from the frustration of working on machine learning projects
with so many indecipherable jupyter notebooks a data scientists produce,
each repeating common activities using arbitrary,localised datasets. This
indecipherability clouded the retrieval of the data scientists thinking
and the knowledge they gained from the subject matter experts they
interacted with.


Though this is a single notebook, one of the powers of Project Hadron is
the ability to reload capability state across new notebooks, not just
locally but even across locations and teams. To load the capability state
we use the same factory method ``from_env`` passing the unique capability
name ``my_select`` which reloads the named capability. We have now
reinstated the original capability state and can continue to work on
this capability.

.. code-block:: python

    fs = FeatureSelect.from_env('my_select')

Lets look at a sample of some commonly used features that allow us to
peek inside the capabilities. These features are extremely useful to
navigate the capability and should become familiar.

The first and probably most useful method call is to be able to retrieve
the results of ``run_component_pipeline``. We do this using the
capability method ``load_persist_canonical``. Because of the retained
state the capability already knows the location of the results, and in
this instance returns a report.

Note: All the capabilities from a package internally work with a canonical
data set. With this package of capabilities, because they are data science
based, use Pandas Dataframes as their canonical, therefore wherever you
see the word canonical this will relate to a Pandas Dataframe.

.. code-block:: python

    df = fs.load_persist_canonical()

The second most used feature is the reporting tool for the canonical. It
allows us to look at the results of the run as an informative
dictionary, this gives a deeper insight into the canonical results.
Though unlike other reports it requests the canonical of interest, this
means it can be used on a wider trajectory of circumstances such as
looking at source or other data that is being injested by the task.

Below we have an example of the processed canonical where we can see the
results of the pipeline that was persisted. The report has a wealth of
information and is worth taking time to explore as it is likely to speed
up your data discovery and the understanding of the dataset.

.. code-block:: python

    fs.canonical_report(df)


When we set up the source and persist we use something called Connector
contracts, these act like brokers between external data and the internal
canonical. These are powerful tools that we will talk more about in a
dedicated tutorial but for now consider them as the means to talk data
to different data storage solutions. In this instance we are only using
a local connection and thus a Connector contract that manages this type
of connectivity.

In order to report on where the source and persist are located, along
with any other data we have connected to, we can use
``report_connectors`` which gives us, in part, the name of the connector
and the location of the data.

.. code-block:: python

    fs.report_connectors()


This gives a flavour of the tools available to look inside a capability
and time should be taken viewing the different reports a capability
offers.


Environment Variables
---------------------

To this point we have been using the default settings of where to store the
named contract and the persisted dataset. These are in general local
and within your working directory. The use of environment variables
frees us up to use an extensive list of connector contracts to store the
data to a location of choice.

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

