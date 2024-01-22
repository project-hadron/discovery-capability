Installation
============

Python editing
--------------

You can run Project Hadron in your favorite code editor, Jupyter notebook, Google Colab, or
anywhere else you write Python.

Python Version
--------------

We recommend using the latest version of Python. Project Hadron supports Python 3.8 and newer.

Package Installation
--------------------
The best way to install the component packages is directly from the Python Package Index
(PPI) repository using pip.

The component package is ``discovery-capability`` and pip installed with:

.. code-block:: bash

    python -m pip install discovery-capability

if you want to upgrade your current version then using pip install upgrade with:

.. code-block:: bash

    python -m pip install -U discovery-capability

This will also install or update dependent third party packages. The dependencies are limited to
Python, PyArrow and related Data manipulation tooling such as Pandas, Numpy, scipy, scikit-learn
and visual packages matplotlib and seaborn, and thus have a limited footprint and non-disruptive
installation in a data processing environment.

dependancies
~~~~~~~~~~~~
Project Hadron is written in pure Python and depends on a few key Python packages. These should
be installed as parge of the pip installation but for troubleshooting, they are:

pyarrow, provides a cross-language, in-memory columnar data representation
pandas, versatile data manipulation and analysis toolset
numpy, core library for numerical and mathematical operations
scipy, scientific computing library that extends the functionality of NumPy
scikit-learn, machine learning library with a focus on predictive data analysis
matplotlib, versatile 2D plotting library
seaborn, statistical data visualization library built on top of Matplotlib


In case of any trouble related to these dependencies, please refer to their respective
installation instructions:

Release Process
---------------

Versions to be released will govern and describe how the ``discovery-capability`` produces a new
release.

To find the current version of ``discovery-capability``, from your
terminal run:

.. code-block:: bash

    $ python -c "import ds_capability; print(ds_capability.__version__)"

Major Releases
**************

A major release will include breaking changes. When it is versioned, it will
be versioned as ``vX.0.0``. For example, if the previous release was
``v10.2.7`` the next version will be ``v11.0.0``.

Breaking changes are changes that break backwards compatibility with prior
versions. The majority of changes to the dependant core abstraction will result in a
major release.

Project Hadron is committed to providing a good user experience
and as such, committed to preserving backwards compatibility as much as possible.
Major releases will be infrequent and will need strong justifications before they
are considered.

Minor Releases
**************

A minor release will include additional methods, classes, or noticeable modifications
to code in a backward-compatable manner which may include miscellaneous bug fixes.
If the previous version released was ``v10.2.7`` a minor release would be versioned
as ``v10.3.0``.

Minor releases will be backwards compatible with releases that have the same
major version number. In other words, all versions that would start with
``v10.`` should be compatible with each other.

Patch Releases
**************

A patch release include small and encapsulated code changes that do
not directly effect a major or minor release, for example changing
``round(...`` to ``np.around(...``, and patch bug fixes that can't
wait to be released before a major or minor release. If the previous
version released ``v10.2.7`` the patch release would be versioned
as ``v10.2.8``.

