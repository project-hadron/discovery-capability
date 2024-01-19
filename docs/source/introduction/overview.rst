Why Project Hadron?
===================

What are we solving?
--------------------
The 80/20 rule, also known as the Pareto Principle, is a concept widely used in various fields,
including data engineering and data science to denote the imbalance between effort and purpose.

In the context of data engineering, the 80/20 rule suggests that approximately 80% of the effects
or outcomes come from 20% of the causes or inputs, such as data veracity, software governance
and solution reuse. While with data scientists, the 80/20 rule suggests that approximately 80% of
time is spent finding, cleaning, and extracting features of interest with only 20% to perform data
analytics initiatives. In addition Gartner suggests, 85% of data science initiatives fail because
they don’t deliver business benefits because they solve the wrong problem.

Further more research shows 62% of data processing pipelines depend on others within their
organization to perform certain steps, within stringent deadlines, in a data processing pipeline.
Yet poor communication and limited visibility between data scientists, data engineers and business
stakeholders directly effects success of business objectives.

Where does Project Hadron fit?
------------------------------
**Project Hadron** is an open-source application framework, taking raw data and identifying,
analysing and extracting prepared data for the purposes of a down stream business objective.

**Project Hadron** is a comprehensive set of tools to build, improved and targeted features of
interest within a data preprocessing pipeline. It complements and enhances both communication and
redistribution within a data science project, while providing clear boundaries between the
preprocessing of data and algorythm optimisation. This separation promotes
transparency and reuse, vastly improving the identification and extraction of features of interest.

**Project Hadron**, within a data processing step, executing business driven analysis, is a
quick-to-market, robust set of tools that build reusable pipelines for the interrogation and
restructure of data for a target use case. It helps in identifying potential failures at the
earliest stage and helps ensure a transparent and traceable data foundations for success. It
handles large data through memory efficiency, facilitates interoperability and optimisation of
CPU and GPU acceleration.

**Project Hadron** has been built to help bridge this gap between data scientists, data engineers
and business stakeholders with a comprehensive set of reporting tools covering data profiling,
data lineage and knowledge acquisition. Its targeted reports can be directly delivered as
spreadsheets for stakeholders, absorbed into an already existing reporting tool for analytics or
saved in cloud storage all saved in parquet files for interoperability with other solutions.

Within the context of data processing, Project Hadron offers data governance optimization, data
quality consistency, data efficiency improvement and risk of error reduction.

What are its design methodologies?
----------------------------------
Project hadron is an open-source application framework, written in pure Python using pyarrow as its
canonical and depends on a few key Python packages found in any analytics environment such as
Pandas and Numpy.

Project Hadron was constructed using object-oriented design (OOD) and object-oriented programming
(OOP) techniques to provide an extendable framework for quick build component solutions. When used
together, Pandas and PyArrow form a powerful combination for handling diverse data processing tasks
efficiently.

It is designed to be used as a development and discovery toolset or a set of Microservices
within a data processing pipeline, with each Microservice having its own pipeline of capabilities.
Each capability, and thus pipeline, has its own reporting methods providing transparency and
traceability.

Where does it sit within a system pipeline?
-------------------------------------------
Project Hadron provides functionalities fundamental to the optimisation and appropriateness of
tabular data for a downstream business objective. As such it places itself as a machine learning
preprocessing or data processing step, though its application can be applied far wider.

Preprocessing, in the context of data science and machine learning, refers to data selection,
feature engineering and feature transformation as steps to clean, format, and organize source
data into a suitable format for the process of model evaluation and tuning.

.. image:: /source/_images/introduction/machine_learning_pipeline_v01.png
  :align: center
  :width: 700

\

This same process exists in 'The Three Stages of Data Processing', where the architecture consists
of three essential elements: a source or sources, processing steps, and a destination. Similar to
the machine learning preprocessing, these steps include transformation, augmentation, filtering,
grouping, and aggregation.

.. image:: /source/_images/introduction/three_phase_pipeline_v01.png
  :align: center
  :width: 650

\

What are capabilities?
----------------------

Capabilities and their separation of concern are fundamental principles in the design of Project
Hadron. Capabilities refer to the range of functionalities and features a software solution
possesses, in our case, to handle and process data efficiently. Within Project Hadron these
capabilities can be identified as

    * data selection
    * feature engineering for creation
    * feature engineering for correlation
    * feature engineering for modelling
    * feature transition

Separation of concerns (SoC) is a design principle that advocates breaking a software system
into distinct, independent modules or components, each addressing a specific concern or aspect of
the system's functionality. Together, defining capabilities helps in understanding what a software
system should achieve, while separation of concerns ensures that the system is designed in a
modular and maintainable way, with each part addressing a specific aspect of its functionality.
Both principles contribute to building modular, robust and scalable software solutions.

