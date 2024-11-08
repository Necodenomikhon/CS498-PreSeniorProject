# AUTHORS   : Alex Wise
# CLASS     : CS498
# DATE      : 11/07/2024
# PROGRAM   : AzureMailReader.py

import msal
import requests
import webbrowser
import json
from datetime import datetime

# Function to prompt user for Azure credentials
def get_azure_credentials():
    client_id = "7ed300eb-2268-49e0-95ce-ee27931470b5"  # replace with your client ID
    tenant_id = "2b30530b-69b6-4457-b818-481cb53d42ae"  # replace with your tenant ID
    return client_id, tenant_id

def get_access_token(client_id, tenant_id):
    authority = f"https://login.microsoftonline.com/common"
    # Define the redirect URI (ensure it matches what you set in Azure portal)
    redirect_uri = "http://localhost:8000"

    # Initialize the MSAL client
    app = msal.PublicClientApplication(client_id, authority=authority)

    # Check if there is an existing token in cache
    accounts = app.get_accounts()
    if accounts:
        token_response = app.acquire_token_silent(["Mail.Read"], account=accounts[0])
    else:
        # If no token in cache, initiate authorization code flow
        flow = app.initiate_device_flow(scopes=["Mail.Read"])
        if "user_code" not in flow:
            raise ValueError("Failed to create device flow")

        # Display the user code and open the browser for login
        print(flow["message"])
        webbrowser.open(flow["verification_uri"])

        # Wait for the user to complete the flow
        token_response = app.acquire_token_by_device_flow(flow)

    if "access_token" in token_response:
        return token_response["access_token"]
    else:
        print("Could not acquire token:", token_response.get("error_description"))
        return None

# Function to fetch emails and write them to a text file
def fetch_emails():
    client_id, tenant_id = get_azure_credentials()
    access_token = get_access_token(client_id, tenant_id)

    if not access_token:
        return

    # Use /me endpoint to fetch the signed-in user's emails
    url = "https://graph.microsoft.com/v1.0/me/messages"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        emails = response.json().get('value', [])
        
        # Open a text file to save emails
        with open("emails.txt", "w", encoding="utf-8") as file:
            for email in emails:
                # Write email details to the file
                file.write("Subject: " + email["subject"] + "\n")
                file.write("From: " + email["from"]["emailAddress"]["address"] + "\n")
                file.write("Received: " + email["receivedDateTime"] + "\n")
                file.write("Body Preview: " + email["bodyPreview"] + "\n")
                file.write("-" * 50 + "\n\n")  # Separator between emails

        print("Emails saved to emails.txt")
    else:
        print("Failed to fetch emails:", response.status_code, response.text)

# Run the script
fetch_emails()
