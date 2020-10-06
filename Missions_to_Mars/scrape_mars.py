from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

def init_browser():
    # Set the path for the chromedriver.exe file and select the browser used
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():

    browser = init_browser()
    data = {}

    # URL of page to be scraped (NASA Mars News Site)
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    # Extract the text of the  latest news title and clean it up
    data["news_title"] = browser.find_by_css(".grid_gallery.list_view .content_title a").text

    # Extract the text of the latest news paragraph and clean it up
    data["news_p"] = browser.find_by_css('div[class="article_teaser_body"]').text

    # -------------------------------------------
    # launch the browser and opens the url for the current Featured Mars Image
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    # navigates the site and finds the image url for the current Featured Mars Image
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text("more info")

    # Extract and assign the url string to a variable
    data["featured_image_url"] = browser.find_by_css('figure[class="lede"] img')["src"]

    # --------------------------------------------
    # URL of page to be scraped for the mars table facts
    url_table = "https://space-facts.com/mars/"

    # Automatically scrape any tabular data from a page
    tables = pd.read_html(url_table)
    
    # Select the first Df from a list od Dfs and rename the column names
    df = tables[0]
    df.rename(columns = {0:"Description", 1:"Value"}, inplace = True)
    
    # Generating a HTML tables from DataFrame and saving it directly to a file
    data["html_table"] = df.to_html()
    
    # ---------------------------------------------
    # URL of page to be scraped for the Mars Hemispheres pictures
    url3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url3)

    #  delay to get the web page loaded
    time.sleep(3)

    # Locating the titles, and storing them into list, as a strings
    titles_object = browser.find_by_tag('h3')
    titles = []
    for x in titles_object:
        titles.append(x.text)
    

    # Creating empty list that will store the image urls
    hemisphere_image_urls = []

    # iterating through the titles list, clicking the title link, and opening the coresponding page and retrieving the link
    for title in titles:
    
        my_dict = {}
        my_dict["title"] = title
        browser.click_link_by_partial_text(title)
        my_dict["img_url"] = browser.find_by_text("Original")['href']
    
        hemisphere_image_urls.append(my_dict)
        browser.back()
     
    data["hemisphere_image_urls"] = hemisphere_image_urls

    return data

# print(scrape())