from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/drive.metadata']


creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)

results = service.files().list(
        pageSize=20, fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])

curr_year = '2021'

for item in items:
    if item['name'] == curr_year:
        results = service.files().list(q="'{}' in parents".format(item['id']),
        spaces='drive',
        pageSize=20, fields="nextPageToken, files(id, name)").execute()
        break

items = results.get('files', [])

# putting 1st Jan 2021 date to starting balance of annual budget
values = None

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

if not items:
    print('No files found.')
else:
    for item in items:
        if item['name'] == 'Jan ' + curr_year:
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=item['id'],
            range='Summary!L8').execute()
            values = result.get('values', [])
            break

print(values)

test = next((elem for elem in items if elem['name'] == 'test'), None)
sheet.values().update(spreadsheetId=test['id'], range='Setup!C13', valueInputOption='USER_ENTERED', body={"values":values}).execute()


# All Jan total Expenses and Income in test Annual budget template

# Expenses
jan = next((elem for elem in items if elem['name'] == 'Jan ' + curr_year), None)
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=item['id'],
range='Summary!E28:E36').execute()
values = result.get('values', [])

print(values)

values_with_commas =  []
for val in values:
    values_with_commas.append(val)
    values_with_commas.append([''])

values_with_commas.pop()

print(values_with_commas)


test = next((elem for elem in items if elem['name'] == 'test'), None)
sheet.values().update(spreadsheetId=test['id'], range='Expenses!D5', 
                      valueInputOption='USER_ENTERED', body={"values":values_with_commas}).execute()

# Incomes
result = sheet.values().get(spreadsheetId=item['id'],
range='Summary!K28:K29').execute()
values = result.get('values', [])

print(values)


sheet.values().update(spreadsheetId=test['id'], range='Income!D4', 
                      valueInputOption='USER_ENTERED', body={"values":values}).execute()


# get Transaction details and create entry or Sheet accordingly

import datetime

x = datetime.datetime(2021, 5, 17)
print(x.date())

month_mapping = {
    1: 'Jan',
    2: 'Feb',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'Aug',
    9: 'Sept',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}

print(str(month_mapping[x.date().month]) + ' ' + str(x.date().year))

test = next((elem for elem in items if elem['name'] == str(month_mapping[x.date().month]) + ' ' + str(x.date().year)), None)
print(test)

if test is None:
    spreadsheet = {
    'properties': {
        'title': str(month_mapping[x.date().month]) + ' ' + str(x.date().year)
    }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                        fields='spreadsheetId').execute()
    print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))
else:
    test = next((elem for elem in items if elem['name'] == 'test'), None)
    print(test)
    sheet.values().update(spreadsheetId=test['id'], range='Expenses!D22', 
    valueInputOption='USER_ENTERED', body={"values":[[str(x.date())]]}).execute()

