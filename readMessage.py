#!/usr/bin/python
import email
import imaplib
from email.header import Header, decode_header, make_header
import os
import subprocess

def loopReadingEmail():
    emailID = "pyimagecv@gmail.com"
    emailPass = "YourEmailPass"
    connMail = imaplib.IMAP4_SSL('imap.gmail.com')
    connMail.login(emailID, emailPass)
    connMail.list()
    connMail.select('inbox')
    restN = 0
    result, data = connMail.uid('search', None, "UNSEEN")
    if result == 'OK':
        indexNumber = len(data[0].split())
        #print(indexNumber,' message')
        for x in range(indexNumber):
            restN = restN + 1
            latestEmail = data[0].split()[x]
            result, emailData = connMail.uid('fetch', latestEmail, '(RFC822)')
            for readEmail in emailData:
                if isinstance(readEmail, tuple):
                    rawEmail = emailData[0][1]
                    rawEmailString = rawEmail.decode('utf-8')
                    emailMessage = email.message_from_string(rawEmailString)
                    emailFrom = str(make_header(decode_header(emailMessage['From'])))
                    subject = str(make_header(decode_header(emailMessage['Subject'])))
                    if subject == '12129' and emailFrom == '2013609973@mms.att.net':
                         print 'Rebooting the system due to unauthrized user'
                         os.system('reboot')
                    elif subject == '-off' and emailFrom == '2013609973@mms.att.net':
                        print 'Rebooting the system due to unauthrized user'
                        os.system('reboot')
                    else:
                        print subject
    #connMail.close()
if __name__ == '__main__':
    try:
        while True:
            loopReadingEmail()
    finally:
        print('goodBye')
