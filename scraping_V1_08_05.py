# indianexpress,indiatoday 
print("scraping started do not turn off network.... it will take 20 minutes on an average....")
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
import mysql.connector
import time,datetime,re
import keyboard,traceback
import requests,logging
from datetime import date
start_time = time.time()

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
api = 'nkfHEWhjkd32874ihfuJHJh93j3iVGHJGY67UTjBYIu32hjlIT'  #Server API to connect and upload data
def updateDB(zip_list,table_name):
    try:
        # config = {
        #   'user': 'root',
        #   'password': 'root',
        #   'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
        #   'database': 'timesbits',
        #   'raise_on_warnings': True,
        # }
        # mydb = mysql.connector.connect(**config)  #server
        
        mydb = mysql.connector.connect(host="localhost",user="root",  passwd="nicpatel963",database="webnews")  # local 
        mycursor = mydb.cursor()
        for img_link,story_title,story_link,story,news_date,news_category,news_cat_id,news_time in zip_list:
            # print(len(img_link),len(story_title),len(story_link),len(story),len(news_date),len(news_category),len(news_cat_id),len(news_time))
            try:            
                def convert_time(t):
                    temp=t[-2]+t[-1]
                    t=t[0:len(t)-3].split(':')
                    if temp =='PM':
                        t[0]=str(int(t[0])+12)
                        if t[0]=='24':
                            t[0]='00'
                    t=':'.join(t)
                    if len(t)==5:
                        t=t+':00'
                    return t

                def addslashes(s):
                    d = {'"': '\\"', "'": "\\'", "\\0": "\\0", "\\": "\\\\"}
                    return ''.join(d.get(c, c) for c in s)

                story_title = ' '.join(story_title.split())
                story_title = addslashes(story_title)
                story = ' '.join(story.split())
                story = addslashes(story)
                
                news_date=re.split(' |-',news_date)
                news_date=datetime.date(int(news_date[2]),int(news_date[1]),int(news_date[0]))
                news_time=convert_time(news_time)
                # print(news_time)

                news_date=str(news_date)+" "+news_time
                # print(news_date,type(news_date))
                # print(news_date)
    # local updatation
                sql="SELECT * from {} where news_url='{}'".format(table_name,story_link)
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                if myresult:
                    print("already inserted in ",table_name)
                else:					
                    sql = "INSERT INTO {} (news_url,news_title,news_description,news_image,news_date,cat_name,cat_id,news_state,content_type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table_name)
                    val = (story_link,story_title,story,img_link,news_date,news_category,news_cat_id,"1","webnews")
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print(mycursor.rowcount, "record inserted in ",table_name)

    # server updatation
                # url = "https://wtclass.000webhostapp.com/api/insert_Recent_Posts/?api_key=%s&cat_id=%s&cat_name=%s&news_title=%s&news_date=%s&news_description=%s&news_image=%s&news_url=%s"%(api,news_cat_id,news_category,story_title,news_date,story,img_link,story_link)
                # print(url)
                # print("Record inserted Sucessfully")
                # resp = requests.get(url)
                # print(resp.status_code)
                # print("read:",resp.content)

                    # else:
                      #  print("record discarded due to incomplete value")
            except Exception as e:
                print(logging.exception(e))
    except Exception as e:
        print(logging.exception(e))

def en_scrap(type_name,table_name,news_cat,news_cat_id):
    print("scraping started for : ",news_cat)
    req = requests.get('https://www.shortpedia.com/en-in/'+type_name+'/',headers=headers)
    page_html = req.content
    page_soup = BeautifulSoup(page_html, "html.parser")
    src = page_soup.findAll('h3', {'itemprop': 'headline'})
    story_link = []
    img_link = []
    story_title = []
    story = []
    news_date=[]
    news_category = []
    news_time=[]
    cat_id = []

    for link in src:
        try:
            # print(link.a['href'])
            req = requests.get(link.a['href'],headers=headers)
            page_html = req.content
            page_soup = BeautifulSoup(page_html, "html.parser")
            img = page_soup.find('img', {'itemprop': 'url'})
            
            info = page_soup.find('p', {'itemprop': 'articleBody'})
            info_title = page_soup.find('h1', {'itemprop': 'headline'})
            info_text = info.text
            info_title_text = info_title.text
            
            #date finding for uploaded news
            span=page_soup.find('span',{'class':'post-date'})
            # print(nd['content'])
            time=span.text.split(',')[0]
            
            date_n_time=span['content'].split('T')
            Date=date_n_time[0].split('-')
            tdate='-'.join(Date)# required for matching newsdate
            Date.reverse()
            Date='-'.join(Date) 
            if tdate==str(date.today()):
                news_date.append(Date)
                news_category.append(news_cat)
                story_title.append(info_title_text)
                cat_id.append(news_cat_id)
                # print(date,time)
                story.append(info_text)
                story_link.append(link.a['href'])
                news_time.append(time)
                if img['data-src']:
                    img_link.append(img['data-src'])
                else:
                    img_link.append(img['src'])
        except Exception as e: 
            # print(logging.exception(e))
            print("error in ",table_name)
            print(link.a['href'])
    # print(img_link, story_title, story_link, story,news_date,news_category,cat_id,news_time)
    zip_list = zip(img_link, story_title, story_link, story,news_date,news_category,cat_id,news_time)
    updateDB(zip_list,table_name)

