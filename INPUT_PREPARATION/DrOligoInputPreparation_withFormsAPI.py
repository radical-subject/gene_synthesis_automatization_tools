#!/usr/bin/env python
#
# File: DrOligoInputPreparation_withFormsAPI.py
# Author: Oleg Fedorov, Kamil Zaynullin
#
# Copyright (C) 2023 Group of automated synthesis
#
# This file is part of gene synthesis automatization pipeline implemented in SBM.

from __future__ import print_function

import argparse
import io
import os
import sys
from warnings import catch_warnings

########################
## GOOGLE API IMPORTS ##
########################
from apiclient import discovery
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import client, file, tools

################################
## ADD COMMAND LINE ARGUMENTS ##
################################
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", required=True)
args = parser.parse_args()
print(f"Hi {args.name} , Welcome ")

ScriptName = os.path.basename(sys.argv[0])
Options = {}
OptionsInfo = {}

#################
## GOOGLE AUTH ##
#################
SCOPES = "https://www.googleapis.com/auth/drive"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"


if os.path.exists("C:\\Users\\fedorov_ov\\Desktop\\token.json"):
    creds = Credentials.from_authorized_user_file(
        "C:\\Users\\fedorov_ov\\Desktop\\token.json", SCOPES
    )
else:
    store = file.Storage("token.json")
    creds = None
    if not creds:
        flow = client.flow_from_clientsecrets("credentials.json", SCOPES)
        creds = tools.run_flow(flow, store)


##################
## GOOGLE FORMS ##
##################
service = discovery.build(
    "forms",
    "v1",
    http=creds.authorize(Http()),
    discoveryServiceUrl=DISCOVERY_DOC,
    static_discovery=False,
)

form_id = "1bVGyD-pz5w3BXM48yHWnhEDVnYNVgzRrF3ysvjAbqHQ"
result = service.forms().responses().list(formId=form_id).execute()
file_list = [
    response["answers"]["778e4a4f"]["fileUploadAnswers"]["answers"]
    for response in result["responses"]
]
print(file_list)


####################################################
# downloading from Google Disk and writing to file #
####################################################
def download_request_file(fileID, filename):
    try:
        service = discovery.build("drive", "v3", credentials=creds)

        file_id = fileID

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}.")

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(file.getbuffer())

    return print(file.getvalue())


for file in file_list:
    download_request_file(file[0]["fileId"], file[0]["fileName"])


##########
## main ##
##########
def main() -> None:
    text = " ".join(sys.argv[1:])


if __name__ == "__main__":
    main()
