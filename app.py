import os
import json
import logging
from flask import Flask, request, redirect
from google.auth.transport.requests import Request
from google.oauth2 import service_account  # Import service_account properly
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load credentials from Render environment variable
try:
    creds_dict = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    logger.info("Google Sheets API credentials loaded successfully.")
except KeyError as e:
    logger.error(f"Error: Environment variable 'GOOGLE_CREDENTIALS_JSON' not found. Make sure it's set correctly. {e}")
    raise
except json.JSONDecodeError as e:
    logger.error(f"Error decoding credentials JSON: {e}")
    raise

# Replace this with your actual Google Sheets ID
SPREADSHEET_ID = '1Y_g4BLsmpKFuy0FO2toO1azlujLpumWwOR7KItLjP0I'  # Your Google Sheet ID
SHEET_RANGE = 'Sheet1!A:D'  # Adjust based on your Google Sheet layout

# Initialize Flask application
app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Get form data
    name = request.form['name']
    course = request.form['course']
    amount = request.form['amount']
    guest = request.form['guest']

    # Step 4: Log the form data to check what’s being received
    logger.info(f"Received form data - Name: {name}, Course: {course}, Amount: {amount}, Guest: {guest}")

    try:
        # Step 5: Send data to Google Sheet
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()

        # Append the data to the Google Sheet
        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=SHEET_RANGE,
            valueInputOption='RAW',
            body={'values': [[name, course, amount, guest]]}
        ).execute()

        # Log the result returned by the Google Sheets API
        logger.info(f"Google Sheets API Response: {result}")

        return f"<h2>Thank you, {name}! Your response has been recorded in the Google Sheet.</h2>"

    except HttpError as err:
        logger.error(f"Google Sheets API error: {err}")
        return f"<h2>There was an issue with Google Sheets. Please try again later.</h2>"
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return f"<h2>There was an issue recording your response. Please try again later.</h2>"

# Run the Flask app
if __name__ == '__main__':
    logger.info("Starting Flask app...")
    app.run(host='0.0.0.0', port=10000)

