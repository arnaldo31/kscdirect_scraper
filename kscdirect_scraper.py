from crawl import log_in
from bs4 import BeautifulSoup
from crawl import product_scraper
from datetime import datetime
import csv
import threading
import time

UserName = 'VOOMSU'
PassWord = 'Voomi1234$'
crawler_speed = 10 # Default is 10 scrape per 5 seconds. change this to 10 + will increase scraping.
max_page = 999999 # you can change on how many pages you like to scrape for each category Default is 999999

savefile = []
savefile_Price = []

def scrape(session,BSoup,url,category):
    ProductInfo,ProductInfoPrice = product_scraper.Product(session=session,BSoup=BSoup,url=url,category=category)
    title = ProductInfo['Title']
    
    if len(title) > 70:
        title = title[:71]
    else:
        for n in range(70-len(title)+1):
            title += ' '
            
    text = f'Category: {category} | Title: {title} | Total: {len(savefile)}'
    print(text)
    savefile.append(ProductInfo)
    
    if 'Price' in ProductInfoPrice.keys():
        savefile_Price.append(ProductInfoPrice)
        
class kscdirect:
    
    def kscdirect_logIn(self):
        self.session = log_in.log_in(username=UserName,password=PassWord)

    def get_categories(self):
        
        main_url = 'https://kscdirect.com/'
        response = self.session.get(main_url)
        soup = BeautifulSoup(response.text,'html.parser')
        #soup.prettify()
        group_links = []
        rows = soup.find_all(class_='row')
        
        for row in rows:
            a_links = row.find_all('a')
            for link in a_links:
                group_url = {'url':'https://kscdirect.com'+link.get('href'),
                             'category':link.text.strip()}
                group_links.append(group_url)

        for group in group_links[1:]:
            self.crawl_category_products(category_url=group)
            self.saving()

    def crawl_category_products(self,category_url:str):
        
        self.category = category_url['category']
        
        # crawl each category
        for page in range(0,max_page):
            #page = 99
            url = category_url['url'] + '&p=' + str(page)
            product_links = self.crawl_pages_products(page_url=url)
            if product_links == []:
                break
            self.scrape_products(product_links=product_links)
        
    def crawl_pages_products(self,page_url:str):
        print(page_url)
        # scrape product links
        product_links = []
        
        # crawl each page
        response = self.session.get(page_url)
        soup = BeautifulSoup(response.text,'html.parser')

        table = soup.find(class_='table table-condensed table-striped')
        if table != None:
            table = table.tbody.find_all('tr')

        if table == [] or table == None:
            return product_links
        
        for tr in table:
            href = 'https://kscdirect.com' + tr.a.get('href')
            product_links.append(href)
        
        return product_links
    
    def scrape_products(self,product_links:list):
        
        links2 = []
        x = crawler_speed
        for i in range(0,len(product_links),x):
            links2.append(product_links[i:i+x])
        
        for links3 in links2:
            start_time = time.time()    
            threads = []
            for url in links3:
                #url = 'https://kscdirect.com/item/90%2BBLK%2B3%252F4/ASC%2BEngineered%2BSolutions_3%252F4%2BBLK%2BMI%2B150%2523%2B90%2BELL'
                th = threading.Thread(target=scrape, args=(self.session,BeautifulSoup,url,self.category,))   
                th.start()
                threads.append(th) 

            for th in threads:
                th.join() # Main thread wait for threads finish
            print("multiple threads took ", (time.time() - start_time), " seconds")
            

    def saving(self):
        current_datetime = datetime.now()
        datetime_string = current_datetime.strftime("%Y_%m_%d")
        
        fieldnames = set()
        for item in savefile:
            fieldnames.update(item.keys())
        fieldnames = list(fieldnames)
        
        self.category = self.category.replace(',','')
        
        # Save all products with info
        with open('.\\save_product\\kscdirect_products_category_{}_{}.csv'.format(self.category,datetime_string),mode='w',encoding='UTF-8',newline='') as file:
            writer = csv.DictWriter(file,fieldnames=fieldnames)
            writer.writeheader()
            for item in savefile:
                writer.writerow(item)
            
            file.close()
                
        # Save all product with price
        with open('.\\save_with_price\\kscdirect_products_category_{}_{}.csv'.format(self.category,datetime_string),mode='w',encoding='UTF-8',newline='') as file:
            writer = csv.DictWriter(file,fieldnames=savefile_Price[0].keys())
            writer.writeheader()
            for item in savefile_Price:
                writer.writerow(item)
            
            file.close()

if __name__ == '__main__':
    kscdirect_scraper = kscdirect()
    kscdirect_scraper.kscdirect_logIn()
    kscdirect_scraper.get_categories()
