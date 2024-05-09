# API

## POST /login

This endpoint is used for user authentication.

### Request

- **Method**: POST
- **URL**: `/login`
- **Body**:
  - `username`: The user's email.
  - `password`: The user's password.





## GET /product/search

This endpoint is used to search for products.

- **Method**: GET
- **URL**: /product/search
- **Parameters**:
   - `product_name` (optional string): The name of the product to search for.
   - `brand` (optional string): The brand of the product to search for.
   - `price` (optional float): The maximum price of the product to search for.