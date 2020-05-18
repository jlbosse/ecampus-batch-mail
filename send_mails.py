#!/usr/bin/env python
"""
Automatically send out the corrected sheets to all students. The filenames 
of the sheets must be "QM_Blatt<i>_<name>_korrigiert.pdf" and you need
to provide a csv file "emails.csv" of the format 

name1, email-addres
name2, email_address
...

where name1, name2, ... have to coincide with the names used in the filenames.
These names will also be used to address the students.
"""
import argparse, configparser
import csv, sys
from getpass import getpass
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ##############################################################################
# Parsing of the filenames
# ##############################################################################
parser = argparse.ArgumentParser(description="""
Automatically send out the corrected sheets to all students.
""")
parser.add_argument("-f", "--files", type=str, nargs="+",
                    help="List of files you want to send. Must be of the form "
                    "'stuff_<name>_morestuff' where <name> must be before the "
                    "last underscore")
parser.add_argument("-s", "--subject",  type=str,
                    help="The subject of the E-Mail")
parser.add_argument("-m", "--message", type=str,
                    help="A file with the contents of the E-Mail. "
                         "Any occurence of '<name>' will be replaced with "
                         "the recipients name")
parser.add_argument("-a", "--addresslist", type=str, default="emails.csv",
                    help="A csv file containing lines <name>, <email-address>. "
                         "Defaults to `emails.csv`")


# ##############################################################################
# Sender and servers settings
# ##############################################################################
config = configparser.ConfigParser()
config.read("config.ini")
sender_email = config["MAIL-SETTINGS"]["sender_email"]
sender_username = config["MAIL-SETTINGS"]["sender_username"]
server_address = config["MAIL-SETTINGS"]["smtp_server"]
port = config["MAIL-SETTINGS"]["port"]
_DEFAULT_CIPHERS = config["MAIL-SETTINGS"]["_DEFAULT_CIPHERS"]


# ##############################################################################
# The main message sending routine
# ##############################################################################
def send_mail(receiver_email, subject, message_body, attachment_fn, password):
    # create the message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(message_body, "plain"))

    # Open PDF file in binary mode
    with open(attachment_fn, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {attachment_fn}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()
    server = smtplib.SMTP(server_address, port)
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.options |= ssl.OP_NO_SSLv2
    context.options |= ssl.OP_NO_SSLv3

    context.set_ciphers(_DEFAULT_CIPHERS)
    context.set_default_verify_paths()
    context.verify_mode = ssl.CERT_REQUIRED
    if server.starttls(context=context)[0] != 220:
        print("starting conection failed")
        return false
    server.login(sender_username, password)
    server.sendmail(sender_email, receiver_email, text)
    server.quit()


# ##############################################################################
# int main(){...}
# ##############################################################################
if __name__ == "__main__":
    args = parser.parse_args()

    if not args.subject or not args.message or not args.files:
        parser.print_help()
        sys.exit(1)
    
    subject = args.subject

    with open(args.message, mode="r") as file:
        message = file.read()

    # read in all the name-address pairs of the students
    with open(args.addresslist, mode="r") as file:
        reader = csv.reader(file)
        address_list = {rows[0] : rows[1] for rows in reader}

    password = getpass("E-Mail password:")

    for fn in args.files:
        name = fn.split("_")[-2]
        body = message.replace("<name>", name)
        receiver_email = address_list[name]
        print(f"sending {fn} to {receiver_email}")
        send_mail(receiver_email, subject, body, fn, password)