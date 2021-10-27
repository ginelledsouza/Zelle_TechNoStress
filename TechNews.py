from bs4 import BeautifulSoup
import requests
import pandas as pd

Image = []
News = []
NewsDetailed = []

def NewsScrapper(url):
    
    r = requests.get(url)
    s = BeautifulSoup(r.content, 'html.parser')
    
    ImageDetails = s.find_all('div',{'class':'thumb'})
    ImageDetails = s.find_all('img')
    ImageDetails = [pt['src'] for pt in ImageDetails]
    
    for i in ImageDetails[3:6]:
        Image.append(i)
        
    NewsDetails = s.find_all('div',{'class':'caption'})
    NewsDetails = [pt.get_text() for pt in NewsDetails]

    for i in NewsDetails[:3]:
        News.append(i)   
        
    Detailed = s.find_all('div',{'class':'nlist bigimglist'})
    Detailed = Detailed[0].find_all('a')
    Detailed = [pt['href'] for pt in Detailed]

    for i in Detailed[:3]:
        NewsDetailed.append(i)  
        
NewsScrapper('https://gadgets.ndtv.com/mobiles')
NewsScrapper('https://gadgets.ndtv.com/laptops')
NewsScrapper('https://gadgets.ndtv.com/tablets')        

TechnicalNews = pd.DataFrame({'Image URL':Image,'Headlines':News,'Detailed':NewsDetailed})
TechnicalNews.drop_duplicates('Headlines',inplace=True)
TechnicalNews = TechnicalNews.sample(frac=1).reset_index(drop=True)
TechTuple = []

for row in range(len(TechnicalNews)):
    record = []
    for col in TechnicalNews.columns:
        record.append(TechnicalNews[col][row])
    TechTuple.append(record)

TechnicalNews = TechTuple

#TRENDING NEWS

Image = []
News = []
NewsDetailed = []

def TopNewsScrapper(url):
    
    r = requests.get(url)
    s = BeautifulSoup(r.content, 'html.parser')
    
    ImageDetails = s.find_all('td',{'class':'pdt15'})
    ImageDetails = s.find_all('img',{'class':'trend_img_brd'})
    ImageDetails = [pt['src'] for pt in ImageDetails]
    
    for i in ImageDetails:
        Image.append(i)
        
    NewsDetails = s.find_all('p',{'class':'trenz_news_head lh22 listing_story_title'})
    NewsDetails = [pt.get_text() for pt in NewsDetails]

    for i in NewsDetails:
        News.append(i)  
        
    Detailed = s.find_all('p',{'class':'trenz_news_head lh22 listing_story_title'})
    DetailedLink = []
    
    DetailedLink = [ i.find_all('a')[0] for i in Detailed]  
    Detailed = [pt['href'] for pt in DetailedLink]

    for i in Detailed:
        NewsDetailed.append(i)  
        
TopNewsScrapper('https://www.ndtv.com/trends/most-popular-gadgets-news')   

TopTechnicalNews = pd.DataFrame({'Image URL':Image,'Headlines':News,'Detailed':NewsDetailed})
TopTechnicalNews.drop_duplicates('Headlines',inplace=True)
TopTechnicalNews = TopTechnicalNews.sample(frac=1).reset_index(drop=True)
TopTechnicalNews = TopTechnicalNews[:5]
TopTechnicalNews.drop_duplicates('Headlines',inplace=True)
TopTechnicalNews = TopTechnicalNews.sample(frac=1).reset_index(drop=True)
TopTechTuple = []

for row in range(len(TopTechnicalNews)):
    record = []
    for col in TopTechnicalNews.columns:
        record.append(TopTechnicalNews[col][row])
    TopTechTuple.append(record)

TopTechnicalNews = TopTechTuple