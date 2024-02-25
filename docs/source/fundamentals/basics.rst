Introducing Capabilities
========================

Project Hadron is designed using Microservices. Microservices are an
architectural patterns that structures an application as a collection
of services, which, themselves are a component_ or collection of components.
In Project Hadron these components are known as capabilities.

.. _component: https://en.wikipedia.org/wiki/Component-based_software_engineering

Capability Fundamentals
-----------------------

Capabilities are components that adhere to the fundamental concepts
of `capability  patterns`_ and `separation of concern`_ (SoC). They are design patterns
and principle that advocates breaking a software system into distinct, independent
modules or components with, low coupling and high cohesion each addressing a specific
concern or aspect of the system's functionality.

Capabilities are reusable and encapsulated tasks which can be applied at any stage of the
life cycle and prescribes a work breakdown structure of functionalities and features a
software solution possesses.

**Capability patterns** is a design pattern that express and communicate process knowledge
for a key area of interest, such as a discipline, and can be directly used by process
practitioners to guide their work. Capability patterns are also used as building blocks
to assemble delivery processes ensuring optimal reuse and application of the key
practices they express

**Separation of concerns** is a design principle that advocates breaking a software
system into distinct, independent modules or components, each addressing a specific
concern while advocating low coupling and high cohesion. This approach aims to enhance
maintainability, scalability, and flexibility by isolating different concerns. It
advocates the modification and extension of specific components without affecting others,
leading to a more modular and comprehensible system.

Together, capability patterns help in understanding what a reusable component task should
achieve, while separation of concerns ensures that the component task is designed in a
modular and maintainable way, with each part addressing a specific aspect of its
functionality. Both principles contribute to building directed, modular, robust and
scalable software solutions.

.. _capability  patterns: https://www.ibm.com/docs/en/engineering-lifecycle-management-suite/lifecycle-optimization-method-composer/7.6.0?topic=processes-capability-patterns
.. _separation of concern: https://en.wikipedia.org/wiki/Separation_of_concerns

Capability Design
-----------------

Each capability class has a parent abstract component class. This means that all
capability instances share common behavior in initialization, connectivity management,
reporting and running the component.

.. image:: /source/_images/fundamentals/component_class_uml.png
  :align: center
  :width: 700

* UML capability component class diagram

Though capabilities share common actions, those actions, and other metadata, are recorded
as a unique runbook of instruction of the :ref:`lineage<Reports: Data Lineage>` of that
instance. This runbook is known as a capability **recipe** that contain all information
relating to a capability, capturing the state of a capability at that moment in time. At
creation the creator gives the capability a unique name that is used identify its recipe.
At initialization, by passing the name, you load the receipt from its previous state,
whereby it can be modified, enhanced or re-run, and then re-saved in its new state.

Capability Structure
--------------------

For this example we are going to use the FeatureSelect capability class.
Other capability classes include FeatureEngineer, FeatureTransform,
FeatureBuild and FeaturePredict

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
important to note we don't instantiate the class directly, but make use
of the factory class methods. In this case ``from_env`` is used to look in the
:ref:`environment<Environment>` for any special settings. This
is the most common way to start any of the capability components.

.. code-block:: python

    fs = FeatureSelect.from_env('my_select', has_contract=False)

The first parameter is a named identifier for this instance and used to create and
retrieve the capabilities recipe containing the current state of the capability.

The final parameter `has_contract` is a fail-safe, only used on first creation
of a capability instance, to validate the recipe should be empty.

connectivity
^^^^^^^^^^^^

A key component of our capability is to be able to get data in and out. This
is achieved through the capabilities connectivity methods. In order to retrieve
data, we initially set up a connector contract which contains the information
for a data source, be it a database, file or cloud storage. This does not
retrieve the data but sets up the parameters of where to retrieve the data.

The base methods call is:

* add_connector_uri('<connector_name>', '<uri>')

