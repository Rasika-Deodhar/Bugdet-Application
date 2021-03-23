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

# if not items:
#     print('No files found.')
# else:
#     print("Files inside {0} :".format(curr_year))
#     for item in items:
#         print(u'{0} ({1})'.format(item['name'], item['id']))


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

jan = next((elem for elem in items if elem['name'] == 'Jan ' + curr_year), None)
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=item['id'],
range='Summary!E28:E36').execute()
values = result.get('values', [])

print(values)

# [ values.insert(i, '') if i%2 else values[i] for i in range(0,len(values))]


# test = next((elem for elem in items if elem['name'] == 'test'), None)
# sheet.values().update(spreadsheetId=test['id'], range='Expenses!D5', valueInputOption='USER_ENTERED', body={"values":values[0][0]}).execute()
# sheet.values().update(spreadsheetId=test['id'], range='Expenses!D5', valueInputOption='USER_ENTERED', body={"values":values[0][0]}).execute()

values_with_commas =  []
for val in values:
    values_with_commas.append(val)
    values_with_commas.append('')

values_with_commas.pop()

print(values_with_commas)

# result = [value if index%2!=0 else "" for index, value in enumerate(values)]
# print(result)

# for x in range(5):
#     for y in range(5):


# [x for x in range(5) for y in range(5)]
    


# print(values)