from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime  
import json
import time


web = 'https://nutrition.info.dining.ucsb.edu/NetNutrition/1#'

# Path to your ChromeDriver
path = 'C:\\Program Files (x86)\\webdrivers\\chromedriver.exe'  

# Create a Service object
service = Service(executable_path=path)

# Create the driver with the service
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(web)

#for DLG
wait = WebDriverWait(driver, 10)


button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='text-white' and contains(text(), 'Portola Dining Commons')]")))
button.click()
#for dlg daily menu
button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='text-white' and contains(text(), \"Portola's Daily Menu\")]")))
button.click()
date_sections = driver.find_elements(By.CSS_SELECTOR, "section.card.mb-3.h4")
nutrition_data = []
menu_links = driver.find_elements(By.CSS_SELECTOR, "a.cbo_nn_menuLink")
for i in range(len(menu_links)):
    menu_links = driver.find_elements(By.CSS_SELECTOR, "a.cbo_nn_menuLink")
    link = menu_links[i]
    # Click the menu link
    link.click()
    time.sleep(2)
    food_items = driver.find_elements(By.XPATH, "//a[starts-with(@id, 'showNutrition_')]")
    
    for i in range(len(food_items)):
        food_items = driver.find_elements(By.XPATH, "//a[starts-with(@id, 'showNutrition_')]")
        food = food_items[i]
        food_name = food.text
        try:
            # Click to open nutrition panel
            food.click()
            # Extract food name and calories
            food_name = food.text
            calories = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@class='inline-div-right bold-text font-22 ']")
                )
            ).text
            fats = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'inline-div-left')]/span[@class='bold-text' and contains(text(), 'Total Fat')]/following-sibling::span")
                )
            ).text.strip()
            carbs = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'inline-div-left')]/span[@class='bold-text' and contains(text(), 'Total Carbohydrate')]/following-sibling::span")
                )
            ).text.strip()
            protein = WebDriverWait(driver, 5).until( 
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'inline-div-left')]/span[@class='bold-text' and contains(text(), 'Protein')]/following-sibling::span")
                )
            ).text.strip()
        
        
            # Store the data
            nutrition_data.append({
                'food': food_name,
                'calories': calories,
                'fats': fats,
                'carbs': carbs,
                'protein': protein
            })
        
            # Close the nutrition panel
            driver.find_element(By.ID, "btn_nn_nutrition_close").click()
        
            # Small pause to ensure panel closes
            WebDriverWait(driver, 2).until(
                EC.invisibility_of_element_located((By.ID, "nutritionLabel"))
            )
        
        except Exception as e:
            print(f"Error processing {food_name}: {str(e)}")
            continue
            

    
    # Wait for the back button to be clickable on the new page
    WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btn_Back*Menu Details"))
          ).click()
    time.sleep(2)
    
def save_to_json(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"nutrition_data_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

for item in nutrition_data:
    print(f"{item['food']}: {item['calories']} calories, {item['fats']} fats, {item['carbs']} carbs, {item['protein']} protein")

save_to_json(nutrition_data)
time.sleep(10)
driver.quit()
