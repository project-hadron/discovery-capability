Introducing Connectors
======================

Project Hadron is designed using Microservices. Microservices are an architectural
patterns that structures an application as a collection of services, which, themselves
are a component or collection of components. These components are known as
:ref:`Capabilities<What are capabilities?>` and each capability has their own set of
communication outlets known as handlers.

Concepts
--------

Connector handlers are a pair of abstract classes, to handle data sourcing and data
persistence. Their design principle follow the same concepts of separation of
concerns through object-oriented design, meaning capabilities use handlers to remain
separated from data type and location until initialization. This allows different
handlers for the same capability across different implementations.

The ConnectorContract class is used as a container class to hold information on the
connection type and location and applied at implementation. By changing the
ConnectorContract you can change the handler.

.. image:: /source/_images/connectors/connector_class_uml.png
  :align: center
  :width: 700

* UML connector contract class diagram

A handler can be thought of as a broker between the internal canonical and the
data storage service format. The ConnectorContract are the dynamic instructions on where
and how the data will be located. Each connection type, AWS S3, MongoDB, Postgres, etc.,
are their own broker or handler and the ConnectorContract the dynamic link between
Capability and a dataset.

By Example
----------

When you set a :ref:`connector using a URI<connectivity>` you pass a URI that is broken
down and stored in a ConnectorContract.

.. code-block:: python

    fs.set_source_uri('https://www.openml.org/data/get_csv/16826755/phpMYEkMl.csv')

This tells us the connection schema is `https`, the address of the location, the path
and the file with its type.

Another example might be a MySQL handler with,

.. code-block:: python

    fs.set_source_uri('mysql://localhost:3306/mydb?query=SELECT cat, num FROM myTable')

Here our ConnectorContract needs to use a MySQL handler, taken from the schema, but
this is just a container and not implemented until initialisation.

As handlers guaranty returning a canonical, all handlers can be used with any capability.

When you run the request to save or load, at that point the ConnectorContract is
allocated to the appropriate handler.

