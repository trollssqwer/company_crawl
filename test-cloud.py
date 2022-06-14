import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
from selenium.webdriver.firefox.options import Options
import traceback 

global download_dir,chrome_driver,page_link,company_id_dir
download_dir = "/home/ec2-user/thong/PDF-list/"
chrome_driver = '/bin/chromedriver'
page_link = "https://bocaodientu.dkkd.gov.vn/"
company_id_dir = "/home/ec2-user/thong/company_list_100"

def set_up(url):
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("start-maximized") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.default_content_settings.popups": 0,
                    "download.default_directory": download_dir, #DOWNLOAD DIRECTORY
                    "directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_driver ,chrome_options=options)
    # Open URL
    driver.get(url)
    return driver

def get_page_pdf(src):
    list_pdf_id = re.findall(r"ctl00_C_CtlList_ctl\d+_LnkGetPDFActive", str(src))
    for pdf_id in list_pdf_id:
        element = driver.find_element(By.ID, value=pdf_id)
        #print("a")
        element.click()
        time.sleep(0.5)

def get_multiple_page(x):
    for i in range(2,x):
        page = driver.find_element(By.XPATH, value="//a[text()='" +str(i)+ "']")
        print(page.text)
        page.click()
        time.sleep(5)
        src = driver.page_source
        get_page_pdf(src)   


def get_company_by_id(id):
    title_page = driver.title
    print(title_page)
    src = driver.page_source
    print(src)
    input_search = driver.find_element(By.ID , value="ctl00_FldSearch")
    input_search.clear()
    input_search.send_keys(id)
    time.sleep(1)
    #input_location = input_search.location
    #print(input_location)

    #divRegister = driver.find_element(By.ID , value="linkRegister")

    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(input_search, 100, 30).click().perform()
    print("click tab")
    time.sleep(3)
    print("click OK")
    try:
        title_page = driver.title
        print(title_page)
        print(driver.current_url)
        
        src = driver.page_source
        print(src)
        pdf_tab = driver.find_element(By.ID ,value="ctl00_C_LnkTab2")
        pdf_tab.click()
        print("click OK")
        time.sleep(2)
        pdf_button = driver.find_element(By.ID ,value="ctl00_C_CtlList_ctl02_LnkGetPDFActive")
        pdf_button.click()
        time.sleep(2)
        lastest_download = latest_download_file()
        new_file = os.path.join(download_dir, str(id)+".pdf")
        os.rename(lastest_download, new_file)
        #print(test)
        time.sleep(1)
        driver.get(page_link)

    except: 
        traceback.print_last(limit=None, file=None, chain=True)
        return




def latest_download_file():
      path = download_dir
      os.chdir(path)
      files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
      newest = files[-1]
      return newest


page_link = "https://bocaodientu.dkkd.gov.vn/"
#driver = set_up(page_link)



options = Options()
options.headless = True
#options.set_preference("browser.download.dir", download_dir)
driver = webdriver.Firefox(options=options, executable_path=r'/bin/geckodriver', service_log_path="/home/ec2-user/thong/geckodriver.log")
print("OK")
driver.get(page_link)
print("OK")
#driver = set_up(page_link)
src = driver.page_source
print(src)
#get_page_pdf(src)
#get_multiple_page(3)
#driver.implicitly_wait(1)

list_company = pd.read_csv(company_id_dir, index_col=0)
print(list_company['id'])
#list_company = ['3901327856','0317325744','0317325769','0110020376','4001252617','0317327491','0317327477','3901327856','0317325744','0317325769','4001252617','0317327491','0317327477']
list_company_id = list_company['id']

get_page_pdf(src)
# try:
#     get_company_by_id("0317325744")
# except:
#     traceback.print_last(limit=None, file=None, chain=True)
# finally:
#     print("end OK")
#     driver.close()
#     driver.quit()


