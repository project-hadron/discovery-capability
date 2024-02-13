==============
Project Hadron
==============

Overview
========

**Project Hadron** is an open-source application framework for in-memory preprocessing, where
data analysis, machine learning, and other data-intensive tasks require efficiency and speed.
With :Apache Arrow as its canonical, and a more directed use of pandas,
**Project Hadron** offers effective data management, extensive interoperability, improved memory
management and hardware optimization.

At its concept, **Project Hadron** was conceived with a desire to improve the availability of
objective relevant data, increase the transparency and traceability of data lineage and facilitate
knowledge transfer, retrieval and reuse.

At its core **Project Hadron** is a selection of capabilities that
represent an encapsulated set of actions that act upon a given set of features or dataset. An
example of this would be FeatureSelection, a capability class, encapsulating cleaning data by
removing uninformative columns.

For a more in-depth view of **Project Hadron** read the supporting `documentation`_.


Installation
============

Python editing
--------------

You can run Project Hadron in your favorite code editor, Jupyter notebook, Google Colab, or
anywhere else you write Python.

Python version
--------------

We recommend using the latest version of Python. Project Hadron supports Python 3.8 and newer.

Package installation
--------------------
The best way to install the component packages is directly from the `Python Package Index`_
using pip.

The component package is ``discovery-capability`` and pip installed with:

.. code-block:: text

    $ python -m pip install discovery-capability

if you want to upgrade your current version then using pip install upgrade with:

.. code-block:: text

    $ python -m pip install -U discovery-capability

This will also install or update dependent third party packages. The dependencies are limited to
Python, PyArrow and related Data manipulation tooling such as Pandas, Numpy, scipy, scikit-learn
and visual packages matplotlib and seaborn, and thus have a limited footprint and non-disruptive
installation in a data processing environment.

dependencies
~~~~~~~~~~~~
Project Hadron is written in pure Python and depends on a few key Python packages. These should
be installed as parge of the pip installation but for troubleshooting, they are:

* pyarrow_, provides a cross-language, in-memory columnar data representation
* pandas_, versatile data manipulation and analysis toolset
* numpy_, core library for numerical and mathematical operations
* scipy_, scientific computing library that extends the functionality of NumPy
* scikit-learn_, machine learning library with a focus on predictive data analysis
* matplotlib_, versatile 2D plotting library
* seaborn_, statistical data visualization library built on top of Matplotlib

In case of any trouble related to these dependencies, please refer to their respective
installation instructions.

Virtual environments
--------------------

Use a virtual environment to manage the dependencies for your project, both in
development and in production.

What problem does a virtual environment solve? The more Python projects you
have, the more likely it is that you need to work with different versions of
Python libraries, or even Python itself. Newer versions of libraries for one
project can break compatibility in another project.

Virtual environments are independent groups of Python libraries, one for each
project. Packages installed for one project will not affect other projects or
the operating system's packages.

Python comes bundled with the :mod:`venv` module to create virtual
environments.

create an environment
~~~~~~~~~~~~~~~~~~~~~

Create a project folder and a :file:`.venv` folder within:

macOS/Linux

.. code-block:: text

    $ mkdir myproject
    $ cd myproject
    $ python3 -m venv .venv

Windows

.. code-block:: text

    > mkdir myproject
    > cd myproject
    > py -3 -m venv .venv

activate the environment
~~~~~~~~~~~~~~~~~~~~~~~~

Before you work on your project, activate the corresponding environment:

macOS/Linux

.. code-block:: text

    $ . .venv/bin/activate

Windows

.. code-block:: text

    > .venv\Scripts\activate

Your shell prompt will change to show the name of the activated
environment.

Viewing examples
----------------

As said before, you can run Project Hadron in your favorite code editor, but to help any
tutorial documentation, you can find examples of the code on GitHub as Jupyter notebooks.

Jupyter Notebooks and Jupyter Labs are available for installation via the `Python Package Index`_
using pip.

We recommend installing JupyterLab with pip:

.. code-block:: text

    $ pip install jupyterlab

Once installed, launch JupyterLab with:

.. code-block:: text

    $ jupyter lab

For more information on JupyterLab go to the `Jupyter documentation`_

Next Steps
==========

To get started go to the `documentation`_ and work through the Getting Started use case.

License
-------
This project uses the following license:
MIT License: `<https://opensource.org/license/mit/>`_.


.. _documentation: https://discovery-capability.readthedocs.io/en/latest/index.html
.. _Python Package Index: https://pypi.org/
.. _Jupyter documentation: https://jupyter.org/
.. _pyarrow: https://arrow.apache.org/
.. _pandas: https://pandas.pydata.org/
.. _numpy: https://numpy.org/
.. _scipy: https://scipy.org/
.. _scikit-learn: https://scikit-learn.org/stable/
.. _matplotlib: https://matplotlib.org/
.. _seaborn: https://seaborn.pydata.org/


