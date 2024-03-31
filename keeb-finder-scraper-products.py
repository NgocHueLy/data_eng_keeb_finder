from urllib.request import urlopen as uReq
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup as soup
import pandas as pd
from datetime import datetime
import re


#### GET NUMBERS OF PAGES
my_url = "https://keeb-finder.com/keyboards"

# opening up connection, grabbing the page
uClient = uReq(my_url)
starting_page_html = uClient.read()
uClient.close()

# html parsing
starting_page_soup = soup(starting_page_html, "html.parser" )


# find last page
last_page = starting_page_soup.find("ul",{"class":"MuiPagination-ul my-nhb8h9"}).find_all("a")[-2]["aria-label"].split()[-1]

# number of keyboards found:
num_keyboard = re.search('\d+',starting_page_soup.h2.text).group()
df_num_keyboards = pd.DataFrame(columns=['number_of_keyboards'])
df_num_keyboards['number_of_keyboards']=num_keyboard

#### CREATE DATAFRAME HEADER:

# header for category page:
cate_headers = ["cate_product_title", "cate_pirce", "cate_vendor", "cate_voucher", "cate_new_tag", "listing_link"]

# header for technical specifications table:

listing_url = "https://keeb-finder.com/keyboards/irok-iyx-mu68"

uClient = uReq(listing_url)
listing_page_html = uClient.read()
uClient.close()

listing_soup = soup(listing_page_html, "html.parser" )

tech_spec_headers = [i.text.strip().strip(":") for i in listing_soup.findAll("div",{"class":"min-w-[200px]"})]


#### CREATE DATAFRAME FOR PRODUCT-DETAIL AND PURCHASE-OPTION

product_headers = cate_headers + ["listing_link"] + tech_spec_headers
df_product = pd.DataFrame(columns=product_headers)


purchase_headers = ['listing_title','Vendor', 'Location', 'In Stock', 'Coupon Code', 'Price (USD)', 'Link*']
df_purchase = pd.DataFrame(columns=purchase_headers)


#### SCRAPE EACH PAGE:

missing_info_products = []
product_values = []
purchase_values = []
err_listing_links = []

# loop through all keyboard category pages:
for i in range(1, int(last_page) + 1):
    
    #define each page url:
    url = f"https://keeb-finder.com/keyboards?page={i}" 
    
    # opening up connection, grabbing the page
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    # html parsing
    page_soup = soup(page_html, "html.parser" )

    # grab all products in the page
    products = page_soup.find_all("figure",{"class":"min-h-[150px] relative m-0 p-0 mb-0.25"})

    
    ### FOR PRODUCTS
    
    for product in products:
        
        ########### GRAB DATA IN CATEGORY PAGE (VALUES)

        # get link for detail product listing:
        listing_link = f"https://keeb-finder.com" + product.figcaption.a["href"]

        

        # get product title:
        cate_product_title = product.figcaption.a.text

        # get price:
        cate_price = product.find("span",{"class":"text-gray-100 font-medium"}).text

        # get vendor name:
        cate_vendor = product.find("span",{"class":"hidden md:inline"}).next_sibling

        
        # get "New" tag if there is otherwise None
        cate_has_new = len(product.find_all("div",{"class":"absolute top-2 left-2 z-10 rounded bg-primary-500 text-white text-xs tracking-wide py-1 px-2"}))
        if cate_has_new > 0:
            cate_new_tag = product.find("div",{"class":"absolute top-2 left-2 z-10 rounded bg-primary-500 text-white text-xs tracking-wide py-1 px-2"}).text
        else:
            cate_new_tag = "None"

        
        # get "voucher" tag if there is otherwise None
        cate_has_voucher = len(product.find_all("span",{"class":"font-medium text-body2 flex items-center bg-[rgb(193,145,11)] p-1 rounded-md text-white text-center z-20 mb-1"}))

        if cate_has_voucher > 0:
            cate_voucher = product.find("span",{"class":"font-medium text-body2 flex items-center bg-[rgb(193,145,11)] p-1 rounded-md text-white text-center z-20 mb-1"}).text
            cate_voucher = float(cate_voucher.strip('%'))/100.0        
        else:
            cate_voucher = "None"
        
        
        

        
        # category Values:
        cate_values = [cate_product_title, cate_price, cate_vendor, cate_voucher, cate_new_tag, listing_link] 
    
        
        
        
        ########## SCRAPE DATA FROM PRODUCT LISTING PAGE

        ###### GRAB TECHNICAL SPECIFICATIONS

        # create connection to listing link:
    
        # opening up connection, grabbing the page
                
        try:
            uClient = uReq(listing_link.encode('ascii', 'ignore').decode('ASCII')) #ignoe chinese/ trademark character in listing_link
        
        except HTTPError:
            err_listing_links.append(listing_link)
            
        else: 
            listing_page_html = uClient.read()
            uClient.close()

        # lising link parser:
        listing_soup = soup(listing_page_html, "html.parser" )

        
        # initial technical specification values

        tech_spec_values = [i.text for i in listing_soup.findAll("div",{"class":"flex items-center space-x-4"})]

        
        # find and replace icons in product details to Yes, No:
        #### first 5 icons are icons of product details:
        
        icons = listing_soup.findAll("svg",{"class":"MuiSvgIcon-root MuiSvgIcon-fontSizeMedium max-w-[16px] max-h-[16px] my-vubbuv"})[0:5]
        icon_text =  [icon["data-testid"] for icon in icons] 
        icon_meanings = []
        for i in icon_text:
            if i == "CheckIcon":
                icon_meanings.append("Yes")
            else:
                icon_meanings.append("No")

        ####  replace icons by Yes/No:
        j = 0
        for i in range(6,11):
            tech_spec_values[i] = icon_meanings[j]
            j += 1
        

        ############# GRAB PURCHASE OPTIONS TABLE
        
        purchase_table = listing_soup.find_all("table",{"class":"MuiTable-root my-iklbb0"})[0]
        
        for i, row in enumerate(purchase_table.find_all('tr',{"class":"MuiTableRow-root my-z7wom4"})):
            combine_row =[listing_link] + [el.text.strip() for el in row.find_all('td')]
            purchase_values.append(combine_row)
    
        
        ############# ADD DATA TO PRODUCT_VALUES 
        
        # combine values from category pages, listing link, technical specification table:
        
        product_value = cate_values + [listing_link] + tech_spec_values

        # avoid missing data, listing in missing_info_poroducts will be check and add manually to final dataframe
        if len(product_headers) != len(product_value):
            missing_info_products.append(listing_link)            
        else:
            product_values.append(product_value)
    
    print(f"finish scraping {url}")

# ADD ROWS TO PRODUCT DATAFRAME

for product_value in product_values:
    df_product.loc[len(df_product)] = product_value


# ADD ROWS TO PURCHASE DATAFRAME
    
for purchase_value in purchase_values:    
    df_purchase.loc[len(df_purchase)]=purchase_value   

# DATAFRAME FOR MANUALLY ADDING PRODUCTS:
df_missing = pd.DataFrame(columns=['listing_link'])
for missing_info_product in missing_info_products:
    df_missing.loc[len(df_missing)]=missing_info_product

# DATAFRAME FOR ERROR LINKS:
df_err = pd.DataFrame(columns=['error_link'])
for err_listing_link in err_listing_links:
    df_missing.loc[len(df_err)] = err_listing_link


# add scraping date to dataframes:

current_date = datetime.now().strftime("%Y-%m-%d")
df_missing['scraping_date'] = current_date
df_num_keyboards['scraping_date'] = current_date
df_product['scraping_date'] = current_date
df_purchase['scraping_date'] = current_date
df_err['scraping_date'] = current_date

# Export csv
path=r"D:/1_projects/keeb_finder/csv/"
product_filename = f"product_{current_date}.csv"
df_product.to_csv(path+product_filename, index=False)

purchase_filename = f"purchase_{current_date}.csv"
df_purchase.to_csv(path+purchase_filename, index=False) 

missing_filename = f"missing_{current_date}.csv"
df_missing.to_csv(path+missing_filename, index=False) 