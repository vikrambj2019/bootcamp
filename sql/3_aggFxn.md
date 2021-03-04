<link rel="stylesheet" href="./themes/markedstyle/github.css">
<img style="float" src="./2020-08-23-20-41-40.png" width="150" height="100"/>

# SQL: Case, Aggregate Functions, and Window Functions

## The Case Function

Our superstore data contains four diffrent sales regions: central, east, south and west. Each region is comprised of different states, as shown below.

| state                | region  |
|----------------------|---------|
| Illinois             | Central |
| Indiana              | Central |
| Iowa                 | Central |
| Kansas               | Central |
| Michigan             | Central |
| Minnesota            | Central |
| Missouri             | Central |
| Nebraska             | Central |
| Oklahoma             | Central |
| South Dakota         | Central |
| Texas                | Central |
| Wisconsin            | Central |
| Connecticut          | East    |
| Delaware             | East    |
| District of Columbia | East    |
| Maryland             | East    |
| Massachusetts        | East    |
| New Hampshire        | East    |
| New Jersey           | East    |
| New York             | East    |
| Ohio                 | East    |
| Pennsylvania         | East    |
| Rhode Island         | East    |
| Alabama              | South   |
| Arkansas             | South   |
| Florida              | South   |
| Georgia              | South   |
| Kentucky             | South   |
| Louisiana            | South   |
| Mississippi          | South   |
| North Carolina       | South   |
| Tennessee            | South   |
| Virginia             | South   |
| Arizona              | West    |
| California           | West    |
| Colorado             | West    |
| Nevada               | West    |
| New Mexico           | West    |
| Oregon               | West    |
| Utah                 | West    |
| Washington           | West    |

Leadership wants to create new sales region definitions, where California, Oregon, and Washington are in their own region called "West Coast", and all other states are in their original regions. 

| state                | region  | newregion  |
|----------------------|---------|------------|
| North Carolina       | South   | South      |
| Delaware             | East    | East       |
| Kentucky             | South   | South      |
| Missouri             | Central | Central    |
| Florida              | South   | South      |
| Ohio                 | East    | East       |
| South Dakota         | Central | Central    |
| California           | West    | West Coast |
| Texas                | Central | Central    |
| Nevada               | West    | West       |
| Pennsylvania         | East    | East       |
| Alabama              | South   | South      |
| Michigan             | Central | Central    |
| Oklahoma             | Central | Central    |
| Utah                 | West    | West       |
| Colorado             | West    | West       |
| Louisiana            | South   | South      |
| Rhode Island         | East    | East       |
| Arizona              | West    | West       |
| Illinois             | Central | Central    |
| New York             | East    | East       |
| Washington           | West    | West       |
| Virginia             | South   | South      |
| Iowa                 | Central | Central    |
| Georgia              | South   | South      |
| Oregon               | West    | West Coast |
| Indiana              | Central | Central    |
| New Jersey           | East    | East       |
| Connecticut          | East    | East       |
| Massachusetts        | East    | East       |
| New Hampshire        | East    | East       |
| Nebraska             | Central | Central    |
| District of Columbia | East    | East       |
| Wisconsin            | Central | Central    |
| Minnesota            | Central | Central    |
| Tennessee            | South   | South      |
| Maryland             | East    | East       |
| Mississippi          | South   | South      |
| Arkansas             | South   | South      |
| Kansas               | Central | Central    |
| New Mexico           | West    | West       |

The task of providing output that shows states assigned to their new sales regions can be accomplished with a `CASE` statement, which takes the basic structure shown below. 

```
SELECT 

CASE
  WHEN <condition 1> THEN <value 1>
  WHEN <condition 2> THEN <value 2>
  ...
  WHEN <condition n> THEN <value n>
  ELSE <value when none of the conditions above are met>
END as <name>

FROM <table>;
```

Let's apply `CASE` to the data to better understand the `CASE` statement's purpose.


```
SELECT DISTINCT 
  state,
  region,
  CASE
    WHEN state IN ('California', 'Oregon', 'Washingtion') THEN 'West Coast'
    WHEN state NOT IN ('California', 'Oregon', 'Washingtion') AND region = 'West' THEN 'West'
    ELSE region
  END as newRegion
FROM scott_adams.superstorejoined;
```

