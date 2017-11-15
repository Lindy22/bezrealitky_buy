import urllib3
import lxml.etree
import time
import datetime
import re
import random
import os
import sqlite3
import psycopg2
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
# from email.message import Message
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

http = "https://"
hostname = "www.bezrealitky.cz"
pripona = "/vyhledat"
pripona2 = "/vypis"
path = "/home/pi/Documents/bezrealitky_proj/buy/"
httpcon = urllib3.PoolManager()
price_reg = re.compile('([0-9]{0,2}.?[0-9]{3}.?[0-9]{3})+')
pagination_reg = re.compile('([0-9]{1,3})+')
surface_room_reg = re.compile('([[0-9]{1}\+[0-9]{1}|[[0-9]{1}\+kk)+')
surface_flat_reg = re.compile('([0-9]{2,3})+')
pager_bezrealitky = "&page={}"
pager_sreality = "&strana={}"
price = 4000000
hour = [7, 19]
minute = [51, 52, 53, 54, 55, 56, 57, 58, 59]

fromaddr = 'xxxx@xxx.xx'
toaddr = 'xxxx@xxx.xx'

username = "Xxxxx"
password = "Xxxxx"

location_paths = {
    "vinohrady":"?advertoffertype=nabidka-prodej&estatetype=byt&region=praha&county=praha-vinohrady&disposition%5B%5D=1-1&disposition%5B%5D=2-kk&disposition%5B%5D=2-1&disposition%5B%5D=3-kk&disposition%5B%5D=3-1&disposition%5B%5D=4-kk&disposition%5B%5D=4-1&disposition%5B%5D=5-kk&disposition%5B%5D=5-1&disposition%5B%5D=6-kk&disposition%5B%5D=6-1&disposition%5B%5D=7-kk&disposition%5B%5D=7-1&disposition%5B%5D=ostatni&priceFrom=&priceTo=&order=time_order_desc&submit=",
    "stare_mesto":"?advertoffertype=nabidka-prodej&estatetype=byt&region=praha&county=praha-stare-mesto&disposition%5B%5D=1-1&disposition%5B%5D=2-kk&disposition%5B%5D=2-1&disposition%5B%5D=3-kk&disposition%5B%5D=3-1&disposition%5B%5D=4-kk&disposition%5B%5D=4-1&disposition%5B%5D=5-kk&disposition%5B%5D=5-1&disposition%5B%5D=6-kk&disposition%5B%5D=6-1&disposition%5B%5D=7-kk&disposition%5B%5D=7-1&disposition%5B%5D=ostatni&priceFrom=&priceTo=&order=time_order_desc&submit=",
    "nove_mesto":"?advertoffertype=nabidka-prodej&estatetype=byt&region=praha&county=praha-nove-mesto&disposition%5B%5D=1-1&disposition%5B%5D=2-kk&disposition%5B%5D=2-1&disposition%5B%5D=3-kk&disposition%5B%5D=3-1&disposition%5B%5D=4-kk&disposition%5B%5D=4-1&disposition%5B%5D=5-kk&disposition%5B%5D=5-1&disposition%5B%5D=6-kk&disposition%5B%5D=6-1&disposition%5B%5D=7-kk&disposition%5B%5D=7-1&disposition%5B%5D=ostatni&priceFrom=&priceTo=&order=time_order_desc&submit=",
    "karlin":"?advertoffertype=nabidka-prodej&estatetype=byt&region=praha&county=praha-karlin&disposition%5B%5D=1-1&disposition%5B%5D=2-kk&disposition%5B%5D=2-1&disposition%5B%5D=3-kk&disposition%5B%5D=3-1&disposition%5B%5D=4-kk&disposition%5B%5D=4-1&disposition%5B%5D=5-kk&disposition%5B%5D=5-1&disposition%5B%5D=6-kk&disposition%5B%5D=6-1&disposition%5B%5D=7-kk&disposition%5B%5D=7-1&disposition%5B%5D=ostatni&priceFrom=&priceTo=&order=time_order_desc&submit=",
    "holesovice":"?advertoffertype=nabidka-prodej&estatetype=byt&region=praha&county=praha-holesovice&disposition%5B%5D=1-1&disposition%5B%5D=2-kk&disposition%5B%5D=2-1&disposition%5B%5D=3-kk&disposition%5B%5D=3-1&disposition%5B%5D=4-kk&disposition%5B%5D=4-1&disposition%5B%5D=5-kk&disposition%5B%5D=5-1&disposition%5B%5D=6-kk&disposition%5B%5D=6-1&disposition%5B%5D=7-kk&disposition%5B%5D=7-1&disposition%5B%5D=ostatni&priceFrom=&priceTo=&order=time_order_desc&submit=",
    "zizkov":"?advertoffertype=nabidka-prodej&estatetype=byt&region=praha&county=praha-zizkov&disposition%5B%5D=1-1&disposition%5B%5D=2-kk&disposition%5B%5D=2-1&disposition%5B%5D=3-kk&disposition%5B%5D=3-1&disposition%5B%5D=4-kk&disposition%5B%5D=4-1&disposition%5B%5D=5-kk&disposition%5B%5D=5-1&disposition%5B%5D=6-kk&disposition%5B%5D=6-1&disposition%5B%5D=7-kk&disposition%5B%5D=7-1&disposition%5B%5D=ostatni&priceFrom=&priceTo=&order=time_order_desc&submit=",
    "vysehrad":"?advertoffertype=nabidka-prodej&estatetype=byt&region=praha&county=praha-vysehrad&disposition%5B%5D=1-1&disposition%5B%5D=2-kk&disposition%5B%5D=2-1&disposition%5B%5D=3-kk&disposition%5B%5D=3-1&disposition%5B%5D=4-kk&disposition%5B%5D=4-1&disposition%5B%5D=5-kk&disposition%5B%5D=5-1&disposition%5B%5D=6-kk&disposition%5B%5D=6-1&disposition%5B%5D=7-kk&disposition%5B%5D=7-1&disposition%5B%5D=ostatni&priceFrom=&priceTo=&order=time_order_desc&submit=",
    "vrsovice":"?advertoffertype=nabidka-prodej&estatetype=byt&region=praha&county=praha-vrsovice&disposition%5B%5D=1-1&disposition%5B%5D=2-kk&disposition%5B%5D=2-1&disposition%5B%5D=3-kk&disposition%5B%5D=3-1&disposition%5B%5D=4-kk&disposition%5B%5D=4-1&disposition%5B%5D=5-kk&disposition%5B%5D=5-1&disposition%5B%5D=6-kk&disposition%5B%5D=6-1&disposition%5B%5D=7-kk&disposition%5B%5D=7-1&disposition%5B%5D=ostatni&priceFrom=&priceTo=&order=time_order_desc&submit=",
    "dejvice":"?advertoffertype=nabidka-prodej&estatetype=byt&region=praha&county=praha-dejvice&disposition%5B%5D=1-1&disposition%5B%5D=2-kk&disposition%5B%5D=2-1&disposition%5B%5D=3-kk&disposition%5B%5D=3-1&disposition%5B%5D=4-kk&disposition%5B%5D=4-1&disposition%5B%5D=5-kk&disposition%5B%5D=5-1&disposition%5B%5D=6-kk&disposition%5B%5D=6-1&disposition%5B%5D=7-kk&disposition%5B%5D=7-1&disposition%5B%5D=ostatni&priceFrom=&priceTo=&order=time_order_desc&submit=",
    "stresovice":"?advertoffertype=nabidka-prodej&estatetype=byt&region=praha&county=praha-stresovice&disposition%5B%5D=1-1&disposition%5B%5D=2-kk&disposition%5B%5D=2-1&disposition%5B%5D=3-kk&disposition%5B%5D=3-1&disposition%5B%5D=4-kk&disposition%5B%5D=4-1&disposition%5B%5D=5-kk&disposition%5B%5D=5-1&disposition%5B%5D=6-kk&disposition%5B%5D=6-1&disposition%5B%5D=7-kk&disposition%5B%5D=7-1&disposition%5B%5D=ostatni&priceFrom=&priceTo=&order=time_order_desc&submit="}

