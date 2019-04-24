# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup 
import re
import time
import pandas as pd

def scrape():

    # Initial dictionary to store scraping code
	Data_code = {}

    # Initialize executable path for the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    # Scrape "NASA Mars News" website for news info, link given(click on it)
    mars_nasa_url = "https://mars.nasa.gov/news/"

    # Retrieve page with Splinter
    browser.visit(mars_nasa_url)
    time.sleep(2)

    # Create BeautifulSoup object and parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Assign the title and paragraphs so you can reference later.
    news_title_list = []
    news_p_list = []

    # Extract all articles and put into lists
    results = soup.find_all('li', class_='slide')
    for result in results:
            # Error handling
        try:
            # Retrieve news title
            nasa_news_title = result.find('div', class_="content_title").a.text
            # Retrieve news paragraph text
            nasa_news_p = result.find('div', class_="article_teaser_body").text

            # Print results only if title and paragraph text are available
            if (nasa_news_title and nasa_news_p):
                news_title_list.append(nasa_news_title)
                news_p_list.append(nasa_news_p)
        except AttributeError as e:
            print(e)

    # Latest news title
    #news_title = news_title_list[0]
    Data_code['news_title'] = news_title_list[0]
    
    # Latest news paragraph text
    #news_p = news_p_list[0]
    Data_code['news_p'] = news_p_list[0]

#print("Title:",news_title)
#print('-----------------------------------------------------------------------------------------------------------------')
#print("Latest News Details:",news_p)

    # Define URL
    jpl_domain = 'https://www.jpl.nasa.gov'
    jpl_path = '/spaceimages/?search=&category=Mars'
    jpl_url = jpl_domain + jpl_path

    # Use Splinter to open up web browser to main page
    browser.visit(jpl_url)
    time.sleep(2)

    # Open the main image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)

    # Open 'more info' page
    browser.click_link_by_partial_text('more info')
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Obtain URL for featured image(make sure its 'largesize' in URL)
    main_img = soup.find('img', class_="main_image")['src']
    #featured_image_url = jpl_domain + main_img
    #print(featured_image_url)
    Data_code['featured_image_url'] = jpl_domain + main_img_path

    # Scrape "Twitter" website for Mars weather info, link given(click on it)
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with Splinter
    browser.visit(mars_weather_url)
    time.sleep(2)

    # Create BeautifulSoup object and parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve the latest weather news 
    weather_news_list = []
    for weather_news in soup.find_all('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
        weather_news_list.append(weather_news.text)
    
    # Assign the list/dict
    Latest_Mars_Weather = weather_news_list[0]
    #mars_weather_dict = {"mar_weather": Latest_Mars_Weather }
    Data_code['mars_weather_dict'] = mar_weather: Latest_Mars_Weather

    # print mars info
    #print('Latest Mars Weather:',Latest_Mars_Weather)    

    # Import pandas library
    import pandas as pd

    # Generate DataFrame using Pandas to pull html table and put into a list
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_list = pd.read_html(mars_facts_url)

    # Put list into a dataframe and format
    mars_facts_df = mars_facts_list[0]
    mars_facts_df.columns = ['Description', 'Value']
    mars_facts_df.set_index('Description', inplace=True)
    mars_facts_df

    # Convert dataframe into an html 
    #marsfacts_table = mars_facts_df.to_html()
    #marsfacts_table
    Data_code['marsfacts_table'] = marsfacts_df.to_html()

    # Define URL
    usgs_domain = 'https://astrogeology.usgs.gov'
    usgs_path = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    usgs_url = usgs_domain + usgs_path

    # Use Splinter to open up web browser to main page
    browser.visit(usgs_url)
    time.sleep(2)

    # Create BeautifulSoup object and parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Assign images to list so you can reference later.
    hemisphere_image_urls = []

    # Find the images
    results = soup.find('div', class_='collapsible results').\
               find_all('div', class_='item')

    for result in results:
    
        # Go to image page
        go_to = result.find('div', class_='description').a.h3.text
        browser.click_link_by_partial_text(go_to)
        time.sleep(2)
    
        # Retrieve the image url
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        path_to_img = soup.find('img', class_='wide-image')['src']
    
        # Create and Append the dictionary with the image url string and the hemisphere title to a lists
        all_images = {}
        all_images["title"] = re.compile('Enhanced').sub('', go_to).rstrip()
        all_images["img_url"] = usgs_domain + path_to_img
        hemisphere_image_urls.append(all_images)
    
        # Go back to main page
        browser.back()
        time.sleep(2)
    
    #print(hemisphere_image_urls)
    Data_code['hemisphere_image_urls'] = hemisphere_image_urls
	return(Data_code)