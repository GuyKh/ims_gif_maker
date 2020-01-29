ims_gif_maker
{{ ims_gif_maker|count * "=" }}

{% if cookiecutter.readme_pypi_badge -%}
.. image:: https://img.shields.io/pypi/v/ims_gif_maker.svg
    :target: https://pypi.python.org/pypi/ims_gif_maker
    :alt: Latest PyPI version
{%- endif %}

{% if cookiecutter.readme_travis_badge -%}
.. image:: {{ cookiecutter.readme_travis_url }}.png
   :target: {{ cookiecutter.readme_travis_url }}
   :alt: Latest Travis CI build status
{%- endif %}

{{ cookiecutter.package_description }}

Usage
-----

Installation
------------

Requirements
^^^^^^^^^^^^

Compatibility
-------------

Licence
-------

Authors
-------

`ims_gif_maker` was written by `Guy Khmelnitsky guykhmel@gmail.com>`_.
