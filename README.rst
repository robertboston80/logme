================================
Logme - Python Logging Made Easy
================================

.. image:: https://badge.fury.io/py/logme.svg
    :target: https://pypi.org/project/logme/

.. image:: https://travis-ci.org/BNMetrics/logme.svg?branch=master
    :target: https://travis-ci.org/BNMetrics/logme

.. image:: https://codecov.io/gh/BNMetrics/logme/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/BNMetrics/logme

.. image:: https://readthedocs.org/projects/logme/badge/?version=latest
    :target: http://logme.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Logme is a Python package that makes logging simple and robost. If you have found
logging in Python not so straight forward, download this package and give it a try! :)


In A Nutshell
-------------

If you have a function you want to log, you can do this in your python file:

.. code-block:: python

    import logme


    @logme.log
    def my_awesome_function(my_arg, logger=None):
        logger.info('this is my log message')
        """rest of the function"""


You can do the same with classes too:

.. code-block:: python

    import logme


    @logme.log
    class MyAwesomeClass:
        def my_function(self, my_arg):
            self.logger.info('this is my log message')



pretty nice right? :)

Documentation
-------------

You can find the documentation at http://logme.readthedocs.io/en/latest/ .
Give it a try!

