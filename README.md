# Final Capstone project

This repository contains the code for the final capstone project for the MCSBT
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

> ALl code documentation is present in specific README inside the API and Client