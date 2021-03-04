<link rel="stylesheet" href="./themes/markedstyle/github.css">
<img style="float" src="./2020-08-23-20-41-40.png" width="150" height="100"/>


# SQL: Working with Dates

## Understanding Timestamps

Many data tables provide timestamps, recording the moment when a specific action is taken. For example, retail data may include timestamps for when a purchase was made and log data for websites contain timestamps for user events, such as logging on and logging off. While there are various specific timestam formats, the timestamps we will examine in this class will take the form of the following example.

**2020-01-31 14:30:01**

| 2020 | 01 | 31 | 14 | 30 | 01|
|------|----|----|----|----|---|
| Year | Month | Day | Hour | Minute | Second |

This timestamp records an event at 2:30 PM and one second, on January 31, 2020. 

## Basic Date Functions

### The Date Function

In some cases a timestamp may provide more data than is necessary. If we are only interested in the date of an action, not the hour, minute, and second, then we could extract the calendar date using the `DATE` function. Let's use `DATE` to return the date for 2020-01-31 14:30:01.

```
SELECT DATE('2020-01-31 14:30:01')
```

The result is 2020-01-31 00:00:00. Here, the output for `DATE` still includes placeholders for the hours, minutes, and seconds, but these are set to values of `00`. Thus, if the `DATE` function is applied to an attribute of timestamps values, any given attribute values will only vary by year, month, and/or day. 


### Extracting Dateparts

You may encounter situations where you need to extract a particular datepart from a timestamp. SQL makes it easy to accomplish this task with `EXTRACT`. For instance, say we need to take the calendar day from the shipping dates in the `orders` table.

```
SELECT orderDate, EXTRACT(day from orderDate) 
FROM scott_adams.orders
LIMIT 10;
```

| orderdate           | date_part |
|---------------------|-----------|
| 2017-11-08 00:00:00 | 8         |
| 2017-11-08 00:00:00 | 8         |
| 2017-06-12 00:00:00 | 12        |
| 2016-10-11 00:00:00 | 11        |
| 2016-10-11 00:00:00 | 11        |
| 2015-06-09 00:00:00 | 9         |
| 2015-06-09 00:00:00 | 9         |
| 2015-06-09 00:00:00 | 9         |
| 2015-06-09 00:00:00 | 9         |
| 2015-06-09 00:00:00 | 9         |

In the output above, the values in the `date_part` column match the value in the day place for associated timestamp value in the `orderdate` column Similarly, we could extract the year of each order date by replacing `day` with `year` in the `EXTRACT` function. 

```
SELECT orderDate, EXTRACT(year from orderDate) 
FROM scott_adams.orders
LIMIT 10;
```

| orderdate           | date_part |
|---------------------|-----------|
| 2017-11-08 00:00:00 | 2017      |
| 2017-11-08 00:00:00 | 2017      |
| 2017-06-12 00:00:00 | 2017      |
| 2016-10-11 00:00:00 | 2016      |
| 2016-10-11 00:00:00 | 2016      |
| 2015-06-09 00:00:00 | 2015      |
| 2015-06-09 00:00:00 | 2015      |
| 2015-06-09 00:00:00 | 2015      |
| 2015-06-09 00:00:00 | 2015      |
| 2015-06-09 00:00:00 | 2015      |

What if we needed to extract the day of the week, not simply the calendar day, from a timestamp? In this situation we could use `dow` in the `EXTRACT` function.

```
SELECT orderDate, EXTRACT(dow from orderDate) 
FROM scott_adams.orders
LIMIT 10;
```

| orderdate           | date_part |
|---------------------|-----------|
| 2017-11-08 00:00:00 | 3         |
| 2017-11-08 00:00:00 | 3         |
| 2017-06-12 00:00:00 | 1         |
| 2016-10-11 00:00:00 | 2         |
| 2016-10-11 00:00:00 | 2         |
| 2015-06-09 00:00:00 | 2         |
| 2015-06-09 00:00:00 | 2         |
| 2015-06-09 00:00:00 | 2         |
| 2015-06-09 00:00:00 | 2         |
| 2015-06-09 00:00:00 | 2         |

In the output above day of week values range from 0-6, with a value of 0 representing Sunday and a value of 6 representing Saturday. 

## Advanced Date Functions

Up to this point we looked at using SQL to extract date parts from timestamps. Now we will expand on our work with timestamps and look at adding and subtracting time from dates. 

### Adding and Subtracting Time: Date Intervals

The `INTERVAL` function can be used to add a specific interval of time to a timestamp. The query below uses `INTERVAL` to create a new column (`orderdate1year`) in the output that is one-year from the date in which a customer's order was made.

```
SELECT 
  orderDate, 
  orderDate + INTERVAL '1 year' as orderDate1Year
FROM scott_adams.superstorejoined
LIMIT 10;
```

| orderdate           | orderdate1year      |
|---------------------|---------------------|
| 2017-11-08 00:00:00 | 2018-11-08 00:00:00 |
| 2017-11-08 00:00:00 | 2018-11-08 00:00:00 |
| 2017-11-08 00:00:00 | 2018-11-08 00:00:00 |
| 2017-06-12 00:00:00 | 2018-06-12 00:00:00 |
| 2017-06-12 00:00:00 | 2018-06-12 00:00:00 |
| 2016-10-11 00:00:00 | 2017-10-11 00:00:00 |
| 2016-10-11 00:00:00 | 2017-10-11 00:00:00 |
| 2016-10-11 00:00:00 | 2017-10-11 00:00:00 |
| 2016-10-11 00:00:00 | 2017-10-11 00:00:00 |
| 2016-10-11 00:00:00 | 2017-10-11 00:00:00 |


