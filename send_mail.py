# -*- coding: UTF-8 -*-

def send_email(recipient, name, ticket_type, ticket_price):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.header import Header
    from email.utils import formataddr

    gmail_user = ''
    gmail_pwd = ''
    FROM = formataddr((str(Header(u'SITCON 夏令營籌備團隊', 'utf-8')), "ask@sitcon.org"))
    TO = recipient # recipient if type(recipient) is list else [recipient]
    REPLY_TO_ADDRESS = formataddr((str(Header(u'SITCON 夏令營籌備團隊', 'utf-8')), "ask@sitcon.camp"))

    msg = MIMEMultipart('alternative')

    fp = open('send_mail.html', 'r', encoding='UTF-8')
    html = fp.read()
    fp.close()

    fp2 = open('send_mail.txt', 'r', encoding='UTF-8')
    text = fp2.read()
    fp2.close()

    data = {'name': name, 'ticket_type': ticket_type, 'ticket_price': ticket_price}
    send_html = html.format(**data)
    send_text = text.format(**data)

    part1 = MIMEText(send_text, 'plain')
    part2 = MIMEText(send_html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    msg['Subject'] = '這是測試的錄取通知'
    msg['From'] = FROM
    msg['To'] = TO
    msg.add_header('reply-to', REPLY_TO_ADDRESS)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, [TO], msg.as_string())
        server.close()
        print('successfully sent the mail')
    except Exception as e:
        print(e)
        print("failed to send mail")


import csv

with open('main.csv', 'r', encoding='UTF-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        send_email(row['email'], row['name'], row['ticket_type'], row['ticket_price'])
