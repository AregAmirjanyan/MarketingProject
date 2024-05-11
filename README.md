# Ecommerce Payment Optimizer

The Payment Optimizer package provides tools for analyzing and optimizing payment methods in e-commerce to maximize revenue generation. It includes A/B testing capabilities using t-tests to compare different payment options' effectiveness.

## Features

- A/B testing (t-test) functionality to evaluate the performance of different payment methods.
- Analysis tools to understand which payment options are more beneficial for e-commerce revenue.
- Integration with Power BI for visualization of test results through a dashboard.
- API for managing user registration, updating user information, adding transactions, and more.

## Subpackages

The payment_optimizer package consists of three essential subpackages:

- **db:** This subpackage facilitates various database operations, including generating fake data, writing data to CSV files, creating schemas, and generating the e_commerce.db file. Additionally, it provides functionalities for populating tables with generated data. The sql_interactions.py module serves as a bridge between SQL and Python, enabling seamless interactions between the two.
- **models:** In this subpackage, the necessary data is prepared, model metrics are created, and A/B testing is conducted for three payment options: only pre-payment is available, both pre and post-payment are available, and only post-payment is available. The results of the model are stored in a dictionary for further use.
- **api:** The API serves as the backend for the PayOpt application, providing endpoints for user authentication, product search, and additional functionalities for users with granted access and special permissions. It includes features such as user login, product search based on various criteria (product name, brand, price), and routers for handling endpoints specific to granted users and authentication requirements.

## Required Inputs

To utilize the package effectively, ensure that the schema adheres to the following format:
![Alt Text](Documents/ERD.png)

## Installation

You can install Payment Optimizer using pip:

```bash
pip install payment_optimizer
```

## Usage

Below is a basic example demonstrating how to utilize certain functions from the package:

```python
from payment_optimizer.models import ABTesting

ab_test = ABTesting(data_connect)
ab_test.preprocess_data()
model_result = ab_test.perform_ab_test(start_date, end_date)
```

## API Calls

### Default Endpoints

- **Root Endpoint:** [http://localhost:8000/](http://localhost:8000/)
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Power BI Report:** [http://localhost:8000/](https://app.powerbi.com/reportEmbed?reportId=1733eb14-e25c-482e-8d8a-6f7172727743&autoAuth=true&ctid=4c0b7b5b-f6ee-4e4e-b961-0512d8fcb5f2)
- **Product Search:** [http://localhost:8000/search](http://localhost:8000/docs#/Default/search_products_product_search_get)

### Denied View Endpoints

- **GET User Transactions:** [http://localhost:8000/mytransactions](http://localhost:8000/docs#/Authentication%20Required/get_user_transactions_mytransactions_get)
- **PUT Update Transaction:** [http://localhost:8000/mytransactions/update](http://localhost:8000/docs#/Authentication%20Required/update_transaction_mytransactions_update_put)
- **POST Create Transaction:** [http://localhost:8000/transactions/new](http://localhost:8000/docs#/Authentication%20Required/create_transaction_transactions_new_post)

### Granted View Endpoints

- **GET Users:** [http://localhost:8000/users](http://localhost:8000/docs#/Granted%20User%20Access%20Required/select_n_rows_users_get)
- **POST Create User:** [http://localhost:8000/user/create](http://localhost:8000/docs#/Granted%20User%20Access%20Required/create_entry_user_create_post)
- **PUT Update User:** [http://localhost:8000/user/update](http://localhost:8000/docs#/Granted%20User%20Access%20Required/update_table_user_update_put)
- **GET Ratings:** [http://localhost:8000/ratings](http://localhost:8000/docs#/Granted%20User%20Access%20Required/select_n_rows_ratings_get)
- **POST Create Rating:** [http://localhost:8000/rating/create](http://localhost:8000/docs#/Granted%20User%20Access%20Required/create_entry_rating_create_post)
- **PUT Update Rating:** [http://localhost:8000/rating/update](http://localhost:8000/docs#/Granted%20User%20Access%20Required/update_table_rating_update_put)
- **GET Payment Methods:** [http://localhost:8000/payment_methods](http://localhost:8000/docs#/Granted%20User%20Access%20Required/select_n_rows_payment_methods_get)
- **POST Create Payment Method:** [http://localhost:8000/payment_method/create](http://localhost:8000/docs#/Granted%20User%20Access%20Required/create_entry_payment_method_create_post)
- **PUT Update Payment Method:** [http://localhost:8000/payment_method/update](http://localhost:8000/docs#/Granted%20User%20Access%20Required/update_table_payment_method_update_put)
- **GET Transactions:** [http://localhost:8000/transactions](http://localhost:8000/docs#/Granted%20User%20Access%20Required/select_n_rows_transactionss_get)
- **POST Create Transaction:** [http://localhost:8000/transaction/create](http://localhost:8000/docs#/Granted%20User%20Access%20Required/create_entry_transactions_create_post)
- **PUT Update Transaction:** [http://localhost:8000/transaction/update](http://localhost:8000/docs#/Granted%20User%20Access%20Required/update_table_transactions_update_put)
- **GET Products:** [http://localhost:8000/products](http://localhost:8000/docs#/Granted%20User%20Access%20Required/select_n_rows_products_get)
- **POST Create Product:** [http://localhost:8000/product/create](http://localhost:8000/docs#/Granted%20User%20Access%20Required/create_entry_product_create_post)
- **PUT Update Product:** [http://localhost:8000/product/update](http://localhost:8000/docs#/Granted%20User%20Access%20Required/update_table_product_update_put)
- **GET Transaction Products:** [http://localhost:8000/transaction_products](http://localhost:8000/docs#/Granted%20User%20Access%20Required/select_n_rows_transaction_products_get)
- **POST Create Transaction Product:** [http://localhost:8000/transaction_product/create](http://localhost:8000/docs#/Granted%20User%20Access%20Required/create_entry_transaction_product_create_post)
- **PUT Update Transaction Product:** [http://localhost:8000/transaction_product/update](http://localhost:8000/docs#/Granted%20User%20Access%20Required/update_table_transaction_product_update_put)

## Documentation

For detailed documentation and usage examples, refer to the official [documentation](https://aregamirjanyan.github.io/MarketingProject/).
Link to our Project in PyPi: [PyPi package:](https://pypi.org/project/new2/1.0.0/)

## License

Payment Optimizer is distributed under the MIT License.