locations = ["vinohrady",
             "stare_mesto",
             "nove_mesto",
             "karlin",
             "holesovice",
             "zizkov",
             "vysehrad",
             "vrsovice",
             "dejvice",
             "stresovice"]

TEMPLATE_FILE = """Lokalita: {title}
Velikost: {surface}
Cena: {price}
Cena za metr: {price_per_meter}
Popis: {desc}
Odkaz na web: {web_adress}"""

TEMPLATE_EMAIL = """Subject: {title}

Lokalita: {title}
Velikost: {surface}
Cena: {price}
Cena za metr: {price_per_meter}
Popis: {desc}
Odkaz na web: {web_adress}"""

TEMPLATE_IAMALIVE = """I am still hardworking!
Please, find the updated file in the attachment."""


def get_url(httpcon, url):
    headers = {}
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    headers["Accept-Encoding"] = "gzip, deflate"
    headers["Accept-Language"] = "cs,en-us;q=0.7,en;q=0.3"
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"
    # headers["Cookie"]="op_cookie-test=ok;op_oddsportal=cv704mv1ek2l60ijve9iq9hn62;op_user_cookie=32830896;D_UID=739B93C4-5FB3-34AB-A4B5-0C2C36C3347E"
    res = httpcon.urlopen("GET", url, headers=headers)
    
    if res.status!=200:
        print res.status
        raise Exception("Unable to get_url "+url)
    # print res.data
    return res.data


