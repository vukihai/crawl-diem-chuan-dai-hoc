# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 00:30:19 2019

@author: Huong
"""

from selenium import webdriver
from time import sleep
import pandas as pd

class Crawler:
    def __init__(self):
        self.driver = webdriver.Chrome()
 
    def crawl(self, url, unicode):
        for year in range(2010,2020):
            self.driver.get(url + "?y=" + str(year))
            try:
                try:
                    view_more_btn = self.driver.find_element_by_id('diemchuan_viewmore')
                    while True:
                        view_more_btn.click()
                        print('load more')
                        sleep(3)
                except:
                    print('no more')
                    
                ma_nganh = []
                ten_nganh = []
                to_hop = []
                diem_chuan = []
                element_ds_ma_nganh = self.driver.find_elements_by_css_selector('.id-branch')
                for element_ma_nganh in element_ds_ma_nganh:
                    text = element_ma_nganh.text
                    ma_nganh.append(text)
        
                element_ds_ten_nganh = self.driver.find_elements_by_css_selector('.name-branch')
                for element_ten_nganh in element_ds_ten_nganh:
                    text = element_ten_nganh.text
                    ten_nganh.append(text)
                
                element_ds_to_hop = self.driver.find_elements_by_css_selector('.group-branch')
                for element_to_hop in element_ds_to_hop:
                    text = element_to_hop.text
                    to_hop.append(text)
                
                element_ds_diem_chuan = self.driver.find_elements_by_css_selector('.col-lg-2 span:nth-of-type(2)')
                for element_diem_chuan in element_ds_diem_chuan:
                    text = element_diem_chuan.text
                    diem_chuan.append(text)
                
                data = [ma_nganh,ten_nganh,to_hop,diem_chuan]
                dataframe = pd.DataFrame(data).T
                file_name = uniCode + "_" + str(year) +".csv"
                if(len(ma_nganh)!= 0):
                    dataframe.to_csv(file_name, sep=',', encoding='utf-8')
            except:
                print("no data for this year")
            
                
 
if __name__ == '__main__':
    universities = pd.read_csv("Danh_sach_truong.csv")
    universitiesUrl = universities.iloc[:,0]
    universitiesCode = universities.iloc[:,1]
#print(universitiesUrl)
    crawler = Crawler()
    for i in range(universitiesUrl.size):
        url = universitiesUrl[i]
        print(url)
        uniCode = universitiesCode[i]
        crawler.crawl(url, uniCode)
    crawler.driver.close()
    
 