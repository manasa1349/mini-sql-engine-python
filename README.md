# Mini SQL Query Engine (Python)

## Overview

This project implements a functional, in-memory SQL query engine in Python.
It simulates the internal processing of SQL queries by implementing a custom parser, execution engine, CSV loader, comparison engine, and output formatter.

The goal of this project is to provide an educational demonstration of how SQL queries are parsed and executed without relying on any external database system.
The engine supports core SQL features required by the assignment along with additional enhancements for improved usability.

## Features Implemented

### Core Required Features

* Load CSV files into memory as database tables
* SQL parsing for:
  * `SELECT`
  * `FROM`
  * `WHERE`
* Projection:
  * `SELECT *`
  * `SELECT column1, column2`
* Filtering:
  * Single and multiple conditions
  * Operators: `=`, `!=`, `>`, `<`, `>=`, `<=`
* Aggregation:
  * `COUNT(*)`
  * `COUNT(column)`
* Robust error handling for:
  * Missing SQL keywords
  * Incorrect syntax
  * Unknown columns
  * Invalid numeric comparisons
  * Malformed WHERE conditions

### Additional Features

These features go beyond the basic requirements and make the engine more complete:

* `ORDER BY` with numeric-aware sorting
* `LIMIT n`
* `SELECT column AS alias`
* Aggregate functions: `SUM`, `AVG`, `MIN`, `MAX`
* Multi-condition filtering with `AND` and `OR`
* Cleaner CLI output formatting
* Friendly and descriptive error messages


## Project Structure

This is the top-level structure of the project:

```
SQL_engine_python/
|
|-- mini_sql/
|   |-- parser.py
|   |-- engine.py
|   |-- loader.py
|   |-- utils.py
|   |-- cli.py
|
|-- sample_data/
|   |-- students_small.csv
|   |-- students_large.csv
|
|-- screenshots/
|   |-- sample_all_tests/
|   |-- 01_cli_start.png
|   |-- 02_select_star.png
|   |-- 03_select_column.png
|   |-- 04_where.png
|   |-- 05_where_comparison.png
|   |-- 06_count_star.png
|   |-- 07_count_column_condition.png
|   |-- 08_order_by.png
|   |-- 09_alias.png
|   |-- 10_and_condition.png
|   |-- 11_avg.png
|   |-- 12_error_handling.png
|
|-- README.md
```

### About the screenshots folder

The `screenshots/` directory contains images demonstrating:

* Starting the CLI
* Running SELECT queries
* Filtering with WHERE
* Comparison operators
* Aggregation
* ORDER BY sorting
* AND/OR logical conditions
* Error handling scenarios

The `sample_all_tests/` folder contains the full set of test screenshots taken during validation.

The screenshots provide visual examples of the engine's behavior across various SQL queries and error scenarios.

## How to Run the CLI

### Step 1: Create a virtual environment

```
python -m venv venv
```

### Step 2: Activate the environment

Windows:
```
venv\Scripts\activate
```

### Step 3: Start the SQL engine

```
python -m mini_sql.cli --file sample_data/students_small.csv
```

You should see:

```
Loaded table: sample_data/students_small.csv
mini-sql>
```

You can now run SQL queries interactively.

### Optional:

Load a different CSV during REPL:

```
load students_large
```


## Supported SQL Grammar

### SELECT

```
SELECT *
SELECT column
SELECT column1, column2
SELECT column AS alias
```

### FROM

```
SELECT ... FROM table_name
```

### WHERE

```
SELECT ... FROM table WHERE column > value
SELECT ... FROM table WHERE column = 'string'
```

Supported operators:

```
=   !=   >   <   >=   <=
```

Multiple condition support:

```
WHERE col1 > 10 AND col2 = 'Yes'
WHERE col1 > 50 OR col2 < 20
```

### ORDER BY

```
SELECT ... FROM table ORDER BY column ASC
SELECT ... FROM table ORDER BY column DESC
```

### LIMIT

```
SELECT ... FROM table LIMIT 5
```

### Aggregates

```
SELECT COUNT(*) FROM table
SELECT COUNT(column) FROM table
SELECT SUM(column) FROM table
SELECT AVG(column) FROM table
SELECT MIN(column) FROM table
SELECT MAX(column) FROM table
```

---

## Example Queries

```
SELECT * FROM students_small LIMIT 5;

SELECT name, mail FROM students_small;

SELECT name, hr_score 
FROM students_small 
WHERE hr_score > 50;

SELECT name, lc_easy 
FROM students_small 
WHERE lc_easy > 50 AND hr_score > 40;

SELECT COUNT(*) FROM students_small;

SELECT AVG(lc_total) FROM students_small;

SELECT name, cc_rating 
FROM students_large 
ORDER BY cc_rating DESC 
LIMIT 10;

SELECT name AS student, mail AS email_id 
FROM students_small 
LIMIT 5;
```


## Error Handling

The engine detects and reports:

### Invalid syntax

```
SELEC name FROM table
Parse error: Missing SELECT clause
```

### Missing FROM

```
SELECT name table
Parse error: Missing FROM clause
```

### Unknown columns

```
SELECT wrong_column FROM students_small
Execution error: Column not found: wrong_column
```

### Invalid numeric comparisons

```
SELECT name FROM students_small WHERE hr_score > 'abc'
Execution error: Invalid numeric comparison: <value> > abc
```

The engine never crashes and always reports clear, descriptive messages.


## Internal Architecture

### parser.py

Breaks SQL strings into structured query components (SELECT, FROM, WHERE, ORDER BY, LIMIT, aggregates).

### engine.py

Executes queries by:

* Filtering rows
* Evaluating conditions
* Performing numeric-aware sorting
* Computing aggregates
* Selecting and renaming columns

### utils.py

Implements:

* Type coercion
* Safety checks
* Comparison rules
* Pretty table formatting
* Aggregate computation

### loader.py

Loads CSV files using `csv.DictReader` and returns table data and column names.

### cli.py

Implements a REPL that:

* Accepts SQL statements
* Executes them through the engine
* Prints formatted output
* Supports table switching through `load` command


## Limitations

* GROUP BY is not supported
* JOINs are not supported
* WHERE operator precedence is left-to-right only
* Only CSV files are supported
* Only simple SQL grammar is implemented

These limitations reflect the intended scope of this lightweight SQL engine and can be expanded in future iterations.

## Conclusion

This project fulfills all mandatory requirements and includes several optional enhancements.
It demonstrates a complete workflow of SQL query processing using Python, with clear modularity, error handling, and user interaction via a CLI.