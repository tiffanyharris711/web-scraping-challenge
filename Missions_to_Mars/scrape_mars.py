# Dependencies
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    
    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/"

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    news_title = soup.find('div', class_="content_title").find('a').text.strip()

    news_p = soup.find('div', class_="rollover_description_inner").text.strip()

    # Featured Image

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    index = "index.html"
    complete_url = f'{url}{index}'
    browser.visit(complete_url)
    html = browser.html
    img_soup = bs(html, 'html.parser')


    urlb = img_soup.find('img', class_='headerimage fade-in')['src']
    featured_image_url = f'{url}{urlb}'

    # Facts Table

    url = 'https://space-facts.com/mars'
    facts_table = pd.read_html(url)[0].to_html()

    # Mars Hemispheres

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    hemi_soup = bs(html, 'html.parser')


    banners_tag = hemi_soup.find_all('h3')
    banners = [x.text for x in banners_tag]

    hemispheres = []
    for i in range(len(banners)):
        hemisphere = {}
        
        browser.visit(url)
        browser.find_by_css('h3')[i].click()
        hemisphere['title'] = banners[i]
        hemisphere['img_url'] = browser.find_by_text('Sample')['href']
        
        hemispheres.append(hemisphere)
        
        browser.back()

    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'facts_table': facts_table,
        'hemispheres': hemispheres
    }

    browser.quit()

    return mars_data



