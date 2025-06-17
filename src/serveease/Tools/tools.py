from agents import function_tool
from serveease.DB.db import get_email_by_username
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()
import os

smtp_password = os.getenv("SMTP_PASSWORD")
def send_email(receiver_email, subject, message_body):
    sender_email = "muhammad11abdullah21@gmail.com"
    app_password = smtp_password

    # Create the email content
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message_body, "plain"))

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", str(e))
@function_tool
def Call_Support(username : str , query : str ) -> str:
    '''
    Args:
        username : str
        query : str

    Returns:
        str

    Call Support will call the support team and demand assistance as soon as possible when a use faces a problem ,
    This tool is called when the user reports an issue , that can be technical , financial or legal .    
    '''
    email = get_email_by_username(username)
    # Send an Email to the user for clearance

    response = send_email(receiver_email=email,subject="Support",message_body=f'''
                          Hi ! {username}
                          We have received your query' {query} 'and we will get back to you as soon as possible .
                          Stay Tuned.
    ''')
    # send_email(receiver_email='bilaltahir2128@gmail.com'
    #            , subject="Test Email from Customer Support", message_body=f''' ----TEST EMAIL ----''')
    
    
    return response

# send_email(receiver_email='abee20531@gmail.com',subject="TEST EMAIL",message_body=f''' ----TEST EMAIL ----''')
# Call_Support(username='user' , query='hello' )