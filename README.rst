=============================
Plugs Payments
=============================

.. image:: https://badge.fury.io/py/plugs-payments.png
    :target: https://badge.fury.io/py/plugs-payments

.. image:: https://travis-ci.org/ricardolobo/plugs-payments.png?branch=master
    :target: https://travis-ci.org/ricardolobo/plugs-payments

Your project description goes here

Documentation
-------------

The full documentation is at https://plugs-payments.readthedocs.io.

Quickstart
----------

Install Plugs Payments::

    pip install plugs-payments

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'plugs_payments.apps.PlugsPaymentsConfig',
        ...
    )

Add Plugs Payments's URL patterns:

.. code-block:: python

    from plugs_payments import urls as plugs_payments_urls


    urlpatterns = [
        ...
        url(r'^', include(plugs_payments_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
