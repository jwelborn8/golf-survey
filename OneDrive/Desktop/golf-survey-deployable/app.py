from flask import Flask, request, send_from_directory
import openpyxl
import os

app = Flask(__name__)
EXCEL_FILE = 'responses.xlsx'

# Create Excel workbook if not exists
if not os.path.exists(EXCEL_FILE):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Survey Responses"
    ws.append(["Name", "Closest Golf Course", "Amount Willing to Pay", "Bringing Guest"])
    wb.save(EXCEL_FILE)

@app.route('/form.html')
def serve_form():
    return send_from_directory('.', 'form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    course = request.form.get('course')
    amount = request.form.get('amount')
    guest = request.form.get('guest')

    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active
    ws.append([name, course, amount, guest])
    wb.save(EXCEL_FILE)

    return f"<h2>Thank you, {name}! Your response has been recorded.</h2>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
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
SPREADSHEET_ID = '1Y_g4BLsmpKFuy0FO2toO1azlujLpumWwOR7KItLjP0I '  # Example: '1aBcD3FgHIjKlMnOPqrS12345xyz6789'
SHEET_RANGE = 'Sheet1!A:D'  # Adjust based on your Google Sheet layout

@app.route('/')
def home():
    return redirect('/form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
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

    return "Thanks for submitting your response!"

