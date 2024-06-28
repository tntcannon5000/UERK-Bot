# Description: This file contains the main logic for the bot. It listens for incoming requests from Discord, and responds to them accordingly.
# Importing required libraries
import os
from flask import Flask, jsonify, request, abort
from discord_interactions import verify_key_decorator, InteractionResponseType
from asgiref.wsgi import WsgiToAsgi
from mangum import Mangum
import requests
import json


# Setting up the Flask app and discord public key
DISCORD_PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

app = Flask(__name__)
app.config["DEBUG"] = True  # Add this line
asgi_app = WsgiToAsgi(app)
handler = Mangum(asgi_app)

# Setting up S3 bucket
def download_random_s3_file_bytesio():
    import boto3
    import csv
    import random
    import io
    
    
    s3 = boto3.client('s3')
    BUCKET_NAME = 'memes-repo-ia'
    INDEX_FILE = 'csv-folder/indexes.csv'

    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=INDEX_FILE)
        data = response['Body'].read().decode('utf-8')
        reader = csv.reader(data.splitlines())
        file_keys = [row[1] for row in reader] # Extract the keys from the CSV
        del file_keys[0]
        num_files = len(file_keys)
        random_file_key = file_keys[random.randint(0, num_files - 1)]

        with io.BytesIO() as file_buffer:
            s3.download_file(BUCKET_NAME, random_file_key, "thefile")
            file_buffer.seek(0)
            theimage = file_buffer.getvalue()

        return theimage, random_file_key
            
    except Exception as e:
        print(f"An error occurred: {e}")
        abort(500, description="Failed to retrieve a meme. Please try again later.") 


def download_random_s3_file():
    import boto3
    import csv
    import random
    import io
    
    
    s3 = boto3.client('s3')
    BUCKET_NAME = 'memes-repo-ia'
    INDEX_FILE = 'csv-folder/indexes.csv'

    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=INDEX_FILE)
        data = response['Body'].read().decode('utf-8')
        reader = csv.reader(data.splitlines())
        file_keys = [row[1] for row in reader] # Extract the keys from the CSV
        del file_keys[0]
        num_files = len(file_keys)
        random_file_key = file_keys[random.randint(0, num_files - 1)]
        filename = os.path.basename(random_file_key)
        filepath = os.path.join("/tmp", filename)
        s3.download_file(BUCKET_NAME, random_file_key, filepath)

        return filepath, random_file_key
            
    except Exception as e:
        print(f"An error occurred: {e}")
        abort(500, description="Failed to retrieve a meme. Please try again later.") 



@app.route('/', methods=['POST'])
async def interactions():
    print(f"Received request: {request.json}")
    raw_request = request.json
    return interact(raw_request)



@verify_key_decorator(DISCORD_PUBLIC_KEY)
def interact(raw_request):
    if raw_request["type"] == 1: # Discord pinging the bot to check if it is alive
        response_data = {
            "type": 1
        }
        


    else:
        # Preparing incoming data for commands
        data = raw_request["data"]
        command_name = data["name"]
        interaction_token = raw_request["token"]
        application_id = raw_request["application_id"]

        # Checking which command, and executing the one that matches
        if command_name == "shitpost":
            image_url = "https://img-9gag-fun.9cache.com/photo/a3ZRrev_460s.jpg"
            response_content = "The bot is currently online and functioning properly."
            response_data = {   
            "type": 4,
            "data": {
                "content": response_content,
                "embeds": [
                    {
                        "image": {
                            "url": image_url
                        }
                    }
                ],
                }
            }
            return jsonify(response_data)

        elif command_name == "echo":
            original_response = data["options"][0]["value"]
            response_content = f"Echoing: {original_response}"
            response_data = {   
            "type": 4,
            "data": {
                "content": response_content
                }
            }
            return jsonify(response_data)

        elif command_name == "silentresponse":
            return

        elif command_name == "statuscheck":
            response_content = "The bot is currently online and functioning properly."
            response_data = {   
            "type": 4,
            "data": {
                "content": response_content
                }
            }
            return jsonify(response_data)
        
        
        else:
            response_data = {   
            "type": 4,
            "data": {
                "content": "UNKNOWN ERROR LMAO CHECK THE CODEEEE"
                }
            }
            return jsonify(response_data)