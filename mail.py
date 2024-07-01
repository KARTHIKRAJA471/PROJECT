from email.message import EmailMessage
import ssl
import smtplib

def mail():
    email_sender = "santhoshdeveloper001@gmail.com"
    email_password = "ovte xyyz vyka yopb"
    email_receiver = "santhoshdeveloper001@gmail.com"

    subject = "Your Participation in Online Classes"

    body = """
     
                   We have noticed that your attendance and participation in our online classes have been inconsistent recently. Active participation in online classes is crucial for your understanding of the course material and your overall success in the program. 

We want to encourage you to prioritize attending all scheduled online sessions and actively participating in class discussions and activities. 

If you are facing any challenges or difficulties that are preventing you from attending classes regularly, please don't hesitate to reach out to us. We are here to support you and provide assistance in any way we can.

Your commitment to your education is commendable, and we believe that with dedication and active engagement, you can achieve your academic goals.

Please let us know if you have any questions or concerns. We are here to help you succeed.

Best regards,
[Instructor's Name]
[Course Name/Code]

    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To']   = email_receiver
    em['Subject'] = subject

    em.set_content(body)
    context = ssl.create_default_context()


    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_receiver,em.as_string())