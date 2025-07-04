
import imaplib
import email
from email.header import decode_header

# -- Read emails and extract sender, subject, and plain text body
def read_emails(user_email, password, sender_filter=None, subject_filter=None):
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(user_email, password)
    imap.select("inbox")

    # Format IMAP search query properly
    criteria = '(ALL)'
    if sender_filter and subject_filter:
        criteria = f'(FROM "{sender_filter}" SUBJECT "{subject_filter}")'
    elif sender_filter:
        criteria = f'(FROM "{sender_filter}")'
    elif subject_filter:
        criteria = f'(SUBJECT "{subject_filter}")'

    status, messages = imap.search(None, criteria)
    if status != 'OK':
        print("❌ Failed to fetch emails.")
        return []

    emails = []

    for num in messages[0].split():
        res, msg_data = imap.fetch(num, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                from_ = msg.get("From")

                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain" and "attachment" not in str(part.get("Content-Disposition")):
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                emails.append({
                    "from": from_,
                    "subject": subject,
                    "body": body.strip()
                })

    imap.close()
    imap.logout()

    return emails