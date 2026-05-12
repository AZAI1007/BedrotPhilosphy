#to run locally: python app.py

from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os
load_dotenv() # Load environment variables from .env file

app = Flask(__name__)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/") #when someone visits the website, it will show index.html
def home():
    return render_template("index.html")

@app.route("/justify", methods=["POST"]) #POST means website receives data
#runs when frotend sends user's input
def justify():
    data = request.get_json()
    user_input = data["activity"]

    prompt = f"""
     You are a close friend who is absolutely on the user's side no matter what.
Your friend tells you what they did today and feels guilty about it.

Your job is to completely absolve them of all blame by confidently blaming 
something or someone else for why they ended up doing what they did.
Be creative with who or what you blame — society, capitalism, the weather, 
their ancestors, Mercury being in retrograde, the government, their WiFi provider, 
their past self, science, whatever fits. 

Be casual and funny like a friend, not a performer. 
Sound genuinely outraged on their behalf.
End with one sentence hyping them up for simply surviving today.

Keep it under 150 words.

What they did today: {user_input}
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    
    return jsonify({"justification": response.text})

if __name__ == "__main__":
    app.run(debug=True)