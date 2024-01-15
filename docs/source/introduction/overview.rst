Why Project Hadron?
===================

What is Project Hadron?
-----------------------
Unfortunately, 85% of data science projects fail due to a lack of the ability to retrieve the right
features from a data pipeline, and communicate with a broadly skilled audience. Similar can be
found within data provisioning for Data Lakes executing business driven analysis.

**Project Hadron** is a data preprocessing and data processing pipeline. It is a comprehensive
set of tools to build improved and targeted features of interest. It manages data sourcing and
persistence and captures discovery activities that provide a better shared environment and
insight into idea generation.

Additionally the low success rate of projects is exacerbated by poor communication between data
scientists, data engineers and business stakeholders, resulting in a disconnect between the three
groups. Project Hadron has been built to bridge this gap between these groups providing comprehensive
reporting and derive meaningful information that can be used for decision-making or further
analysis.

Project Hadron, as a data processing step, is quick-to-market, identifying
failures early and ensuring robust foundations for success. It handles large data through memory
efficiency, facilitates interoperability and optimisation of CPU and GPU acceleration. Project
Hadron, as a reusable, comprehensive solution with a light touch, is built in-house allowing
flexibility, adaptability and retained knowledge.

What are its methodologies and architecture?
--------------------------------------------
Project Hadron is Python package built using object-oriented design (OOD) and object-oriented
programming (OOP) to provide an extendable framework for quick build component solutions. When used
together, Pandas and PyArrow form a powerful combination for handling diverse data processing tasks
efficiently.

It is designed to be used as a development and discovery toolset or a set of Microservices
within a data processing pipeline, with each Microservice having its own pipeline of capabilities.
Each capability, and thus pipeline, has its own reporting methods providing transparency and
traceability.

Where does it sit within a system pipeline?
-------------------------------------------
Project Hadron provides functionalities fundamental to data processing, and as such targets machine
learning preprocessing pipeline and data processing pipeline, though its application can be applied
far wider.

The term "preprocessing" is commonly used in the field of data science and machine learning
to refer to data selection, feature engineering and feature transformation as steps to clean,
format, and organize source data into a suitable format for the process of model evaluation &
tuning.

.. image:: /images/introduction/machine_learning_pipeline_v01.png
  :align: center
  :width: 700

\

This same process exists in 'The Three Stages of Data Processing', but in this case known
simply as data processing. The architecture consists of three essential elements: a source or
sources, processing steps, and a destination. Just as with machine learning preprocessing,
these steps include transformation, augmentation, filtering, grouping, and aggregation.

.. image:: /images/introduction/three_phase_pipeline_v01.png
  :align: center
  :width: 650

\

To note, extract, transform, and load (ETL) systems are a kind of data pipeline in that they move
data from a source, transform the data, and then load the data into a destination. But ETL is
usually just a sub-process. Depending on the nature of the pipeline, ETL may be automated or
may not be included at all. On the other hand, a data pipeline is broader in that it is the entire
process involved in transporting data from one location to another.

Then what is a capability pipeline?
-----------------------------------
Project Hadron for data processing has been built as a set of capabilities to handle the
different types of processing data. These are Data Selection, Feature Engineering, Feature
Transition and Feature Build, for specialized capabilities. In order to be able to run these
capabilities as a cohesive microservice, a specialist capability, called a Controller, coordinates
the running order of these capabilities, that form the microservice.

.. image:: /images/introduction/hadron_data_pipeline_overview.png
  :align: center
  :width: 400

\

From the diagram you can see the encapsulated microservice within which the Hadron pipeline exists.
This is referred to as a component pipeline, and each capability referred to as a component
capability or just a component.  Each component has their own runbook script which defines the
component and how it runs. The Controller also has its own runbook script which describes how the
component pipeline should run.

This means that component pipelines can go from simple input output microservices to more complex
and dependent solution pipelines.

.. image:: /images/introduction/hadron_data_pipelines_type1.png
  :align: center
  :width: 600

\

fig. 1 Shows a straight through process with one source and one output and three capability
components.

fig. 2 maintains a single source but in this case each capability has its own output.

.. image:: /images/introduction/hadron_data_pipelines_type2.png
  :align: center
  :width: 700

\

fig. 3 shows a more complex multi input with five components and two merging pipelines being
encapsulated within a single microservice,

fig. 4, while still providing the same complex input output, has been separated into
three microservices with the responsibility of managing the pipeline with the environment system.

This allows the designer and implementer to choose the best way to manage and monitor a set of
component pipelines.

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

Where can it be applied?
------------------------
Project Hadron is targeted at data improvement for all types of data processing and runs in the
relevant environment for the user of the tool. It can run as (1) a complementary functional toolkit in
Jupyter Notebooks for Data Scientists, (2) an object oriented collection of abstract and concrete
classes for a Python IDE, such as PyCharm or Visual Studio, (3) or an implementation of a script
image into a Docker environment or as a collection of Microservices in a cloud-native
architecture. Its light footprint and quick-to-market design lends itself perfectly to pilots and
POCs when including its extensive interoperability. It targets Data Science environments, allowing a vastly
improved set of background systems for data management and idea sharing, of knowledge retention and
separation of concerns. It integrates with familiar Data Science tools while offering functions to
uncover features, provide robustness, and elevate ideas to a broad audience.

Who would use it?
-----------------
As a Data Scientist. Project Hadron requires a knowledge of Python 3.8+, PyArrow, Pandas, Numpy as
a core with a skilled blend of domain expertise, inference and the ability to adopt alternative
systems to improve project sharing and feature identification. An understanding of Jupyter
Notebooks or Jupyter Lab.

As a software developer, Project Hadron requires a knowledge of Python 3.8+ and PyArrow. A good
understanding of some sort of Python interface, or Python IDE such as PyCharm or Visual Studio or as
Jupyter Notebooks. Data selection, feature engineering and feature transition are the most
essential part of Hadron, building a usable data pipeline and involves a skilled blend of domain
expertise, intuition and lateral thought.

As an implementer, Project Hadron component pipelines, the skill set depends very much on the
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
contributed to its wide usage in data engineering, analytics, and other data-intensive applications.

Main features
-------------

* Data Selection
* Feature Engineering
* Feature Transformation
* Knowledge Augmentation
* Apache PyArrow Canonical
* large Data Processing
* Interoperability
* MicroServices
* Reuse

Data Selection
~~~~~~~~~~~~~~



Data Reporting
--------------
* Data Lineage
* Data Profiling
* Data Traceability

