sokoenginepy - Sokoban and variants game engine
***********************************************

.. start-badges

|version| |license| |travis| |docs| |requirements| |codacy_grade| |codacy_coverage| |wheel| |python_versions|

.. |version| image:: https://img.shields.io/pypi/v/sokoenginepy.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/sokoenginepy/

.. |license| image:: https://img.shields.io/pypi/l/sokoenginepy.svg
    :alt: License
    :target: https://opensource.org/licenses/GPL-3.0

.. |wheel| image:: https://img.shields.io/pypi/wheel/sokoenginepy.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/sokoenginepy/

.. |python_versions| image:: https://img.shields.io/pypi/pyversions/sokoenginepy.svg
    :alt: Supported versions
    :target: https://pypi.org/project/sokoenginepy/

.. |python_implementations| image:: https://img.shields.io/pypi/implementation/sokoenginepy.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/sokoenginepy/

.. |travis| image:: https://api.travis-ci.org/tadams42/sokoenginepy.svg
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/tadams42/sokoenginepy

.. |docs| image:: https://readthedocs.org/projects/sokoenginepy/badge/?style=flat
    :target: http://sokoenginepy.readthedocs.io/en/latest/
    :alt: Documentation Status

.. |requirements| image:: https://requires.io/github/tadams42/sokoenginepy/requirements.svg?branch=master
     :target: https://requires.io/github/tadams42/sokoenginepy/requirements/?branch=master
     :alt: Requirements Status

.. |codacy_grade| image:: https://api.codacy.com/project/badge/Grade/492a7c08b97e4dbe991b0190dd3abf02
    :alt: Codacy grade
    :target: https://app.codacy.com/app/tadams42/sokoenginepy/dashboard

.. |codacy_coverage| image:: https://api.codacy.com/project/badge/Coverage/492a7c08b97e4dbe991b0190dd3abf02
    :alt: Codacy coverage
    :target: https://app.codacy.com/app/tadams42/sokoenginepy/dashboard

.. end-badges

sokoenginepy is game engine for Sokoban and variants, written in Python and loaded with features:

- implements game logic for ``Sokoban``, ``Hexoban``, ``Trioban`` and ``Octoban`` variants
    - supports ``Sokoban+`` for all implemented variants
    - supports ``Multiban`` (muliple pushers on board) for all variants
- reading and writing level collections
    - fully compatible with `SokobanYASC`_ .sok file format and variants (.xsb, .tsb, .hsb, .txt)
- Optional C++ native bindings using `pybind11`_ and `Boost.Graph`_ for ultimate speed

sokoenginepy was inspired by `SokobanYASC`_, `JSoko`_, MazezaM

Installing
----------

Installing sokoenginepy should be as simple as

.. code-block:: sh

    pip install sokoenginepy

There is optional C++ native extension that is built automatically with ``pip
install`` if all dependencies are met. It relies on `Boost.Graph`_ and `pybind11`_. `Boost.Graph`_ needs to be installed on system, everything else is pulled automatically:

.. code-block:: sh

    sudo apt install python3-dev libboost-graph-dev

Using
-----

- For quick glance of features and usage check the `Tutorial`_.
- For in-depth docs of whole package see `API Reference`_.
- For C++ library API docs see `C++ API Reference`_


.. _pybind11: http://pybind11.readthedocs.io/en/stable/index.html
.. _NetworkX: https://networkx.github.io/
.. _Boost.Graph: http://www.boost.org/doc/libs/1_61_0/libs/graph/doc/index.html
.. _SokobanYASC: https://sourceforge.net/projects/sokobanyasc/
.. _JSoko: https://www.sokoban-online.de/
.. _Sokobano: http://sokobano.de/en/index.php
.. _Sokoban for Windows: http://www.sourcecode.se/sokoban/
.. _Tutorial: https://sokoenginepy.readthedocs.io/en/latest/tutorial.html
.. _API reference: https://sokoenginepy.readthedocs.io/en/latest/api.html
.. _C++ API Reference: http://tadams42.github.io/sokoenginepy/