In this query we have two conditions that explicitly define the "West Coast" and "West" sales regions. `WHEN state IN ('California', 'Oregon', 'Washingtion') THEN 'West Coast'` tells the SQL engine (i.e., the software that translates a SQL query and performs the query on a table or set of tables) that if a given record has a value of "California", "Oregon", or "Washington" in the `state` attribute, that record will have a value of "West Coast" in the `newRegion` column. What about the remaining states in the original West region? We could just list out those states in the `IN` clause, or we specify two conditions that need to be satisfied. First, a given record's  `state` attribute cannot have values of "California", "Oregon", or "Washington". Second, the `region` value for a given record must be "West". 

Again, for all other regions outside of the original West region we could specify a third condition listing out the `state` values for each region as we did in the first two `WHEN` clauses in the `CASE` statement. Alternatively, we could just tell the SQL engine that if those first two conditions are not satisfied for a record, then that record will take the original `region` value.Now that all the conditional statements are specified it is time to close the `CASE` statment. Note that every `CASE` statement needs to close with `END`, which tells the SQL engine that "there are no more conditions to specify." If you do not include `END` you will get an error message. 


## Aggregate Functions

Aggregate functions are operations that output a number that represents a particular numerical summary of some set of values. Below is a list and description of SQL aggregate functions we will cover.

| Syntax       | Description |
|--------------|-------------|
| `COUNT()`    | Returns the number of rows in the table if * is in parentheses. If an individual column is listed in parentheses the number of rows with non-null values are returned.|
| `MIN()`      | Returns the minimum value for the column specified in the parentheses. |
| `MAX()`      | Returns the maximum value for the column specified in the parentheses. |
| `SUM()`      | Returns the sum of all values for the column specified in parentheses. |
| `AVG()`      | Returns the mean value for the column specified in the parentheses. |

### Count

When supplied with a `*`, `COUNT` will return the total number of records in a table. The query below outputs the total number of rows in the `superstorejoinednulls` table, which is 9,994 rows.

```
SELECT COUNT(*) FROM scott_adams.superstorejoinednulls;
```

However, when the `*` is replaced by the name of an attribute it is possible that a different number will be output.

```
SELECT COUNT(shipDate) FROM scott_adams.superstorejoinednulls;
```
The query above returns 9,989 rows, but we know there are 9,994 in this table. What is going on? Well, when `COUNT` is applied to an attribute the output will be the number of records with non-NULL values on the attribute of interest. Recall from the previous section on NULL values in this lesson that the `shipDate` attribute in the `superstorejoinednulls` table has five NULL values, hence, 9,989 non-NULL values.

### MIN and MAX

When the four tables comprising the superstore data are joined, each record represents the transaction for an individual product in a specifi order. Customers can purchase multiple quantities of a given product in their order. To illustrate, order CA-2017-152156 contains two different products, the Bush Somerset Collection Bookcase and Hon Deluxe Fabric Upholstered Stacking Chairs, Rounded Back	3. Furthermore, two Bush Somerset Collection Bookcase and three Hon Deluxe Fabric Upholstered Stacking Chairs, Rounded Back items were purchased in this order. Now, let's look at the minimum and maximum quantities of products purchased across all transactions.

```
SELECT 
  MIN(quantity), 
  MAX(quantity) 
FROM scott_adams.superstorejoinednulls;
```

| min | max |
|-----|-----|
| 1   | 14  |


### SUM

Whereas `COUNT` is useful for returning the number of items, `SUM` should be used when we are interested in adding records with varying values on an attribute together. For instance, say we wanted to obtain the total revenue recorded in `superstorejoinednulls`. Here, we would use the following query.

```
SELECT SUM(sales) FROM scott_adams.superstorejoinednulls;
```

We can see that our company has earned $2,297,200.86 in sales based on the provided data. 

### AVG

`AVG` provides the mean across a set of attribute values. Note that the mean for a set of values that take on value of 0 or 1 only is a **proportion**, which can be multiplied by 100 to show a percentage. 

Let's now use `AVG` to provide the mean profit for all transaction recorded in `superstorejoinednulls`.

```
SELECT AVG(profit) FROM scott_adams.superstorejoinednulls;
```

We can see that the mean profit generated for a purchase in a given order is $28.66.


## Aggregate Functions Across Groups

The aggregate functions we covered thus far were performed across all available records. However, there may be cases where we want to perform an aggregate function by values. Take, for instance, a request from a stakeholder to understand regional differences in profitability. With the superstore data joined together, we have can look at both `REGION` and `PROFIT` (not that in this section I am using the `superstorejoined` table, not `superstorejoinednulls`). Furthermore, we can calculate the total profit by region using `GROUP BY` as shown below.

