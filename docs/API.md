# Endpoints

## Shared Endpoints

These endpoints are accessible to both users granted and not granted special permissions. Permissions are handled based on the user table's `db_view` column.

### Root Endpoint

- **Description:** Retrieves the root endpoint HTML page.
- **HTTP Method:** GET
- **URL:** `/`
- **Response:** HTML page with links to Swagger UI, ReDoc, and Reports.

### User Login

- **Description:** Validates user credentials and returns an access token upon successful authentication.
- **HTTP Method:** POST
- **URL:** `/login`
- **Request Body:** OAuth2PasswordRequestForm
- **Response Body:** Dictionary containing access token and token type.

### Search Products

- **Description:** Searches for products based on product name, brand, and price.
- **HTTP Method:** GET
- **URL:** `/product/search`
- **Query Parameters:**
  - `product_name` (optional): Name of the product to search for.
  - `brand` (optional): Brand of the product to search for.
  - `price` (optional): Maximum price of the product to search for.
- **Response:** List of products matching the search criteria.

---

## Endpoints Specific to Users

These endpoints are specific to users who are not granted special permissions.

### My Transactions

- **Description:** Retrieves transactions associated with the current user.
- **HTTP Method:** GET
- **URL:** `/mytransactions`
- **Response:** List of transactions associated with the current user.

### Update Transaction

- **Description:** Updates details of a transaction associated with the current user.
- **HTTP Method:** PUT
- **URL:** `/mytransactions/update`
- **Request Body:** Details of the transaction to be updated.
- **Response:** Message indicating the success of the transaction update.

### Create Transaction

- **Description:** Creates a new transaction for the current user.
- **HTTP Method:** POST
- **URL:** `/transactions/new`
- **Request Body:** Details of the new transaction.
- **Response:** Details of the newly created transaction.

---

# auth_required

## Authentication Required

These endpoints require authentication, and users must be granted special permissions to access them.

### My Transactions (Granted User)

- **Description:** Retrieves transactions associated with the current user (Granted User).
- **HTTP Method:** GET
- **URL:** `/mytransactions`
- **Response:** List of transactions associated with the current user (Granted User).

### Update Transaction (Granted User)

- **Description:** Updates details of a transaction associated with the current user (Granted User).
- **HTTP Method:** PUT
- **URL:** `/mytransactions/update`
- **Request Body:** Details of the transaction to be updated.
- **Response:** Message indicating the success of the transaction update.

### Create Transaction (Granted User)

- **Description:** Creates a new transaction for the current user (Granted User).
- **HTTP Method:** POST
- **URL:** `/transactions/new`
- **Request Body:** Details of the new transaction.
- **Response:** Details of the newly created transaction.









---

# Authentication Required Endpoints

Endpoints specific to users who are not granted with special permission. Permission is handled from user table db_view column.

## GET /mytransactions

Retrieves the transactions associated with the current user.

### Parameters

- **current_user**: *schemas.TokenData, optional* - The current authenticated user. Defaults to Depends(u.get_current_user).

### Returns

- **list[schemas.MyTransactionsOut]**: A list of transactions associated with the current user.

## PUT /mytransactions/update

Updates the details of a transaction associated with the current user.

### Parameters

- **transaction_id**: *int* - The ID of the transaction to be updated.
- **payment_method_name**: *Literal['Debit Card', 'PayPal', 'Cash', 'Credit Card']* - The payment method name for the transaction.
- **rating_description**: *Literal['bad', 'normal', 'good', 'perfect', 'terrible']* - The rating description for the transaction.
- **status**: *Literal['returned', 'purchased', 'canceled']* - The status of the transaction.
- **type**: *Literal['pre-payment', 'post-payment']* - The type of transaction.
- **shipping_address**: *str, optional* - The shipping address for the transaction. Defaults to None.
- **current_user**: *schemas.TokenData, optional* - The current authenticated user. Defaults to Depends(u.get_current_user).

### Raises

- **HTTPException**: If the user does not own the specified transaction.

### Returns

- **dict**: A message indicating the success of the transaction update.

## POST /transactions/new

Creates a new transaction for the current user.

### Parameters

- **payment_method_name**: *Literal['Debit Card', 'PayPal', 'Cash', 'Credit Card']* - The payment method name for the transaction.
- **rating_description**: *Literal['bad', 'normal', 'good', 'perfect', 'terrible']* - The rating description for the transaction.
- **status**: *Literal['returned', 'purchased', 'canceled']* - The status of the transaction.
- **type**: *Literal['pre-payment', 'post-payment']* - The type of transaction.
- **shipping_address**: *str, optional* - The shipping address for the transaction. Defaults to None.
- **current_user**: *schemas.TokenData, optional* - The current authenticated user. Defaults to Depends(u.get_current_user).

### Returns

- **schemas.CreateTransactionOut**: Details of the newly created transaction.


# granted_user_required
# GRANTED VIEW

## Endpoints Specific to Users with Granted Permission

These endpoints are specific to users who are granted special permissions. Permissions are handled based on the user table's `db_view` column.

### Retrieve n Rows

- **Description:** Retrieves `n` rows from the specified table.
- **HTTP Method:** GET
- **URL:** `/{table}s`
- **Query Parameters:**
  - `n` (required): Number of rows to retrieve.
- **Response:** Dictionary containing the retrieved data.

### Create Entry

- **Description:** Creates an entry in the specified table.
- **HTTP Method:** POST
- **URL:** `/{table}/create`
- **Request Body:** Details of the new entry.
- **Response:** Dictionary indicating the success of the operation.

### Update Table

