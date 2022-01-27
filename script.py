import pyodbc 
import requests
from requests.auth import HTTPBasicAuth

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-PV9CJTBH\MSSQLSERVER01;'
                      'Database=WhatsUp;'
                      'Trusted_Connection=yes;')

datas = []
cursor = conn.cursor()
cursor.execute("SELECT TOP (10) * FROM dbo.Device")
result = cursor.fetchall()

index = 1;
for row in result:
    notes = []
    splitted = row[12].split("\r\n\r\n")
    for note in splitted:
        splittedNote = note.split("\r\n")
        if len(splittedNote) > 0:
            notes.append({
                "head": splittedNote[0].strip(),
                "body": splittedNote[1].strip() if len(splittedNote) > 1 else None,
                "additionalNotes": splittedNote[2:len(splittedNote)] if len(splittedNote) > 2 else None
            })

    reqBody = {
        "deviceId": row[0],
        "deviceName": row[1],
        "deviceType": row[2],
        "note": notes,
    }

    requestHeader = { "Content-Type" : "application/json" }
    x = requests.post("https://contoh.es.eu-west-1.aws.found.io:9243/mfdsix2/1",json=reqBody, auth = HTTPBasicAuth('elastic', '3vYdqpIJJb0x0veeb1ezp0n2'), headers=requestHeader)
    print(x.text)