Let's look at a one month interval now. 

```
SELECT 
  orderDate, 
  orderDate + INTERVAL '1 month' as orderDate1Month
FROM scott_adams.superstorejoined
LIMIT 10;
```

| orderdate           | orderdate1month     |
|---------------------|---------------------|
| 2017-11-08 00:00:00 | 2017-12-08 00:00:00 |
| 2017-11-08 00:00:00 | 2017-12-08 00:00:00 |
| 2017-11-08 00:00:00 | 2017-12-08 00:00:00 |
| 2017-06-12 00:00:00 | 2017-07-12 00:00:00 |
| 2017-06-12 00:00:00 | 2017-07-12 00:00:00 |
| 2016-10-11 00:00:00 | 2016-11-11 00:00:00 |
| 2016-10-11 00:00:00 | 2016-11-11 00:00:00 |
| 2016-10-11 00:00:00 | 2016-11-11 00:00:00 |
| 2016-10-11 00:00:00 | 2016-11-11 00:00:00 |
| 2016-10-11 00:00:00 | 2016-11-11 00:00:00 |

Note that you can also use `INTERVAL` to subtract time from dates. 

```
SELECT 
  orderDate, 
  orderDate - INTERVAL '1 year' as oneYearPrior
FROM scott_adams.superstorejoined
LIMIT 10;
```

| orderdate           | oneyearprior        |
|---------------------|---------------------|
| 2017-11-08 00:00:00 | 2016-11-08 00:00:00 |
| 2017-11-08 00:00:00 | 2016-11-08 00:00:00 |
| 2017-11-08 00:00:00 | 2016-11-08 00:00:00 |
| 2017-06-12 00:00:00 | 2016-06-12 00:00:00 |
| 2017-06-12 00:00:00 | 2016-06-12 00:00:00 |
| 2016-10-11 00:00:00 | 2015-10-11 00:00:00 |
| 2016-10-11 00:00:00 | 2015-10-11 00:00:00 |
| 2016-10-11 00:00:00 | 2015-10-11 00:00:00 |
| 2016-10-11 00:00:00 | 2015-10-11 00:00:00 |
| 2016-10-11 00:00:00 | 2015-10-11 00:00:00 |


### Time Between Two Dates

We have examined how to use `INTERVAL` the find the date that falls plus or minus a certain amount of time from a given date, but what if we wanted to know how much time elapsed between dates? At our superstore, we may be asked to calculate the number of days between the date an order is placed and the date an order is shipped and performing such a calculation is straightforward. All we need to do is subtract the name of one datetime attribute from another datetime attribute.

```
SELECT 
  orderDate, 
  shipDate,
  shipDate - orderDate as orderShipDiff
FROM scott_adams.superstorejoined
LIMIT 10;
```

| orderdate           | shipdate            | ordershipdiff |
|---------------------|---------------------|---------------|
| 2017-11-08 00:00:00 | 2017-11-11 00:00:00 | 3 days        |
| 2017-11-08 00:00:00 | 2017-11-11 00:00:00 | 3 days        |
| 2017-11-08 00:00:00 | 2017-11-11 00:00:00 | 3 days        |
| 2017-06-12 00:00:00 | 2017-06-16 00:00:00 | 4 days        |
| 2017-06-12 00:00:00 | 2017-06-16 00:00:00 | 4 days        |
| 2016-10-11 00:00:00 | 2016-10-18 00:00:00 | 7 days        |
| 2016-10-11 00:00:00 | 2016-10-18 00:00:00 | 7 days        |
| 2016-10-11 00:00:00 | 2016-10-18 00:00:00 | 7 days        |
| 2016-10-11 00:00:00 | 2016-10-18 00:00:00 | 7 days        |
| 2016-10-11 00:00:00 | 2016-10-18 00:00:00 | 7 days        |


If we do not want the "days" string at the end of each value in `ordershipdiff` we can use `EXTRACT`. However, instead of extracting the day from a single column, we are going to calculate the extract the day from the difference between two dates. 

```
SELECT 
  orderDate, 
  shipDate,
  EXTRACT(day from shipDate - orderDate) as orderShipDiff
FROM scott_adams.superstorejoined
LIMIT 10;
```

| orderdate           | shipdate            | ordershipdiff |
|---------------------|---------------------|---------------|
| 2017-11-08 00:00:00 | 2017-11-11 00:00:00 | 3             |
| 2017-11-08 00:00:00 | 2017-11-11 00:00:00 | 3             |
| 2017-11-08 00:00:00 | 2017-11-11 00:00:00 | 3             |
| 2017-06-12 00:00:00 | 2017-06-16 00:00:00 | 4             |
| 2017-06-12 00:00:00 | 2017-06-16 00:00:00 | 4             |
| 2016-10-11 00:00:00 | 2016-10-18 00:00:00 | 7             |
| 2016-10-11 00:00:00 | 2016-10-18 00:00:00 | 7             |
| 2016-10-11 00:00:00 | 2016-10-18 00:00:00 | 7             |
| 2016-10-11 00:00:00 | 2016-10-18 00:00:00 | 7             |
| 2016-10-11 00:00:00 | 2016-10-18 00:00:00 | 7             |

