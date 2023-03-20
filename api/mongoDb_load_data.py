# Import required packages
import pymongo
from dotenv import load_dotenv
import os
import pandas as pd


# Function to open a connection to the database
def open_connection_to_db():
    try:
        # Load environment variables
        load_dotenv()

        # Create a MongoDB client using environment variables
        client = pymongo.MongoClient(
            os.getenv("MONGODB_URI").format(os.getenv("USER"), os.getenv("PASSW"), os.getenv("HOST")))

        # Return a reference to the specified database
        return client[os.getenv("DATABASE")]

    except Exception as error:
        # Print the error and return False if there is an exception
        print(error)
        return False


# Function to upload a CSV file to a MongoDB collection
def upload_collection_to_mongo(db, collection_name):
    try:
        # Dictionary containing URLs for different data files
        url_dict = {
            "customers": "https://drive.google.com/file/d/1VerQ3_t3S5UBoN-6qteiuuntAf3pShBv/view?usp=sharing",
            "transactions": "https://drive.google.com/file/d/1n3y0re8mZfhYfz-SnKrGcq9yt9pc0rhD/view?usp=share_link",
            "articles": "https://drive.google.com/file/d/1jMwJOvIKZax47YHTn9wJu683uHAiqtes/view?usp=sharing",
        }

        # Extract the Google Drive file ID and build a direct download URL
        url = 'https://drive.google.com/uc?id=' + url_dict[collection_name].split('/')[-2]

        # Read the CSV file from the URL into a pandas DataFrame
        df = pd.read_csv(url)

        # Remove any unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Convert the DataFrame to a list of dictionaries
        df_dict = df.to_dict("records")

        # Connect to the specified collection and insert the data
        collection = db[collection_name]
        collection.insert_many(df_dict)

        return True

    except Exception as error:
        # Print the error and return False if there is an exception
        print(error)
        return False


# Function to check if a collection is in the database and upload it if not
def check_if_collection_in_db(collection_name):
    # Open a connection to the database
    db = open_connection_to_db()

    # Check if the database connection was successful and if the collection is present in the database
    if db is not None and collection_name in db.list_collection_names():
        print(collection_name, " is present in the db")
        return True

    elif db is not None:
        # If the collection is not present, attempt to upload it
        print(collection_name, " not present in the db, uploading...")
        upload_status = upload_collection_to_mongo(db, collection_name)
        if upload_status:
            return True
        else:
            # Print an error message if the upload fails
            print("Something went wrong uploading the collection: ", collection_name)
            return False

    else:
        # Print an error message if the database connection fails
        print("Something went wrong connecting to the db")
        return False


# Function to verify and upload collections to the database
def collections_verifies_uploader():
    # Load environment variables
    load_dotenv()

    # Iterate over the list of collections specified in the environment variable
    for collection in os.getenv("COLLECTIONS_LIST").split(","):
        res = check_if_collection_in_db(collection)
