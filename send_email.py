import smtplib
import os
import imghdr
from email.message import EmailMessage

PASSKEY = os.getenv('PASSKEY')
SENDER = "tmd526@gmail.com"
RECEIVER = "tmd526@gmail.com"


def send_email(image_path):
    """
    takes image_path which should be an image file.
    uses email.message to construct email message
    image file is opened in rb and then attached to email.

    :param image_path:
    :return:
    """
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("New customer!")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSKEY) # currently have a bug with this feature.
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()

if __name__ == "__main__":
    send_email(image_path="images/19.png")