```
SELECT 
  region,
  SUM(profit)
FROM scott_adams.superstorejoined
GROUP BY region;
```

| region  | sum               |
|---------|-------------------|
| South   | 30175.13570000007 |
| West    | 98008.22490000006 |
| East    | 94604.31210000008 |
| Central | 63609.34900000003 |

We can see that the West is the most profitable sales region overall, while the South is the least profitable. Now, what if we wanted to order this resulting table from highest profit to lowest? We use `ORDER BY`, of course.

```
SELECT 
  region,
  SUM(profit)
FROM scott_adams.superstorejoined
GROUP BY region
ORDER BY SUM(profit);
```

| region  | sum               |
|---------|-------------------|
| South   | 30175.13570000007 |
| Central | 63609.34900000003 |
| East    | 94604.31210000008 |
| West    | 98008.22490000006 |

Let's make one final alteration. Let's change the header of the second column to something more informative than "sum" using an alias. How about "total profit"?

```
SELECT 
  region,
  SUM(profit) as "total profit"
FROM scott_adams.superstorejoined
GROUP BY region
ORDER BY SUM(profit);
```

| region  | total profit      |
|---------|-------------------|
| South   | 30175.13570000007 |
| Central | 63609.34900000003 |
| East    | 94604.31210000008 |
| West    | 98008.22490000006 |

We can also group by two or more levels with SQL (notice that ordering is changed in the query below so output is order from most to least profitable). 

```
SELECT 
  state,
  region,
  SUM(profit) as "total profit"
FROM scott_adams.superstorejoined
GROUP BY region, state
ORDER BY SUM(profit) DESC;
```

| state                | region  | total profit       |
|----------------------|---------|--------------------|
| California           | West    | 59398.31250000002  |
| New York             | East    | 58177.834100000066 |
| Washington           | West    | 24405.796599999983 |
| Texas                | Central | 20528.91100000002  |
| Pennsylvania         | East    | 13604.935000000007 |
| Georgia              | South   | 12781.342599999998 |
| Arizona              | West    | 9563.200100000004  |
| Illinois             | Central | 9560.145599999993  |
| Wisconsin            | Central | 8569.869700000003  |
| Michigan             | Central | 7752.2969000000085 |
| Minnesota            | Central | 7202.522500000001  |
| Virginia             | South   | 6940.111200000005  |
| Ohio                 | East    | 5985.887000000001  |
| Massachusetts        | East    | 5905.5446          |
| Kentucky             | South   | 4513.313999999998  |
| Tennessee            | South   | 3434.276499999999  |
| Delaware             | East    | 3336.382700000002  |
| Alabama              | South   | 2845.0624          |
| Indiana              | Central | 2707.349500000002  |
| Louisiana            | South   | 2659.2401          |
| New Jersey           | East    | 2336.7531999999997 |
| Rhode Island         | East    | 2276.7013          |
| Iowa                 | Central | 2258.5883          |
| Missouri             | Central | 2212.8746999999994 |
| Utah                 | West    | 1818.1938000000005 |
| New Hampshire        | East    | 1519.1695999999997 |
| New Mexico           | West    | 1340.1399          |
| Nebraska             | Central | 1166.0176          |
| Colorado             | West    | 970.4647000000001  |
| Oklahoma             | Central | 829.0181999999999  |
| Florida              | South   | 750.7423999999971  |
| South Dakota         | Central | 682.5541999999999  |
| Mississippi          | South   | 550.6658999999999  |
| Connecticut          | East    | 533.4986999999999  |
| District of Columbia | East    | 490.95669999999996 |
| Maryland             | East    | 436.64919999999984 |
| Nevada               | West    | 278.06780000000003 |
| Oregon               | West    | 234.04950000000014 |
| Kansas               | Central | 139.20080000000002 |
| Arkansas             | South   | -62.9462           |
| North Carolina       | South   | -4236.673200000001 |

### In-Class Exercise #2

- Using `superstorejoinednulls`, write a query that replicates the table below.

| meansales         | totalsales        | meanprofit         | totalprofit       |
|-------------------|-------------------|--------------------|-------------------|
| 229.8580008304938 | 2297200.860299955 | 28.656896307784802 | 286397.0217000013 |


- Using the `products` table, recreate the output below, which shows the number of unique products by product category.

| category        | numberofproducts |
|-----------------|------------------|
| Furniture       | 375              |
| Office Supplies | 1083             |
| Technology      | 404              |


