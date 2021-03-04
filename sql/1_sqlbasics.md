<link rel="stylesheet" href="/Users/scottadams/gdrive/work/promotable/dataToInsights2020b/1_sqlbasics/themes/markedstyle/github.css">

<img style="float" src="/Users/scottadams/gdrive/work/promotable/dataToInsights2020b/project/2020-08-23-20-41-40.png" width="150" height="100"/>


# SQL Basics

- [SQL Basics](#sql-basics)
  - [The Anatomy of a Select Statement](#the-anatomy-of-a-select-statement)
    - [Case Insensitivity](#case-insensitivity)
    - [Comparison Operators](#comparison-operators)
  - [Superstore Database](#superstore-database)
  - [Querying a Table](#querying-a-table)
  - [In-Class Exercise 1](#in-class-exercise-1)
  - [Looking For Nulls](#looking-for-nulls)
  - [Order By](#order-by)
  - [Offset](#offset)
  - [In-Class Exercise 2](#in-class-exercise-2)
  - [Aliases](#aliases)
    - [Aliasing Attribute Names](#aliasing-attribute-names)
  - [Homework](#homework)


## The Anatomy of a Select Statement

When we want to *query* (i.e., pull data) a table in SQL we use a `SELECT` statement. The basic grammar of a `SELECT` statement is provided below.

```{sql}
SELECT <attributes> FROM <table> <additional keywords and statements> ;
```

`<attributes>` is a placeholder for the columns we want to pull from a given table (note that the terms attribute and column are interchangable unless otherwise specified). The name of the desired table is placed in the `<table>` placeholder. If we wanted to select all columns from a table we can list out each column name in the table, separated by a comma, or we can use the asterisk character, `*`, in the `<attributes>` placeholder. For instance, if we have a table named _Example_ that has three columns, _Col1_, _Col2_, and _Col3_, we could select all the rows in all of these columns by executing the syntax below (note that in this query there is no comma between `Col3` and `FROM`, as the placing a comma after the last column name will return an error).

```{sql, connection=myconn, eval=F, echo=T}
SELECT Col1, Col2, Col3 FROM Example;
```


If we wanted to save some time, however, we could replace `Col1, Col2, Col3` with `*`.
```{sql}
SELECT * FROM Example;
```

As mentioned above, the names specified immediately after `SELECT` only specify which columns to output. In order to specify which rows to return there are of pieces of syntax that are written in the `<additional keywords and statments placeholder>` section of the basic `SELECT` grammar statment. For example, if we wanted to select all the columns from the hypothetical table _Example_ but only the first 10 rows we could use the `LIMIT` keyword.

```{sql, connection=myconn, eval=F, echo=T}
SELECT * FROM Example;
LIMIT 10;
```

Now, let's say that each record in _Col1_ can have a value of either "A", "B", or "C". If we wanted to select all columns from _Example_ but only return those records that have a value of "A" on _Col1_ we need to use a `WHERE` statement.

```{sql}
SELECT * FROM Example;
WHERE Col1 = "A";
```

Note that when specifying an actual value from a text attribute that value has to be in quotations, which is why _A_ in `WHERE Col1 = "A"` is surrounded by quotation marks. However, you can use either double or single quotes around the text value. Thus, the syntax below would give the same results as the previous syntax.

```{sql}
SELECT * FROM Example;
WHERE Col1 = 'A';
```

### Case Insensitivity

The syntax used for SQL is case-insensitive. This means that keywords and column names can be written in either upper- or lower-case. For instance, any of the following three queries will return all columns and rows from _Example_.

```{sql}
SELECT * FROM example;
WHERE Col1 = 'A';
```

```{sql}
SELECT * FROM example;
WHERE col1 = 'A';
```

```{sql}
SELECT * FROM example;
WHERE COL1 = 'A';
```

The only exception to case-insensitivity is that actual text values specified in a query must match the corresponding value in the data. Accordingly, you will notice that in all three of the previous queries above the letter 'A' in the last line of syntax is always capitalized. If we used a lower case 'a' in the `WHERE` statement the query would still run, but would not return any data because there are no records in _Col1_ of example with a value of 'a'. The only available values for _Col1_ are 'A', 'B', or 'C'.

### Comparison Operators

We have seen the "equal to" operator in action in the `WHERE` clauses in the examples above and in the table below is a list of other comparison operators that you we can use in SQL. While many of these are rather common, such as "greater than" and "less than", the "not equal to" operators are often new to many people (note that there are two ways to specify "not equal to"). 

| Operator | Meaning                  |
|----------|--------------------------|
| =        | Equal To                 |
| >        | Greater Than             |
| <        | Less Than                |
| >=       | Greater Than or Equal To |
| <=       | Less Than or Equal To    |
| <>       | Not Equal To             |
| !=       | Not Equal To             |

## Superstore Database

The exercises we will cover use four tables (*sales*, *products*, *orders*, and *customers*) of sales-related data from an office supply superstore. These tables are available to the public on [Mode](https://mode.com/) in the *scott_adams* space. Basic **schemas**--information about tables--are shown below.

![](2020-08-02-11-11-52.png)

![](2020-08-02-11-13-45.png)

![](2020-08-02-11-13-22.png)

![](2020-08-02-11-12-29.png)

## Querying a Table

When querying any of the four superstore tables, use the following convention to identify the table of interest:

scott_adams.table

replacing "table" with the name of the actual table you want to query.

Use the query below to select the names of the first 10 customers in the _Customers_ table. For example, to return the first 10 records from the *customername* attribute from the *customers* table, use the syntax below.

```{sql}
SELECT customername FROM scott_adams.customers LIMIT 10;
```
Here is the result from the query.

| customername       |
|--------------------|
| Claire Gute        |
| Darrin Van Huff    |
| Sean O'Donnell     |
| Brosina Hoffman    |
| Andrew Allen       |
| Irene Maddox       |
| Harold Pawlan      |
| Pete Kriz          |
| Alejandro Grove    |
| Zuschuss Donatelli |


Next, select the first 10 rows of customer names, cities, and states from _Customers_.

```{sql}
SELECT customername, city, state FROM scott_adams.customers LIMIT 10;
```

| customername       | city            | state          |
|--------------------|-----------------|----------------|
| Claire Gute        | Henderson       | Kentucky       |
| Darrin Van Huff    | Los Angeles     | California     |
| Sean O'Donnell     | Fort Lauderdale | Florida        |
| Brosina Hoffman    | Los Angeles     | California     |
| Andrew Allen       | Concord         | North Carolina |
| Irene Maddox       | Seattle         | Washington     |
| Harold Pawlan      | Fort Worth      | Texas          |
| Pete Kriz          | Madison         | Wisconsin      |
| Alejandro Grove    | West Jordan     | Utah           |
| Zuschuss Donatelli | San Francisco   | California     |


Now, select the first 10 rows from all attributes in *customers*.
```{sql, connection=myconn, eval=T, echo=T}
SELECT * FROM scott_adams.customers LIMIT 10;
```

| customerid | customername       | segment     | country       | city            | state          | postalcode | region  |
|------------|--------------------|-------------|---------------|-----------------|----------------|------------|---------|
| CG-12520   | Claire Gute        | Consumer    | United States | Henderson       | Kentucky       | 42420      | South   |
| DV-13045   | Darrin Van Huff    | Corporate   | United States | Los Angeles     | California     | 90036      | West    |
| SO-20335   | Sean O'Donnell     | Consumer    | United States | Fort Lauderdale | Florida        | 33311      | South   |
| BH-11710   | Brosina Hoffman    | Consumer    | United States | Los Angeles     | California     | 90032      | West    |
| AA-10480   | Andrew Allen       | Consumer    | United States | Concord         | North Carolina | 28027      | South   |
| IM-15070   | Irene Maddox       | Consumer    | United States | Seattle         | Washington     | 98103      | West    |
| HP-14815   | Harold Pawlan      | Home Office | United States | Fort Worth      | Texas          | 76106      | Central |
| PK-19075   | Pete Kriz          | Consumer    | United States | Madison         | Wisconsin      | 53711      | Central |
| AG-10270   | Alejandro Grove    | Consumer    | United States | West Jordan     | Utah           | 84084      | West    |
| ZD-21925   | Zuschuss Donatelli | Consumer    | United States | San Francisco   | California     | 94109      | West    |


Lastly, we will select the first 10 rows of customer names, cities, and states from _Customers_ from customers residing in Chicago, Illinois. This query is an example of why it is important to know the data types of your attributes. Here, the *city* and *state* attributes contain string (i.e., text) data and the values specified for each attribute in the `WHERE` condition must be placed within single-quotes (note that in the version of SQL we are using you cannot use double-quotes to identify individual string values).
```{sql}
SELECT
  customername,
  city,
  state
  FROM scott_adams.customers
WHERE
  city = 'Chicago' AND state = 'Illinois'
LIMIT 10;
```

| customername       | city    | state    |
|--------------------|---------|----------|
| Paul Stevenson     | Chicago | Illinois |
| Christopher Schild | Chicago | Illinois |
| Rick Bensley       | Chicago | Illinois |
| Jennifer Braxton   | Chicago | Illinois |
| Ken Lonsdale       | Chicago | Illinois |
| Dan Reichenbach    | Chicago | Illinois |
| Roy Collins        | Chicago | Illinois |
| Philisse Overcash  | Chicago | Illinois |
| Sue Ann Reed       | Chicago | Illinois |
| Emily Phan         | Chicago | Illinois |

## In-Class Exercise 1
#1 Select the first 15 records and all attributes from the _Products_ table (remember to use the `scott_adams` prefix, i.e., `scott_adams.products`).

#2 Select the first 5 records and the _productId_ and _productName_ columns from the _Products_ table 

## Looking For Nulls

Whenever you are working with data, especially new data, it is good practice to examine missing values. In SQL, if a record has a `NULL` for a particular attribute, this means that valid data was not recorded for said cell. However, rather than using the `= NULL` or `<> NULL` in a `WHERE` clause to filter to NULL or non-NULL values, respectively, we need to use `IS NULL` to return NULL values and `IS NOT NULL` to return non-NULL values. 

The query below uses a copy of the fully joined superstore data, but with certain values set to NULL. This example will return records where the shipping data is missing.

```
SELECT * 
FROM scott_adams.superstorejoinednulls
WHERE shipDate IS NULL;
```

| salesid | shipdate |
|---------|----------|
| 6       |          |
| 6558    |          |
| 6730    |          |
| 9913    |          |
| 9914    |          |


## Order By

Sometimes when querying a table you will need to output to be ordered in a specific way. For example, say we want to see sales records from the _Sales_ table, ordered in ascending order (lowest to highest) by _profit_.

```
SELECT * FROM scott_adams.sales
ORDER BY profit
LIMIT 10;
```

| salesid | orderid        | productid       | sales    | quantity | discount | profit     |
|---------|----------------|-----------------|----------|----------|----------|------------|
| 7773    | CA-2017-108196 | TEC-MA-10000418 | 4499.985 | 5        | 0.7      | -6599.978  |
| 684     | US-2018-168116 | TEC-MA-10004125 | 7999.98  | 4        | 0.5      | -3839.9904 |
| 9775    | CA-2015-169019 | OFF-BI-10004995 | 2177.584 | 8        | 0.8      | -3701.8928 |
| 3012    | CA-2018-134845 | TEC-MA-10000822 | 2549.985 | 5        | 0.7      | -3399.98   |
| 4992    | US-2018-122714 | OFF-BI-10001120 | 1889.99  | 5        | 0.8      | -2929.4845 |
| 3152    | CA-2016-147830 | TEC-MA-10000418 | 1799.994 | 2        | 0.7      | -2639.9912 |
| 5311    | CA-2018-131254 | OFF-BI-10003527 | 1525.188 | 6        | 0.8      | -2287.782  |
| 9640    | CA-2016-116638 | FUR-TA-10000198 | 4297.644 | 13       | 0.4      | -1862.3124 |
| 1200    | CA-2017-130946 | OFF-BI-10004995 | 1088.792 | 4        | 0.8      | -1850.9464 |
| 2698    | CA-2015-145317 | TEC-MA-10002412 | 22638.48 | 6        | 0.5      | -1811.0784 |

Likewise, if we wanted to see these same records ordered by _profit_ in descending order (highest to lowest), we would include the `DESC` keyword at the end of the `ORDER BY` statement.

```
SELECT * FROM scott_adams.sales
ORDER BY profit DESC
LIMIT 10;
```

| salesid | orderid        | productid       | sales     | quantity | discount | profit    |
|---------|----------------|-----------------|-----------|----------|----------|-----------|
| 6827    | CA-2017-118689 | TEC-CO-10004722 | 17499.95  | 5        | 0        | 8399.976  |
| 8154    | CA-2018-140151 | TEC-CO-10004722 | 13999.96  | 4        | 0        | 6719.9808 |
| 4191    | CA-2018-166709 | TEC-CO-10004722 | 10499.97  | 3        | 0        | 5039.9856 |
| 9040    | CA-2017-117121 | OFF-BI-10000545 | 9892.74   | 13       | 0        | 4946.37   |
| 4099    | CA-2015-116904 | OFF-BI-10001120 | 9449.95   | 5        | 0        | 4630.4755 |
| 2624    | CA-2018-127180 | TEC-CO-10004722 | 11199.968 | 4        | 0.2      | 3919.9888 |
| 510     | CA-2016-145352 | OFF-BI-10003527 | 6354.95   | 5        | 0        | 3177.475  |
| 8489    | CA-2017-158841 | TEC-MA-10001127 | 8749.95   | 5        | 0        | 2799.984  |
| 7667    | US-2017-140158 | TEC-CO-10001449 | 5399.91   | 9        | 0        | 2591.9568 |
| 6521    | CA-2018-138289 | OFF-BI-10004995 | 5443.96   | 4        | 0        | 2504.2216 |

`ORDER BY` also works with text. When an attribute with text values is ordered in ascending order (the default), output will be ordered in alphabetical order by the attribute of interest. Conversely, using the `DESC` option with a text attribute will order in reverse alphabetical order. Consider the query below, for instance.

```
SELECT * FROM scott_adams.products
ORDER BY productName DESC
LIMIT 10;
```

| productid       | category        | subcategory | productname                                          |
|-----------------|-----------------|-------------|------------------------------------------------------|
| OFF-BI-10000145 | Office Supplies | Binders     | Zipper Ring Binder Pockets                           |
| TEC-MA-10000045 | Technology      | Machines    | Zebra ZM400 Thermal Label Printer                    |
| OFF-AR-10003560 | Office Supplies | Art         | Zebra Zazzle Fluorescent Highlighters                |
| TEC-MA-10004002 | Technology      | Machines    | Zebra GX420t Direct Thermal/Thermal Transfer Printer |
| TEC-MA-10001695 | Technology      | Machines    | Zebra GK420t Direct Thermal/Thermal Transfer Printer |
| OFF-BI-10004236 | Office Supplies | Binders     | XtraLife ClearVue Slant-D Ring Binder, White, 3"     |
| OFF-BI-10000285 | Office Supplies | Binders     | XtraLife ClearVue Slant-D Ring Binders by Cardinal   |
| OFF-ST-10002214 | Office Supplies | Storage     | X-Rack File for Hanging Folders                      |
| TEC-PH-10002114 | Technology      | Phones      | Xiaomi Mi3                                           |
| TEC-MA-10003353 | Technology      | Machines    | Xerox WorkCentre 6505DN Laser Multifunction Printer  |


## Offset

A offset will return the $k^th + 1$ record. For example, the _Sales_ table is  ordered by the _salesId_ attribute in ascending order. The _salesId_ values are just integers from 1 to 9,994 (the total number of records in the _Sales_ table). The following query will return the first 10 records from _Sales_, which are the records for _salesId_ 1-10.

```
SELECT COUNT(*) FROM scott_adams.sales
``` 

| salesid | orderid        | productid       | sales    | quantity | discount | profit   |
|---------|----------------|-----------------|----------|----------|----------|----------|
| 1       | CA-2017-152156 | FUR-BO-10001798 | 261.96   | 2        | 0        | 41.9136  |
| 2       | CA-2017-152156 | FUR-CH-10000454 | 731.94   | 3        | 0        | 219.582  |
| 3       | CA-2017-138688 | OFF-LA-10000240 | 14.62    | 2        | 0        | 6.8714   |
| 4       | US-2016-108966 | FUR-TA-10000577 | 957.5775 | 5        | 0.45     | -383.031 |
| 5       | US-2016-108966 | OFF-ST-10000760 | 22.368   | 2        | 0.2      | 2.5164   |
| 6       | CA-2015-115812 | FUR-FU-10001487 | 48.86    | 7        | 0        | 14.1694  |
| 7       | CA-2015-115812 | OFF-AR-10002833 | 7.28     | 4        | 0        | 1.9656   |
| 8       | CA-2015-115812 | TEC-PH-10002275 | 907.152  | 6        | 0.2      | 90.7152  |
| 9       | CA-2015-115812 | OFF-BI-10003910 | 18.504   | 3        | 0.2      | 5.7825   |
| 10      | CA-2015-115812 | OFF-AP-10002892 | 114.9    | 5        | 0        | 34.47    |

Now let's add `OFFSET(2)` to the previous query, which will exclude the first 2 records and treat the third record as the starting record, meaning that our first observation output will be the record for _salesId_ 3. 

```
SELECT * FROM scott_adams.sales
OFFSET(2)
LIMIT 10;
```

| salesid | orderid        | productid       | sales    | quantity | discount | profit   |
|---------|----------------|-----------------|----------|----------|----------|----------|
| 3       | CA-2017-138688 | OFF-LA-10000240 | 14.62    | 2        | 0        | 6.8714   |
| 4       | US-2016-108966 | FUR-TA-10000577 | 957.5775 | 5        | 0.45     | -383.031 |
| 5       | US-2016-108966 | OFF-ST-10000760 | 22.368   | 2        | 0.2      | 2.5164   |
| 6       | CA-2015-115812 | FUR-FU-10001487 | 48.86    | 7        | 0        | 14.1694  |
| 7       | CA-2015-115812 | OFF-AR-10002833 | 7.28     | 4        | 0        | 1.9656   |
| 8       | CA-2015-115812 | TEC-PH-10002275 | 907.152  | 6        | 0.2      | 90.7152  |
| 9       | CA-2015-115812 | OFF-BI-10003910 | 18.504   | 3        | 0.2      | 5.7825   |
| 10      | CA-2015-115812 | OFF-AP-10002892 | 114.9    | 5        | 0        | 34.47    |
| 11      | CA-2015-115812 | FUR-TA-10001539 | 1706.184 | 9        | 0.2      | 85.3092  |
| 12      | CA-2015-115812 | TEC-PH-10002033 | 911.424  | 4        | 0.2      | 68.3568  |

With an offset, the number in parentheses will be the number of records skipped. In our example, `OFFEST(2)` skipped the first two rows and treated the third row as the first record in the output. Had we wrote `OFFSET(5)` the first five records would have been excluded and the sixth record would be the first record in the output.

Note that `OFFSET` does not change anything in the underlying table. To actually make changes to tables in a database you would need **write permissions**. In the examples in this course, we only have **read permissions**, so we do not need to worry about accidentally deleting records and tables. 

`OFFSET` and `ORDER BY` are very useful for finding the $k^th$ record according to some order. For instance, we previously ordered the _Sales_ table in descending order by _profit_ so that the output of transactions would be ordered from highest to lowest profits. With `OFFSET` we could easily find the transaction with the third highest profit. 

```
SELECT * FROM scott_adams.sales
ORDER BY profit DESC
OFFSET(2)
LIMIT 10;
```

| salesid | orderid        | productid       | sales     | quantity | discount | profit    |
|---------|----------------|-----------------|-----------|----------|----------|-----------|
| 4191    | CA-2018-166709 | TEC-CO-10004722 | 10499.97  | 3        | 0        | 5039.9856 |
| 9040    | CA-2017-117121 | OFF-BI-10000545 | 9892.74   | 13       | 0        | 4946.37   |
| 4099    | CA-2015-116904 | OFF-BI-10001120 | 9449.95   | 5        | 0        | 4630.4755 |
| 2624    | CA-2018-127180 | TEC-CO-10004722 | 11199.968 | 4        | 0.2      | 3919.9888 |
| 510     | CA-2016-145352 | OFF-BI-10003527 | 6354.95   | 5        | 0        | 3177.475  |
| 8489    | CA-2017-158841 | TEC-MA-10001127 | 8749.95   | 5        | 0        | 2799.984  |
| 7667    | US-2017-140158 | TEC-CO-10001449 | 5399.91   | 9        | 0        | 2591.9568 |
| 6521    | CA-2018-138289 | OFF-BI-10004995 | 5443.96   | 4        | 0        | 2504.2216 |
| 1086    | US-2017-143819 | TEC-MA-10003979 | 4899.93   | 7        | 0        | 2400.9657 |
| 4278    | US-2017-107440 | TEC-MA-10001047 | 9099.93   | 7        | 0        | 2365.9818 |

With `OFFSET(2)`, the first row in the output is the sale that generated the third highest profit. If we change `LIMIT 10` to `LIMIT 1`, we can isolate this record. 

| salesid | orderid        | productid       | sales    | quantity | discount | profit    |
|---------|----------------|-----------------|----------|----------|----------|-----------|
| 4191    | CA-2018-166709 | TEC-CO-10004722 | 10499.97 | 3        | 0        | 5039.9856 |

```
| salesid | orderid        | productid       | sales    | quantity | discount | profit    |
|---------|----------------|-----------------|----------|----------|----------|-----------|
| 4191    | CA-2018-166709 | TEC-CO-10004722 | 10499.97 | 3        | 0        | 5039.9856 |
```

## In-Class Exercise 2
What is the _salesId_ for the record with the fifth largest _sales_ value?

## Aliases

An alias is like a nickname that can refer to a table or attribute. Take the following query, for example, which returns the first five customer names from the _Customers_ table.

```{sql}
SELECT salesId
FROM scott_adams.sales
LIMIT 5;
```

| salesid |
|---------|
| 1       |
| 2       |
| 3       |
| 4       |
| 5       |

If we wanted to be more specific about what table the _salesId_ attribute comes from in the `SELECT` line, we could prefix the attribute name with the table name. 

```{sql}
SELECT sales.salesId
FROM scott_adams.sales
LIMIT 5;
```

Now, you might be asking "why would I want to prefix the attribute name with the table name?". Well, consider that we can output records from attributes in different tables in a single SQL query. As we will see in the next lesson, in some queries attributes from multiple tables will be selected. To demonstrate the general idea that attributes from different tables can be selected, consider an example where we want to select the first five _salesId_ and _orderId_ records from the _sales_ and _orders_ tables, respectively. Let's try this query below.

```{sql}
SELECT salesId, orderId
FROM scott_adams.sales, scott_adams.orders 
LIMIT 5;
```

What happened? You should have received the following error message.

![](2020-08-09-17-10-38.png)

The _orderId_ attribute is in both the _sales_ and _orders_ table, so when this query is executed, the software does not know whether to pull _orderId_ from _sales_ or _orders_. We need to be more explicit in our instructions. 

```{sql}
SELECT sales.salesId, orders.orderId
FROM 
  scott_adams.sales, 
  scott_adams.orders 
LIMIT 5;
```

This query above is successful, but do not spend too much time interpreting the output. Keep in mind this query is just an illustration, not an actual query we would want to run in real life.

| salesid | orderid        |
|---------|----------------|
| 1       | CA-2017-152156 |
| 1       | CA-2017-152156 |
| 1       | CA-2017-138688 |
| 1       | US-2016-108966 |
| 1       | US-2016-108966 |

Now, with just two attributes and two tables, writing out each table name as a prefix is not too cumbersome, but with several or more attributes across two or more tables, such a query could become very wordy very fast. So, instead of prefixing the full table names, we can alias the _sales_ and _orders_ tables as _s_ and _o_, respectively (or you can alias the tables with anything you want, as long as it makes sense to you, and anyone else who will be using your code). There are two ways to alias. First, you can use the  `as` keyword following the item you want to alias and the alias name after `as`.

```
SELECT s.salesId, o.orderId
FROM 
  scott_adams.sales as s, 
  scott_adams.orders as o
LIMIT 5;
```

Second, you can just write the alias name following the item you want to alias.

```
SELECT s.salesId, o.orderId
FROM 
  scott_adams.sales s, 
  scott_adams.orders o
LIMIT 5;
```
Using `as` or not is a matter of personal preference. Some people may prefer using `as` because it may draw attention to the alias definition. Others may prefer to avoid `as` to avoid typing more than necessary. Whichever way you choose, just be consistent. 

### Aliasing Attribute Names

In addition to table names, we can also alias attribute names. Take an example where we need to provide a list of customer names and associated addresses. Rather than outputting the attribute names as the column headers, we could make the column headers look a bit nicer with aliases.

```
SELECT 
  customerName "Customer Name", 
  city "City",
  state "State", 
  postalcode "Postal Code"
FROM scott_adams.customers
LIMIT 10;
```

| Customer Name      | City            | State          | Postal Code |
|--------------------|-----------------|----------------|-------------|
| Claire Gute        | Henderson       | Kentucky       | 42420       |
| Darrin Van Huff    | Los Angeles     | California     | 90036       |
| Sean O'Donnell     | Fort Lauderdale | Florida        | 33311       |
| Brosina Hoffman    | Los Angeles     | California     | 90032       |
| Andrew Allen       | Concord         | North Carolina | 28027       |
| Irene Maddox       | Seattle         | Washington     | 98103       |
| Harold Pawlan      | Fort Worth      | Texas          | 76106       |
| Pete Kriz          | Madison         | Wisconsin      | 53711       |
| Alejandro Grove    | West Jordan     | Utah           | 84084       |
| Zuschuss Donatelli | San Francisco   | California     | 94109       |

## Homework

**#1** Select the first 10 records from `tutorial.city_populations`.

**#2** Using the `tutorial.city_populations` table, find the five cities with the largest estimated populations from 2012.

**#3** What are the cities from California with 2012 estimated population sizes exceeding 1 million people? 