where `connector_name` is the :ref:`connector<Introducing Connectors>` reference name
and the `uri` is a fully qualified URI reference to the data or feature set.

For ease of coding this method has been extended to mirror the source
and the persist, where source is a read-only sub-class of the persist class.
Though you can use persist for all your connectivity, it is good practice
to use the read-only source calls when referencing downstream data to
protect from accidental overwrite.

The methods `set_source(...)` and `set_persist()` use the environment variable
`HADRON_DEFAULT_PATH`, which, by default, is set to point to a local path.
You can find more on this at `Environment`_. With `set_persist()`
there is the option to be able to set the name of the target file, otherwise
a default name is used.

For ease, all the `set_` methods automatically set a standard name reference,
more of which is in the next section. While the `add_connector_` still use a
reference name to allow new connect pipelines to restrict those pipelines
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
as reference. The other method calls are shortcuts with the connector name
assumed from the call.

**load**

* load_canonical('<connector_name>')
* load_source_canonical()
* load_persist_canonical()

**save**

* save_canonical('<connector_name>', canonical)
* save_persist_canonical(canonical)

For ease, the add and set connectivity methods return the class instance
allowing you to chain the set with the load, for example:

.. code-block:: python

    tbl = fs.set_source('myfile.parquet').load_source_canonical()

Both setting the source and returning the canonical table

run pipeline
^^^^^^^^^^^^
To this point we have created our core recipe for this capability.
Though there are no actions associated, using the common method calls,
we have created a working capability that ingest data from where we require,
passes it through our component and persists it to a location specified.

But rather than write this each time we want to be able to run our capability,
using the recipe, created in the background from our activities, to repeat
those activities. We do this through the `run_component_pipeline` method
call.

This call reads the recipe, loading the source data, executing the capability
task, of which there are none, then persists the results. As this is a background
process, it expects the source and persist connector contracts to be set.

.. code-block:: python

    fs.run_component_pipeline()

To view the results of the run you simply load the persisted data.

.. code-block:: python

    tbl = fs.load_persist_canonical()

To view the connectivity of where the data came from and went to, use the
connectivity report

.. code-block:: python

    report = fs.report_connectors()

To view the data itself as a readable table, the two following calls might
be useful, and certainly worth an explore.

.. code-block:: python

    data_dictionary = fs.canonical_report(canonical=tbl)

    data_head = fs.table_report(canonical=tbl, head=5)

Understanding these first order calls in a capability, gives you access to understanding
all capabilities at there base methods and create components quickly ready to add
the actions pertinent to each capability.

Environment
-----------

To this point we have been using the default settings of where to find the named
source and store the persisted dataset. In addition the default location of
where to store the capability recipes is also set. These are set up at initialization
as environment variables and are relative to your working directory.

The current set of environment variables can be viewed with the report

.. code-block:: python

    report = fs.report_environ()

The first notable environment variable observed from the report is:

* HADRON_DEFAULT_PATH

Indicating the location of a default path where data can be retrieved and placed. By
changing the paths to an shared location, for example, would allow cooperation between
team members through sharing common data resources.

This templated path only applies to `set_source('<file_name.ext>')` and
`set_persist()`, where the others require a fully qualified URI.

In addition environment variables can be user-defined, for example if you wanted
to have a dynamic URI, set up at run time. This is simply achieved by including as
an environment variable the name of your adhoc reference and then referring to it
in your call as a string with the $ sign and wrapped using braces.

.. code-block:: python

    os.environ['HADRON_EXAMPLE_URI'] = 's3://bucket/path/file.csv'

    fs.set_source_uri('${HADRON_EXAMPLE_URI}')

Here we set the environment variable, and then set the dynamic value as our source
URI. This same technique applies to some action parameters that can take a special
variable as its value. As good practice, reduce conflicts and to ensure compatibility
with the `report_environ()`, you should always start your environment variable with
`HADRON_`.

Capability API
--------------

.. toctree::
   :maxdepth: 1

   capability_connect
   capability_io
   capability_run