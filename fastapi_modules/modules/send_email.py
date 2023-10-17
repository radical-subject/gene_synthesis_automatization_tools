# -*- coding: utf-8 -*-

import os
from datetime import datetime
import smtplib

import email.utils
import email.header

from email.message import EmailMessage

EMAIL_ADDRESS = 'oligosynthesis@sysbiomed.ru'
EMAIL_PASSWORD = 'Lv5wAEiVL1ztsCgUuZN4'

def reformat_address(s: str) -> str:
    """
    Функция для форматирования имен адресатов и их почтовых адресов, честно
    позаимствована со Stackoverflow. \n \n
    :param s: строка для форматирования
    :return: отформатированная подходящим образом строка
    """
    # parse email to get user real name and email address
    name, address = email.utils.parseaddr(s)
    # encode the user name use utf-8 to avoid encoding error
    name_encoded = (email.header.Header(name, 'utf-8')).encode()
    # construct the email address again
    return email.utils.formataddr((name_encoded, address))


def send_email():
    # формально вы можете передавать его как вам удобно
    # указать актуальный файл с адресами
    with open("KJE0008_customer_emails-Copy1.txt", "r") as fr:
        recipients_list = fr.read().splitlines()

    # вот тут тоже, можете каждому письму что-то свое придумать, some tables,logos, reports есть в тексте письма
    attachments_list = [
        "attachments/some_tables.tsv",
        "attachments/some_logs.txt",
        "attachments/some_reports.pdf"
    ]

    # прочитаем наш шаблон письма
    # тут очень важно заранее соотнести все переменные,
    # чтобы потом не получить нелепых ошибок имен

    #указать актуальный текст письма

    with open("mail.template", "r", encoding="utf-8") as fr:
        template = fr.read()

    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    oligos_val = "455"
    plate_name = "OFVV322"
    plate_file = "some_tables.tsv"

    type(eval(template))
    msg = EmailMessage()

    msg['Subject'] = 'This is an example mail'  # это тема письма, тоже можно подставить какое-то имя синтеза
    msg['From'] = EMAIL_ADDRESS
    # используем функцию и превращаем все в список адресатов
    # с корректными и точно кодируемыми адресамми
    # это нужно на случай идиотских имен и форматов
    msg['To'] = ', '.join(list(map(reformat_address, recipients_list)))

    # тут текст письма, который скомпилировали ранее
    msg.set_content(eval(template))

    # прикрепляем файлы
    for elem in attachments_list:
        with open(elem, 'rb') as frb:  # главное открывать бинарно файлы, иначе не отправятся
            msg.add_attachment(
                frb.read(),
                maintype='application',
                subtype='octet-stream',
                filename=os.path.split(elem)[1]  # вот тут извлекаем только имя файла, чтобы пути остались у нас
            )

    with smtplib.SMTP_SSL('smtp.mail.ru', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        
    return "ok"
