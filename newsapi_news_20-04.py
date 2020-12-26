from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
import requests as req
import json
import mysql.connector
import time,datetime,re
apikey="3bf2d032493c4a8c96023d3015eaba0d"
uploadapikey = 'nkfHEWhjkd32874ihfuJHJh93j3iVGHJGY67UTjBYIu32hjlIT'  #Server API to connect and upload data

def updateDB(zip_list,table_name):
    count=0
    try:
        config = {
          'user': 'root',
          'password': 'root',
          'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
          'database': 'timesbits',
          'raise_on_warnings': True,
        }

        # mydb = mysql.connector.connect(**config)  #server
        mydb = mysql.connector.connect(host="localhost",user="root",  passwd="nicpatel963",database="webnews")
        mycursor = mydb.cursor()

        for img_link,story_title,story_link,story,news_date,news_category,news_cat_id in zip_list:

            try:
                story_title = ' '.join(story_title.split())
                story = ' '.join(story.split())

                news_date=re.split(' |-',news_date)
                news_date=datetime.date(int(news_date[0]),int(news_date[1]),int(news_date[2]))
# server updatation
                # url = "https://wtclass.000webhostapp.com/api/insert_Recent_Posts/?api_key=%s&cat_id=%s&cat_name=%s&news_title=%s&news_date=%s&news_description=%s&news_image=%s&news_url=%s" % (
                # uploadapikey, news_cat_id, news_category, story_title, news_date, story, img_link, story_link)
                # print(url)
                # count += 1
                # print("Record inserted Sucessfully")
                # resp = req.get(url)
                # print(resp.status_code)
                # print(resp.json())
                # json_data = json.loads(resp.text)
                # print(json_data)
#local table updatation
                sql="SELECT * from {} where news_url='{}'".format(table_name,story_link)
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                if myresult:
                    # for x in myresult:    #printing result if contain
                    #     print(x[1])
                    print("already inserted in ",table_name)
                else:
                    sql = "INSERT INTO {} (news_url,news_title,news_description,news_image,news_date,cat_name,cat_id,news_state,content_type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table_name)   
                    val = (story_link,story_title,story,img_link,news_date,news_category,news_cat_id,"1","webnews")
                    mycursor.execute(sql, val)
                    mydb.commit()
                    count+=1
                    print(mycursor.rowcount, "record inserted in ",table_name)
            except Exception as e:
                print(e)
        print("total insertion:",count)
    except Exception as e:
        print(e)

def news_api(table_name,news_cat,news_cat_id,type_name=''):

    if type_name:
        type_name="&category="+type_name
        print("scraping started for :",type_name)
    
    req = urlopen('http://newsapi.org/v2/top-headlines?country=in'+type_name+'&apiKey=3bf2d032493c4a8c96023d3015eaba0d')
    page_html = req.read()
    data=json.loads(page_html)
    img_link = []
    story_title = []
    story_link = []
    story = []
    news_date=[]
    news_category = []
    cat_id = []

    for i in range(len(data['articles'])):
        story_link.append(data['articles'][i]['url'])
        story_title.append(data['articles'][i]['title'])
        temp=data['articles'][i]['content']
        try:
            if '…' in temp:
                print(temp)
        except:
            pass
        story.append(temp)
        img_link.append(data['articles'][i]['urlToImage'])
        news_date.append(data['articles'][i]['publishedAt'].split('T')[0])
        news_category.append(news_cat)
        cat_id.append(news_cat_id)

    zip_list = zip(img_link, story_title, story_link, story,news_date,news_category,cat_id)


    updateDB(zip_list,table_name)

news_api('tbl_news','business_en','25','business')
news_api('tbl_news','entertainment_en','28','entertainment')
news_api('tbl_news','technology_en','27','technology')
news_api('tbl_news','technology_en','27','science')
news_api('tbl_news','sports_en','26','sports')
