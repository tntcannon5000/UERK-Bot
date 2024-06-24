import os
from magnum import Magnum
from flask import Flask, jsonify, request
from discord_interactions import verify_key_decorator
from asgiref.wsgi import WsgiToAsgi


DISCORD_PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")
app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
handler = Magnum(asgi_app)



@app.route('/', methods=['POST'])
async def interactions():
    print(f"Received request: {request.json}")
    raw_request = request.json
    return interact(raw_request)

@verify_key_decorator(DISCORD_PUBLIC_KEY)
def interact(raw_request):
    if raw_request["type"] == 1: # Discord pinging the bot to check if it is alive
        response_content = {
            "type": 1
        }
    else:
        # Preparing incoming data for commands
        data = raw_request["data"]
        command_name = data["name"]

        # Checking which command, and executing the one that matches
        if command_name == "echo":
            original_response = data["options"][0]["value"]
            response_content = f"Echoing: {original_response}"

        elif command_name == "statuscheck":
            response_content = "The bot is currently online and functioning properly."

        elif command_name == "shitpost":
            response_content = "temp"
        
        # Building the response json object
        response_data = {   
            "type": 4,
            "data": {
                "content": response_content
            }
        }

        return jsonify(response_data)