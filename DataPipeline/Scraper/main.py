from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import json
import random
from helper import *
import traceback

courseRowValue = None

processing = True 
errorCount = 0

while processing and errorCount < 6: 

    try: 
        driver = webdriver.Chrome()
        driver.get('https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm')
        driver.implicitly_wait(0.5)

        # Navigating to "Course Campus" tab on the left, and proceeding to select "Keele" to load up all courses offered at keele.
        driver.find_element(By.XPATH, "/html/body/p/table/tbody/tr[2]/td[1]/table/tbody/tr[6]/td/a/img").click()
        driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td/form/table/tbody/tr[2]/td[2]/select/option[3]").click()
        driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td/form/table/tbody/tr[3]/td[2]/input").click()

        driver.implicitly_wait(5)

        # Creating a new tab to switch to
        tab_main_id = driver.current_window_handle
        driver.switch_to.new_window('tab')
        tab_secondary_id = driver.current_window_handle
        driver.switch_to.window(tab_main_id)

        #Iterate through course links
        courseRowValue = count_lines_in_file("SecondaryItinerary.txt") + 1

        if count_lines_in_file("SecondaryItinerary.txt") < 2:
            courseRowValue = 2

        # Save course details within a txt file
        # courseItinerary = []

        delay_counter = 0

        while courseRowValue != 5005:

            if delay_counter == 10:
                sleep(random.randint(7, 15))
                delay_counter = 0

            random_delay_1 = random.randint(2, 3)
            random_delay_2 = random.randint(2, 3)

            courseLink = f"/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td/table[2]/tbody/tr[{courseRowValue}]/td[3]/a"
            currentCourseURL = driver.find_element(By.XPATH, courseLink).get_attribute("href")

            sleep(random_delay_1)

            driver.switch_to.window(tab_secondary_id)
            driver.get(currentCourseURL)

            driver.implicitly_wait(5)
            course_title = driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td/table[1]/tbody/tr/td[1]/h1").text
            course_description = driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td/p[3]").text

            sleep(random_delay_2)

            print(f"{course_title} | {course_description[:20]}")

            courseObject = {
                "course_title": course_title,
                "course_description": course_description
            }

            # courseItinerary.append(courseObject)

            add_json_entry(courseObject, "SecondaryItinerary.txt")

            driver.switch_to.window(tab_main_id)
            courseRowValue += 1
            delay_counter += 1
        processing = False
    except Exception as e: 
        print(f"Error at Course Row Value: {courseRowValue}. Restarting...")
        print(e)
        errorCount += 1
        sleep(15)

# with open('CourseItinerary.txt', 'w') as json_file:
#     json.dump(courseItinerary, json_file)






