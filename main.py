import yaml,smtplib,os
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import time
from google_images_download import google_images_download



config = yaml.load(open('config.yaml'), Loader=yaml.FullLoader)

def GetTargets():
    receivers = []
    phonenumber = [config['Phone_Number']]
    carrier = ['@vzwpix.com','@pm.sprint.com', '@tmomail.net', '@mms.att.net']
    for c in carrier:
        for num in phonenumber:
            receivers.append(num+c)
            
    return receivers

def GetAttachments():
    response = google_images_download.googleimagesdownload()

    arguments = {"keywords": config["Attachments"],
                 "output_directory": "attachments/",
                 "no_directory": True,
                 "format": "jpg",
                 "chromedriver": config["Chrome_Driver"], 
                 "limit":config["Number_Of_MSGs"], 
                 "size": "medium"}
    try: 
        response.download(arguments) 
      
    # Handling File NotFound Error     
    except FileNotFoundError as Error:  
        print(Error)

def SendSMS():
    
    receiver = GetTargets()   

    message = "Hey"

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(config["Sender"], config["Sender_Pass"])
        server.sendmail(config["Sender"], receiver, message)         
        print("Successfully sent email")

    except smtplib.SMTPException:
        print("Error: unable to send email")

def SendMMS(attachment):

    receiver = GetTargets()

	###List of attachments###
    
    outer = MIMEMultipart()
    outer['Subject'] = "Hey"


	###Add the attachments to the message###
    # for file in arr:
    try:
        with open('attachments/'+attachment, 'rb') as fp:
            msg2 = MIMEBase('application', "octet-stream")
            msg2.set_payload(fp.read())
        encoders.encode_base64(msg2)
        msg2.add_header('Content-Disposition', 'attachments', filename=os.path.basename(attachment))
        outer.attach(msg2)
    except:
        print("Unable to open one of the attachments.")
        raise

    composed = outer.as_string()

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(config["Sender"], config["Sender_Pass"])
    server.sendmail(config["Sender"],receiver,composed)
    server.quit()
    print("IMAGE SENT")
    time.sleep(20)


if __name__ == "__main__":
    
    GetAttachments()

    arr = os.listdir("attachments")
    for attachment in arr:
        SendMMS(attachment)