## `HAVING`: The `WHERE` of Aggregate Functions

Our superstore company has decided to start a new marketing campaign tailored to our best customers. The company wants to extend special promotions to customers who have spent at least $5,000 and it is our job to find these customers. Let's break this task down step-by-step. First, we are looking at the total sales among customers, so we will need to use `SUM(sales)` aggregated over customers. On the topic of identifying customers, let's use both `customerID` and `customerName`.

```
SELECT 
  customerId,
  customerName,
  SUM(sales) as totalSales
FROM scott_adams.superstorejoined
GROUP BY
  customerID,
  customerName 
```

Of course, this query does not restrict the list of customers to those with sales of at least $5,000. Now, a first logical choice for implementing such a condition would be to use a `WHERE` clause.

```
SELECT 
  customerId,
  customerName,
  SUM(sales) as totalSales
FROM scott_adams.superstorejoined
GROUP BY
  customerID,
  customerName
WHERE SUM(sales) >= 5000 
```

However, this will return an error because `WHERE` is intended to place conditions on individual records. In the current case with which we are faced, we are trying to apply a condition to aggregated records. This distinction may appear to be nuanced, and maybe even arbitrary, but it is worth paying attention to the fundamental unit of analysis in a query, that is, the smallest unit of measurement with which we are interested. If we were not concerned with aggregating, our unit of analysis would be individual purchases within specific orders, but now that we are interested in total sales by customers, our unit of analysis is the customer. To successfully perform a conditional statement on an aggregate function, we must use `HAVING` instead of `WHERE`. 

```
SELECT 
  customerId,
  customerName,
  SUM(sales) as totalSales
FROM scott_adams.superstorejoined
GROUP BY
  customerID,
  customerName 
HAVING SUM(sales) >= 1000
```

Below, the first 10 rows from the previous query are shown.

| customerid | customername         | totalsales        |
|------------|----------------------|-------------------|
| MH-18115   | Mick Hernandez       | 5503.092999999999 |
| HM-14860   | Harry Marie          | 8236.7648         |
| BM-11650   | Brian Moss           | 7294.185          |
| JW-15220   | Jane Waco            | 7721.714          |
| TB-21400   | Tom Boeckenhauer     | 9133.99           |
| IL-15100   | Ivan Liston          | 5040.736          |
| DR-12880   | Dan Reichenbach      | 6528.033999999999 |
| CM-12385   | Christopher Martinez | 8954.02           |
| KM-16375   | Katherine Murray     | 5620.186          |
| TP-21415   | Tom Prescott         | 5329.0048         |


## Using Aggregated Results as Conditions

In the previous section we focused on using the values of an aggregate function as a condition, but what if we want to identify individual records with attribute values equal to the value of an aggregate function? For example, what if we wanted to find the record with that produced the highest revenue recorded? Let's again break this task down into steps. 

First, let's write the query for the desired aggregate function. 

```
SELECT MAX(sales) FROM scott_adams.superstorejoined
```

This query returns a result of $22,638.48. In other words, the largest revenue recorded for a single product is $22,638.48. Now, we need to obtain the details for this transaction, including values for `salesId`, `customerId`, `customerName`, `orderId`, `productId`, `productName`, and `orderDate`. To accomplish this step, we will need to treat the previous query as a subquery.

```
SELECT 
  salesId,
  sales,
  customerId,
  customerName,
  orderId,
  productId,
  productName,
  orderDate
FROM scott_adams.superstorejoined
WHERE sales = (SELECT MAX(sales) FROM scott_adams.superstorejoined)
```

We see that `salesId` 2698, a purchase for six Cisco TelePresence System EX90 Videoconferencing Units made by Sean Miller on 2018-02-03, holds the record for the highest revenue-producing sale. 

| salesid | sales    | customerid | customername | orderid        | productid       | productname                                           | quantity | orderdate           |
|---------|----------|------------|--------------|----------------|-----------------|-------------------------------------------------------|----------|---------------------|
| 2698    | 22638.48 | SM-20320   | Sean Miller  | CA-2015-145317 | TEC-MA-10002412 | Cisco TelePresence System EX90 Videoconferencing Unit | 6        | 2018-02-03 00:00:00 |

## Window Functions

Throughout this lesson we have focused heavily on the unit of analysis. In a given dataset, the data may be structured in a hierarchical fashion, with records nested in multiple groups. Thus, it is important to understand the funadmental object to which your data refers. 

