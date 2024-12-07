# AUTHORS   : Alex Wise
# CLASS     : CS498
# DATE      : 11/07/2024
# PROGRAM   : MailAppReader.py

import imaplib
import email
from email.header import decode_header
import getpass

def fetch_emails():
    # Prompt user for email, password, and IMAP server
    username = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ")
    imap_server = input("Enter your IMAP server (e.g., outlook.office365.com): ")
    
    # Connect to the server
    try:
        mail = imaplib.IMAP4_SSL(imap_server, 993)
        mail.login(username, password)
        print("\nLogin successful!\n")
    except imaplib.IMAP4.error:
        print("\nLogin failed. Please check your credentials and try again.")
        return

    # Select the mailbox you want to use (e.g., inbox)
    mail.select("inbox")

    # Search for all emails
    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()
    
    # Process the latest 5 emails
    for email_id in email_ids[-5:]:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                # Decode email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                
                # Get sender email
                from_ = msg.get("From")
                
                print("Subject:", subject)
                print("From:", from_)
                
                # If the email message is multipart
                if msg.is_multipart():
                    for part in msg.walk():
                        # If part is text/plain or text/html, get the content
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            print("Body:", body[:100])  # Print first 100 chars of the body
                            break
                else:
                    # If not multipart, get the payload directly
                    body = msg.get_payload(decode=True).decode()
                    print("Body:", body[:100])  # Print first 100 chars of the body
                
                print("-" * 50)
    
    # Logout and close the connection
    mail.logout()

# Run the script
fetch_emails()
