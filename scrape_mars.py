# Imports
import requests
import time
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd


def scrape():
        
    # Scrape Mars News
    url = 'https://mars.nasa.gov/news/'
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=True)
    browser.visit(url)
    soup = BeautifulSoup(browser.html, 'html.parser')
    news_title = soup.find_all(class_='content_title')[0].get_text()
    news_p = soup.find_all(class_='article_teaser_body')[0].get_text()


    # Scrape Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    soup = BeautifulSoup(browser.html, 'html.parser')
    featured_image_url = 'https://www.jpl.nasa.gov/' + \
        soup.find_all(class_='button fancybox')[0]['data-fancybox-href']


    # Scrape Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    soup = BeautifulSoup(browser.html, 'html.parser')
    mars_weather = ''
    for item in soup.find_all(class_='tweet-text'):
        tweet_text = item.get_text()
        if ('sol' in tweet_text) and ('high' in tweet_text) and ('low' in tweet_text):
            mars_weather = tweet_text
            break



    # Scrape images
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    soup = BeautifulSoup(browser.html, 'html.parser')
    hemisphere_image_urls = []
    base_url='https://astropedia.astrogeology.usgs.gov'
    for item  in soup.find_all(class_='description'):
        img_url = base_url  + item.find('a')['href'] + '.tif/full.jpg'
        img_url = img_url.replace('search/map', 'download')
        title = item.find('a').find('h3').get_text()
        hemisphere_image_urls.append({
            'title': title,
            'img_url': img_url
        })

    scraped_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_weather': mars_weather,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    return scraped_data

if __name__ == "__main__":
    data = scrape()
    print(data)