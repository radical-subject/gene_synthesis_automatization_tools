#!/usr/bin/env python
# coding: utf-8

# In[26]:


# # ### basic required packages ###
# get_ipython().system('pip install numpy')
# get_ipython().system('pip install pyopenms')
# get_ipython().system('pip install biopython')
# get_ipython().system('pip install openpyxl')


# # In[27]:


# # ### GOOGLE AUTH ###
# get_ipython().system('pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib')
# get_ipython().system('pip3 install --upgrade oauth2client')
# get_ipython().system('pip3 install --upgrade oauth2client')


# In[34]:


#######################
###  Запускать тут ####
#######################

import glob
import logging
import os
import shutil
import sys
import unicodedata

import pandas as pd

# # CHANGE THIS
# EXPERIMENT_NAME = "KJE0006"

# Список для хранения обработанных DataFrame из каждого файла

sys.path.append("..")


def xlsx_paths(EXPERIMENT_NAME):
    # specifying the path to csv files
    filepath = os.path.join("..", "INPUT_PREPARATION", "requests", f"{EXPERIMENT_NAME}")

    # csv files in the path
    file_paths = glob.glob(filepath + "/*.xlsx")
    return file_paths


def csv_paths(EXPERIMENT_NAME):
    # specifying the path to csv files
    filepath = os.path.join("..", "INPUT_PREPARATION", "requests", f"{EXPERIMENT_NAME}")

    # csv files in the path
    file_paths = glob.glob(filepath + "/*.csv")
    return file_paths


def is_valid_sequence(seq):
    if pd.isna(seq):
        return False
    valid_chars = set("ATGCUYRSWKMBDHVN.-")
    return all(c in valid_chars for c in str(seq))


def process_excel_files(xlsx_paths, dfs_list):
    for file_path in xlsx_paths:
        # Чтение файла Excel
        df = pd.read_excel(file_path, header=None)

        if len(df.columns) == 1:
            df = df[0].str.split(",", expand=True)

        if len(df.columns) < 4:
            return print("ERROR IN INPUT FILE")
        df.dropna(how="any", inplace=True)

        # df curation
        for column in df.columns:
            df[column] = df[column].apply(
                lambda x: unicodedata.normalize("NFC", str(x))
            )
        #  pandas' Series.str.strip() method
        df = df.apply(lambda x: x.str.strip())

        df[0] = df[0].apply(lambda x: x.upper())

        # Получение имени самого левого столбца
        leftmost_column = df.columns[0]
        print(file_path, len(df))
        # Фильтрация строк согласно заданным условиям
        df = df[df[leftmost_column].apply(is_valid_sequence)]

        print(file_path, len(df))
        # Добавление обработанного DataFrame в список
        dfs_list.append(df)

        if dfs_list != None:
            pass
        else:
            dfs_list = []
            print([])

    return dfs_list


def process_csv_files(csv_paths, dfs_list):
    for file_path in csv_paths:
        # Чтение файла Excel
        df = pd.read_csv(file_path, header=None, sep=",")
        print(df)
        df.dropna(how="any", inplace=True)
        if len(df.columns) == 1:
            df = df[0].str.split(",", expand=True)

        if len(df.columns) < 4:
            return print("ERROR IN INPUT FILE")

        # df curation
        for column in df.columns:
            df[column] = df[column].apply(
                lambda x: unicodedata.normalize("NFC", str(x))
            )
        #  pandas' Series.str.strip() method
        df = df.apply(lambda x: x.str.strip())

        df[0] = df[0].apply(lambda x: x.upper())

        # Получение имени самого левого столбца
        leftmost_column = df.columns[0]
        print(file_path, len(df))
        # Фильтрация строк согласно заданным условиям
        df = df[df[leftmost_column].apply(is_valid_sequence)]

        # Добавление обработанного DataFrame в список
        dfs_list.append(df)

        if dfs_list != None:
            pass
        else:
            dfs_list = []
            print([])

    return dfs_list


def process_files(EXPERIMENT_NAME):
    dfs_list = []
    dfs_list = process_excel_files(xlsx_paths(EXPERIMENT_NAME), dfs_list)
    if dfs_list != None:
        print(dfs_list)
    else:
        dfs_list = []
    dfs_list = process_csv_files(csv_paths(EXPERIMENT_NAME), dfs_list)
    return dfs_list


