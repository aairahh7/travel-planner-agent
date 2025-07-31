from flask import Flask, render_template, request, jsonify
import os
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# IBM Watsonx Setup
api_key = os.getenv("IBM_API_KEY")
project_id = os.getenv("IBM_PROJECT_ID")
url = os.getenv("IBM_URL")

authenticator = IAMAuthenticator(api_key)
model = ModelInference(
    model_id="granite-13b-chat",
    credentials={"apikey": api_key, "url": url},
    project_id=project_id,
    authenticator=authenticator
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/plan', methods=['POST'])
def plan_trip():
    user_message = request.json['message']

    prompt = f"""
You are a helpful travel planning assistant. A user says: "{user_message}".
Respond with:
1. Destination
2. Travel Dates
3. Accommodation
4. Activities
"""

    gen_params = {
        GenTextParamsMetaNames.PROMPT: prompt,
        GenTextParamsMetaNames.MAX_NEW_TOKENS: 300,
        GenTextParamsMetaNames.TEMPERATURE: 0.6
    }

    try:
        response = model.generate_text(gen_params)
        reply = response['results'][0]['generated_text']
    except Exception as e:
        reply = f"Error generating response: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)


   
frontend UPI
<!DOCTYPE html>
<html>
<head>
  <title>Travel Planner Agent</title>
  <script src="{{ url_for('static', filename='script.js') }}"></script>
  <style>
    body { font-family: Arial; background: #f4f4f4; padding: 40px; }
    .chatbox { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; }
    #response { white-space: pre-wrap; margin-top: 20px; }
  </style>
</head>
<body>
  <div class="chatbox">
    <h2>Welcome to Travel Planner Agent</h2>
    <p>This agent helps you plan trips by suggesting destinations, creating itineraries, estimating budgets, and even booking accommodations.</p>
    
    <input type="text" id="userInput" placeholder="Plan a trip to Paris..." style="width: 80%;">
    <button onclick="sendMessage()">Send</button>
    
    <div id="response"></div>
  </div>
</body>
</html>











IBM GRANITE(TO ENTER ACCOMADATION)
import os
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Load environment variables
load_dotenv()

# IBM Watsonx credentials
api_key = os.getenv("IBM_API_KEY")
project_id = os.getenv("IBM_PROJECT_ID")
url = os.getenv("IBM_URL")

# Authenticate and set up the Granite model
authenticator = IAMAuthenticator(api_key)
model = ModelInference(
    model_id="granite-13b-chat",
    credentials={"apikey": api_key, "url": url},
    project_id=project_id,
    authenticator=authenticator
)

def get_accommodation(destination):
    prompt = f"""You are a helpful travel assistant.
For the destination "{destination}", recommend one hotel with a short stylish description.
Example:
Destination: Paris
Response: Hotel Le Marais – A stylish hotel located in the heart of the Marais district.

Now for: {destination}"""

    gen_params = {
        GenTextParamsMetaNames.PROMPT: prompt,
        GenTextParamsMetaNames.MAX_NEW_TOKENS: 100,
        GenTextParamsMetaNames.TEMPERATURE: 0.5
    }

    try:
        response = model.generate_text(gen_params)
        reply = response['results'][0]['generated_text'].strip()
        return reply
    except Exception as e:
        return f"Error: {str(e)}"

# Example use
if __name__ == "__main__":
    destination = "Paris"
    result = get_accommodation(destination)
    print("Accommodation Suggestion:", result)



