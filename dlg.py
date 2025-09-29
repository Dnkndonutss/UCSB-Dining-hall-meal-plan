from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime  
import json
import time

def scrape_nutrition_data():
    web = 'https://nutrition.info.dining.ucsb.edu/NetNutrition/1#'
    
    # Create the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(web)

    wait = WebDriverWait(driver, 10)

    # Navigate to Carrillo Dining Commons
    button = wait.until(EC.element_to_be_clickable((By.XPATH, 
        "//a[@class='text-white' and contains(text(), 'De La Guerra Dining Commons')]")))
    button.click()
    
    # Navigate to Daily Menu
    button = wait.until(EC.element_to_be_clickable((By.XPATH, 
        "//a[@class='text-white' and contains(text(), \"De La Guerra's Daily Menu\")]")))
    button.click()
    time.sleep(1)
    # Extract date sections
    date_sections = driver.find_elements(By.CSS_SELECTOR, "section.card.mb-3.h4")
    nutrition_data = []
    num_date_sections = len(date_sections)
    
    # Iterate through each date section
    for date_index in range(num_date_sections):
        date_sections= driver.find_elements(By.CSS_SELECTOR, "section.card.mb-3.h4")
        date_section = date_sections[date_index]
        # Extract the date from the section header
        date_text = date_section.find_element(By.CSS_SELECTOR, "header.card-title").text
        print(f"Processing date: {date_text}")
        
        # Find all meal links within this date section
        meal_links = date_section.find_elements(By.CSS_SELECTOR, "a.cbo_nn_menuLink")
        num_meal_links = len(meal_links)
        # Process each meal (Breakfast, Lunch, Dinner)
        for meal_index in range(num_meal_links):
            date_sections= driver.find_elements(By.CSS_SELECTOR, "section.card.mb-3.h4")
            date_section = date_sections[date_index]
            meal_links = date_section.find_elements(By.CSS_SELECTOR, "a.cbo_nn_menuLink")
            meal_link = meal_links[meal_index]
            meal_name = meal_link.text
            print(f"Processing meal: {meal_name}")
            
            # Click the meal link
            meal_link.click()
            time.sleep(2)
            
            # Extract food items for this meal
            food_items = driver.find_elements(By.XPATH, "//a[starts-with(@id, 'showNutrition_')]")
            
            for i in range(len(food_items)):
                food_items = driver.find_elements(By.XPATH, "//a[starts-with(@id, 'showNutrition_')]")
                food_item = food_items[i]
                food_name = food_item.text
                try:
                    # Click to open nutrition panel
                    food_item.click()
                    
                    # Extract nutrition information
                    calories = wait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//div[@class='inline-div-right bold-text font-22 ']")
                        )
                    ).text
                    
                    fats = wait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//div[contains(@class, 'inline-div-left')]/span[@class='bold-text' and contains(text(), 'Total Fat')]/following-sibling::span")
                        )
                    ).text.strip()
                    
                    carbs = wait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//div[contains(@class, 'inline-div-left')]/span[@class='bold-text' and contains(text(), 'Total Carbohydrate')]/following-sibling::span")
                        )
                    ).text.strip()
                    
                    protein = wait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//div[contains(@class, 'inline-div-left')]/span[@class='bold-text' and contains(text(), 'Protein')]/following-sibling::span")
                        )
                    ).text.strip()
                    
                    # Store the data with date and meal information
                    nutrition_data.append({
                        'date': date_text,
                        'meal': meal_name,
                        'food': food_name,
                        'calories': calories,
                        'fats': fats,
                        'carbs': carbs,
                        'protein': protein
                    })
                    
                    # Close the nutrition panel
                    driver.find_element(By.ID, "btn_nn_nutrition_close").click()
                    WebDriverWait(driver, 2).until(
                        EC.invisibility_of_element_located((By.ID, "nutritionLabel"))
                )
                    
                except Exception as e:
                    print(f"Error processing {food_name}: {str(e)}")
                    continue
            
            # Go back to the date menu page
            WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "btn_Back*Menu Details"))
                ).click()
            
            time.sleep(2)
            date_sections = driver.find_elements(By.CSS_SELECTOR, "section.card.mb-3.h4")

    

    
    driver.quit()
    return nutrition_data

def save_to_json(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"nutrition_data_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")
    
# Keep all your imports and scrape_nutrition_data / save_to_json functions as they are

def main():
    # Run the scraper
    nutrition_data = scrape_nutrition_data()

    # Print and save results
    for item in nutrition_data:
        print(f"{item['date']} - {item['meal']}: {item['food']} - {item['calories']} calories")

    save_to_json(nutrition_data)


# Only run main() if this file is executed directly
if __name__ == "__main__":
    main()



