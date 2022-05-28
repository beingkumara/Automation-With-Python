from http import server
from msilib.schema import MIME
from traceback import print_stack
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime


def headline():
    web_read = requests.get(
        'https://www.cricbuzz.com/').text
    bsoup = BeautifulSoup(web_read, 'lxml')
    news = bsoup.find('div', class_='cb-hm-lft')
    list_of_headlines = news.find_all(
        'div', class_='cb-col-100 cb-lst-itm cb-lst-itm-sm')
    head_news = ""
    head_news += '<h2> Trending Cricket News </h2> \n'
    count = 1
    for i in list_of_headlines:
        head_news += '<br>'
        head_news += str(count) + " : : " + i.a['title'] + '.' + '<br>'
        head_news += "https://www.cricbuzz.com/" + i.a['href']
        head_news += '<br>'
        count += 1
    return head_news


c = headline()

print('Composing Email.................')

SERVER = 'smtp.gmail.com'
port_number = 587
from_add = 'kumaracads@gmail.com'
to_add = 'maruthi.tiruvaipati.21033@iitgoa.ac.in'
password = ''


body_of_mail = MIMEMultipart()
body_of_mail['From'] = from_add
body_of_mail['To'] = to_add

present_day = datetime.datetime.now()

body_of_mail['Subject'] = 'Cricket News' + str(present_day.day) + '-' + str(
    present_day.month) + '-' + str(present_day.year) + '\n'

body_of_mail.attach(MIMEText(c, 'html'))

print('Initialising the Server................')

server = smtplib.SMTP(SERVER, port_number)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(from_add, password)
server.sendmail(from_add, to_add, body_of_mail.as_string())

print("Mail Sent")
server.quit()
