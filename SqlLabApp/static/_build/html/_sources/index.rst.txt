.. SqlLabDocs documentation master file, created by
   sphinx-quickstart on Tue Apr  4 12:25:40 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SqlLab's documentation!
======================================

SQL Lab is an automated system where instructors can create tests that students can take online. The system issues questions and validates answer given by students by checking comparing them with those given by the instructors. The system also measures and reports the comparative performance of the answers given by students.

.. toctree::
   :maxdepth: 2
  
System Documentation
=====================

* :ref:`User Roles`
* :ref:`ER Model`
* :ref:`Dynamic Tables`
* :ref:`SQL Parser`
* :ref:`search`


.. _User Roles:

User Roles
===========
Instructor
----------
Instructor is given privileges to set test questions, specify the duration and maximum number of attempts allowed as well as track the students' performance. 

Instructor Privileges
++++++++++++++++++++++

* Create a Module
* Create a Test
* Edit a Test
* Review a Test
* Delete a Test
* Take a Test

Instructor Home
++++++++++++++++

Upon login, the instructor will be presented with the following:

* Option to create a new module
* List of all the modules the instructor has created
 

Student
-------

The student will be able to take tests that are assigned to him/her within a specified time period as well as track his/her own scores.

Student Privileges
++++++++++++++++++++++

* Take a Test
* Track Test Scores


Student Home
+++++++++++++

Upon login, the student will be presented with the following:

* Take Test if available
* Review past Tests if available

.. _ER Model:

ER Model
=========

Entity Relationship Diagram
----------------------------
.. figure::  images/ermodel.jpg
   :align:   center

   **ER diagram of the SQL Lab System**

**Note:** Attributes that are marked with '*' have a table that is created in their names dynamically.


SQL Lab Database Tables
------------------------
The backend of the SQL Lab system stores data pertaining to the questions, answers and studnets' performance in a series of database tables. The database schema is presented in the :ref:`ER Model`. This section details on each of the database schema and its purpose.


1. User
++++++++
The **User** relation stores the follwoign attributes pertaining to the user:

* *email* 
* *password*
* *full name* 

These attributes are colelcted from each user upon registration into the SQL Lab system. Each user is uniquely indentified by his/her *email*.

2. Role
++++++++
Each user is defined a *role*. A user can either be a *student* or an *instructor*. It is also possible for a user to hold multiple roles. The **Role** is designed to be a weak entity and is uniquly identified by both the *role* and *email* of the user.

3. Class
+++++++++
The **Class** relation holds data pertaining to the class conducted. Each class has the following attributes:

* *class ID*
* *class name* 
* *semster* class is conducted
* *facilitators* 

Each *class* is uniquely identified by a *class id*. Each class is conducted by the *instructor(s)* and is attended by the *student(s)*. The class is a weak entity of the relationship between the **User** model and the **Role** model. 

**Note:** It is not possible for a user to be both a student as well as a instructor for the same class.

4. Question Data
+++++++++++++++++
This relation stores the names of the relations in which the questions reside for each test. It also stores the a boolean value for the visibility attribute, which denotes if a student will be able to see a particular instance. This relation is designed to be a weak entity of **Test** and is uniquly identified by both the *database table name*, *test ID*, and *class ID*.


5. Teacher Conducts Class
++++++++++++++++++++++++++
This table denotes the relation between the *instructor* and the *class* (s)he conducts. It has the following attributes:

* *class ID*
* *instructor email*

Both the attributes uniquely determine each record in this relation.

6. Student Attends Class
+++++++++++++++++++++++++
This table denotes the relation between the *student* and the *class* (s)he attends. It has the following attributes:

* *class ID*
* *student email* 

Both the attributes uniquely determine each record in this relation.

7. Class Holds Test
++++++++++++++++++++
Instructors set tests to be taken online. A test consists of a database and a sequence of questions, a visible database schema and a visible database instance. Each **Test** relation consists of the following attributes:

* *test ID*
* *class ID*
* *test name*
* *start time*
* *end time*
* *maximum number of attempts*

Each *test* is uniquely identified by its *test ID*. The *test name* attribute stores the name of the test i.e. Midterms. There will be corresponding table called '*Midterms*' that will be generated dynamically once the *instructor* creates the test and adds the questions and answers to the system.

**Note:** The *test* relation is merged with the *Holds* relationship due to the mandatory 1-1 partcipation constraint.

8. Student Attempts Test
+++++++++++++++++++++++++
This table denotes the relationship between the *student* and the *test* taken. It keeps track of each student's number of attempts and marks obtained. It has the following attributes:

* *test ID*
* *student email*
* *attempt number*
* *total marks*

Both the *test ID* and *student email* uniquely determine each record in this table.

.. _Dynamic Tables:

Dynamic Tables
==============
There are some tables that are created in real time when the instructors upload questions and answers to the SQL Lab system. These dynamic tables will be addressed in this section.

1. Data Table
--------------
The instructor is allowed to upload multiple database schemas, out of which some are made visible to the students while others are kept as hidden instnces. The SQL Lab parser will create a separate table for each instance of the same schema.

For instance, if the instructor uploads a '*Employee*' schema and splits it into 2 instances, the SQL parser will create 2 tables with the names '*Employee1*' and '*Employee2*'. These will be created once the schemas are uploaded into the system and will be persistently stored to the backend.


2. Test Name
-------------
Each Test Name table is created based on the name of the test stored in the *Class Holds Test* relation. It contains the questions and the corresponding answers given by the instructors. The arttributes of the relation are as follow:

* *question ID*
* *question*
* *Instructor SQL answer query*
* *marks*

Each **Test Name** table is referenced using the *test ID* i.e. *tid.testName*.


3. Student Attempts
---------------------
This table stores the question and the student's answer entered. This will ensure that the student's answers are saved across multiple attempts. This relation has the following fields:

* *question ID*
* *question*
* *Student SQL answer query*
* *marks obtained*

The *question ID* uniquely detemrines each record in this relation.
 
.. _SQL Parser:

SQL Parser
===============

SQL Parser Dependency:
-----------------------
Library : SqlParse 0.2.3 

The parser is used heavily in our application.

SQL Parser Functionalities
---------------------------

1. Creating Test Data Tables from SQL Dump
++++++++++++++++++++++++++++++++++++++++++++ 
The SQL Parser is able to parse the table name from the SQL dump file uploaded and create separate instances of the same table while reading the dump file.

2. Parsing SQL queries given in Tests
+++++++++++++++++++++++++++++++++++++++
The SQL Parser will ensure that no query will lead to loss or corruption of data. For instance, if any user gives a query to drop the table, it will ensure that the *DROP* statement is not executed. It will only ensure that valid SQL statements are being run against the visbile database instances, which will be constructed real-time using regular expressions (e.g. *warehouse1* and *warehouse2* will be parsed out of the table *warehouse*, if only *warehouse1* and *warehouse2* are made visble during the test).


Limitations and Improvements
-----------------------------

SqlParse is one of the few opensource libraries available for python postgres parsing of SQL queries. Despite its effectivness in parsing SQL queries and tokenising them, it still has its limitations as it is unable to identify and extract table names from the queries. Such limitations can only be overcome by extending the SQL Parser by the engineers.

Our team is constantly working on extending the Parser's functionalities and making it more robust so as to improve its accuracy. 
