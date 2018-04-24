from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def getTime():
    today = datetime.today()
    yesterday = today - timedelta(1)
    return [str(today)[0:4], str(today)[5:7], str(today)[8:10], str(yesterday)[0:4], str(yesterday)[5:7], str(yesterday)[8:10]]

def getHTML(jahr, monat, tag):
    if len(str(monat))==1:
        monat = '0'+str(monat)
    else:
        monat = str(monat)

    if len(str(tag))==1:
        tag = '0'+str(tag)
    else:
        tag = str(tag)

    html = urlopen('http://www.tagesschau.de/multimedia/video/videoarchiv2~_date-'+str(jahr)+str(monat)+str(tag)+'.html')
    return BeautifulSoup(html)

def getData(bs):
    datum = bs.findAll('p', {'class':'dachzeile'})
    titel = bs.findAll('h4')
    inhalt = bs.findAll('p', {'class':'teasertext'})

    text = ''
    for i in range(len(titel)):
        text += titel[i].get_text().upper()+', '+datum[i].get_text()+'\n'
        for j in inhalt[i].get_text().split(', '):
            text += j+'\n'
        text += '\n'
    return text

def main():
    year_t, month_t, day_t, year_y, month_y, day_y = getTime()
    bs_today = getHTML(year_t, month_t, day_t)
    text = ''
    text += getData(bs_today)
    bs_yesterday = getHTML(year_y, month_y, day_y)
    text += getData(bs_yesterday)
    return text

headlines = str(main())
year_t, month_t, day_t, year_y, month_y, day_y = getTime()

fromaddr = "..."
toaddr = "..."
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Tagesschau "+day_t+'.'+month_t+'.'+year_t

body = headlines
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "...")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
