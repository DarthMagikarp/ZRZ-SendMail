import smtplib
import string
import random
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailSender:
    def __init__(self, in_username, in_password, in_server=("smtp.gmail.com", 587), use_SSL=False):
        self.username = in_username
        self.password = in_password
        self.server_name = in_server[0]
        self.server_port = in_server[1]
        self.use_SSL = use_SSL

        if self.use_SSL:
            self.smtpserver = smtplib.SMTP_SSL(self.server_name, self.server_port)
        else:
            self.smtpserver = smtplib.SMTP(self.server_name, self.server_port)
        self.connected = False
        self.recipients = []

    def __str__(self):
        return "Type: Mail Sender \n" \
               "Connection to server {}, port {} \n" \
               "Connected: {} \n" \
               "Username: {}, Password: {}".format(self.server_name, self.server_port, self.connected, self.username, self.password)

    #def set_message(self, in_plaintext, in_subject="", in_from=None, in_htmltext=None):
    def set_message(self, in_plaintext, in_subject, in_from):
        #print(in_plaintext)
        #print(in_subject)
        #print(in_from)

        in_from='Salud mental UDP'

        in_plaintext = "<p><span style='font-size: 18px;'>"+in_plaintext+"</span></p>"
        in_htmltext = "<html > <head> <title>UDP</title> <style type='text/css'> body { margin: 0 !important; padding: 0 !important; -webkit-text-size-adjust: 100% !important; -ms-text-size-adjust: 100% !important; -webkit-font-smoothing: antialiased !important; } img { border: 0 !important; outline: none !important; } p { Margin: 0px !important; Padding: 0px !important; } table { border-collapse: collapse; mso-table-lspace: 0px; mso-table-rspace: 0px; } td, a, span { border-collapse: collapse; mso-line-height-rule: exactly; } .ExternalClass * { line-height: 100%; } .em_defaultlink a { color: inherit !important; text-decoration: none !important; } span.MsoHyperlink { mso-style-priority: 99; color: inherit; } span.MsoHyperlinkFollowed { mso-style-priority: 99; color: inherit; } @media only screen and (min-width:481px) and (max-width:699px) { .em_main_table { width: 100% !important; } .em_wrapper { width: 100% !important; } .em_hide { display: none !important; } .em_img { width: 100% !important; height: auto !important; } .em_h20 { height: 20px !important; } .em_padd { padding: 20px 10px !important; } } @media screen and (max-width: 480px) { .em_main_table { width: 100% !important; } .em_wrapper { width: 100% !important; } .em_hide { display: none !important; } .em_img { width: 100% !important; height: auto !important; } .em_h20 { height: 20px !important; } .em_padd { padding: 20px 10px !important; } .em_text1 { font-size: 16px !important; line-height: 24px !important; } u + .em_body .em_full_wrap { width: 100% !important; width: 100vw !important; } } </style> </head> <body class='em_body' style='margin:0px; padding:0px;' bgcolor='#efefef'> <table class='em_full_wrap' valign='top' width='100%' cellspacing='0' cellpadding='0' border='0' bgcolor='#efefef' align='center'> <tbody> <tr> <td valign='top' align='center'> <table class='em_main_table' style='width:700px;' width='700' cellspacing='0' cellpadding='0' border='0' align='center'> <tbody> <tr> <td style='padding:15px;' class='em_padd' valign='top' bgcolor='#f6f7f8' align='center'> <table width='100%' cellspacing='0' cellpadding='0' border='0' align='center'>  <tbody>  <tr>   </tbody> </table> </td> </tr> <tr> <td valign='top' align='center'> <table width='100%' cellspacing='0' cellpadding='0' border='0' align='center'>  <tbody>  <tr>  <td valign='top' align='center'><img class='em_img' alt='Banbif' style='display:block; font-family:Arial, sans-serif; font-size:30px; line-height:34px; color:#000000; max-width:700px;' src='https://i.ibb.co/4TnJStf/000.png' width='700' border='0' height='245'></td>  </tr>  </tbody> </table> </td> </tr> <tr> <td style='padding:35px 70px 30px;' class='em_padd' valign='top' bgcolor='#FFFFFF' align='center'> <table width='100%' cellspacing='0' cellpadding='0' border='0' align='center'>  <tbody>  <tr>  <td valign='top' align='justify'> <br><br>"+in_plaintext+"</td>  </tr>  </tbody> </table> </td> </tr> <tr> <td style='padding:38px 30px;' class='em_padd' valign='top' bgcolor='#f6f7f8' align='center'> <table width='100%' cellspacing='0' cellpadding='0' border='0' align='center'></table> <tbody> <tr> </tr> <tr> <td> <center><b>© 2024 UDP. Todos los derechos reservados.</b></center></tr> </tbody> </table> </td> </tr> <tr> <td class='em_hide' style='line-height:1px;min-width:700px;background-color:#ffffff;'><img alt='' src='images/spacer.gif' style='max-height:1px; min-height:1px; display:block; width:700px; min-width:700px;' width='700' border='0' height='1'></td> </tr> </tbody> </table> </td> </tr> </tbody></table>  <div class='em_hide' style='white-space: nowrap; display: none; font-size:0px; line-height:0px;'>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</div> </body></html>"
        
        if in_htmltext is not None:
            self.html_ready = True
        else:
            self.html_ready = False

        if self.html_ready:
            self.msg = MIMEMultipart('alternative')  # 'alternative' allows attaching an html version of the message later
            self.msg.attach(MIMEText(in_plaintext, 'plain'))
            self.msg.attach(MIMEText(in_htmltext, 'html'))
        else:
            self.msg = MIMEText(in_plaintext, 'plain')

        self.msg['Subject'] = in_subject
        if in_from is None:
            self.msg['From'] = self.username
        else:
            self.msg['From'] = in_from
        self.msg["To"] = None
        self.msg["CC"] = None
        self.msg["BCC"] = None


    def clear_message(self):
        self.msg.set_payload("")

    def set_subject(self, in_subject):
        self.msg.replace_header("Subject", in_subject)

    def set_from(self, in_from):
        self.msg.replace_header("From", in_from)

    def set_plaintext(self, in_body_text):
        if not self.html_ready:
            self.msg.set_payload(in_body_text)
        else:
            payload = self.msg.get_payload()
            payload[0] = MIMEText(in_body_text)
            self.msg.set_payload(payload)

    def set_html(self, in_html):
        try:
            payload = self.msg.get_payload()
            payload[1] = MIMEText(in_html, 'html')
            self.msg.set_payload(payload)
        except TypeError:
            print("ERROR: "
                  "Payload is not a list. Specify an HTML message with in_htmltext in MailSender.set_message()")
            raise

    def set_recipients(self, in_recipients):
        if not isinstance(in_recipients, (list, tuple)):
            raise TypeError("Recipients must be a list or tuple, is {}".format(type(in_recipients)))

        self.recipients = in_recipients

    def add_recipient(self, in_recipient):
        self.recipients.append(in_recipient)

    def connect(self):
        if not self.use_SSL:
            self.smtpserver.starttls()
        self.smtpserver.login(self.username, self.password)
        self.connected = True
        print("Connected to {}".format(self.server_name))

    def disconnect(self):
        self.smtpserver.close()
        self.connected = False

    def send_all(self, close_connection=True):
        if not self.connected:
            raise ConnectionError("Not connected to any server. Try self.connect() first")

        print("Message: {}".format(self.msg.get_payload()))

        for recipient in self.recipients:
                self.msg.replace_header("To", recipient)
                print("Sending to {}".format(recipient))
                self.smtpserver.send_message(self.msg)

        print("All messages sent")

        if close_connection:
            self.disconnect()
            print("Connection closed")
