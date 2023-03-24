# REST API Documentation - Flask-RESTx

This document outlines the REST API built using Flask-RESTx for a web application that manages articles, transactions, and customers.

## Overview

This REST API is designed to provide access to the following resources:

- Articles
- Transactions
- Customers
- Users

It includes operations for fetching, creating, and managing these resources. The API uses JSON Web Tokens (JWT) for authentication and authorization.



## Required Modules

Before using the REST API, the following Python modules must be installed:

1. Flask: `pip install Flask`
2. Flask-RESTx: `pip install flask-restx`
3. Flask-JWT-Extended: `pip install flask-jwt-extended`
4. PyMongo: `pip install pymongo`
5. Python-dotenv: `pip install python-dotenv`
6. Pandas: `pip install pandas`

## Utility Functions

The REST API uses the following utility functions:

### `get_collection(collection_name)`

- Description: Fetches a collection from the database.
- Input: `collection_name` (string) - The name of the collection to fetch.
- Output: JSON array of the specified collection.

### `login(username, password)`

- Description: Verifies a user's credentials and returns their details.
- Input:
  - `username` (string): The username of the user.
  - `password` (string): The password of the user.
- Output: JSON object containing the user's details, or `None` if the credentials are invalid.

### `register(username, password)`

- Description: Registers a new user in the database.
- Input:
  - `username` (string): The desired username of the new user.
  - `password` (string): The desired password of the new user.
- Output: JSON object containing the new user's details, or `None` if registration fails.

### `collections_verifies_uploader()`

- Description: Verifies that the necessary collections are present in the database and uploads them if they are missing.
- Output: None.

These utility functions are called by the code to manage the resources, authenticate users, and interact with the database. Make sure to have them properly implemented and imported in your project.


## Endpoints

### Articles

#### GET /api/v1/articles

- Description: Fetches all articles.
- Authorization: Requires a valid JWT access token.
- Response:
  - Status code: 201 on success.
  - Body: JSON array of articles.

### Transactions

#### GET /api/v1/transactions

- Description: Fetches all transactions.
- Authorization: Requires a valid JWT access token.
- Response:
  - Status code: 201 on success.
  - Body: JSON array of transactions.

### Customers

#### GET /api/v1/customers

- Description: Fetches all customers.
- Authorization: Requires a valid JWT access token.
- Response:
  - Status code: 201 on success.
  - Body: JSON array of customers.

### Users

#### GET /api/v1/users/login

- Description: Logs in a user and generates access and refresh tokens.
- Request:
  - Query parameters:
    - username (string): The username of the user.
    - password (string): The password of the user.
- Response:
  - Status code: 200 on success.
  - Body: JSON object containing the user details, access token, refresh token, and their respective expiration times.

#### POST /api/v1/users/register

- Description: Registers a new user and generates access and refresh tokens.
- Request:
  - Query parameters:
    - username (string): The desired username of the new user.
    - password (string): The desired password of the new user.
- Response:
  - Status code: 200 on success.
  - Body: JSON object containing the user details, access token, refresh token, and their respective expiration times.

#### POST /api/v1/users/refresh

- Description: Refreshes an access token using a valid refresh token.
- Authorization: Requires a valid JWT refresh token.
- Response:
  - Status code: 200 on success.
  - Body: JSON object containing the new access token and its expiration time.

## Error Handling

In case of errors, the API will return a JSON object containing an error message and an appropriate HTTP status code.

## Authentication and Authorization

The API uses JWT for authentication and authorization. Users must log in or register to obtain a valid access token, which must be included in the Authorization header of requests to protected endpoints. Access tokens have a limited lifetime, and users can refresh them using their refresh token at the /api/v1/users/refresh endpoint.

