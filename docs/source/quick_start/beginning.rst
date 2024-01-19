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

Basic usage
-----------
You can run Project Hadron in your favorite code editor, Jupyter notebook, Google Colab, or
anywhere else you write Python.

Feature Build

.. code-block:: python

    from ds_capability import FeatureEngineer

    fe = FeatureEngineer.from_memory()
    tbl = fe.tools.get_synthetic_data_types(100)

This is what the data looks like

.. image:: /source/_images/quick_start/qs_01.png
  :align: center
  :width: 550

\

Feature Select

.. code-block:: python

    from ds_capability import FeatureSelect

    fs = FeatureSelect.from_memory()
    tbl = fs.tools.auto_clean_header(tbl, case='upper')
    tbl = fs.tools.auto_drop_columns(tbl, headers='STRING')


Headers changed and column dropped

.. image:: /source/_images/quick_start/qs_02.png
  :align: center
  :width: 550

\

Back to Feature Engineering

.. code-block:: python

    tbl = fe.tools.correlate_date_element(tbl, target='DATE',
                                          matrix=['yr', 'mon', 'day', 'hr', 'min'],
                                          drop_target=True)

Resulting in

.. image:: /source/_images/quick_start/qs_03.png
  :align: center
  :width: 550

\

Need to change types

Then back to Feature Selection

.. code-block:: python

    tbl = fs.tools.auto_to_string(tbl, regex=['DATE'])

    tbl.schema

Now the
