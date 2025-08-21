import logging
from .mail_body import Email_body
import requests
from msal import ConfidentialClientApplication
import os
from django.conf import settings

logger = logging.getLogger(__name__)




def get_access_token():
    logger.info("Getting access token for sending an email.")
    AUTHORITY = f"https://login.microsoftonline.com/{settings.TENANT_ID}" 
    CLIENT_CREDENTIALS = ConfidentialClientApplication(
        client_id=settings.CLIENT_ID, # type: ignore
        client_credential=settings.CLIENT_SECRET, # type: ignore
        authority=AUTHORITY,
    )
    token = CLIENT_CREDENTIALS.acquire_token_for_client(scopes=settings.SCOPE) # type: ignore
    return token



def send_email(subject,to_emails, cc_emails, body, access_token, email_address):
    try:
        message = {
            "message": {"Subject": subject, "Body": {"Content": body,
                                                     "ContentType": "html"},
                        "ToRecipients": [{"EmailAddress": {"Address": email.strip()}} for email in to_emails],
                        }
        }

        if cc_emails:
            cc_recipients = [{"EmailAddress": {"Address": email.strip()}} for email in cc_emails]
            message["message"]["CcRecipients"] = cc_recipients

        url = f"https://graph.microsoft.com/v1.0/users/{email_address}/sendMail"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(url, headers=headers, json=message)

        if response.status_code == 202:
            logger.info("Email sent successfully!")
        else:
            logger.info(f"Error sending email: {response.status_code} - {response.text}")

    except Exception as e:
        logger.info(f"An error occurred in send_email script: {e}")


#################################################################################################################################
def Send_Email(username, userlogin, password, email_to):
    logger.info("Preparing to send email notification to user for login.")
    token = get_access_token()
    access_token = token["access_token"]
    body= Email_body(username, userlogin, password)
    send_email(settings.EMAIL_SUBJECT,email_to, settings.EMAIL_CC, body, access_token, settings.EMAIL_FROM_ADDRESS)