def hi_scrap(type_name,table_name,news_cat,news_cat_id,flag=0):
	print("scraping started for : ",news_cat)
	story_link = []        
	img_link = []         
	story_title = []      
	story = []    
	news_date=[]
	sections=[]       
	news_category = []
	news_time=[]
	cat_id = []
	links=[]
	for i in range(1,5):
	    html = requests.get('https://www.bhaskar.com/'+type_name+'/'+str(i),headers=headers)
	    # print('https://www.bhaskar.com/'+type_name+'/'+str(i))
	    
	    page_soup=BeautifulSoup(html.content,'html.parser')
	    sections.extend(page_soup.find_all('section',{'class':'lpage_bottom_data'}))

	for section in sections:
	    if flag==1:
	        STORY_LINK=section.div.a['href']
	        # story_link.append( )
	    else:
	        STORY_LINK='https://www.bhaskar.com'+section.div.a['href']
	        # story_link.append( )         
	    links.append(STORY_LINK)
	# print(len(links))

	for link in links:
		STORY_LINK=link
		IMAGE_LINK=None
		STORY_TITLE=None
		NEWSDATE=None
		STORY=None
		NEWSTIME=None
		try:
	        # print(link)
			html = requests.get(link, headers=headers)
			page_soup=BeautifulSoup(html.content,'html.parser')
	        # print(link)
			try:
			    image=page_soup.find('div',{'class':'db_storyimg openPopup'}).img
			    if image == None:
			        image=page_soup.find('figure',{'class':'norfigure'}).img
			    IMAGE_LINK=image['src']
			    # img_link.append()
			except:
			    pass

			div=page_soup.find('div',{'class':'db_storycontent'})
			STORY=div.p.text
			# story.append()
			title=page_soup.find('section',{'class':'db_storybox'}).h1
			STORY_TITLE=title.text
			# story_title.append()
			datetime=str(page_soup.find('div',{'class':'db_storytime'}))
			# print(datetime)
			try:
			    datetime=datetime.split('</h4>')[1]
			except:
			    datetime=datetime.split('db_storytime">')[1]
			datetime=datetime.split(',')
			time=datetime[2].split('IST')
			NEWSTIME=time[0].strip()
			datetime=[i.lstrip().rstrip() for i in datetime]
			temp=datetime[0].split(' ')
			# print("temp[0]:",temp[0])
			temp_dic={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','June':'06','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
			if temp[0] in temp_dic:
			    temp[0]=temp_dic.get(temp[0])
			else:
			    print("Error in date ,something wrong line:219 ")

			# print(temp)

			tdate=datetime[1]+"-"+str(temp[0])+"-"+str(temp[1])#required for current date matching

			# print(date,time)
			# news_date.append(date)
			
			# news_time.append(time)
		except Exception as e:
		    print(logging.exception(e))
		try:
            # print("______________________________________\n")
            # print("STORY:",STORY)
            # print("STORY_LINK:",STORY_LINK)
            # print("STORY_TITLE:",STORY_TITLE)
            # print("IMAGE_LINK:",IMAGE_LINK)
            # print("NEWSDATE:",NEWSDATE)
            # print("NEWSTIME:",NEWSTIME)
            # print("news_category:",news_cat)
            # print("news_cat_id:",news_cat_id)
			if tdate== str(date.today()):
				temp=str(temp[1])+"-"+str(temp[0])
				NEWSDATE=str(temp)+"-"+str(datetime[1])
				if STORY is not None and STORY_TITLE is not None and STORY_LINK is not None and IMAGE_LINK is not None and NEWSDATE is not None and NEWSTIME is not None and news_cat is not None and news_cat_id is not None:
					story.append(STORY)
					story_link.append(STORY_LINK)
					story_title.append(STORY_TITLE)
					img_link.append(IMAGE_LINK)
					news_date.append(NEWSDATE)
					news_time.append(NEWSTIME)
					news_category.append(news_cat)
					cat_id.append(news_cat_id)
			# print(STORY,STORY_LINK,STORY_TITLE,IMAGE_LINK,NEWSDATE,NEWSTIME)
		except Exception as e:
		    print(logging.exception(e))
	# print(len(img_link),len(story_title),len(story_link),len(story),len(news_date),len(news_category))
	zip_list = zip(img_link, story_title, story_link, story,news_date,news_category,cat_id,news_time)
	updateDB(zip_list,table_name)

def gu_scrap(type_name,table_name,news_cat,news_cat_id):
	print("scraping started for : ",news_cat)
	req = requests.get('https://www.vtvgujarati.com/'+type_name+'/',headers=headers)
	page_html = req.content
	page_soup = BeautifulSoup(page_html, 'html.parser')
	divs = page_soup.find_all('div', {'class', 'newsBox'})
	story_link = []
	img_link = []
	story_title = []
	story = []
	news_date=[]
	news_category = []
	news_time=[]
	cat_id = []
	url='None'
	for div in divs:
		try:
			STORY_LINK=None
			IMAGE_LINK=None
			STORY_TITLE=None
			NEWSDATE=None	
			STORY=None
			NEWSTIME=None
			STORY_LINK = div.a['href']
			req = requests.get(STORY_LINK,headers=headers)
			ps = BeautifulSoup(req.content, 'html.parser')
			div_cont = ps.find('div', {'class': 'article-blog cf'})
			# finding title without extra text
			IMAGE_LINK=div_cont.img['src']
			temp = div_cont.h1
			STORY=div_cont.h2.text
			STORY_TITLE=temp.text.strip()
			try:
			    span = temp.span
			    span.extract()
			except:
			    pass
			#finding date of uploaded.
			date_n_time=ps.find('div',attrs={'class':'article-info-blog cf'})
			Date=date_n_time.text.strip()
			Date=Date.split('|')
			Date[0].strip()
			Date=Date[0].split(',')
			time=Date[0].split('\n')[1]
			# print(time)
			Date=Date[1].strip().split(' ')
			Date[2]='20'+Date[2]
			temp_dic={'Jan':'01','Fab':'02','Mar':'03','Apr':'04','May':'05','June':'06','July':'07','Aug':'08','Sept':'09','Oct':'10','Nov':'11','Dec':'12'}
			if Date[1] in temp_dic:
			    Date[1]=temp_dic.get(Date[1]);
			else:
			    print("month abbrevation error ")
			tdate=Date[2]+"-"+Date[1]+"-"+Date[0]

			if tdate==str(date.today()):
			    Date=Date[0]+" "+Date[1]+" "+Date[2]
			    news_date.append(Date)
			    news_category.append(news_cat)
			    cat_id.append(news_cat_id)
			    # print(date,time)
			    news_time.append(time)
			    story_link.append(STORY_LINK)  # link here
			    img_link.append(IMAGE_LINK)  # img here.
			    story.append(STORY) # story here.
			    story_title.append(STORY_TITLE)  # title here.
			else:
				# print("tdate:",tdate)
				pass
		except Exception as e: 
			print(e,"\n",url)
			print("error in ",table_name) 

	zip_list = zip(img_link, story_title, story_link, story,news_date,news_category,cat_id,news_time)
	updateDB(zip_list,table_name)


en_scrap('miscellaneous-news','tbl_news','home_en','23')                   #   en_index():
en_scrap('entertainment-news','tbl_news','entertainment_en','28')          #   en_entertainment():
en_scrap('sports-news','tbl_news','sports_en','26')                        #   en_sports():
en_scrap('technology-news','tbl_news','technology_en','27')                #   en_technology():
en_scrap('trending-news','tbl_news','trending_en','24')                    #   en_trending_news():
en_scrap('business-news','tbl_news','business_en','25')                    #   en_business():
en_scrap('latest-news','tbl_news','latest_en','22')                        #   en_latest_news():
en_scrap('politics-news','tbl_news','politics_en','29')                    #   en_politics():

hi_scrap('national','tbl_news','home_hi','23')                             #   hi_index()
hi_scrap('entertainment','tbl_news','entertainment_hi','28')               #   hi_entertainment():
hi_scrap('sports','tbl_news','sports_hi','26')                             #   hi_sports():
hi_scrap('tech-auto','tbl_news','technology_hi','27')                      #   hi_technology():
hi_scrap('db-original','tbl_news','trending_hi','24')                      #   hi_trending_news():
hi_scrap('business','tbl_news','business_hi','25')                         #   hi_business():
hi_scrap('topics/top/news','tbl_news','latest_hi','22',1)                  #   hi_latest_news():
hi_scrap('topics/politics/news','tbl_news','politics_hi','29',1)           #   hi_politics():

gu_scrap('vtv-vishesh','tbl_news','home_gu','23')                          #   gu_index()
gu_scrap('category/bollywood','tbl_news','entertainment_gu','28')          #   gu_entertainment():
gu_scrap('Sports-News','tbl_news','sports_gu','26')                        #   gu_sports():
gu_scrap('category/tech-auto','tbl_news','technology_gu','27')             #   gu_technology():
gu_scrap('','tbl_news','trending_gu','24')                                 #   gu_trending_news():
gu_scrap('business-news','tbl_news','business_gu','25')                    #   gu_business():
gu_scrap('vtv-vishesh','tbl_news','latest_gu','22')                        #   gu_latest_news():
gu_scrap('category/politics','tbl_news','politics_gu','29')                #   gu_politics():


print("--- %s minutes ---" % ((time.time() - start_time)/60))
