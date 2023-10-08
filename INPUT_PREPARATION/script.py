from __future__ import print_function

import os, io
from warnings import catch_warnings
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = "https://www.googleapis.com/auth/drive"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

# if os.path.exists('C:\\Users\\fedorov_ov\\Desktop\\token.json'):
#     creds = Credentials.from_authorized_user_file('C:\\Users\\fedorov_ov\\Desktop\\token.json', SCOPES)
store = file.Storage('token.json')
creds = None
if not creds:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

service = discovery.build('forms', 'v1', http=creds.authorize(Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False) # 

# Prints the title of the sample form:
form_id = '1bVGyD-pz5w3BXM48yHWnhEDVnYNVgzRrF3ysvjAbqHQ'
result = service.forms().responses().list(formId=form_id).execute()
file_list = [response["answers"]["778e4a4f"]["fileUploadAnswers"]["answers"] for response in result["responses"]]
print(file_list)



###################################
# downloading and writing to file #
###################################
def download_request_file(fileID, filename):
    try:
        service = discovery.build('drive', 'v3', credentials=creds)

        file_id = fileID

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')


    except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(file.getbuffer())

    return print(file.getvalue())


for file in file_list:
    download_request_file(file[0]["fileId"], file[0]["fileName"])