# AUTHORS   : Alex Wise
# CLASS     : CS498
# DATE      : 11/07/2024
# PROGRAM   : OutlookReader.py

import win32com.client

# Connect to Outlook
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)  # 6 refers to the inbox
messages = inbox.Items

# Fetch emails
for message in messages:
    try:
        print("Subject:", message.Subject)
        print("Sender:", message.SenderEmailAddress)
        print("Received:", message.ReceivedTime)
        print("Body Preview:", message.Body[:100])  # Print first 100 characters of the body
        print("-" * 50)
    except Exception as e:
        print(f"Could not read email due to: {e}")
