from flask import Flask, request, redirect
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

app = Flask(__name__)

# Load credentials from Render environment variable
creds_dict = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

# Replace this with your actual Google Sheets ID
SPREADSHEET_ID = '1Y_g4BLsmpKFuy0FO2toO1azlujLpumWwOR7KItLjP0I' # Your Google Sheet ID
SHEET_RANGE = 'Sheet1!A:D'  # Adjust based on your Google Sheet layout

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
    print(f"Name: {name}")
    print(f"Course: {course}")
    print(f"Amount: {amount}")
    print(f"Guest: {guest}")

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
        print(f"Google Sheets API Response: {result}")

        return f"<h2>Thank you, {name}! Your response has been recorded in the Google Sheet.</h2>"

    except Exception as e:
        # Log any exceptions or errors
        print(f"Error occurred: {e}")
        return f"<h2>There was an issue recording your response. Please try again later.</h2>"
