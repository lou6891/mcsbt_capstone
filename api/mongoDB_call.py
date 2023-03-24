# Import required packages
import pymongo
from dotenv import load_dotenv
import os


# Function to get data from a MongoDB collection
def get_collection(collection_name, limit):
    try:
        # Load environment variables
        load_dotenv()

        # Create a MongoDB client using environment variables
        client = pymongo.MongoClient(
            os.getenv("MONGODB_URI").format(os.getenv("DB_USER"), os.getenv("PASSW"), os.getenv("HOST")))

        # Connect to the specified database
        db = client[os.getenv("DATABASE")]

        # Connect to the specified collection
        collection = db[collection_name]

        # Get up to 1000 documents from the collection and store them in a list
        output = list(collection.find().limit(limit))

        # Close the MongoDB client
        client.close()

        # Remove the '_id' field from each document in the output list
        for row in output:
            del row['_id']

        # Return the output list
        return output

    except Exception as error:
        # Print the error and return False if there is an exception
        print(error)
        return False


# Function to log in a user by checking their username and password
def login(username, password):
    try:
        # Load environment variables
        load_dotenv()

        # Create a MongoDB client using environment variables
        client = pymongo.MongoClient(
            os.getenv("MONGODB_URI").format(os.getenv("DB_USER"), os.getenv("PASSW"), os.getenv("HOST")))

        # Connect to the specified database
        db = client[os.getenv("DATABASE")]

        # Connect to the 'users' collection
        collection = db["users"]

        # Find a document that matches the given username and password
        output = collection.find_one({"username": username, "password": password})

        # Close the MongoDB client
        client.close()

        # If a matching document is found, return true
        if output:
            return "Login Successful"
        else:
            # If no matching document is found, return False
            return False

    except Exception as error:
        # Print the error and return False if there is an exception
        print(error)
        return False
