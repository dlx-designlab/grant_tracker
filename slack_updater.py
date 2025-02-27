# Slack Bot Settings: https://api.slack.com/apps/
import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackUpdater:
    def __init__(self, ):
        SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
        if not SLACK_BOT_TOKEN:
            raise ValueError("SLACK_BOT_TOKEN environment variable not set")
        
        self.CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
        if not self.CHANNEL_ID:
            raise ValueError("SLACK_CHANNEL_ID environment variable not set")
        
        self.client = WebClient(token=SLACK_BOT_TOKEN)

    def send_message(self, message):
        try:
            response = self.client.chat_postMessage(channel=self.CHANNEL_ID, text=message)
            print("Message sent successfully!", response["ts"])  # Response contains the timestamp
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")

# Example usage
if __name__ == "__main__":
    
    # Load environment variables
    load_dotenv()

    MESSAGE = "Hello, Slack! This is a Test 🚀🚀🚀 <https://example.com|link> !!!"
    
    slack_updater = SlackUpdater()
    slack_updater.send_message(MESSAGE)