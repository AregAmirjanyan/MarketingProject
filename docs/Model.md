# models.py

This module defines classes for database interaction and A/B testing.

## DatabaseConnector

#### Description

- Provides methods for fetching and joining data from different tables in the database.

#### Methods

- **`__init__(self, db_name)`**: Initializes the DatabaseConnector object.
  - `db_name` (str): Name of the database to connect to.

- **`data_fetcher(self, table_name)`**: Fetches data from a specified table in the database.
  - `table_name` (str): Name of the table to fetch data from.

- **`join_tables(self)`**: Joins transaction-related tables to create a comprehensive DataFrame.

## ABTesting

#### Description

- Performs A/B testing on transaction data.

#### Methods

- **`__init__(self, db_connector)`**: Initializes the ABTesting object.
  - `db_connector` (DatabaseConnector): Instance of DatabaseConnector to access data.

- **`preprocess_data(self)`**: Preprocesses the data for A/B testing.

- **`parse_date(self, date_str)`**: Parses a date string into a datetime object.

- **`perform_ab_test(self, start_date=None, end_date=None)`**: Performs A/B testing.
  - `start_date` (str, optional): Start date for the analysis.
  - `end_date` (str, optional): End date for the analysis.

- **`results(self)`**: Retrieves the results of the A/B test.
