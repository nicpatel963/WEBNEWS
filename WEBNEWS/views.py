
from bs4 import BeautifulSoup
from urllib.request import urlopen
from django.http import HttpResponse
from django.shortcuts import render
from googletrans import Translator
translator = Translator()


def index(request):
    login_data = request.POST.dict()
    lang = login_data.get("lang")
    req = urlopen('https://www.indiatoday.in/')
    page_html = req.read()
    page_soup = BeautifulSoup(page_html, "html.parser")
    ul_data = page_soup.find('ul', {'class': 'itg-listing'})
    li_data = ul_data.findAll('li')
    li_title = []
    a_href = []
    for li in li_data:
        if lang:
            li["title"] = translator.translate(li["title"], dest=lang).text
        li_title.append(li["title"])
        a_href.append("https://www.indiatoday.in" + li.a["href"])

    param = {'param': {li_title[i]: a_href[i] for i in range(len(li_title))}}

    return render(request, 'index.html', param)


def sport(request):
    login_data = request.POST.dict()
    lang = login_data.get("lang")
    req = urlopen('https://indianexpress.com/section/sports/')
    page_html = req.read()
    page_soup = BeautifulSoup(page_html, "html.parser")
    story_link = []
    story_title = []
    img_src = []
    section = page_soup.main.find('section', {'class': 'o-listing o-listing--latest o-listing--last'})
    div = section.find('div', {'class': 'o-listing__items o-listing__items--tight'})
    div2 = div.find('div', {'class': 'a-pt5'})
    div3 = div2.findAll('div', {'class': 'l-grid__item l-grid__item--divided'})

    for d in div3:
        link_div = d.find('div', {'class': 'm-article-landing__inner'})
        story_link.append(link_div.a['href'])
        if lang:
            link_div.a['title'] = translator.translate(link_div.a['title'], dest=lang).text
        story_title.append(link_div.a['title'])
        img_div = d.find('div', {'class': 'article-thumb m-article-landing__thumb'})
        img_src.append(img_div.img['data-src'])

    zip_list = zip(img_src, story_title, story_link)
    param = {'zip_list': zip_list}

    return render(request, 'sport.html', param)


def technology(request):
    login_data = request.POST.dict()
    lang = login_data.get("lang")
    req = urlopen('https://www.indiatoday.in/technology/')
    page_html = req.read()
    page_soup = BeautifulSoup(page_html, "html.parser")
    ul_data = page_soup.find('ul', {'class': 'itg-listing'})
    li_data = ul_data.findAll('li')
    li_title = []
    a_href = []
    for li in li_data:
        if lang:
            li["title"] = translator.translate(li["title"], dest=lang).text
        li_title.append(li["title"])
        a_href.append("https://www.indiatoday.in" + li.a["href"])

    param = {'param': {li_title[i] : a_href[i] for i in range(len(li_title))}}

    return render(request, 'technology.html', param)


def trending_news(request):
    login_data = request.POST.dict()
    lang = login_data.get("lang")

    req = urlopen('https://www.indiatoday.in/trending-news/')
    page_html = req.read()
    page_soup = BeautifulSoup(page_html, "html.parser")
    div_all = page_soup.findAll('div', {'class': 'catagory-listing'})
    img_src = []
    story_title = []
    story_link = []
    for div in div_all:
        pic_div = div.find('div', {'class': 'pic'})
        detail_div = div.find('div', {'class': 'detail'})
        img_src.append(pic_div.img['src'])
        if lang:
            detail_div.h2['title'] = translator.translate(detail_div.h2['title'], dest=lang).text
        story_title.append(detail_div.h2['title'])
        story_link.append('https://www.indiatoday.in' + detail_div.a['href'])

    zip_list=zip(img_src,story_title,story_link)
    param={'zip_list':zip_list}

    return render(request, 'trending_news.html', param)


def binge_watch(request):
    login_data = request.POST.dict()
    lang = login_data.get("lang")

    req = urlopen('https://www.indiatoday.in/binge-watch/')
    page_html = req.read()
    page_soup = BeautifulSoup(page_html, "html.parser")
    div_all = page_soup.findAll('div', {'class': 'catagory-listing'})
    img_src = []
    story_title = []
    story_link = []
    for div in div_all:
        pic_div = div.find('div', {'class': 'pic'})
        detail_div = div.find('div', {'class': 'detail'})
        img_src.append(pic_div.img['src'])
        if lang:
            detail_div.h2['title'] = translator.translate(detail_div.h2['title'], dest=lang).text
        story_title.append(detail_div.h2['title'])
        story_link.append('https://www.indiatoday.in' + detail_div.a['href'])

    zip_list=zip(img_src,story_title,story_link)
    param={'zip_list':zip_list}

    return render(request, 'binge_watch.html', param)


