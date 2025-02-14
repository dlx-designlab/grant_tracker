# Get Emails From cloudmailin.net
# Run this script to start the server
from openai import OpenAI
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

openai_api_key = os.getenv('OPENAI_API_KEY')
# print(f'API Key: {api_key}')
client = OpenAI(api_key=openai_api_key)
messages = [
            {"role": "developer", 
             "content": 
             "Make a summary of this email which includes details of an acedemic grant." 
             "The email is in japanese. Summarize it in english." 
             "Provide the summary in the foillowing structured format:"
             "Titlle: A Short catchy Title,"
             "Content: max 300 chracters description,"
             "Eligibility: the eligibility criteria for the grant,"
             "Categoty: one of the following categories: Medical, Materials, Energy, Environment, Social Sciences, Humanities, Engineering, Computer Science, Mathematics, Physics, Chemistry, Biology, Other."
             "Amount: the grant ammount, preferably a number in JPY, "
             "Internal Deadline: date of internal submission deadline."
             "Actual Deadline: the deadline for the grant application submission to the prividing agency."
             "Other Deadlines: any other deadlines mentioned in the email."
             "Comments: any additional comments or information."
             "URL: the URL of the grant announcement."
             "Contact: the contact email for the grant."
            },
        ]


@app.route('/email', methods=['POST'])
def receive_email():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    # Extract subject and body from the JSON payload
    # Json Structure reference: https://docs.cloudmailin.com/http_post_formats/json_normalized/
    subject = data.get('headers', {}).get('subject', 'No Subject')
    body = data.get('plain', 'No Body')

    # Print the subject and body
    print(f'Subject: {subject}')
    print(f'Body: {body}')

    user_prompt = f"Subject: {subject}\nBody: {body}"
    messages.append({"role": "user", "content": user_prompt})
    response = client.chat.completions.create(
            model = "gpt-4o-mini",
            store = True,
            messages = messages
        )
    print("##############################")
    print(f"Email Summary: \n {response.choices[0].message.content}")
    

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)