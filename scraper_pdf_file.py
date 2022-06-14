# Import Module
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
import traceback

global download_dir,chrome_driver,page_link,company_id_dir
download_dir = "/Users/macbook/Desktop/PDF_list/"
chrome_driver = '/Users/macbook/Downloads/chromedriver'
page_link = "https://bocaodientu.dkkd.gov.vn/"
company_id_dir = "/Users/macbook/Downloads/company_list_100"

def set_up(url):
    options = Options()
    options.add_argument("--disable-extensions")
    #options.add_argument("--headless")
    options.add_argument("start-maximized") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--no-sandbox')
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
    input_search = driver.find_element(By.ID , value="ctl00_FldSearch")
    input_search.clear()
    input_search.send_keys(id)
    time.sleep(1)
    #input_location = input_search.location
    #print(input_location)

    #divRegister = driver.find_element(By.ID , value="linkRegister")
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(input_search, 100, 30).click().perform()

    #time.sleep(3)
    try:
        pdf_tab = driver.find_element(By.ID ,value="ctl00_C_LnkTab2")
        pdf_tab.click()
        print("click OK")
        time.sleep(2)
        try:
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
            
            product_button = driver.find_element(By.ID ,value="ctl00_C_LnkTab3")
            product_button.click()
            print("product click")
            time.sleep(3)
            get_company_by_product()

    except: 
        traceback.print_last(limit=None, file=None, chain=True)
        return


def get_company_by_product():
    try:
        bocao_tab = driver.find_element(By.ID ,value="ctl00_C_RptAvailableProd_ctl04_LnkSubCatEGAZETTE")
        bocao_tab.click()
        time.sleep(2)
        bocao_detail_tab = driver.find_element(By.ID ,value="ctl00_C_RptAvailableProd_ctl04_LnkProduct")
        bocao_detail_tab.click()
        time.sleep(2)

        add_order = driver.find_element(By.ID ,value="ctl00_C_RptAvailableProd_ctl04_LnkProdExecuteUP")
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element_with_offset(add_order, 30, 20).click().perform()
        print("click order")
        time.sleep(3)
        shopping_cart = driver.find_element(By.ID,value="ctl00_UpdShoppingCart")
        shopping_cart.click()
        print("click shop")
        time.sleep(3)
        pay_button = driver.find_element(By.ID,value="ctl00_C_btnProceed")
        pay_button.click()
        print("click pay")
        time.sleep(5)
        driver_new = driver.find_element(By.ID , value="ctl00_C_InfoPnl")
        input_search_name = driver_new.find_element(By.ID , value="ctl00_C_UC_BUYER_DETAILSEditCtl_FIRST_NAMEFld")
        input_search_name.clear()
        input_search_name.send_keys("Thong Tran")
        input_search_adds = driver_new.find_element(By.ID , value="ctl00_C_UC_BUYER_DETAILSEditCtl_ADDRESS_TEXTFld")
        input_search_adds.clear()
        input_search_adds.send_keys("236 HQV")
        input_search_email = driver_new.find_element(By.ID , value="ctl00_C_UC_BUYER_DETAILSEditCtl_EMAILFld")
        input_search_email.clear()
        input_search_email.send_keys("buyfail@gmail.com")
        input_search_phone = driver_new.find_element(By.ID , value="ctl00_C_UC_BUYER_DETAILSEditCtl_PHONEFld")
        input_search_phone.clear()
        input_search_phone.send_keys("09483293232")
        submit_buy = driver.find_element(By.ID , value="ctl00_C_btnProceed")
        submit_buy.click()
        time.sleep(5)
        

        driver.switch_to.alert.accept()
        time.sleep(1)
        submit_buy.click()
        driver.switch_to.alert.accept()
        time.sleep(5)
        acept_term_button = driver.find_element(By.ID , value="ctl00_C_agreeTermsChk")
        acept_term_button.click()
        
        acept_term_button2 = driver.find_element(By.ID , value="ctl00_C_btnSendPayment")
        acept_term_button2.click()
        time.sleep(50)
    except:
        return





def latest_download_file():
      path = download_dir
      os.chdir(path)
      files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
      newest = files[-1]
      return newest



driver = set_up(page_link)
#src = driver.page_source
#get_page_pdf(src)
#get_multiple_page(3)
#driver.implicitly_wait(1)
# list_company = pd.read_csv(company_id_dir, index_col=0)
# print(list_company['id'])
#list_company = ['0317272161','3901327856','0317325744','0317325769','0110020376','4001252617','0317327491','0317327477','3901327856','0317325744','0317325769','4001252617','0317327491','0317327477']
# list_company_id = list_company['id']
# for i in list_company_id:
#     get_company_by_id(i)

try:
    get_company_by_id("0317272161")
    print("get company done")
except:
    traceback.print_last(limit=None, file=None, chain=True)
finally:
    print("QUIT")
    driver.close()
    driver.quit()




print("OK")
driver.close()
driver.quit()


