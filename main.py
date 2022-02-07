import base64
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
import requests
from bs4 import BeautifulSoup
import time
import gspread
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

def hello_pubsub():
    print('scraping started')


base_url='https://www.kijiji.ca'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}


# url='https://www.kijiji.ca/b-canada/onewheel/k0l0?rb=true&dc=true'
# response=requests.get(url,headers=headers)

credentials={
  "type": "service_account",
  "project_id": "wide-jigsaw-311323",
  "private_key_id": "",
  "private_key": ""
  "client_id": "103366387568667672496",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/davidporterbot%40wide-jigsaw-311323.iam.gserviceaccount.com"
}

gc=gspread.service_account_from_dict(credentials)


sh=gc.open_by_url("https://docs.google.com/spreadsheets/d/12InSfczAcxYKp0kdr0P5L4Wrl9G8ELECmUVK4lfCF7A/edit#gid=0")
worksheet=sh.get_worksheet(1)

Names=[]
Location=[]
Url=[]
Price=[]



items=[]
#print(len(items))
def send_email(data,subject,reciever_address):
    sender_address='reducted'
    sender_pass='reducted'
    message= MIMEMultipart()
    message['From']=sender_address
    message['To']=reciever_address
    message['Subject']=subject
    attachment = MIMEApplication(data)
    attachment["Content-Disposition"] = 'attachment; filename=" {}"'.format(f"{subject}.csv")
    message.attach(attachment)
    session=smtplib.SMTP('smtp.gmail.com',587)
    session.starttls()
    session.login(sender_address,sender_pass)
    text=message.as_string()
    session.sendmail(sender_address,reciever_address,text)
    session.quit()
    print('mail sent')


    
search_items=['flower-vase','trek-bike','boosted-board','Ninebot','onewheel','onewheel-xr','onewheel-pint']
for target in search_items:

    #Manipulate b-canada to any location such as b-ontario
    #https://www.kijiji.ca/b-buy-sell/ontario/{target}/k0c10l9004
    #https://www.kijiji.ca/b-buy-sell/ontario/{target}/k0c10l9004
    url=f'https://www.kijiji.ca/b-canada/{target}/k0l0?rb=true&dc=true'
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.content,'lxml')
    products=soup.find_all('div',class_='info-container')
    print(f'scraping {target}')
    for product in products:
        price=product.find('div',class_='price')
        price=price.text.strip()
        
        link=product.find('a',class_='title',href=True)
        link=base_url+link['href']
        
        name=product.find('a',class_='title')
        name=name.text.strip()
        
        try:
            location=product.find('div',class_='location').find('span')
            location=location.text.strip()
        except:
            location=product.find('div',class_='cas-shipping-label')
            location=location.text.strip()
        
        data=f'Name: {name}, Price: {price}, Location: {location} , URL:{link}'
        test_list = ['Will buy your   Boosted Board   in excellent condition!', 'OneWheel Pint  genuine charger NEW!', 'Want  to buy    your OneWheel']
        if any(ele in data for ele in test_list):
            continue
        if '' in data:
            items.append(data)
            Price.append(price)
            Url.append(link)
            Names.append(name)
            Location.append(location)
        else:
            continue
            #worksheet.append_row(items)
            #del items
            
            # time.sleep(10)              
Product_Urls=worksheet.col_values(4)

data={
    'Name':Names,
    'Price':Price,
    'Location':Location,
    'Url':Url
    
}
update=[]
dataframe=pd.DataFrame(data)
print(len(Url)) #48
print(len(Product_Urls)-1) #49
[update.append(x) for x in Url if x not in Product_Urls] 
worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
res = list(set(Product_Urls+Url))

print(len(update))
#print(res)

product_name=[]
blank=[]
blank2=[]
if len(update) != 0:
    for i in update:
        
        new=i.split('/')
        name=new[-2]
        
        product_name.append(name)
        #update.append(name)
    for i in range(len(product_name)):
        blank.append('..')
        blank2.append('...')
        
    i=update
    result={
        'Name': product_name,
        '_':blank,
        'Url':update,
        '_':blank,
        '-':blank2
    }
    data=pd.DataFrame(result)
    data=data.to_csv(index=False)
    send_email(data,'A New Product Has Been Posted','reducted')
    
