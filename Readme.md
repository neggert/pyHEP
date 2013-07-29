pyHEP
=====

A package for working with high-energy physics data in python. This package is
intended to provide an alternative to the C++/ROOT ecosystem, with a focus
on ease of use.

Unlike in C++, many of the mathematical tools needed for analysis are already
present in python, though the excellent [numpy](http://www.numpy.org) and [scipy](http://www.scipy.org)
packages. This package does not attempt to duplicate that functionality, but rather
focusses on the subset of tasks that are unique to HEP.

The main tool in pyHEP is a full-featured Lorentz four vector class. It also provides
data structures for events and ensembles of events. Ensembles of events can be saved
to disk easily. To do this, pyHEP makes use of the [Zope Object Database](http://www.zodb.org).

Many of the ideas in this package are borrowed from [ROOT](http://root.cern.ch),
but implemented in a more python-like way.

The code includes fairly extensive docstrings, and work is underway to add a more complete
set of examples. This is very early code and is far from feature-complete, so use at your
own risk. I'm taking feature requests, so please leave those and bug reports on the issues
page.
