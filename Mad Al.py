#!/usr/bin/env python
# coding: utf-8

# In[13]:


import requests
import time
from lxml import html

import pandas as pd


# In[14]:


#helper functions
def extract_source(url, headers):

    source=requests.get(url, headers=headers)
    tree = html.fromstring(source.content)
    #product_container_urls = tree.xpath(product_url_xpath)
    return tree


# In[15]:


#scraper header
headers = {'Host': 'madal.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 12105.75.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.102 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'http://madal.com/internet-retailer-products/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9'
    }


# In[16]:


#This URL will be the URL that your login form points to with the "action" tag.
POST_LOGIN_URL = "https://madal.com/login.php?action=check_login" #https://madal.com/login.php?action=check_login 
#This URL is the page you actually want to pull down with requests.
REQUEST_URL = 'http://madal.com/internet-retailer-products/'


# In[17]:


payload = {
    "login_email": "patrick@drcommerceshop.com",
    "login_pass": "mynameismypassword1"
}


# In[20]:


base_url = 'http://madal.com/internet-retailer-products/?sort=alphaasc&page='
max_page = 389

page_url_list = []
for i in range(1, max_page):
    page_url_list.append(base_url + str(i))
    
url_set = page_url_list[125:max_page]
url_set


# In[21]:


product_title_xpath = '/html/body/div[3]/div[1]/div/div[1]/section[1]/div/h1/text()'
product_url_xpath = '//*[@id="product-listing-container"]/form[2]/ul/li/article/div/h4/a/@href'

#product page xpaths
product_title_xpath = "//*[@class='productView-title']/text()"
product_price_xpath = "//*[@class='productView-product']//span[@class='price price--withoutTax']/text()"
product_sku_xpath = "//*[@class='productView-info-value'][1]/text()"
product_upc_xpath = "//*[@class='productView-info-value'][2]/text()"
product_instock_al_xpath = "//*[@class='productView-info-value'][4]/text()"
product_instock_ky_xpath = "//*[@class='productView-info-value'][5]/text()"
product_img_xpath = "//*[@class='productView-thumbnail-link']/img/@src"


# In[ ]:


output_df = pd.DataFrame()

title_list = []
upc_list = []
price_list = []
in_stock_al_list = []
in_stock_ky_list = []
img_list = []
url_list = []

with requests.Session() as session:
    
    #### login ###
    post = session.post(POST_LOGIN_URL, data = payload)
    #get page source
    
    #for page in page_url_list:
    for page in url_set:
        
        source = session.get(page, headers = headers)
        tree = html.fromstring(source.content)
    
        #get product page urls
        skus_urls = tree.xpath(product_url_xpath)
        print(page)
        print(skus_urls)
        
        for url in skus_urls:
            single_item_source = session.get(url, headers=headers)
            single_item_tree = html.fromstring(single_item_source.content)
            
            single_item_title = single_item_tree.xpath(product_title_xpath)
            single_item_upc = single_item_tree.xpath(product_upc_xpath)
            single_item_price = single_item_tree.xpath(product_price_xpath)
            single_item_stock_al = single_item_tree.xpath(product_instock_al_xpath)
            single_item_stock_ky = single_item_tree.xpath(product_instock_ky_xpath)
            single_item_img = single_item_tree.xpath(product_img_xpath)
            
            title_list.append(single_item_title)
            upc_list.append(single_item_upc)
            price_list.append(single_item_price)
            in_stock_al_list.append(single_item_stock_al)
            in_stock_ky_list.append(single_item_stock_ky)
            img_list.append(single_item_img)
            url_list.append(url)
            
            print(url)
            #pause for 500ms
            time.sleep(.500)
            
        


# In[24]:


d = {'title':title_list,'price':price_list,'upc':upc_list,'in stock ky':in_stock_ky_list,
    'in stock al':in_stock_al_list,'image':img_list, 'product url':url_list}
output_df = pd.DataFrame(d)
output_df
#final_df = pd.DataFrame(title_list, price_list, upc_list, in_stock_al_list, in_stock_ky_list, img_list)


# In[25]:


output_df.to_csv('/home/patrick/Downloads/madal_partial_08072019_2.csv')


# In[23]:





# # everything below is not used

# In[ ]:




    #for page in sku_urls:
    #first product group page
    #page_source = session.get(test_url, headers = headers)
    #page_tree = html.fromstring(page_source.content)
    
    #title = tree.xpath(product_title_xpath)
    
    #print(tree)
   #product_group_page_urls = tree.xpath(product_url_xpath)
    
    #single_product_page = product_group_page_urls[0]
    #print(single_product_page)
    
    #single_product_source = session.get(single_product_page, headers = headers)
    #single_product_tree = html.fromstring(single_product_source.content)
    
    #single_product_title = single_product_tree.xpath(product_title_xpath)
    
    #print(single_product_tree)
    #print(single_product_title)


# In[ ]:


#GET page info at category level
#print(REQUEST_URL)
#r = requests.get(REQUEST_URL)
#tree = html.fromstring(r.content)

#product_df = pd.DataFrame(columns = ["title","sku","upc","price"])

for page_url in page_url_list:
    r = requests.get(page_url)
    tree = html.fromstring(r.content)
    
    product_container_urls = tree.xpath(product_url_xpath)
    print(page_url)
    print(tree)
    for url in product_container_urls:
        print(url)
        #df = pd.DataFrame(columns = ["title","sku","upc","price"])

    #    r=requests.get(url)
    #    tree = html.fromstring(r.content)

    #    title = tree.xpath(product_title_xpath)
        #sku = tree.xpath(product_sku_xpath)
        #if sku == []:
        #    sku = 0
        #else:
        #sku = tree.xpath(product_sku_xpath)
        #if upc == []:
        #    upc = 0
        #else:
        #upc = tree.xpath(product_upc_xpath)
        #price = tree.xpath(product_price_xpath)

        #if not upc:
        #    upc = ['0']
        #if not sku:
        #    sku = ['0']

        #df['title'] = title
        #df['sku'] = sku
        #df['upc'] = upc
        #df['price'] = price

        #print(url)
        #print(title)
        #print(sku)
        #print(upc)
        #print(price)
        
        #product_df = product_df.append(df)

#product_df


# In[ ]:


#product_url_xpath = '//*[@id="product-listing-container"]//a/@href'

single_url = page_url_list[0]
print(single_url)



with requests.Session() as session:

    post = session.post(POST_LOGIN_URL, data=payload)
    test_r = session.get(single_url, headers = headers)
    print(test_r.content.decode()) #print(result.content.decode())
    #test_tree = html.fromstring(test_r.content)

    #print(test_tree)
    #test_urls = test_tree.xpath(product_url_xpath)
    
    #test_urls


# In[ ]:





# In[ ]:


product_df
product_df.to_csv('/home/patrick/Downloads/empire_discount.csv')


# In[ ]:




