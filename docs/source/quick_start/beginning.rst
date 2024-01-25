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
        "col1": [0, 2, None, 3, 1, None, 2, 2, 3, 1],
        "col2": [0]*10
    })

With the results

.. code-block:: python

    pyarrow.Table
    col1: int64
    col2: int64
    ----
    col1: [[0,2,null,3,1,null,2,2,3,1]]
    col2: [[0,0,0,0,0,0,0,0,0,0]]

Feature Select
~~~~~~~~~~~~~~

.. code-block:: python

    from ds_capability import FeatureSelect

    fs = FeatureSelect.from_memory()
    tbl = fs.tools.auto_drop_noise(tbl)

With result

.. code-block:: python

    pyarrow.Table
    col1: int64
    ----
    col1: [[0,2,null,3,1,null,2,2,3,1]]

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
    col1: [[0,2,2,3,1,2,2,2,3,1]]

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
    col1: [[0,0.67,0.67,1,0.33,0.67,0.67,0.67,1,0.33]]

Making Reusable Capabilities
----------------------------

Environment
~~~~~~~~~~~

.. code-block:: python

    import os

    os.environ['HADRON_CLEAN_SOURCE_URI'] = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv'
    os.environ['HADRON_CLEAN_PERSIST_URI'] = 'event://demo/'

Feature auto clean
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ds_capability import FeatureSelect

    fs = FeatureSelect.from_env('auto_clean', has_contract=False)
    fs.set_source_uri('${HADRON_CLEAN_SOURCE_URI}')
    fs.set_persist_uri('${HADRON_CLEAN_PERSIST_URI}')

    tbl = fs.load_source_canonical()

    tbl = fs.tools.auto_clean_header(tbl)
    tbl = fs.tools.auto_drop_noise(tbl)
    tbl = fs.tools.auto_drop_correlated(tbl)
    tbl = fs.tools.auto_drop_duplicates(tbl)

Capability registration
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from ds_capability import Controller

    ctr = Controller.from_env(has_contract=False)
    ctr.register.feature_select('auto_clean')

Receipt reuse
~~~~~~~~~~~~~

.. code-block:: python

    import os

    os.environ['HADRON_CLEAN_SOURCE_URI'] = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv'
    os.environ['HADRON_CLEAN_PERSIST_URI'] = 'event://demo/'

    os.environ['HADRON_PM_REPO'] = './hadron/contracts/'


.. code-block:: python

    from ds_capability import Controller

    ctr = Controller.from_env()
    ctr.run_controller()

Proof of outcome
~~~~~~~~~~~~~~~~

.. code-block:: python

    ctr.set_persist_uri('event://demo/')
    ctr.load_persist_canonical().column_names

Shown new headers

.. code-block:: python

    ['total_bill', 'tip', 'sex', 'smoker', 'day', 'time', 'size']

Our receipt `auto_clean` can now be used on any dataset.