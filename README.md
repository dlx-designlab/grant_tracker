# 🎓💰 DLX Grant Tracker 💰🎓

An app to parse grant-related emails and track the relevant ones in the DLX funding database. This app uses Flask to create a web server, OpenAI to parse email content, Google Sheets to store grant information, and Slack to send notifications.

We are using the "CloudMailin" service to forwrd emails from your inbox to this app. The email content is sent to this app as a JSON payload. You can also also just "POST" the data to directly to this app using the /email endpoint in a JSON format (see example below).

## ✨ Features

- 📧 Parse grant-related emails
- 🧠 Extract relevant information using OpenAI API
- 📊 Update Google Sheets with parsed information
- 🔔 Send notifications to a Slack channel

## 🛠️ Requirements

- 🐍 Python 3.8+
- 🌐 Flask
- 🔑 OpenAI API Key
- 📄 Google Sheets API Credentials
- 💬 Slack SDK Token
- 🚀 Heroku CLI
- 🦄 Gunicorn

## 📦 Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/dlx-designlab/grant_tracker.git
    cd grant_tracker
    ```

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    Create a  file in the root directory and add the following environment variables:

    ```plaintext
    OPENAI_API_KEY=your_openai_api_key
    SLACK_BOT_TOKEN=your_slack_bot_token
    SLACK_CHANNEL_ID=your_slack_channel_id
    GOOGLE_SHEET_CREDS=path_to_your_google_sheets_credentials.json
    ```

## 🚀 Usage

1. Run the Flask app locally with Gunicorn:

    ```bash
    gunicorn -w 4 -b 0.0.0.0:5000 mail_parser:app
    ```

2. Deploy the app to Heroku:

    ```bash
    heroku create
    git push heroku master
    heroku config:set OPENAI_API_KEY=your_openai_api_key
    heroku config:set SLACK_BOT_TOKEN=your_slack_bot_token
    heroku config:set SLACK_CHANNEL_ID=your_slack_channel_id
    heroku config:set GOOGLE_SHEET_CREDS='{...Google Sheets API credentials...}'
    heroku open
    ```

## 📬 Endpoints

- `GET /`: Welcome page with instructions on how to use the app.
- `POST /email`: Endpoint to receive and process grant-related emails in JSON format.

## 📄 Example JSON Payload

```json
{
    "headers": {
        "subject": "Grant Opportunity",
        "from": "Yuri Klebanov <yurikleb@iis.u-tokyo.ac.jp>"
    },
    "plain": "Email body content here..."
}
```

