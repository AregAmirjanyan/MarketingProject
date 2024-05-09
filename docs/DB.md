# Database Documentation

Table of Contents:
- [schema.py](#schema-py)
- [basic_etl.py](#basic-etl-py)
- [csv_files_creator.py](#csv-files-creator-py)
- [data_generator.py](#data-generator-py)

This document provides an overview of the database-related modules and functionalities within the `db` folder.

## schema.py

The `schema.py` file is responsible for defining the database schema and initializing the database.

### `Functions`

#### `initialize_database(db_file_path)`

Initializes the database by creating tables if they do not exist.

- **Parameters**:
  - `db_file_path` (str): The path to the SQLite database file.

### `Tables`

Defines the following database tables:
- `User`
- `Rating`
- `PaymentMethod`
- `Transaction`
- `Product`
- `TransactionProduct`
- `ABTestingResults`

## basic_etl.py

The `basic_etl.py` file handles basic ETL (Extract, Transform, Load) operations for importing data into the database.

#### `Dependencies`

- `SqlHandler` from `sql_interactions`
- `CustomFormatter` from `logger`
- `pandas` for data manipulation

### `Functions`

#### `insert_many(df)`

Inserts data from DataFrames into respective tables in the database.


## csv_files_creator.py

This script generates CSV files containing sample data for database tables.

#### `Functionality`

The script generates the following CSV files with sample data:
- `user.csv`
- `product.csv`
- `PaymentMethod.csv`
- `Rating.csv`
- `TransactionProduct.csv`
- `Transaction.csv`

#### `Usage`

1. **Navigate to Project Directory**:
   The script navigates up the directory tree until it reaches the root directory of the project, named "MarketingProject".

2. **Data Generation**:
   Random data is generated for the tables using data generator functions.

3. **CSV File Creation**:
   CSV files are created in the `data` directory within the project folder if they do not already exist. Each CSV file corresponds to a database table and contains the generated sample data.

4. **Writing Data to CSV Files**:
   Data generated for each entity is written to the respective CSV file.




## data_generator.py

This script provides functions to generate sample data for database tables.