def fact_check(request):
    login_data = request.POST.dict()
    lang = login_data.get("lang")

    req = urlopen('https://www.indiatoday.in/fact-check/')
    page_html = req.read()
    page_soup = BeautifulSoup(page_html, "html.parser")
    div_all = page_soup.findAll('div', {'class': 'catagory-listing'})
    img_src = []
    story_title = []
    story_link = []
    for div in div_all:
        pic_div = div.find('div', {'class': 'pic'})
        detail_div = div.find('div', {'class': 'detail'})
        img_src.append(pic_div.img['src'])
        if lang:
            detail_div.h2['title'] = translator.translate(detail_div.h2['title'], dest=lang).text
        story_title.append(detail_div.h2['title'])
        story_link.append('https://www.indiatoday.in' + detail_div.a['href'])

    zip_list = zip(img_src,story_title,story_link)
    param = {'zip_list': zip_list}

    return render(request, 'fact_check.html', param)


def business(request):
    login_data = request.POST.dict()
    lang = login_data.get("lang")

    req = urlopen('https://www.indiatoday.in/business/')
    page_html = req.read()
    page_soup = BeautifulSoup(page_html, "html.parser")
    div_all = page_soup.findAll('div', {'class': 'catagory-listing'})
    img_src = []
    story_title = []
    story_link = []
    for div in div_all:
        pic_div = div.find('div', {'class': 'pic'})
        detail_div = div.find('div', {'class': 'detail'})
        img_src.append(pic_div.img['src'])
        if lang:
            detail_div.h2['title'] = translator.translate(detail_div.h2['title'], dest=lang).text
        story_title.append(detail_div.h2['title'])
        story_link.append('https://www.indiatoday.in' + detail_div.a['href'])

    zip_list = zip(img_src, story_title, story_link)
    param = {'zip_list':zip_list}

    return render(request, 'fact_check.html', param)


def world(request):
    login_data = request.POST.dict()
    lang = login_data.get("lang")
    req = urlopen('https://www.indiatoday.in/world/')
    page_html = req.read()
    page_soup = BeautifulSoup(page_html, "html.parser")
    div_all = page_soup.findAll('div', {'class': 'catagory-listing'})
    img_src = []
    story_title = []
    story_link = []
    for div in div_all:
        pic_div = div.find('div', {'class': 'pic'})
        detail_div = div.find('div', {'class': 'detail'})
        img_src.append(pic_div.img['src'])
        if lang:
            detail_div.h2['title'] = translator.translate(detail_div.h2['title'], dest=lang).text
        story_title.append(detail_div.h2['title'])
        story_link.append('https://www.indiatoday.in' + detail_div.a['href'])

    zip_list = zip(img_src, story_title, story_link)
    param = {'zip_list':zip_list}

    return render(request, 'world.html', param)


def latest(request):
    login_data = request.POST.dict()
    lang = login_data.get("lang")
    req = urlopen('https://www.shortpedia.com/en-in/latest-news/')
    page_html = req.read()
    page_soup = BeautifulSoup(page_html, "html.parser")
    src = page_soup.findAll('h3', {'itemprop': 'headline'})
    src = src[0:10]
    story_link = []
    img_link = []
    story_title = []
    story = []

    for link in src:
        story_link.append(link.a['href'])
        req = urlopen("https:" + link.a['href'])
        page_html = req.read()
        page_soup = BeautifulSoup(page_html, "html.parser")
        img = page_soup.find('img', {'itemprop': 'url'})
        img_link.append(img['src'])
        info = page_soup.find('p', {'itemprop': 'articleBody'})
        info_title = page_soup.find('h1', {'itemprop': 'headline'})
        info_text = info.text
        info_title_a_text = info_title.a.text
        if lang:
            info_text = translator.translate(info_text, dest=lang).text
            info_title_a_text = translator.translate(info_title_a_text, dest=lang).text
        story.append(info_text)
        story_title.append(info_title_a_text)

    zip_list = zip(img_link, story_title, story_link, story)
    param = {'zip_list': zip_list}

    return render(request, 'latest.html', param)

