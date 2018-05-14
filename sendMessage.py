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
emailPass = "123456789a!"


# sendThisImage= recamear('.jpg')
def sendMessages(image):
    #cam = Camear()
    #cam.camear()
    msg = MIMEMultipart()
    msg['From'] = emailId
    msg['To'] = sendToNumber
    msg['Subject'] = "Unauthrized User"
    body = time.strftime('%c') + "\nYour system is used! "

    #imageSize = Image.open(cam.saveImageName)
    #imageReSize = imageSize.resize((500,300), Image.ANTIALIAS)
    #imageReSize.save('image22.jpg', quality=100)

    #time.sleep(1)
    newImage = 'image22.jpg'

    #attachment =
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
    time.sleep(20) # trying 10s
    readMessage.loopReadingEmail()
    time.sleep(80) # tried 60
    server.quit()
    #print ('sent')
    #readMessage.loopReadingEmail()


#if __name__ == "__main__":
#     pass
     #sendMessages()
#     a.sendMessages()

        # sendThisImage = recamear('.jpg')
