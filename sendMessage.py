import smtplib
import time
from PIL import Image
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import cv2
import readMessage


#class SendMessage(object):
emailId = 'pyimagecv@gmail.com'
sendToNumber = "2013609973@mms.att.net"
emailPass = "yourEmailpass"


# sendThisImage= recamear('.jpg')
def sendMessages(image):
    #cam = Camear()
    #cam.camear()
    msg = MIMEMultipart()
    msg['From'] = emailId
    msg['To'] = sendToNumber
    msg['Subject'] = "Unauthrized User"
    body = time.strftime('%c') + "\nYour system is used! "
    newImage = 'image22.jpg'
    cv2.imwrite(newImage, image)
    attachment = open(newImage, "rb")
    #message size exceeds fixed maximum message size
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; {}".format(newImage))
    msg.attach(part)
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(emailId, emailPass)
    text = msg.as_string()
    server.sendmail(emailId, sendToNumber, text)
    server.ehlo()
    maxLimit = int(server.esmtp_features['size'])
    print(maxLimit)
    time.sleep(20)
    readMessage.loopReadingEmail()
    time.sleep(80) 
    server.quit()
