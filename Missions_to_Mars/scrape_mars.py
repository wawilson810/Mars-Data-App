from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_url = "https://redplanetscience.com/"
    images_url = "https://spaceimages-mars.com/"
    facts_url = "https://galaxyfacts-mars.com/"
    hemi_url = "https://marshemispheres.com/"
    
    browser.visit(news_url)
    news_html = browser.html
    news_soup = bs(news_html, 'html.parser')
    news_articles = news_soup.find_all('div', class_ = 'list_text')
    latest_news = news_articles[0]
    news_title = latest_news.find('div', class_='content_title').text
    news_p = latest_news.find('div', class_='article_teaser_body').text

    browser.visit(images_url)
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')
    image = image_soup.find('img', class_='headerimage')
    featured_image_url = images_url + image.get('src')

    browser.visit(facts_url)
    facts_html = browser.html
    facts_soup = bs(facts_html, 'html.parser')
    table_source = facts_soup.find('table', class_ = 'table-striped')
    table_rows = table_source.find_all('tr')
    row_dict = []
    for row in table_rows:
        row_dict.append({'Description':row.th.text, 'Mars':row.td.text.split('\t')[-1]})
    facts_df = pd.DataFrame(row_dict)
    table_html = facts_df.to_html(classes="table table-striped", index=False)

    browser.visit(hemi_url)
    hemi_html = browser.html
    hemi_soup = bs(hemi_html, 'html.parser')
    hemi_blurb = hemi_soup.find_all('div', class_='item')
    hemi_links = []
    for blurb in hemi_blurb:
        link = blurb.find('div', class_='description').a.h3
        hemi_links.append(link.text)
    hemisphere_image_urls = []

    for link in hemi_links:
        browser.links.find_by_partial_text(link).click()
        temp_html = browser.html
        temp_soup = bs(temp_html, 'html.parser')
        
        img = temp_soup.find('img', class_='wide-image').get('src')
        full_url = hemi_url+img
        
        title = temp_soup.find('div', class_='cover').h2.text
        
        hemisphere_image_urls.append({"title":title, "img_url":full_url})
        browser.visit(hemi_url)

    data = {}
    data["news"] = {"title": news_title, "text": news_p}
    data["featured_image"] = featured_image_url
    data["data_table"] = table_html
    data["hemispheres"] = hemisphere_image_urls

    browser.quit()

    return data
