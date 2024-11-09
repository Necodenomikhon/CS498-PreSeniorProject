# AUTHORS   : Alex Wise
# CLASS     : CS498
# DATE      : 11/07/2024
# PROGRAM   : AzureMailReader.py

import os
import msal
import requests
import webbrowser

# Function to prompt user for Azure credentials
def get_azure_credentials():
    client_id = "7ed300eb-2268-49e0-95ce-ee27931470b5"
    tenant_id = "2b30530b-69b6-4457-b818-481cb53d42ae"
    return client_id, tenant_id

def get_access_token(client_id, tenant_id):
    authority = f"https://login.microsoftonline.com/common"
    redirect_uri = "http://localhost:8000"

    # Initialize the MSAL client
    app = msal.PublicClientApplication(client_id, authority=authority)
    accounts = app.get_accounts()
    if accounts:
        token_response = app.acquire_token_silent(["Mail.Read"], account=accounts[0])
    else:
        flow = app.initiate_device_flow(scopes=["Mail.Read"])
        if "user_code" not in flow:
            raise ValueError("Failed to create device flow")

        print(flow["message"])
        webbrowser.open(flow["verification_uri"])
        token_response = app.acquire_token_by_device_flow(flow)

    if "access_token" in token_response:
        return token_response["access_token"]
    else:
        print("Could not acquire token:", token_response.get("error_description"))
        return None

# Function to fetch emails, save them to a file, and return a string of the email contents
def fetch_emails():
    client_id, tenant_id = get_azure_credentials()
    access_token = get_access_token(client_id, tenant_id)

    if not access_token:
        return

    url = "https://graph.microsoft.com/v1.0/me/messages"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        emails = response.json().get('value', [])
        
        # Define the path to the 'fetched' folder in the main directory
        main_dir = os.path.dirname(os.path.dirname(__file__))  # Get the parent directory of 'scripts'
        output_folder = os.path.join(main_dir, "fetched")
        os.makedirs(output_folder, exist_ok=True)  # Create 'fetched' folder if it doesn't exist
        
        # Specify the path for the emails file
        output_file_path = os.path.join(output_folder, "emails.txt")
        
        # Collect email data in a string
        email_data = ""
        for email in emails:
            email_data += "Subject: " + email["subject"] + "\n"
            email_data += "From: " + email["from"]["emailAddress"]["address"] + "\n"
            email_data += "Received: " + email["receivedDateTime"] + "\n"
            # email_data += "Body Preview: " + email["bodyPreview"] + "\n"
            email_data += "Body:\n" + email["body"]["content"] + "\n"
            email_data += "-" * 50 + "\n\n"  # Separator between emails
            break # Only print out first email

        # Write emails to the file
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(email_data)

        print(f"Emails saved to {output_file_path}")
        return email_data  # Return the collected email data as a string
    else:
        print("Failed to fetch emails:", response.status_code, response.text)
        return None

# Run the script
if __name__ == "__main__":
    email_text = fetch_emails()
    print("Emails as a text string:\n")
    print(email_text)
