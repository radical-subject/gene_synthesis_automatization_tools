#!/usr/bin/env python
#
# File: DrOligoInputPreparation_withFormsAPI.py
# Author: Oleg Fedorov, Kamil Zaynullin
#
# Copyright (C) 2023 Group of automated synthesis
#
# This file is part of gene synthesis automatization pipeline implemented in SBM.

from __future__ import print_function

import io
import os

########################
## GOOGLE API IMPORTS ##
########################
from apiclient import discovery
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import client, file, tools

SCOPES = "https://www.googleapis.com/auth/drive"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"


def creating_dirs(EXPERIMENT_NAME):
    #################
    ## CREATE DIR  ##
    #################
    cwd = os.getcwd()
    dir = os.path.join(cwd, "requests", EXPERIMENT_NAME)
    if not os.path.exists(dir):
        os.mkdir(dir)


def google_auth():
    #################
    ## GOOGLE AUTH ##
    #################

    """
    caution! it appeares to be deprecated!!!

    """
    cwd = os.getcwd()
    token_file = os.path.join(cwd, "token.json")
    if os.path.exists(token_file):
        print("auth token already exists")
        store = file.Storage(token_file)
        creds = store.get()
    else:
        store = file.Storage("token.json")
        creds = None
        if not creds:
            flow = client.flow_from_clientsecrets("credentials.json", SCOPES)

            creds = tools.run_flow(flow, store)
    return creds


def retrive_forms_data(creds):
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
    return file_list


####################################################
# downloading from Google Disk and writing to file #
####################################################
def download_request_file(fileID, filename, creds):
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
    filepath = os.path.join(os.getcwd(), "requests", EXPERIMENT_NAME, filename)
    with open(filepath, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(file.getbuffer())

    return print(file.getvalue())


def download_all_files(creds):
    for file in retrive_forms_data(creds):
        download_request_file(file[0]["fileId"], file[0]["fileName"], creds)


##########
## main ##
##########
def main() -> None:
    creating_dirs(EXPERIMENT_NAME)
    # retrive_forms_data()
    creds = google_auth()
    download_all_files(creds)


if __name__ == "__main__":
    EXPERIMENT_NAME = input("enter EXPERIMENT_NAME:")
    main()
    print("done")
    print("press ENTER to exit")
    input()
