# ================================================== #
#   Importation Of Default Module
# ================================================== #
from typing import List

# ================================================== #
#   Importation Of 3rd Party Module
# ================================================== #
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# ================================================== #
#   Importation Of Self Development Module
# ================================================== #

# ================================================== #
#   Declaration AND Definition Of This Module Variable
# ================================================== #

# ================================================== #
#   Declaration AND Definition Of This Module Fucntion
# ================================================== #
def SendMail (smtp_server: str="", smtp_port: int=None, source_addr: str="", pw: str="", destination_addr: List[str]=[], subject: str="",
              message: str="", attachment: List[List[str]]=[]):
    content = MIMEMultipart()
    
    if (source_addr != ""):
        content["From"] = source_addr
    else:
        print("Please Set Sender eMail Address")
        return
    
    if (type(destination_addr) != list):
        print("Please Set Receiver eMail As A List")
    if (len(destination_addr) > 0):
        content["To"] = ",".join(destination_addr)
    else:
        print("Please Set Receiver eMail Address")
        return
    
    content["Subject"] = subject

    content.attach(MIMEText(message))

    if (type(attachment) != list):
        print("Please Set Attachment As A List")
        print("Your Attachment Won't Be Sent")
    else:
        for att in attachment:
            fp = open(att[0], "rb")
            tmp = MIMEApplication(fp.read())
            tmp.add_header("content-disposition", "attachment", filename=att[1])
            content.attach(tmp)
            fp.close()

    mail_text = content.as_string()

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(source_addr, pw)
    server.sendmail(source_addr, ",".join(destination_addr), mail_text)

    server.quit()

# ================================================== #
#   Declaration AND Definition Of This Module Class
# ================================================== #

# ================================================== #
#   Testing Of This Module
# ================================================== #
if (__name__ == "__main__"):
    source_addr = input("Please Input Your eMail: ")
    pw = input("Please Input You Password: ")
    SendMail(smtp_server="smtp.gmail.com",
             smtp_port=587,
             source_addr=source_addr,
             pw=pw,
             destination_addr=[source_addr],
             subject="Hello World",
             message="FYI\n\n\nHello World\n\n\nBest Regards",
             attachment=[["Listed Normal Symbol.csv", "Symbol List.csv"]])
    