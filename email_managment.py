import smtplib
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from LLM import large_model, small_model

# -- Send custom email (used for interview invitations or summaries)
def send_email(sender_email, sender_password, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"✅ Email sent to {recipient_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {recipient_email}: {e}")

# -- Send summary of top candidates to the manager
def send_summary_email(summaries,jobreq,cvs, top_n, sender_email, sender_password, manager_email):

   
    summary_text = summaries[0]  # Assuming one summary block

    subject = f'AI Candidate Evaluation - Top {top_n} Candidates'
    send_email(sender_email, sender_password, manager_email, subject, summary_text)


