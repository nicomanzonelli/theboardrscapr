from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class boardr_scrapr:

	#Initiate with the driver path of your chrome driver
	def __init__(self, driver_path, D = {}):
			self.driver_path = driver_path
			self.driver = webdriver.Chrome(driver_path) #This webscraper uses a Chrome Driver
			self.raw_data = D

	#scrape skaters names within a list
	def scrape_skaters(self, skater_list):
		driver = self.driver
		for skater in skater_list:
			d = {}
			d['name'] = skater
			driver.get('https://theboardr.com/skaters')
			text_box = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div[1]/div[1]/div/div/input')
			text_box.send_keys(skater)
			sub_button = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div[1]/div[2]/button')
			sub_button.click()

			try:
				link = WebDriverWait(driver, 5).until(
					EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div/div[1]/div[3]/div/div[2]/ul/li/a')))
				d['profile_link'] = link.get_attribute('href')
				link.click()
			except:
				d['profile_link'] = 'NA'
				continue

			try:		
				sponsors = WebDriverWait(driver, 5).until(
					EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div/div[1]/div[2]/div[1]/p')))
				d['sponsors'] = sponsors.text
			except:
				d['sponsors'] = 'NA'

			try:
				insta = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div/p/a')
				d['insta'] = insta.text
			except:
				d['insta'] = 'NA'

			try:
				age_sex = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/p')
				d['age_sex'] = age_sex.text
			except:
				d['age_sex'] = 'NA'

			try:
				stance = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div[1]/div[2]/div[2]/div[3]/div/p')
				d['stance'] = stance.text
			except:
				d['stance'] = 'NA'

			try:
				hometown = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div/h3')
				d['hometown'] = hometown.text
			except:
				d['hometown'] = 'NA'

			try:
				num_comp_pages = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div[2]/div[5]/div/p/strong')
				iter_clicks = int(num_comp_pages.text[12:14]) - 1

				comps = []
				iter_page = 0
				while iter_page < iter_clicks:
					for comp_i in range(1,6):
						comp_name = WebDriverWait(driver, 10).until(
							EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div/div[2]/div[5]/div/ul/a[' + str(comp_i) + ']/div[2]/span')))
						comp_date = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div[2]/div[5]/div/ul/a['+ str(comp_i) + ']/div[2]/p/div/div[1]')
						comps.append((comp_name.text, comp_date.text))

					next_comp_button = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div[2]/div[5]/div/ul/li/nav/ul/li[9]/button')
					next_comp_button.click()
					iter_page += 1

				d['comps'] = comps

			except:
				d['comps'] = ["NA"]


			self.raw_data[skater] = d

	#Close webdriver
	def closr(self):
		self.driver.quit()


