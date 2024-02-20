Implementation in Docker
========================
Docker
------

`Docker`_ is a platform for developing, shipping, and running applications in containers.
Containers are lightweight, portable, and self-contained environments that encapsulate 
all the necessary dependencies and configurations needed to run an application.

Docker provides a way to package an application with its dependencies into a container, 
which can then be run on any machine with the Docker runtime installed. This allows 
developers to create consistent environments for their applications across different 
systems, which can simplify the process of deploying and scaling applications.

Project Hadron is designed using Microservices. These components services are represented
as a capability pipeline, the metadata files of a Project Hadron component build, and can
be run as Docker Containers.

Go to `Docker installation`_ for further reading on getting started

.. _Docker: https://docs.docker.com/manuals/
.. _Docker installation: https://docs.docker.com/get-docker/

Docker Compose
--------------

Docker is the core platform for building and running containers, while `Docker Compose`_
is a tool built on top of Docker that simplifies the orchestration of multi-container
applications. For the purposes of testing and demonstration we use docker-compose where
in production, more advanced orchestration tools like Docker Swarm or Kubernetes are
often used for container orchestration at scale.

Go to `Docker compose installation`_ for further reading on getting started

.. _Docker Compose: https://docs.docker.com/compose/
.. _Docker compose installation: https://docs.docker.com/compose/install/

build compose yaml
~~~~~~~~~~~~~~~~~~

Docker Compose relies on a YAML configuration file, usually named `compose.yaml`. With
Compose, you can use a YAML file to configure your application's services, networks, and
volumes, and then use a single command to create and start all the containers that make
up your application.

An example of our docker yaml running :ref:`Use Case Two: Churn Pipeline` would be

.. code-block:: yaml

    version: '3.9'
    x-common-variables: &common-variables
      HADRON_DOMAIN_REPO_PATH: https://raw.githubusercontent.com/project-hadron/hadron-asset-bank/master/contracts/pyarrow/docs/use_case_two/
      HADRON_DEFAULT_PATH: /cache/data
    services:
      domain-controller:
        image: gigas64/hadron_pyarrow:1.4
        environment:
          <<: *common-variables
          HADRON_CHURN_SOURCE_PATH = https://raw.githubusercontent.com/project-hadron/hadron-asset-bank/master/datasets/toy_sample/churn.csv
          HADRON_CHURN_PERSIST_PATH = ./hadron/data/hadron_docs_churn_predict.parquet
        volumes:
          - ./cache:/tmp/cache

running compose
~~~~~~~~~~~~~~~

Docker Compose is a tool that allows you to define and run multi-container Docker applications. With Compose,
you can use a YAML file to configure your application's services, networks, and volumes, and then use a single
command to create and start all the containers that make up your application.

With the compose.yaml file in the same directory, run the following command to create
the docker container using docker-compose.

.. code-block:: bash

   &> docker-compose up

It will run the docker-compose in the foreground and you can not exit the terminal. To
run the compose in background, add the **-d** option with the command.

.. code-block:: bash

   &> docker-compose up -d

If the compose.yml file is not present in the current working directory or the
name of the file is other than docker-compose.yml, use the **-f** option to specify the
compose file.

.. code-block:: bash

   &> docker-compose -f ~/docker-compose/docker-compose.yml up -d

After running compose, check the status of the docker container.

.. code-block:: bash

   &> docker-compose ps

To only stop a container

.. code-block:: bash

   &> docker-compose stop

To stop and remove containers, networks, etc.

.. code-block:: bash

    $> docker-compose down

Finally, to shut down and remove volumes

.. code-block:: bash

    $> docker-compose down --volumes


Next Steps
----------

Try different capability pipeline components with additional environment variables and
use the Docker documentation to learn about Hadron containers with remote or differing
data locations.

Project Hadron has been built as a component model to fit seamlessly into an orchestration
engine for production such as Docker Swarm or Kubernetes.