=====
Usage
=====

To use Plugs Payments in a project, add it to your `INSTALLED_APPS`:

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
