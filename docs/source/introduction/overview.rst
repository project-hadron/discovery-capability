Why Project Hadron?
===================
Unfortunately, 85% of data science projects fail due to a lack of understanding of the real
business problem. Likewise similar is found within data provisioning for Data Lakes executing business
driven analysis. This is usually because of poor communication between data scientists, data
engineers and business teams, resulting in a disconnect between the three groups. Project Hadron
has been built to bridge the gap between these groups providing comprehensive reporting and derive
meaningful information that can be used for decision-making or further analysis.

Having the ability to derive meaningful information from a data processing pipeline is
fundamental for making informed decisions, solving problems, optimizing resource allocation and
predicting future trends. Project Hadron gives this robust and reusable, comprehensive solution
with a light footprint and is built in-house allowing flexibility and retained knowledge.

What are the key elements of its methodologies and architecture?
----------------------------------------------------------------
Project Hadron is Python package built using object-oriented design (OOD) and object-oriented
programming (OOP) to provide an extendable framework for quick build component solutions. It
uses PyArrow as its canonical combining with Pandas as a directed specialist toolset. PyArrow
complements Pandas by providing a more memory-efficient in-memory representation, enabling
effective data interchange between different systems, supporting distributed computing, and
enhancing compatibility with other programming languages. When used together, Pandas and
PyArrow form a powerful combination for handling diverse data processing tasks efficiently.

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

Then what is a hadron pipeline?
-------------------------------
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
Capabilities" and their "Separation of Concerns" are fundamental principles in the design of
Hadron, that help in creating maintainable, scalable, and modular software systems. In the context
of software development, capabilities refer to the functionalities or features that a software
system can provide. These can be identified as data selection, feature engineering and feature
transition. Separation of Concerns is a design principle that advocates breaking a software system
into distinct, independent modules or components, each addressing a specific concern or aspect of
the system's functionality. Together, defining capabilities helps in understanding what a software
system should achieve, while separation of concerns ensures that the system is designed in a
modular and maintainable way, with each part addressing a specific aspect of its functionality.
Both principles contribute to building robust and scalable software architectures.

Where Can it be Applied?
------------------------
Project Hadron capabilities can be used as an SDK in Jupyter, integrating with other tools to build
Machine Learning preprocessing for algorithm optimisation. Its light footprint and quick-to-market
design lends itself perfectly to a POC in a Python IDE, while the ability to build robust
microservices and shared interoperability through PyArrow are ideal for data processing steps in
a Three Stage Data Processing.

Who would use it?
-----------------
Both developers and implementers can use Project Hadron with a broad scope of consumers of the
reporting and data output

As a developer, Project Hadron requires a knowledge of Python 3.8+ and PyArrow. It can be used with
any Python interface, command line, Python IDE such as PyCharm or Visual Studio or as Jupyter
Notebooks. Data selection, feature engineering and feature transition are the most essential part
of Hadron building a usable data pipeline and involves a skilled blend of domain expertise,
intuition and lateral thought.

As an implementer, Project Hadron component pipelines, the skill set depends very much on the
environment the pipeline is being implemented into. For example if you are implementing Hadron
pipelines into a Docker environment there are no code requirements from Hadron as it is presented
as a Docker image and the parameters around that. This will be the same for most implementations,
brad there is no or low code input.


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

