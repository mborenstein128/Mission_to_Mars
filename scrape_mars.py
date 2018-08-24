from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd

def scrape():

    news_url = "https://mars.nasa.gov/news/"
    response = requests.get(news_url)
    soup = bs(response.text, "html.parser")
    
    news_title = soup.find("div", class_="content_title").text

    news_p = soup.find("div", class_="rollover_description_inner").text

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(1)
    browser.click_link_by_partial_text("more info")

    html = browser.html
    soup = bs(html, "html.parser")

    results = soup.find("article")
    extension = results.find("figure", "lede").a["href"]
    base_url = "https://www.jpl.nasa.gov"
    featured_image_url = base_url + extension

    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    weather_html = browser.html
    weather_soup = bs(weather_html, "html.parser")
    mars_weather = weather_soup.find("p", class_="tweet-text").text

    facts_url = "http://space-facts.com/mars/"
    browser.visit(facts_url)
    facts_html = browser.html
    facts_soup = bs(facts_html, "html.parser")
    mars_col1 = facts_soup.find_all("td", class_="column-1")
    mars_col2 = facts_soup.find_all("td", class_="column-2")

    attributes = []
    values = []

    for row in mars_col1:
        attribute = row.text.strip()
        attributes.append(attribute)
        
    for row in mars_col2:
        value = row.text.strip()
        values.append(value)
        
    mars_df = pd.DataFrame({"Attribute":attributes, "Value":values})

    mars_facts = mars_df.to_html(header=False, index=False)

    usgs_base_url = "https://astrogeology.usgs.gov"

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    browser.click_link_by_partial_text("Cerberus")

    cerberus_html = browser.html
    cerberus_soup = bs(cerberus_html, "html.parser")

    cerberus_results = cerberus_soup.find("img", class_="wide-image")["src"]
    cerberus_url = usgs_base_url + cerberus_results

    browser.visit(hemispheres_url)

    browser.click_link_by_partial_text("Schiaparelli")

    schiaparelli_html = browser.html
    schiaparelli_soup = bs(schiaparelli_html, "html.parser")

    schiaparelli_results = schiaparelli_soup.find("img", class_="wide-image")["src"]
    schiaparelli_url = usgs_base_url + schiaparelli_results

    browser.visit(hemispheres_url)

    browser.click_link_by_partial_text("Syrtis")

    syrtis_html = browser.html
    syrtis_soup = bs(syrtis_html, "html.parser")

    syrtis_results = syrtis_soup.find("img", class_="wide-image")["src"]
    syrtis_url = usgs_base_url + syrtis_results

    browser.visit(hemispheres_url)

    browser.click_link_by_partial_text("Valles")

    valles_html = browser.html
    valles_soup = bs(valles_html, "html.parser")

    valles_results = valles_soup.find("img", class_="wide-image")["src"]
    valles_url = usgs_base_url + valles_results

    #extract titles
    cerberus_title = cerberus_soup.find("title").text
    schiaparelli_title = schiaparelli_soup.find("title").text
    syrtis_title = syrtis_soup.find("title").text
    valles_title = valles_soup.find("title").text
    sep = "Enh"
    cerberus_title = cerberus_title.split(sep, 1)[0]
    schiaparelli_title = schiaparelli_title.split(sep, 1)[0]
    syrtis_title = syrtis_title.split(sep, 1)[0]
    valles_title = valles_title.split(sep, 1)[0]

    hemisphere_image_urls = [
    {"title": cerberus_title, "img_url": cerberus_url},
    {"title": schiaparelli_title, "img_url": schiaparelli_url},
    {"title": syrtis_title, "img_url": syrtis_url},
    {"title": valles_title, "img_url": valles_url},
    ]


    mars_data = {}

    mars_data["news_title"] = news_title.strip()
    mars_data["news_paragraph"] = news_p.strip()
    mars_data["featured_image"] = featured_image_url
    mars_data["weather"] = mars_weather
    mars_data["mars_df"] = mars_facts
    mars_data["images"] = hemisphere_image_urls

    return mars_data