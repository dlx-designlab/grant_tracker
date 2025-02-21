# Get Emails From cloudmailin.net
# Run this script to start the server
from openai import OpenAI
from pydantic import BaseModel
import os
import json
import re
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from google_sheets_updater import GoogleSheetsUpdater
from slack_updater import SlackUpdater

# Load environment variables
load_dotenv()

google_sheets_updater = GoogleSheetsUpdater()
slack_updater = SlackUpdater()

app = Flask(__name__)

class GrantEmailData(BaseModel):
    Title: str
    Code: str    
    Content: str
    Amount: int
    Internal_Deadline: str
    Official_Deadline: str
    Other_Deadlines: str
    Category: str
    Eligibility: str
    Comments: str
    URL: str
    Contact: str
    # participants: list[str]


openai_api_key = os.getenv('OPENAI_API_KEY')
# print(f'API Key: {api_key}')
client = OpenAI(api_key=openai_api_key)
messages = [
            {"role": "developer", 
             "content": 
             "Make a summary of this email which includes details of an acedemic grant." 
             "The email is in japanese. Summarize it in english." 
             "Provide the summary in the foillowing structured format:"
             "Title: A Short catchy Title,"
             "Code: the public announcement identification code - 公募識別コード,"
             "Content: max 300 chracters description,"
             "Eligibility: the eligibility criteria for the grant,"
             "Categoty: one of the following categories: Medical, Materials, Energy, Environment, Social Sciences, Humanities, Engineering, Computer Science, Mathematics, Physics, Chemistry, Biology, Other."
             "Amount: the grant ammount, preferably a number in JPY, "
             "Internal Deadline: date of internal submission deadline."
             "Official Deadline: the deadline for the grant application submission to the prividing agency."
             "Other Deadlines: any other deadlines mentioned in the email."
             "Comments: any additional comments or information."
             "URL: the URL of the grant announcement."
             "Contact: the contact email for the grant."
            },
        ]

@app.route('/')
def index():
    return """
    <h1>Welcome to the DLX Grant Tracker App</h1>
    <p>This app helps you track academic grants by parsing emails and updating Google Sheets and Slack.</p>
    <p> We are using the "CloudMailin" service to receive emails and OpenAI to parse them.</p>
    <p> You can also also just "POST" the data to directly to this app using the /email endpoint in a JSON format.</p>
    <p>Example JSON format:</p>
    <pre>
    {
        "headers": {
            "subject": "Grant Opportunity",
            "from": "Yuri Klebanov <yurikleb@iis.u-tokyo.ac.jp>"
        },
        "plain": "Email body and grant details content here..."
    }
    </pre>
    <p>Make sure to include the subject and body of the email in the JSON payload.</p>
    <p>fore more information, visit <a href="https://docs.cloudmailin.com/http_post_formats/json_normalized/">CloudMailin JSON Payload</a>documentation page</p>
    """


@app.route('/email', methods=['POST'])
def receive_email():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    # Extract subject and body from the JSON payload
    # Json Structure reference: https://docs.cloudmailin.com/http_post_formats/json_normalized/
    subject = data.get('headers', {}).get('subject', 'No_Subject')
    body = data.get('plain', 'No_Body')
    
    # Extract the name part from the sender string
    # sender = re.sub(r'\s*<[^>]+>', '', data.get('headers', {}).get('from', 'No Sender'))
    sender = data.get('headers', {}).get('from', 'No_Sender').split(" ")[0].strip()

    # Print the subject and body
    print(f'Subject: {subject}')
    print(f'Body: {body}')

    # Send the email to OpenAI for parsing and ask for a structured JSON response
    # https://platform.openai.com/docs/guides/structured-outputs
    user_prompt = f"Subject: {subject}\nBody: {body}"
    messages.append({"role": "user", "content": user_prompt})
    response = client.beta.chat.completions.parse(
            model = "gpt-4o-mini",
            store = True,
            messages = messages,
            response_format = GrantEmailData,
        )
    # print("##############################")
    # print(f"Email Summary: \n {response.choices[0].message.parsed}")
    
    parsed_message = response.choices[0].message.parsed

    # Print the structured JSON elements
    print("##############################")
    print("Email Summary....")
    print(f"From: {sender}")
    for key, value in parsed_message.model_dump().items():
        print(f"{key}: {value}")
    
    # Send the parsed message to Slack
    print("sending message to slack...")
    slack_message = json.dumps(parsed_message.model_dump(), indent=0).replace("{", "").replace("}", "").replace(",", "\n")
    slack_updater.send_message(
        f"🎓💰 Hey All,\n{sender} just found a grant he would like to share.\n"
        f"Check out the details below:\n```{slack_message}```\n"
        f"☝🏻 I will also update the <https://docs.google.com/spreadsheets/d/18taAPoE91R-0lna41CsCIO-xjD-CcRy90ikaV3EnQl0/edit?usp=sharing|DLX Funding Database> with this information."
    )
    
    # Update google sheet
    print("updating google sheet...")
    google_sheets_updater.append_data_to_column(parsed_message.model_dump().items())

    print("Done!")

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)