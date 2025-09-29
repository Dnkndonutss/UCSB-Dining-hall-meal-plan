# UCSB Dining Hall Nutrtion Scraper And Meal Plan creater

This project scrapes nutritional data from UCSB’s official dining hall website using Selenium, structures it with Pandas, and recommends foods to meet user-specified macronutrient goals.

## Tech Stack
Python
Selenium (scraping)
Pandas (data processing)
Webdriver-Manager (handles ChromeDriver)

## It contains:

Dining-hall-specific scrapers (carillo.py, dlg.py, portola.py)
A main.py entry point that takes user preferences (dining hall + macros) and outputs food suggestions

## How It Works:
First, the project asks the user what Dining hall they are eating from(carillo, dlg, or portola). Based on the user's response, the project will run its corresponging scrapper (carillo.py, dlg.py, or portola.py). Using selenium and Webdriver-manager, the project will navigate through the official UCSB Nutrional Website, and gather the nutrional data of each item in the menu. Then it will save the data to a Json file. The data is then converted into a Pandas dataframe. The project then asks the user the date and what meal they are eating (Breakfast, Brunch, Lunch or Dinner), How many calories they are eating, and the amount of protein, fat, and carbs they want. After gathering the user's criteria, the project will turn the Pandas DataFrame into a list of dictionary, where each dictionary is one food item, and it tries possible combinations of 2-5 food items. It will then calculate the totals for the combination and see how close it is to the user's criteria, and this loop will find the closest combination to the user's criteria, and write out the best combination in the console. 


## Future Improvements
Find a way to speed up the webscrapping process, perhaps by only scrapping the menu for the day and meal the user asks for instead of the whole weeks worth. 
Make it a loop so that the user doesn't have to redo the whole process if they want another meal plan.


