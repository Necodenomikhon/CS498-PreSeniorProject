# AUTHORS   : Alex Wise
# CLASS     : CS498
# DATE      : 11/07/2024
# PROGRAM   : AzureMailReader.py

import msal
import requests

import msal
import requests
import getpass

# Function to prompt user for Azure credentials
def get_azure_credentials():
    client_id = input("Enter your Azure Client ID: ")
    client_secret = getpass.getpass("Enter your Azure Client Secret: ")
    tenant_id = input("Enter your Azure Tenant ID: ")
    return client_id, client_secret, tenant_id

# Authentication function using Azure credentials
def get_access_token(client_id, client_secret, tenant_id):
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)
    token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" in token:
        return token["access_token"]
    else:
        print("Could not acquire token:", token.get("error"))
        return None

# Fetch emails function
def fetch_emails():
    # Prompt for Azure credentials
    client_id, client_secret, tenant_id = get_azure_credentials()
    access_token = get_access_token(client_id, client_secret, tenant_id)
    
    if not access_token:
        return

    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://graph.microsoft.com/v1.0/me/messages"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        emails = response.json().get('value', [])
        for email in emails:
            print("Subject:", email["subject"])
            print("From:", email["from"]["emailAddress"]["address"])
            print("Received:", email["receivedDateTime"])
            print("Body Preview:", email["bodyPreview"])
            print("-" * 50)
    else:
        print("Failed to fetch emails:", response.status_code, response.text)

# Run the script
fetch_emails()