def create_file(path,advert_dict):
    for j in advert_dict:
        advert_output = advert_dict[j].split(';')
        with open(path+advert_output[-1]+"-"+advert_output[3]+".txt","w") as fi:
            out = TEMPLATE_FILE.format(title = advert_output[0],
                                  web_adress = advert_output[1],
                                  surface = advert_output[2],
                                  price = advert_output[3],
                                  price_per_meter = advert_output[4],
                                  desc = advert_output[5],
                                  id_advert = advert_output[6])
            fi.write(out)


def get_adverts_from_file(path):
    name_list = []
    for filename in os.listdir(path):
        if ".txt" in filename:
            name_list.append(filename.replace(".txt",""))
    return(name_list)


def send_email(username,password,fromaddr,toaddr,path,advert_dict):
    server = smtplib.SMTP('smtp.gmail.com:587')
    # server = smtplib.SMTP('smtp.seznam.cz:25')
    server.starttls()
    server.login(username,password)
    for k in advert_dict:
        advert_output = advert_dict[k].split(';')
        msg = TEMPLATE_EMAIL.format(title = advert_output[0],
                              web_adress = advert_output[1],
                              surface = advert_output[2],
                              price = advert_output[3],
                              price_per_meter = advert_output[4],
                              desc = advert_output[5],
                              id_advert = advert_output[6])
        server.sendmail(fromaddr, toaddr, msg)
    server.quit()


def get_flats_bezrealitky(httpcon, main_url, old_advert_list, price_threshold, quarter):

    htmlparser = lxml.etree.HTMLParser()
    page = get_url(httpcon, main_url)
    # print page
        
    p=lxml.etree.fromstring(page,htmlparser)
    # print ''.join(p.itertext()).encode('utf-8')
    # flat_list=p.xpath(u'body//div[@class="list"]/div[@class="item ng-scope highlight"]')
    pagination_xpath = p.xpath(u'body//div[@class="box-body"]/a/text()')
    pagination_list = [str(pagination_reg.findall(m)).strip("[]''""") for m in pagination_xpath]
    pagination_list = filter(None,pagination_list)
    advert_dict = {}
    id_advert_dict = {}
    count = 1
    if len(pagination_list) > 0:
        page_cnt = len(pagination_list)
    else:
        page_cnt = 1
        
    for page in range(page_cnt):
        flat_list=p.xpath(u'body//div[@class="record highlight"]')
        flat_list2=p.xpath(u'body//div[@class="record "]')
        flat_list = flat_list + flat_list2
    # print flat_list
        for r in flat_list:
            title_xpath = r.xpath('div[@class="details"]/h2/a/text()')
            web_adress_xpath = r.xpath('div[@class="details"]/p[@class="short-url"]/text()')
            surface_xpath = r.xpath('div[@class="details"]/p[@class="keys"]/text()')
            price_xpath = r.xpath('div[@class="details"]/p[@class="price"]/text()')
            desc_xpath = r.xpath('div[@class="details"]/p[@class="description"]/text()')

            title = title_xpath[1].replace(u'\xb2',"2").encode('utf-8').strip()
            web_adress = web_adress_xpath[0].encode('utf-8')
            id_advert = web_adress.split('/')[-1]
            surface_all = surface_xpath[0].replace(u'\xb2',"2").encode('utf-8')
            price = price_xpath[0].encode('utf-8')
            desc = desc_xpath[0].replace(u'\xb2',"2").replace(u'\u200b',"2").encode('utf-8','ignore').lstrip()
            price_int = price_reg.findall(price)
            price_int = [int(l.replace(".","")) for l in price_int]
            surface_room = surface_room_reg.findall(surface_all)
            surface_flat = surface_flat_reg.findall(surface_all)
            surface_flat = [float(m) for m in surface_flat]            
            price_per_meter =  "{:.0f}".format(sum(price_int) / sum(surface_flat))
            
            if sum(price_int) > price_threshold: #omezeni na vyssi celkoveho najmu
                continue        
            if id_advert+"-"+str(price) in old_advert_list:
                continue
            else:
                advert_list = title + ';' + web_adress + ';' + surface_all + ';' + str(price) + ';' + str(price_per_meter) + ';' + desc + ';' + id_advert
                advert_dict[count] = advert_list
                id_advert_dict[count] = id_advert
                count += 1
        url=main_url+pager_bezrealitky.format(page+2)
        page=get_url(httpcon,url)
        p=lxml.etree.fromstring(page,htmlparser)
                    
