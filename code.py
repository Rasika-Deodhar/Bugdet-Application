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
        print('results: ', results)
        break

items = results.get('files', [])

if not items:
    print('No files found.')
else:
    print("Files inside {0} :".format(curr_year))
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))