Then what is a capability recipe?
---------------------------------
Capabilities, on their own, are tightly focused on their concerns, albeit with a use case in mind.
It is not till we collectively link our capabilities in a meaningful order, we build our reusable use case or
microservice. In order to capture a set of capabilities into a reusable
microservice, Project Hadron creates a collection of capabilities, and their actions, that relate
to a reusable test to a encapsulating how they should run.

It has been built as a set of capabilities to handle the
different types of processing data. These are Data Selection, Feature Engineering, Feature
Transition and Feature Build, for specialized capabilities. In order to be able to run these
capabilities as a cohesive microservice, a specialist capability, called a Controller, coordinates
the running order of these capabilities, that form the microservice.

.. image:: /source/_images/introduction/hadron_data_pipeline_overview.png
  :align: center
  :width: 400

\

From the diagram you can see the encapsulated microservice within which the Hadron capabilities
exists. This is referred to as a capability recipe, and each capability referred to as a component
capability or just a component.  Each component has their own runbook script which defines the
component and how it runs. The Controller also has its own runbook script which describes how the
capability recipe should run.

This means that capability recipes can go from simple input output microservices to more complex
and dependent solution pipelines.

.. image:: /source/_images/introduction/hadron_data_pipelines_type1.png
  :align: center
  :width: 600

\

fig. 1 Shows a straight through process with one source and one output and three capability
components.

fig. 2 maintains a single source but in this case each capability has its own output.

.. image:: /source/_images/introduction/hadron_data_pipelines_type2.png
  :align: center
  :width: 700

\

fig. 3 shows a more complex multi input with five components and two merging pipelines being
encapsulated within a single microservice,

fig. 4, while still providing the same complex input output, has been separated into
three microservices with the responsibility of managing the pipeline with the environment system.

This allows the designer and implementer to choose the best way to manage and monitor a set of
capability recipes.

Where can Project Hadron be applied?
------------------------------------
Project Hadron can run as (1) a complementary functional toolkit in
Jupyter Notebooks for Data Scientists, (2) an object oriented collection of abstract and concrete
classes for a Python IDE, such as PyCharm or Visual Studio, (3) or an implementation of a script
image into a Docker environment or as a collection of Microservices in a cloud-native
architecture.

Written in pure Python and depends on only a few well-established and supported Python packages,
Project Hadron's quick-to-market design lends itself pilots and with extensive interoperability,
POCs. Its robustness and reuse along with its implementation as microservices place it in any
larger project for data analytics and data processing.

Who would use Project Hadron?
-----------------------------
As a Data Scientist. Project Hadron requires a knowledge of Python 3.8+, PyArrow, Pandas, Numpy as
a core with a skilled blend of domain expertise, inference and the ability to adopt alternative
systems to improve project sharing and feature identification. An understanding of Jupyter
Notebooks or Jupyter Lab.

As a software developer, Project Hadron requires a knowledge of Python 3.8+ and PyArrow. A good
understanding of some sort of Python interface, or Python IDE such as PyCharm or Visual Studio or
as Jupyter Notebooks. Data selection, feature engineering and feature transition are the most
essential part of Hadron, building a usable data pipeline and involves a skilled blend of domain
expertise, intuition and lateral thought.

As an implementer, Project Hadron capability recipes, the skill set depends very much on the
environment the pipeline is being implemented into. For example if you are implementing Hadron
pipelines into a Docker environment there are no code requirements from Hadron as it is presented
as a Docker image and the parameters around that. This will be the same for most implementations,
brad there is no or low code input.

What is PyArrow?
----------------
PyArrow is a Python package for Apache Arrow Python bindings. Apache Arrow is a development
platform for in-memory analytics. It contains a set of technologies that enable big data systems
to store, process and move data fast. Project Hadron uses PyArrow as its canonical combining with
Pandas as a directed specialist toolset optimizing the advantages of both.

PyArrow enhances Pandas by providing a more efficient, columnar data representation that
facilitates seamless interoperability with other systems, improved performance, and support for
efficient file formats like Parquet. It extends Pandas' capabilities, especially in scenarios
where performance and data interchange with other systems are critical. These benefits have
contributed to its wide usage in data engineering, analytics, and other data-intensive
applications.

For more information visit `Apache Arrow`_

.. _Apache Arrow: https://arrow.apache.org/

Quick glance features
---------------------

Capabilities
~~~~~~~~~~~~

* Data Selection
* Feature Creation
* Feature Transformers
* Time series
* Knowledge Augmentation

Performance
~~~~~~~~~~~

* Apache PyArrow Canonical
* improved memory management
* large Data Processing
* Interoperability
* MicroServices
* Reuse

Reporting
~~~~~~~~~

* Data Lineage
* Data Profiling
* Knowledge Acquisition

