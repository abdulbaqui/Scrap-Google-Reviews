import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.webdriver.common.by import By

options = Options()
driver =  webdriver.Chrome('/usr/lib/chromium-browser/chromedriver',options=options)

url = "https://www.google.com/maps/place/Aspria+Berlin+Ku%E2%80%99damm/@52.5003887,13.2919884,17z/data=!4m10!3m9!1s0x47a850c4b634ef93:0x2faf0f02eacd864e!5m2!4m1!1i2!8m2!3d52.5003887!4d13.2941771!9m1!1b1"
driver.get(url)
time.sleep(2)
driver.find_element("xpath", '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button').click()
driver.refresh()

def scroll_all_reviews():
    total_reviews= int(re.sub('\D','',driver.find_element("xpath",'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]').text))
    scrollbar_div = driver.find_element("xpath",'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')
    time.sleep(1)
    #Scroll reviews
    for i in range(0,(round(total_reviews/8))):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollbar_div)
        time.sleep(1)

def get_reviews_to_csv():  
    review_count = 0
    list_reviewer_name = []
    list_review_content = []
    list_rating = []
    list_review_time = []
    list_if_owner_reply = []
    list_reply_from_owner = []
    list_full_review_link = []
    dict_review = {}
    
    for element in driver.find_elements("xpath",'//div[@class="jftiEf fontBodyMedium"]'):
        review_count = review_count +1
        try:
            reviewer_name = element.find_element("xpath",'.//div[@class="d4r55"]/span').text
        except:
            reviewer_name = ""
        try:
            review_content = element.find_element("xpath",'.//div[@class="MyEned"]/span[2]').text
        except:
            review_content = ""
        try:
            xpath_for_reviewlink ="'"+"Aktionen für die Rezension von " + reviewer_name +"'"
            driver.find_element("xpath", '//button[@aria-label=' + xpath_for_reviewlink + ']').click()
            time.sleep(1)
            driver.find_element("xpath", '//*[@id="action-menu"]/div[1]').click()
            time.sleep(1)
            full_review_link = driver.find_element("xpath",'//*[@id="modal-dialog"]/div/div[2]/div/div[3]/div/div/div[1]/div[4]/div[2]/input').get_attribute("value")
            time.sleep(1)
            driver.find_element("xpath",'//*[@id="modal-dialog"]/div/div[2]/div/div[2]/button').click()
        except:
            full_review_link =""
            print(reviewer_name +'\'s review link not scraped')    
        rating = element.find_element("xpath",'.//div[@class="DU9Pgb"]/span').text 
        
        rating = int(rating[0])
        review_time_information = element.find_element("xpath",'.//div[@class="DU9Pgb"]/span[3]/span').text
        try: 
            reply_from_owner = element.find_element("xpath",'.//div[@class="wiI7pd"]').text
        except:
            reply_from_owner = ""
        if_owner_reply = False if reply_from_owner == "" else True
        list_reviewer_name.append(' '.join((re.sub('[$@&!,]',' ',reviewer_name).split())))
        list_review_content.append(' '.join((re.sub('[$@&!,]',' ',review_content).split())))
        list_rating.append(rating)
        list_review_time.append(' '.join((re.sub('[$@&!,]',' ',review_time_information).split())))
        list_if_owner_reply.append(if_owner_reply)
        list_reply_from_owner.append(' '.join((re.sub('[$@&!,]',' ',reply_from_owner).split())))
        list_full_review_link.append(' '.join((re.sub('[$@&!,]',' ',full_review_link).split())))
        time.sleep(1)
        print('Review number %i scraped!' % review_count)
    dict_review = {'reviewer_name':list_reviewer_name,'review_content':list_review_content,'full_review_link':list_full_review_link,
                   'rating':list_rating,'review_time_information':list_review_time,'reply_from_owner':list_if_owner_reply,
                   'reply_text':list_reply_from_owner}
    df = pd.DataFrame(dict_review) 
    df.to_csv('reviews.csv',index=False,encoding='utf8') 
    print("CSV Created With %i reviews" % review_count)

scroll_all_reviews()
get_reviews_to_csv()
driver.quit()

       