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