Nonetheless, it may also be useful to aggregate at multiple levels simultaneously. For instance, in a single report we may be asked to show sales figures at three different levels:
- by states,
- by regions,
- for the entire company

Simultaneously aggregating to multiple levels can be accomplished with **window functions**, which we will discuss in more detail below. 

### Introduction to Window Functions

The syntax of a window function takes the following basic structure.

```
SELECT <aggregate function>(<attribute>) OVER(PARTITION BY <attribute>, <additional arguments>)
```

To illustrate, let's look at an aggregate function applied to a single level of an attribute, the total sales by region.

```
SELECT 
  region,
  SUM(sales)
FROM scott_adams.superstorejoined
GROUP BY region;
```

| region  | sum                |
|---------|--------------------|
| South   | 402031.98330000014 |
| West    | 764634.4452999996  |
| East    | 611734.2995000008  |
| Central | 518800.13220000075 |

We can produce the same results (with the rows in different order, however) with the following query.

```
SELECT 
  DISTINCT region, 
  SUM(sales) OVER(PARTITION BY region)
FROM scott_adams.superstorejoined;
```

| region  | sum                |
|---------|--------------------|
| East    | 611734.2995000008  |
| Central | 518800.13220000133 |
| South   | 402031.98330000014 |
| West    | 764634.4452999993  |

Let's break down the query that produced the output above, starting with `SUM(sales) OVER(GROUP BY region)`. This piece of syntax begins by taking the sum of the `sales` column with `SUM(sales)`. Next, `OVER` is an instruction to calculate the specified aggregate function within values a specific attribute, or set of attributes. `PARTITION BY region` essentially serves the same purpose as `GROUP BY region`, identifying the attribute by which the aggregation is to be performed. 

Alright, so why `DISTINCT region`? Well, we want to be able to identify the regions associated with the summed sales values, so we need to supply `region` as a column. Why `DISTINCT`? Let's look at the first few rows of the same query ran without `DISTINCT`

```
SELECT 
  region, 
  SUM(sales) OVER(PARTITION BY region)
FROM scott_adams.superstorejoined;
```

| region  | sum                |
|---------|--------------------|
| Central | 518800.13220000133 |
| Central | 518800.13220000133 |
| Central | 518800.13220000133 |
| Central | 518800.13220000133 |
| Central | 518800.13220000133 |
| Central | 518800.13220000133 |
| Central | 518800.13220000133 |
| Central | 518800.13220000133 |
| Central | 518800.13220000133 |
| Central | 518800.13220000133 |

Without `DISTINCT` the query will return the `region` value and the sum of the `sales` attribute for every record in the `superstorejoined` table (9,994 records).


### Multiple Levels of Aggregation

Let's now consider more advanced uses of window functions. Recall that we have been asked to analyze our sales at three different levels:

- by states,
- by regions,
- for the entire company.

To be more realistic, let's also say we are only required to provide such sales figures for the most recent year on record (2018). We already saw how to use a window function to aggregate by region and the syntax, `SUM(sales) OVER(PARTITION BY region)` can be extended to aggregate by `state`. What may be less obvious is how to aggregate over the entire data table. The solution is to exclude any syntax in the parentheses associated with `OVER`.

```
SELECT 
  DISTINCT region, 
  SUM(sales) OVER()
FROM scott_adams.superstorejoined;
```

| region  | sum               |
|---------|-------------------|
| Central | 2297200.860299955 |
| South   | 2297200.860299955 |
| West    | 2297200.860299955 |
| East    | 2297200.860299955 |

$2,297,200 is the total sales amount, which can also be obtained with the query `SELECT SUM(sales) FROM scott_adams.superstorejoined;`. Now, let's put the sum of sales by region and overall together. 

```
SELECT 
  DISTINCT region, 
  SUM(sales) OVER(PARTITION BY region) as salesRegion,
  SUM(sales) OVER() as salesTotal
FROM scott_adams.superstorejoined;
```

| region  | salesregion        | salestotal        |
|---------|--------------------|-------------------|
| South   | 402031.98330000014 | 2297200.860299957 |
| East    | 611734.2995000008  | 2297200.860299957 |
| Central | 518800.13220000133 | 2297200.860299957 |
| West    | 764634.4452999993  | 2297200.860299957 |

Now we have aggregation at two different levels in the same output. There is just one last aggregation to perform, the state-level.

```
SELECT 
  DISTINCT state, region,
  SUM(sales) OVER(PARTITION BY state) as salesState,
  SUM(sales) OVER(PARTITION BY region) as salesRegion,
  SUM(sales) OVER() as salesTotal
FROM scott_adams.superstorejoined
ORDER BY state, region;
```

