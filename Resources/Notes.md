# Notes

[TOC]

## SQLAlchemy

SQLAlchemy is the Python SQL toolkit and Object Relational Manager that gives app developers full power of SQL



Common Task when programming any web service is construction of a solid database backend.

Nowdays, programmers write Object Relational Mapping programs to remove neccesity of writing tedious and error-prone SQL statments into databases.

ORM is programming technique for converting data b/t incompatiblbe type systems through Object Oriented Programming languages.

In order to deal with complexity of managing objects, people developed new class of system called ORM.


3 most important components in writing SQLAlchemy code

* Table that represents a table in a database
* mapper that maps a python class to a table in a database
* class object that definees how database record maps to normal python object


Instead of having to write code for Table mapper and the class object at different places, SQLAlchemy's declarative allows a Table, mapper, and a class object to be defined at once in one class definition.

https://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/


## Flask


Inside index.html, AJAX call is placed for the route

Then, the route is activated, and serves the requested information to front end