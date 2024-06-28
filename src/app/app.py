# Description: This file contains the main logic for the bot. It listens for incoming requests from Discord, and responds to them accordingly.
# Importing required libraries
import os
from flask import Flask, jsonify, request, abort
from discord_interactions import verify_key_decorator
from asgiref.wsgi import WsgiToAsgi
from mangum import Mangum
import requests


# Setting up the Flask app and discord public key
DISCORD_PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")


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


def download_random_s3_file(type):
    import boto3
    import csv
    import random
    
    s3 = boto3.client('s3')
    BUCKET_NAME = 'memes-repo-ia'

    if type == "shitpost":
        INDEX_FILE = 'csv-folder/indexes.csv'

    elif type == "bean":
        INDEX_FILE = 'csv-folder/indexes-bean.csv'

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
        return filepath
            
    except Exception as e:
        print(f"An error occurred: {e}")


def upload_to_discord(file_path, channel_id):
    
    file_name = os.path.basename(file_path)
    extension = os.path.splitext(file_name)[1]
    content_type_map = {
        # Images
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'bmp': 'image/bmp',
        'webp': 'image/webp',
        'tiff': 'image/tiff',
        'tif': 'image/tiff',

        # Videos
        'mp4': 'video/mp4',
        'avi': 'video/x-msvideo',
        'mov': 'video/quicktime', 
        'mkv': 'video/x-matroska',
        'webm': 'video/webm',
        'flv': 'video/x-flv', 
        'wmv': 'video/x-ms-wmv',
        'mpeg': 'video/mpeg',
        'mpg': 'video/mpeg'
        }
    
    content_type = content_type_map.get(extension[1:], 'application/octet-stream')
    with open(file_path, 'rb') as f:
        file = {'file': (file_name, f, content_type)} 
        URL = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        headers = {
            "Authorization": f"Bot {BOT_TOKEN}"
        }
        
        response = requests.post(URL, headers=headers, files=file)

        if response.status_code == 200:
            data = response.json()
            attachments = data.get("attachments", [])
            if attachments:
                return attachments[0]["url"]
            else:
                print("File uploaded, but URL not found in response.")
        else:
            print(f"Error uploading file: {response.text}")
    return None




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
        return jsonify(response_data)
        

    else:
        # Preparing incoming data for commands
        data = raw_request["data"]
        command_name = data["name"]
        channel_id = raw_request["channel_id"]

        # Checking which command, and executing the one that matches
        if command_name == "shitpost":
            upload_to_discord(download_random_s3_file(command_name), channel_id)
            response_data = {
            "type": 1
            }
            return jsonify(response_data)
        if command_name == "bean":
            upload_to_discord(download_random_s3_file(command_name), channel_id)
            response_data = {
            "type": 1
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