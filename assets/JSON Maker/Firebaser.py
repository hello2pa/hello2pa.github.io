#This file will replace a collection in your
#firestore database with JSON files as
#documents. The name of each document will
#be the name of the JSON file.

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore_async

# FILES
SERVICE_ACCOUNT_PATH = #Firebase account JSON file thingy path
FOLDER_PATH = #Path to the folder that contains your JSON files
COLLECTION_NAME = #Input your own collection name

# FIREBASE CRAP
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

# START BY CLEARING THE COLLECTION
def clear_collection(collection_name):
    print(f"Clearing collection: {collection_name}")
    docs = db.collection(collection_name).stream()
    deleted = 0
    for doc in docs:
        db.collection(collection_name).document(doc.id).delete()
        deleted += 1
    print(f"Deleted {deleted} documents from '{collection_name}'")

# LOAD JSON FILES IN
def upload_json_folder(folder_path, collection_name):
    files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    print(f"Found {len(files)} JSON files to upload.")

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                doc_id = os.path.splitext(filename)[0]
                db.collection(collection_name).document(doc_id).set(data)
                print(f"Uploaded: {filename} -> doc ID: {doc_id}")
            except Exception as e:
                print(f"Error uploading {filename}: {e}")

# 80085
if __name__ == '__main__':
    clear_collection(COLLECTION_NAME)
    upload_json_folder(FOLDER_PATH, COLLECTION_NAME)
    print("Upload complete.")
