Getting Started
===============

Before we begin
---------------
Project Hadron is written in Python_. If you're new to the language you might want to start by
getting an idea of what the language is like, to get the most out of this package.

If you're already familiar with other languages, and want to learn Python quickly, the
`Python Tutorial`_ is a good resource.

If you're new to programming and want to start with Python, the following books may be useful
to you:

* `Automate the Boring Stuff With Python`_

* `How To Think Like a Computer Scientist`_

* `Learn Python 3 The Hard Way`_

You can also take a look at `this list of Python resources for non-programmers`_, as well as
the `suggested resources in the learnpython-subreddit`_.

.. _Python: https://www.python.org/
.. _this list of Python resources for non-programmers: https://wiki.python.org/moin/BeginnersGuide/NonProgrammers
.. _Python Tutorial: https://docs.python.org/3/tutorial
.. _Automate the Boring Stuff With Python: https://automatetheboringstuff.com/
.. _How To Think Like a Computer Scientist: http://openbookproject.net/thinkcs/python/english3e/
.. _Learn Python 3 The Hard Way: https://learnpythonthehardway.org/python3/
.. _suggested resources in the learnpython-subreddit: https://www.reddit.com/r/learnpython/wiki/index#wiki_new_to_python.3F

First Feature Actions
---------------------



PyArrow Table
~~~~~~~~~~~~~

.. code-block:: python

    import pyarrow as pa

    tbl = pa.table({
        "col1": [0, 2, None, 3, 1, None, 2, 2],
    })

With the results

.. code-block:: python

    pyarrow.Table
    col1: int64
    ----
    col1: [[0,2,null,3,1,null,2,2]]

Feature Engineer
~~~~~~~~~~~~~~~~

.. code-block:: python

    from ds_capability import FeatureEngineer

    fe = FeatureEngineer.from_memory()
    tbl = fe.tools.model_missing(tbl)

With the results

.. code-block:: python

    pyarrow.Table
    col1: int64
    ----
    col1: [[0,2,2,3,1,0,2,2]]

Feature Transition
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ds_capability import FeatureTransform

    ft = FeatureTransform.from_memory()
    tbl = ft.tools.scale_normalize(tbl)

Resulting in

.. code-block:: python

    pyarrow.Table
    col1: double
    ----
    col1: [[0,0.67,0.67,1,0.33,0,0.67,0.67]]


Making Reusable Actions
-----------------------