#    send_email(username,password,fromaddr,toaddr,path,advert_dict)
    create_file(path+quarter+"/",advert_dict)
#    print(id_advert_dict)
    for j in advert_dict:
        advert_output = advert_dict[j].split(';')
        # write to the database, line by line (flat by flat)
        with sqlite3.connect('bezrealitky.db') as connection:
            connection.text_factory = str
            c = connection.cursor()
            c.execute("INSERT INTO inzeraty_praha(DateTime, WebAdress, Surface, Price, PricePerMeter, Location) values (?,?,?,?,?,?)", (str(time.strftime('%Y-%m-%d %H:%M:%S')), advert_output[1], advert_output[2], advert_output[3], advert_output[4],quarter))
        connection.close()
        
        # write to the postgres DB, line by line (flat by flat)
        with psycopg2.connect(host = "localhost", database="bezrealitky", user = "xxxx",password = "xxxx") as conn:
            cc = conn.cursor()
            cc.execute("INSERT INTO inzeraty_praha(DateTime, WebAdress, Surface, Price, PricePerMeter, Location) values (%s,%s,%s,%s,%s,%s)", (str(time.strftime('%Y-%m-%d %H:%M:%S')), advert_output[1], advert_output[2], advert_output[3], advert_output[4],quarter))
        conn.close()
        
        # write to the .csv file, line by line (flat by flat)
        with open ("inzeraty_bezrealitky.csv","ab") as f:
            f.write(str(time.strftime('%Y-%m-%d %H:%M:%S')) + ";" + advert_output[1] + ";" + advert_output[2] + ";" + advert_output[3] + ";" + advert_output[4]+ ";" + quarter +'\n')
        f.close()    


def execute_script():
    time.sleep(random.uniform(3300,3600))


def i_am_alive(current_time,username,password, fromaddr,toaddr):
    # if current_time.hour in hour and current_time.minute in minute:
    if current_time.hour in hour:
        # if you use gmail
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username,password)
        msg = MIMEMultipart()
        msg['Subject'] = str("Check a new flats")
        fileToSend = "inzeraty_bezrealitky.csv"
        ctype,encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/",1)
        fp = open(fileToSend,"rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition","attachment", filename = fileToSend)
        msg.attach(attachment)
        body = MIMEText(TEMPLATE_IAMALIVE)
        msg.attach(body)
        server.sendmail(fromaddr, toaddr, msg.as_string())        
        server.quit()


while True:
    tstart = time.time()
    if os.path.exists("/home/pi/Documents/bezrealitky_proj/verze/inzeraty_bezrealitky.csv") == False:
        with open("inzeraty_bezrealitky.csv", "ab") as f:
            f.write("DateTime;WebAdress;Surface;Price;PricePerMeter;Location\n")
        f.close()
    for i in locations:
        old_advert_list = get_adverts_from_file(path+i+"/")
        get_flats_bezrealitky(httpcon, http+hostname+pripona2+location_paths[i], old_advert_list, price, i)
    current_time = datetime.datetime.now()
    print current_time
    print "total time", time.time()-tstart
    print "bezrealitky_buy_Praha.py"
    i_am_alive(current_time,username,password, fromaddr,toaddr)
    execute_script()
