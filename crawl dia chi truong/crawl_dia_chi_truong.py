from selenium import webdriver
import pymongo as pm
import pandas as pd
import time

class Crawler:
    def __init__(self):
        self.driver = webdriver.Chrome() 
    def crawl(self, uniName):
        time.sleep(5) # sleep để tránh gửi request nhanh quá bị captcha
        self.driver.get("http://google.com.vn/search?q=" + uniName) # seach tên trường uniName
        try:
            addressElement = self.driver.find_element_by_css_selector("span.LrzXr") # chọn vị trí địa lý
            address = addressElement.text
            return (True, address) #trả về true và địa chỉ nếu crawl thành công
        except:
            return (False, "") # trả về false nếu k crawl được
        
        
if __name__ == '__main__':    
    myMongoClient = pm.MongoClient("mongodb://localhost:27017") # kết nối mongo
    myMongoDb = myMongoClient["unisec-db"]
    uniCol = myMongoDb["universities"]

    error_log = [] # ghi lại những trường không craw được để bổ sung bằng tay
    
    crawler = Crawler()
    for doc in uniCol.find(): # duyệt qua tất cả các trường
        uniName = doc["name"] 
        address = crawler.crawl(uniName) # chạy crawl 
        if address[0] : # crawler trả về thành công
            print("địa chỉ trường " + uniName + " là " + address[1])
            uniCol.update_one({"name": uniName}, {"$set": {"address": address}}) # lưu vào db
        else :    
            error_log.append(uniName) # crawl thất bại thì lưu vào log
            print("không crawl được địa chỉ trường " + uniName)
    crawler.driver.close()
    
    error = pd.DataFrame(error_log)
    error.to_csv("address_error.csv") # lưu lại danh sách các trường không crawl được