| state                | region  | salesstate         | salesregion        | salestotal        |
|----------------------|---------|--------------------|--------------------|-------------------|
| Alabama              | South   | 31038.99180000001  | 402031.9833000008  | 2297200.860299964 |
| Arizona              | West    | 81986.12299999998  | 764634.4453000004  | 2297200.860299964 |
| Arkansas             | South   | 4582.556000000001  | 402031.9833000008  | 2297200.860299964 |
| California           | West    | 451036.5823000012  | 764634.4453000004  | 2297200.860299964 |
| Colorado             | West    | 57523.116200000026 | 764634.4453000004  | 2297200.860299964 |
| Connecticut          | East    | 18549.801000000003 | 611734.2995000016  | 2297200.860299964 |
| Delaware             | East    | 21056.085          | 611734.2995000016  | 2297200.860299964 |
| District of Columbia | East    | 2198.4500000000003 | 611734.2995000016  | 2297200.860299964 |
| Florida              | South   | 50002.98979999998  | 402031.9833000008  | 2297200.860299964 |
| Georgia              | South   | 51400.145          | 402031.9833000008  | 2297200.860299964 |
| Illinois             | Central | 112819.77200000001 | 518800.13220000133 | 2297200.860299964 |
| Indiana              | Central | 22977.86399999999  | 518800.13220000133 | 2297200.860299964 |
| Iowa                 | Central | 12426.147          | 518800.13220000133 | 2297200.860299964 |
| Kansas               | Central | 1727.652           | 518800.13220000133 | 2297200.860299964 |
| Kentucky             | South   | 29143.844999999994 | 402031.9833000008  | 2297200.860299964 |
| Louisiana            | South   | 16625.867999999995 | 402031.9833000008  | 2297200.860299964 |
| Maryland             | East    | 1588.8099999999997 | 611734.2995000016  | 2297200.860299964 |
| Massachusetts        | East    | 28411.344999999983 | 611734.2995000016  | 2297200.860299964 |
| Michigan             | Central | 58076.85980000002  | 518800.13220000133 | 2297200.860299964 |
| Minnesota            | Central | 50062.380500000014 | 518800.13220000133 | 2297200.860299964 |
| Mississippi          | South   | 19347.245000000003 | 402031.9833000008  | 2297200.860299964 |
| Missouri             | Central | 13013.175000000003 | 518800.13220000133 | 2297200.860299964 |
| Nebraska             | Central | 6492.410000000001  | 518800.13220000133 | 2297200.860299964 |
| Nevada               | West    | 1214.986           | 764634.4453000004  | 2297200.860299964 |
| New Hampshire        | East    | 9720.146           | 611734.2995000016  | 2297200.860299964 |
| New Jersey           | East    | 20267.067999999996 | 611734.2995000016  | 2297200.860299964 |
| New Mexico           | West    | 6046.187999999998  | 764634.4453000004  | 2297200.860299964 |
| New York             | East    | 279549.8235000001  | 611734.2995000016  | 2297200.860299964 |
| North Carolina       | South   | 116635.46149999995 | 402031.9833000008  | 2297200.860299964 |
| Ohio                 | East    | 74771.33           | 611734.2995000016  | 2297200.860299964 |
| Oklahoma             | Central | 5135.818           | 518800.13220000133 | 2297200.860299964 |
| Oregon               | West    | 17327.171000000002 | 764634.4453000004  | 2297200.860299964 |
| Pennsylvania         | East    | 142838.551         | 611734.2995000016  | 2297200.860299964 |
| Rhode Island         | East    | 12782.889999999996 | 611734.2995000016  | 2297200.860299964 |
| South Dakota         | Central | 2339.5979999999995 | 518800.13220000133 | 2297200.860299964 |
| Tennessee            | South   | 36733.58319999997  | 402031.9833000008  | 2297200.860299964 |
| Texas                | Central | 192758.20489999966 | 518800.13220000133 | 2297200.860299964 |
| Utah                 | West    | 16323.026999999996 | 764634.4453000004  | 2297200.860299964 |
| Virginia             | South   | 46521.297999999995 | 402031.9833000008  | 2297200.860299964 |
| Washington           | West    | 133177.25180000006 | 764634.4453000004  | 2297200.860299964 |
| Wisconsin            | Central | 40970.251          | 518800.13220000133 | 2297200.860299964 |
