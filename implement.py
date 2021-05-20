from boardr_scrapr import boardr_scrapr
import pandas as pd
import pickle

skater_df = pd.read_csv('skater_names.csv')

skater_list = list(pd.unique(skater_df['skater']))

#initiate class with the location of your chromedriver
scraper = boardr_scrapr('C:\Program Files (x86)\chromedriver.exe')

scraper.scrape_skaters(skater_list)

sk8r_dict = scraper.raw_data

#print(sk8r_dict)

scraper.closr()

#dump dicitonairy into a pickle to use later
with open('sk8r_dict.pkl', "wb") as file:
	pickle.dump(sk8r_dict, file)
	file.close()

