# SQL-Engine
SQL Engine implemented using python

Written in Python 3
[Python 3.5.2]

## Data format

1. Tables are all csv files. <br>
If a file is *File1.csv* , the table name would be *File1* 
<br>There will be no tab separation or space separation, so you are not required to handle it but you have to make sure to take care of both csv file type cases: the one where values are in double quotes and the one where values are without quotes. 
2. The file named ```metadata.txt``` has the following structure for each table: 
<br><begin_table> 
<br><table_name> 
<br>< attributes, one each line> 
<br><end_table> 

## How to query a table using this engine

To query a table, stored in csv format [say, table1.csv] with the metadata -->
```
python sqlEngine.py “<query>”
```

## Supported queries

1. Select all records : 
<br>```Select * from table_name; ```
2. Aggregate functions: Simple aggregate functions on a single column. Sum, average, max and min. They will be very trivial given that the data is only numbers: 
<br>```Select max(col1) from table1;```
3. Project Columns(could be any number of columns) from one or more tables : <br>```Select col1, col2 from table_name;```
4. Select/project with distinct from one table: (distinct of a pair of values indicates the pair should be distinct) 
<br>```Select distinct col1, col2 from table_name;```
5. Select with where from one or more tables : 
<br>```Select col1,col2 from table1,table2 where col1 = 10 AND col2 = 20;```
* In the where queries, there would be a maximum of one AND/OR operator with no NOT operators. 
* Relational operators that are to be handled in the assignment, the operators include "< , >, <=, >=, =". 
6. Projection of one or more(including all the columns) from two tables with one join condition : 
* ```Select * from table1, table2 where table1.col1=table2.col2; ```
* ```Select col1, col2 from table1,table2 where table1.col1=table2.col2;```

The details about the implementation can be found in this [pdf](https://github.com/nonejk/Mini-SQL-Engine/blob/master/details.pdf).
