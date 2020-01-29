import yaml,smtplib


config = yaml.load(open('config.yaml'), Loader=yaml.FullLoader)


def Send():
    sender = 'jesustakethewheel8080@gmail.com'
    pwd = 'emoxzkqzmgegmpzy'
    receivers = ['7196414411@vtext.com']

    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    Subject: SMTP e-mail test

    This is a test e-mail message.
    """

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sender, pwd)
        server.sendmail(sender, receivers, message)         
        print("Successfully sent email")

    except smtplib.SMTPException:
        print("Error: unable to send email")