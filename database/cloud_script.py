# Script that can be deploted in cloud server or local machine to scrape data from ARC website and dowloads data to database.csv
import random
import time
import warnings

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

warnings.filterwarnings("ignore", category=DeprecationWarning)

driver_path = "PATH TO CHROMEDRIVER"


counter = 0
time_start = time.time()

while True:

    try:

            counter += 1
            print("Scan: ", counter)
            print("Time Elapsed: ", (time.time() - time_start)/60)


            try:
                with open("database.csv", "r") as file:
                    print("Database Loaded")
            except FileNotFoundError:
                with open("database.csv", "w") as file:
                    print("Database Created")

            url = "https://connect2concepts.com/connect2/?type=circle&key=59ac279f-1fd6-4e55-925c-f7e02764ab00"



            options = Options()
            options.headless = True
            driver = webdriver.Chrome(driver_path, options=options)

            driver.implicitly_wait(20)
            driver.get(url)

            time.sleep(random.random() * 5)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            driver.quit()

            venue_data = soup.find_all('div', {'style': 'text-align:center;'})

            df = pd.DataFrame()

            dictionary = {"Arc Floor One": [], "Climbing": [], "Arc Olympic Lifting Zones": [], "Arc Floor Two": [], "South Court": [],
                          "Four Court Gym": [], "North Court": [], "Recreation Pool": [], "Competition Pool": [], "Arc Express": [],
                          "Spa": [], "Aquaplex Pool Deck": [], "Tennis Courts": []}


            for venue in venue_data:
                data = venue.text

                venue_name = data.split("(")[0]

                open_status = data.split("(")[1]
                open_status = open_status.split(")")[0]

                person_count = data.split("Last Count: ")[1]
                person_count = person_count.split("Updated: ")[0]

                last_updated = data.split("Updated: ")[1]
                last_updated = last_updated[0:10]

                last_time = data[-8:]

                dictionary[venue_name] = (last_updated, last_time, open_status, person_count)




            pd.DataFrame(dictionary).T.to_csv('database.csv', header=False, mode='a')

            for i in range(10):
                print("Sleeping" + i * ".")
                time.sleep(60)


    except:
        print("Error")
        time.sleep(5)
        pass
