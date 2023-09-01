from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as exceptions
import time
from tqdm import tqdm
import pandas as pd
import re


# Read a list from a text file
file_path = 'visited_links.txt'
with open(file_path, 'r') as file:
    visited_links = [line.strip() for line in file.readlines()]


columns = ['id', 'location', 'price', 'specifications-1', 'specifications-2', 'stickers']
cars_df = pd.DataFrame(columns=columns)
# visited_links = []

for page in tqdm(range(281+350+190, 1001)):
    url = f"https://www.myauto.ge/ka/s/iyideba-manqanebi-sedani-jipi-kupe-hechbeqi-kabrioleti-universali-hechbeqi-universali-sedani-universali-sedani-jipi-kabrioleti-kabrioleti-bmw-\
        chevrolet-ford-honda-hyundai-kia-lexus-mazda-mercedes-benz-mitsubishi-nissan-subaru-toyota-volkswagen?vehicleType=0&bargainType=0&mansNModels=3-5-12-14-16-20-23-24-25-29-30-39-\
            41-42&vehicleCats=1.5.4.2.6.3.29.30.13.15.66&currId=1&mileageType=1&locations=2.3.4.7.15%5C.30.113.52.37.36.38.39.40.31.5.41.44.47.48.53.54.8.16.6.14.13.12.11.10.9.55.56.57.\
                59.58.61.62.63.64.66.71.72.74.75.76.77.78.80.81.82.83.84.85.86.87.%5C88.91.96.97.101.109&hideDealPrice=1&sort=1&page={page}"
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('detach', True)
    options.add_experimental_option('useAutomationExtension', False)

    # Run Chrome in headless mode
    options.add_argument('--headless')

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Wait for the page to load
        wait = WebDriverWait(driver, 100)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'span')))

        time.sleep(10)
        page_source = driver.page_source
        
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all the 'a' elements with the specific pattern
        elements = soup.find_all('a', href=lambda href: href and href.startswith('/ka/pr/'))

        # Extract the car links from each element
        car_links = set([element['href'] for element in elements])
        
        driver.quit()

        for link in tqdm(list(car_links)):
            if link not in visited_links[-50:]:
                url = f"https://www.myauto.ge{link}"

                options = webdriver.ChromeOptions()
                options.add_argument('start-maximized')
                options.add_experimental_option('excludeSwitches', ['enable-automation'])
                options.add_experimental_option('detach', True)
                options.add_experimental_option('useAutomationExtension', False)

                # Run Chrome in headless mode
                options.add_argument('--headless')

                try:
                    driver = webdriver.Chrome(options=options)
                    driver.get(url)

                    # Wait for the page to load
                    wait = WebDriverWait(driver, 100)
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'span')))

                    time.sleep(3)
                    page_source = driver.page_source

                    # Extract car information
                    soup = BeautifulSoup(page_source, 'html.parser')
                    
                    car_id = [c_id.text for c_id in soup.find_all(class_='d-flex align-items-center text-blue-250 font-size-12 font-medium text-nowrap')]

                    loc = [loc.text for loc in soup.find_all(class_='d-flex align-items-center text-gray-650 font-size-13 text-nowrap mr-10px mr-md-16px mr-lg-24px')]

                    price = [price.text for price in soup.find_all(class_='inline-flex items-center font-size-28 line-height-1 text-gray-800 font-bold')]

                    specs_keys = [key.text for key in soup.find_all(class_='w-50 w-md-40 text-gray-850')]
                    specs_values = [value.text for value in soup.find_all(class_='w-50 w-md-60 text-gray-800')]
                    colors = [value.text for value in soup.find_all(class_='w-50 w-md-60 text-gray-800 d-flex align-items-center')]
                    if len(colors)==1:
                        specs_values.insert(specs_keys.index('საჭე')+1, colors[0])
                    elif len(colors)==2:
                        specs_values.insert(specs_keys.index('საჭე')+1, colors[0])
                        specs_values.insert(specs_keys.index('საჭე')+2, colors[1])
                    else:
                        continue
                    specs_1 = [[k, v] for k, v in zip(specs_keys, specs_values)]

                    specs_2 = [[item.text, 'Yes'] if 'id="dont"' not in str(item) else [item.text, 'No'] for item in soup.find_all(class_='d-flex align-items-center text-gray-800 font-size-14 my-8px')]

                    stickers = [sticker.text for sticker in soup.find_all(class_='d-flex flex-wrap')]

                    data = [car_id, loc, price, specs_1, specs_2, stickers]
                    cars_df = pd.concat([cars_df, pd.DataFrame([data], columns=columns)], ignore_index=True)

                    driver.quit()

                except exceptions.WebDriverException:
                        print("Broken link")


        # add to visited_links
        visited_links += car_links
            
        # Check if it's the tenth iteration
        if page % 10 == 0:
            # Save DataFrame to CSV file
            cars_df.to_csv(f'cars.csv', index=False)
            print('Data saved')

            # Save visited links
            with open('visited_links.txt', 'w') as file:
                for item in visited_links:
                    file.write(str(item) + '\n')
            print('Saved visited links')
    
    except exceptions.WebDriverException:
        print('An error occurred')