- **Description:** Updates a table with new values based on the specified condition.
- **HTTP Method:** PUT
- **URL:** `/{table}/update`
- **Query Parameters:**
  - `condition_col` (required): Name of the column to apply the condition.
  - `condition_val` (required): Value of the condition.
- **Request Body:** New values to update in the table.
- **Response:** Dictionary indicating the success of the operation.

---

## Endpoints Specific to Tables

These endpoints are specific to each table and allow users with granted permission to perform CRUD operations on individual tables.

### User Table

- **Retrieve n Rows:** GET `/users`
- **Create Entry:** POST `/user/create`
- **Update Table:** PUT `/user/update`

### Rating Table

- **Retrieve n Rows:** GET `/ratings`
- **Create Entry:** POST `/rating/create`
- **Update Table:** PUT `/rating/update`

### Payment Method Table

- **Retrieve n Rows:** GET `/payment_methods`
- **Create Entry:** POST `/payment_method/create`
- **Update Table:** PUT `/payment_method/update`

### Transactions Table

- **Retrieve n Rows:** GET `/transactions`
- **Create Entry:** POST `/transaction/create`
- **Update Table:** PUT `/transaction/update`

### Product Table

- **Retrieve n Rows:** GET `/products`
- **Create Entry:** POST `/product/create`
- **Update Table:** PUT `/product/update`

### Transaction Product Table

- **Retrieve n Rows:** GET `/transaction_products`
- **Create Entry:** POST `/transaction_product/create`
- **Update Table:** PUT `/transaction_product/update`




# Utils 

This module contains utility functions used for user authentication and authorization within the PayOpt API.

## Functions

### create_access_token

- **Description:** Creates an access token with the provided data.
- **Arguments:**
  - `data` (dict): Data to encode in the token.
- **Returns:** Encoded JWT access token.

### verify_access_token

- **Description:** Verifies and decodes the access token.
- **Arguments:**
  - `token` (str): JWT access token.
  - `credentials_exception` (HTTPException): Exception to raise if credentials are invalid.
- **Returns:** Decoded token data.

### get_current_user

- **Description:** Gets the current user based on the provided access token.
- **Arguments:**
  - `token` (str, optional): JWT access token. Defaults to Depends(oauth2_scheme).
- **Returns:** Current user's token data.

### check_privilege

- **Description:** Checks the privilege level of the current user.
- **Arguments:**
  - `token` (str, optional): JWT access token. Defaults to Depends(get_current_user).
- **Returns:** Privilege level of the current user.

## Constants

### SECRET_KEY

- **Description:** Secret key for JWT encoding and decoding.

### ALGO

- **Description:** Algorithm used for JWT encoding and decoding.

### ACCESS_TOKEN__EXPIRE_MINUTES

- **Description:** Expiration time (in minutes) for the access token.

### oauth2_scheme

- **Description:** OAuth2 password bearer for token URL.





# Schemas Module

This module defines Pydantic models representing various entities in the system.

## Models

### User

- **Description:** Represents a user in the system.
- **Fields:**
  - `password` (str)
  - `first_name` (str)
  - `last_name` (str)
  - `email` (str)
  - `phone_number` (Optional[str], default=None)
  - `db_view` (str, default="denied")

### Rating

- **Description:** Represents a rating for a transaction.
- **Fields:**
  - `description` (Optional[str], default=None)

### PaymentMethod

- **Description:** Represents a payment method.
- **Fields:**
  - `method_name` (str)

### Transactions

- **Description:** Represents a transaction in the system.
- **Fields:**
  - `user_id` (int)
  - `payment_method_id` (int)
  - `rating_id` (int)
  - `status` (str)
  - `type` (Optional[str], default=None)
  - `shipping_address` (Optional[str], default=None)
  - `explored_bandit_type` (Literal['bandit A', 'bandit B'])

### Product

- **Description:** Represents a product.
- **Fields:**
  - `product_name` (str)
  - `brand` (Optional[str], default=None)
  - `price` (float)

### TransactionProduct

- **Description:** Represents a product associated with a transaction.
- **Fields:**
  - `transaction_id` (int)
  - `product_id` (int)
  - `quantity` (Optional[int], default=None)
  - `date` (Optional[TDate], default=None)

### UserLogIn

- **Description:** Represents user login credentials.
- **Fields:**
  - `email` (str)
  - `password` (str)

### SearchProductOut

- **Description:** Represents the output of a product search.
- **Fields:**
  - `product_name` (Optional[str], default=None)
  - `brand` (Optional[str], default=None)
  - `price` (Optional[float], default=None)

### Token

- **Description:** Represents an authentication token.
- **Fields:**
  - `access_token` (str)
  - `token_type` (str)

### TokenData

- **Description:** Represents token data.
- **Fields:**
  - `id` (int)
  - `privilege` (str)

### MyTransactionsOut

- **Description:** Represents transaction details for the current user.
- **Fields:**
  - `transaction_id` (int)
  - `payment_method_name` (str) 
  - `rating_description` (Optional[str], default=None)
  - `status` (str)
  - `type` (Optional[str], default=None)
  - `shipping_address` (Optional[str], default=None)

### CreateTransactionOut

- **Description:** Represents the output of creating a transaction.
- **Fields:**
  - `payment_method_name` (Literal['Debit Card', 'PayPal', 'Cash', 'Credit Card'])
  - `rating_description` (Optional[Literal['bad', 'normal', 'good', 'perfect', 'terrible']], default=None)
  - `status` (Optional[Literal['returned', 'purchased', 'canceled']], default=None)
  - `type` (Literal['pre-payment', 'post-payment'])
  - `shipping_address` (Optional[str], default=None)