def export_to_input_files(dfs_list, EXPERIMENT_NAME):
    # Конкатенация всех обработанных DataFrame по строкам
    final_df = None
    final_df = pd.concat(dfs_list, axis=0, join="outer", ignore_index=True)

    if len(final_df) > 384 and len(final_df) <= 768:
        df_A = final_df[:384]
        df_B = final_df[384:]

        filepath = os.path.join(
            "..",
            "INPUT_PREPARATION",
            "result_input",
            f"{EXPERIMENT_NAME}",
            f"{EXPERIMENT_NAME}_concatenated_file",
        )
        # Сохранение результата в новый файл CSV
        df_A.to_csv(
            filepath + "_plate_A.csv",
            index=False,
            sep=",",
            header=None,
            encoding="UTF-8",
        )

        # Сохранение результата в новый файл Excel
        df_A.to_excel(filepath + "_plate_A.xlsx", index=False, header=None)

        # Сохранение результата в новый файл CSV
        df_B.to_csv(
            filepath + "_plate_B.csv",
            index=False,
            sep=",",
            header=None,
            encoding="UTF-8",
        )
        # Сохранение результата в новый файл Excel
        df_B.to_excel(filepath + "_plate_B.xlsx", index=False, header=None)

    elif len(final_df) > 768:
        print("error, too much oligos HALP")

    else:
        # Сохранение результата в новый файл CSV
        final_df.to_csv(
            filepath + ".csv",
            index=False,
            sep=",",
            header=None,
            encoding="UTF-8",
        )

        # Сохранение результата в новый файл Excel
        final_df.to_excel(filepath + ".xlsx", index=False, header=None)


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
    dir = os.path.join("..", "INPUT_PREPARATION", "requests", EXPERIMENT_NAME)
    if not os.path.exists(dir):
        os.makedirs(dir)

    dir = os.path.join("..", "INPUT_PREPARATION", "result_input", EXPERIMENT_NAME)
    if not os.path.exists(dir):
        os.makedirs(dir)


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
def download_request_file(fileID, filename, creds, EXPERIMENT_NAME):
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
    filepath = os.path.join(
        "..", "INPUT_PREPARATION", "requests", EXPERIMENT_NAME, filename
    )
    with open(filepath, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(file.getbuffer())

    return print(file.getvalue())


def download_all_files(creds, EXPERIMENT_NAME):
    for file in retrive_forms_data(creds):
        download_request_file(
            file[0]["fileId"], file[0]["fileName"], creds, EXPERIMENT_NAME
        )


##########
## main ##
##########
def main(EXPERIMENT_NAME) -> None:
    # EXPERIMENT_NAME = input("enter EXPERIMENT_NAME:")
    creating_dirs(EXPERIMENT_NAME)
    # retrive_forms_data()
    creds = google_auth()
    download_all_files(creds, EXPERIMENT_NAME)
    print("downloads finished")
    return


# In[38]:


#####################################
#### EXPORTING EMAILS FROM FORMS ####
#####################################

import json
import re


def get_emails_data():
    creds = google_auth()

    service = discovery.build(
        "forms",
        "v1",
        http=creds.authorize(Http()),
        discoveryServiceUrl=DISCOVERY_DOC,
        static_discovery=False,
    )

    form_id = "1bVGyD-pz5w3BXM48yHWnhEDVnYNVgzRrF3ysvjAbqHQ"
    result = service.forms().responses().list(formId=form_id).execute()
    #     print(json.dumps(result, indent=2))

    return result


def remove_duplicate_emails(response_str):
    response_dict = json.loads(
        response_str
    )  # Преобразование JSON-строки в Python-объект
    email_set = set()

    for response in response_dict["responses"]:
        email = response.get("respondentEmail", None)
        if email:
            email_set.add(email)

        email_set.add(
            response["answers"]["4d5a72c8"]["textAnswers"]["answers"][0]["value"]
        )

    email_list = list(email_set)

    #     print(email_list)
    return email_list


regex = re.compile(
    r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9\-]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
)


def emailValid(unique_emails):
    iterable = unique_emails.copy()
    for item in iterable:
        #         print(item)
        if re.fullmatch(regex, item):
            pass
            print(item, "The given mail is valid")
        else:
            unique_emails.remove(item)
            print(item, "The given mail is invalid")
    #     print(len(iterable))
    return unique_emails


def create_file_with_emails(EXPERIMENT_NAME):
    # Использования функции
    result = get_emails_data()
    response_str = json.dumps(result, indent=2)
    unique_emails = remove_duplicate_emails(response_str)
    #     print(unique_emails)
    unique_emails = emailValid(unique_emails)
    #     print(unique_emails)

    filepath = os.path.join(
        "..",
        "INPUT_PREPARATION",
        "result_input",
        EXPERIMENT_NAME,
        f"{EXPERIMENT_NAME}_customer_emails.txt",
    )
    # write to file
    with open(filepath, "w") as f:
        for email in unique_emails:
            f.write(f"{email}\n")


# In[39]:


def combined_pipeline(EXPERIMENT_NAME):
    print(os.getcwd())
    logger = logging.getLogger("uvicorn")
    logger.info(
        "KASJCBKJVBEASKJCVGHQKAVHCKJASBCKJHEQBKJBC\nLKSADMVLKDMVLKSMDVLKMSLDMVLSKDMVLKSMDLVKMSDLMV"
    )

    main(EXPERIMENT_NAME)
    print(EXPERIMENT_NAME)
    dfs_list = process_files(EXPERIMENT_NAME)
    export_to_input_files(dfs_list, EXPERIMENT_NAME)
    create_file_with_emails(EXPERIMENT_NAME)

    dirpath = os.path.join(
        "..", "INPUT_PREPARATION", "result_input", f"{EXPERIMENT_NAME}"
    )

    target_dirpath = os.path.join("/", "SEQUENCES")
    shutil.copytree(dirpath, target_dirpath, dirs_exist_ok=True)


# In[ ]:


# !jupyter labextension install @jupyterlab/dataregistry-extension


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:
