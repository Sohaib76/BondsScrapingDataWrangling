
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
path = r'C:\\Users\\Sx\\Documents\\chromedriver_win32\\chromedriver.exe'
browser = webdriver.Chrome(executable_path = path)
browser.implicitly_wait(2)


link = "https://www.investing.com/rates-bonds/world-government-bonds?maturity_from=10&maturity_to=310"
browser.get(link)
browser.maximize_window()

# time.sleep(5)

browser.find_element_by_class_name("login").click()

inputEm = browser.find_element_by_id('loginFormUser_email')
inputEm.send_keys("wonderhaven20@gmail.com")

inputPass = browser.find_element_by_id("loginForm_password")
inputPass.send_keys("waspbeastring12")

div = browser.find_element_by_id("loginPopup")
div.find_element_by_class_name("newButton").click()


time.sleep(4)




tabLen = browser.find_elements_by_tag_name("table")


table_count = 3
for t in range(0,len(tabLen)-1):
    
    tab = browser.find_elements_by_tag_name("table")
    slicedTab = tab[table_count]

    print(slicedTab.text)
    # rowsList = []

    rowsLen = slicedTab.find_elements_by_tag_name("a")
    row_count = 0
    for i in range(0,len(rowsLen)-1):#-1
        time.sleep(2)
        
        tab = browser.find_elements_by_tag_name("table")
        slicedTab = tab[table_count]
        rows = slicedTab.find_elements_by_tag_name("a")
        print(row_count)
        
        sliced = rows[row_count]
    
        

    

        print(sliced.text)
        
        timeout = 3
        try:
            element_present = EC.presence_of_element_located((By.ID, 'rates_bonds_table_51'))
            WebDriverWait(browser, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")
            sliced.click()
 
      
        try:
            myElem = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.ID, 'js_instrument_chart_wrapper')))
            browser.find_element_by_link_text("Historical Data").click()
        except TimeoutException:
            print ("Loading took too much time!")


        

        try:
            
            browser.find_element_by_class_name("js-download-data").click()
        except:
            time.sleep(4)
            
            browser.find_element_by_class_name("js-download-data").click()

       
        browser.execute_script("window.history.go(-2)")

        print("{0} Row completed Of Table {1}".format(row_count,table_count))
        row_count+=1

   
    print("Completed Tables",table_count)
    table_count += 1


exit()


# browser.execute_script("window.scrollTo(0, 400)") 

lk = tab.find_element_by_tag_name("a")
lk.click()


# browser.execute_script("window.scrollTo(0, 500)") 
time.sleep(2)


browser.find_element_by_link_text("Historical Data").click()

time.sleep(4)

browser.find_element_by_class_name("js-download-data").click()

browser.back()
browser.back()

# browser.close()

exit()


















from bs4 import BeautifulSoup
import requests


 
r  = requests.get("https://www.investing.com/rates-bonds/world-government-bonds?maturity_from=10&maturity_to=310")
data = r.text
soup = BeautifulSoup(data, "html5lib")

x = soup.find("table")
print(x)



exit()
#     ll = []
#     for elem in x:
#         ll.append(elem.find("a").get("href"))

#     print(len(ll)) 



#     #--------------------------------------------------

#     from selenium import webdriver
#     import time
#     path = r'C:\\Users\\Sx\\Documents\\chromedriver_win32\\chromedriver.exe'
#     # browser = webdriver.Chrome(executable_path = path)





#     count = 1
#     for link in ll:

        
#         print("Working on Page {0} Product {1}".format(pageNo,count))
#         count += 1

#     # link = "https://www.fragrancenet.com/perfume/coach/coach/eau-de-parfum#289429"

#         browser = webdriver.Chrome(executable_path = path)
#         browser.get(link)

    

#         titlesPerPage = []
#         brandsPerPage = []
#         imgUrlsPerPage = []
#         retailsPerPage = []
#         pricesPerPage = []
#         sizesPerPage = []
#         descsPerPage = []
#         urlsPerPage = []
        
#         sizesBox = browser.find_elements_by_class_name("variantText")
#             #for size in sizesBox:
#             #size.click()
#         sizeLen = len(sizesBox)
#         for sizee in sizesBox:
#             browser.execute_script("window.scrollTo(0, 400)") 

#             sizee.click()

#             try:
#                 size = browser.find_element_by_id('variantInfo')
#                 print(size.text)
#                 sizesPerPage.append(size.text)

#             except:
#                 sizesPerPage.append(" ")
            
#             try:
#                 retailPrice = browser.find_elements_by_id("retailprice")
#                 print(retailPrice[1].text)
#                 retailsPerPage.append(retailPrice[1].text)
#             except:
#                 retailsPerPage.append(" ")

#             try:
#                 price = browser.find_elements_by_class_name("ourPrice")
#                 print(price[1].find_element_by_class_name("price").text)
#                 pricesPerPage.append(price[1].find_element_by_class_name("price").text)
#             except:
#                 pricesPerPage.append(" ")
            
            
#             try:
#                 imgUrl = browser.find_element_by_class_name("mainProductImage").get_attribute("src")
#                 print(imgUrl)
            
#                 imgUrlsPerPage.append(imgUrl)
#             except:
            
#                 imgUrlsPerPage.append(" ")

            

        

#             urlsPerPage.append(link)


#         try:
#             title = browser.find_element_by_class_name("productTitle")
#             print(title.text)
#             for i in range(0,sizeLen):
#                 titlesPerPage.append(title.text)
#         except:
#             for i in range(0,sizeLen):
#                 titlesPerPage.append(" ")

#         try:
#             brand = browser.find_element_by_class_name("uDesigner")
#             brnd = brand.find_element_by_tag_name("a").text
#             print(brnd)
#             for i in range(0,sizeLen):
#                 brandsPerPage.append(brnd)
#         except:
#             for i in range(0,sizeLen):
#                 brandsPerPage.append(" ")


#         #print(imgUrlsPerPage)


    
        
#         # print(size.text)
#         # sizesPerPage.append(size.text)
#         #except:
#         #    print("asmfkmmfa")





#         browser.execute_script("window.scrollTo(0, 1000)") 
#         time.sleep(4)

        
        
#         xx  = browser.find_elements_by_tag_name("a")
#         try:
#             for i in xx:
#                 if i.get_attribute("href") == "https://www.fragrancenet.com/#productDescription":
#                     i.click()
        

#             desc = browser.find_element_by_class_name("lpdesc")
#             print(desc.text)
#             for i in range(0,sizeLen):
#                 descsPerPage.append(desc.text)
#         except:
#             for i in range(0,sizeLen):
#                 descsPerPage.append(" ")

    
#         browser.close()
    

#     #--------------------

#         womenFragnence = open("uniFrag.csv","a+")
#         for a,b,c,d,e,f,g,h in zip(urlsPerPage, titlesPerPage,brandsPerPage,sizesPerPage,pricesPerPage,retailsPerPage,imgUrlsPerPage,descsPerPage):
#             womenFragnence.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(a,b,c,d,e,f,g,h))
#     womenFragnence.close() 

#     pageNo += 1


# exit()





