# Final Capstone project

This repository contains the code for the final capstone project for the MCSBT.
This project aims to create a complete data visualization solution, which includes understanding the dataset, deploying 
a database solution, integrating a back-end service, developing a front-end, and ensuring proper documentation and structure.

The structure of this repo is as follows:
- API
  - Contains the API created using flask_restx
  - It connects to a MongoDB database and retrieves the data necessary for the client
- Client
  - Created with Streamlit
  - Enables data visualization and analysis
- Data
  - The data uploaded to MongoDb they are not used by the API or Client, they have documentation purposes.

## Assigment Requirements

1. Understanding of the Data Set: 
   - Generate valuable KPIs based on the provided datasets or your own datasets. 
2. Database Solution:
   - Deploy a MongoDB database . At a minimum, all datasets should be stored as tables. You may also include processed tables for easier data management. 
3. Back-end Integration: 
   - Deploy a Flask service in Google App Engine that exposes an API to query data from the database in JSON format via HTTP GET requests. The API should require an API key for authentication. 
4. Front-end Development: 
   - Deploy a Streamlit service in Google App Engine or create your own charts using JavaScript, CSS, and HTML. The front-end should include filters to query data from the API and display the results in JSON format. User password authentication should be implemented. 
5. Documentation, Structure of the Coding, and Presentation: 
   - Use Swagger for API documentation, GitHub for version control, and create a presentation for the project. 
6. Solidness of the Solution and Creativity/Going Beyond: 
   - Evaluate the robustness of the solution and the level of creativity involved.

## Local testing / deploying with .env
To test local or deploy using .env for environmental variables it's necessary to set the following:

1. In the **api** folder create a .env file containing the following:<br>
   - MONGODB_URI=mongodb+srv://{0}:{1}@{2}/?retryWrites=true&w=majority 
   - DB_USER=<your_username>
   - PASSW=<your_password>
   - HOST=<your_host>
   - DATABASE=<your_database>
   - COLLECTIONS_LIST=articles,transactions,customers

2. In the **client** folder create a .env file containing the following:<br>
   - BASE_API_URL=<your_api_url> <br> EX: http://127.0.0.1:5000

## Deploy on Google App Engine
To deploy on google app engine it's necessary to create app.yalm files with the settings and environmental variables

> The .env do not work on app engines

1. In the **api** folder create a file called app.yaml with the following:
    ```
    runtime: python
    service : <your_service_name>
    env: flex
    
    entrypoint: gunicorn -b :$PORT main:app
    
    runtime_config:
        python_version: 3
    
    manual_scaling:
      instances: 1
    
    env_variables:
        MONGODB_URI: "mongodb+srv://{0}:{1}@{2}/?retryWrites=true&w=majority"
        DB_USER: "<your_username>"
        PASSW: "<your_password>"
        HOST: "<your_host>"
        DATABASE: "<your_database>"
        COLLECTIONS_LIST: "articles,transactions,customers"
    ```

2. In the **client** folder create a file called app.yaml with the following:
    ```
   runtime: python
    service : <your_service_name>
    env: flex
    
    entrypoint : streamlit run 1_Home.py --server.port $PORT
    
    runtime_config:
        python_version: 3.7
    
    manual_scaling:
      instances: 1
    
    env_variables:
      BASE_API_URL: "<your_api_url>"
    ```




> **More detailed information for each component is present in relative README file inside the API and Client**