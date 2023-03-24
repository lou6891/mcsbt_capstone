# Import required packages
import pymongo
from dotenv import load_dotenv
import os


# Function to register a new user with a given username and password
def register(username, password):
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

        # Create a dictionary containing the user's data
        userData = {"username": username, "password": password}

        # Check if a document with the same user data already exists in the collection
        if collection.find_one(userData):
            # Close the MongoDB client and return a message if the user already exists
            client.close()
            return "User already in DB"
        else:
            # Insert the new user data into the collection, close the MongoDB client, and return a success message
            collection.insert_one(userData)
            client.close()
            return "User created correctly"

    except Exception as error:
        # Print the error and return False if there is an exception
        print(error)
        return False
