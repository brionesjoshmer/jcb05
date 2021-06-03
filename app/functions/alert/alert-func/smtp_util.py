import logging
import os
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient

def send_email(event: dict):
    """
    Send an email from SMTP server.
    Mail sender, SMTP host, port number is retrieved from Key Vault container.

    :param event:       event data sent from Event hubs
    :type event:        dict
    """
    logging.info("------ send_email --------")

    credential = ManagedIdentityCredential()

    # KV
    key_vault_name = os.environ["KEY_VAULT_NAME"]
    logging.info("key_vault_name: %s", key_vault_name)
    kv_uri = f"https://{key_vault_name}.vault.azure.net"

    secret_client = SecretClient(
        vault_url=kv_uri,
        credential=credential
    )


    # Mail sender and receiver
    to_email = get_recipient_list()
    from_email = secret_client.get_secret("FROM-EMAIL").value

    if not to_email:
        logging.info("sender is none")
        return

    # Set subject and text of the mail
    msg = MIMEMultipart()
    subject, message_text = make_message_text_and_subject(event)
    msg['Subject'] = subject
    msg.attach(MIMEText(message_text))
    msg['From'] = from_email
    msg['To'] = ', '.join(to_email)

    # Connection to SMTP server
    smtp_host = secret_client.get_secret("SMTP-HOST").value
    smtp_port = int(secret_client.get_secret("SMTP-PORT").value)
    login_user = secret_client.get_secret("LOGIN-USER").value
    login_key = secret_client.get_secret("LOGIN-KEY").value
    server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
    server.ehlo()
    server.starttls()
    server.login(login_user, login_key)
    server.sendmail(from_email, to_email, msg.as_string())
    server.close()

    # logging
    logging.info("***** sent message *****")


def get_recipient_list():
    """
    Create sender list from the event

    :param event:       event data from Event Hubs
    :type event:        dict
    :return:            list of recipients
    :rtype:             [str]
    """

    logging.info("------ get_recipient_list --------")

    recipient_list = []
    user_data = get_json_user_data_from_storage()
    for data in user_data:
        recipient_list.append(data["email"])

    logging.info("****** recipient list ******")
    logging.info(recipient_list)

    return recipient_list


def get_json_user_data_from_storage():
    """
    Get JSON user data from Blob Storage

    :return: user data
    :rtype: dict
    """
    logging.info("------ get_json_user_data_from_storage --------")

    credential = ManagedIdentityCredential()

    # blob
    storage_name = os.environ["STORAGE_NAME"]

    blob_uri = f"https://{storage_name}.blob.core.windows.net"
    blob_service_client = BlobServiceClient(
        account_url=blob_uri,
        credential=credential
    )
    container_name = os.environ["CONTAINER_NAME"]
    container_client = blob_service_client.get_container_client(container_name)
    blob_name = "notification_user_data.json"
    blob_client = container_client.get_blob_client(blob_name)
    blob = blob_client.download_blob().readall()
    users_data = json.loads(blob)

    logging.info("**** users_data ****")
    logging.info(users_data)
    return users_data


def make_message_text_and_subject(event: dict):
    """
    Create a subject and text of the mail from event

    :param event:       event data from Event Hubs
    :type event:        dict
    :return:            subject, text
    :rtype:             str, str
    """

    logging.info("------ make_message_text_and_subject --------")

    subject = "Abnormal status is detected."
    message_text = (
        "Abnormal status is detected. \n\n" +
        "【Temperature】\n" +
        str(event["temperature"]) + "\n" +
        "【Humidity】\n" +
        str(event["humidity"])
    )

    logging.info("**** subject ****")
    logging.info(subject)

    logging.info("**** message_text ****")
    logging.info(message_text)

    return subject, message_text

