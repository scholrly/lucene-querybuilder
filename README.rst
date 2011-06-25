Lucene Query Builder
====================

:synopsis: Allows creation of Lucene queries without needing to know the language well in Python.

The objective is to be able to quickly create multiple lucene query strings easily without having to learn the language itself. The syntax is simple to use and allows creating larger queries from multiple smaller ones. A basic lesson on proper Lucene queries can be found here_.


Getting Started
---------------

To use the Lucene Query Builder, you need only import it:

  >>> from lucenequerybuilder import Q


Creating Queries
----------------

A basic query can be given by passing in a string into Q's constructor.

  >>> q = Q('a')
  
  >>> q = Q('The quick brown fox')

The query builder will automatically detect whether a term (no whitespace) or a phrase (multiple terms together seaparated by whitespace) and properly bound them with quotation marks.

Ranges are also easy to put into a query. There are two types of range queries, inclusive range and exclusive range. These are passed into the query builder with keyword arguments.

  >>> q = Q(inrange=(1,5))
  
  >>> q = Q(exrange=['egg','hgg'])

Ranges will work with any list-like object.


Chaining Queries
----------------

You can chain queries with `&` (AND), `|` (OR), `& ~` (AND NOT), `+` (MUST), and `-` (MUST NOT). AND, OR, and AND NOT require a query before and after it shows up. MUST and MUST NOT only work on the query directly afterwards. Some examples are below::

  >>> q = Q('a') & Q('b')
  
  >>> q = Q('a') & ~Q('b')
  
  >>> q = +Q('a') -Q('b')


Nested Queries
--------------

Queries can be nested inside of each other to create new queries. This makes it easy to group queries together. Examples below::

  >>> q = Q(Q('a') & Q('b')) & ~Q('c')
  
  >>> q = Q(Q(Q('a') | Q(inrange=[1,2])) +Q('c))


Fields
------

Fields can be added to queries by putting in a field as your first argument. Fields cannot have any whitespace and cannot be nested inside each other. The following examples are valid queries::

  >>> q = Q('name', 'Edward')
  
  >>> q = Q('text', 'Mary had a little lamb')
  
  >>> q = Q('age', inrange=[10, 9001])

The following examples are invalid queries which will raise an error::

  >>> q = Q('name', Q('lastname', 'Purcell'))
  
  >>> q = Q('bad', Q('range', inrange=[10, 9001]))

.. _here: http://lucene.apache.org/java/3_2_0/queryparsersyntax.html
