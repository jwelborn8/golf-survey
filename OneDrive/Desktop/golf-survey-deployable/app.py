ffrom flask import Flask, request, redirect
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
SPREADSHEET_ID = '1Y_g4BLsmpKFuy0FO2toO1azlujLpumWwOR7KItLjP0I'  # Example: '1aBcD3FgHIjKlMnOPqrS12345xyz6789'
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

    # Send data to Google Sheet
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_RANGE,
        valueInputOption='RAW',
        body={'values': [[name, course, amount, guest]]}
    ).execute()

    return f"<h2>Thank you, {name}! Your response has been recorded in the Google Sheet.</h2>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
