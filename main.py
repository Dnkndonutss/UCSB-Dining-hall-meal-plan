import json
import re
import pandas as pd
import os
import glob
from itertools import combinations_with_replacement


while True:
    dining_hall = input("Enter dining hall (dlg, carillo, portola): ").strip().lower()
    if dining_hall in ['dlg', 'carillo', 'portola']:
        break
    else:
        print("Invalid dining hall. Please choose from dlg, carillo, portola,")
print(f"Selected dining hall: {dining_hall}")
print("Scraping data... This may take a few minutes. Please wait...\n")

if dining_hall == 'dlg':
    import dlg
    dlg.main()
elif dining_hall == 'carillo': 
    import carillo
    carillo.main()
elif dining_hall == 'portola':
    import portola
    portola.main()
print("Data scraping completed.\n")

def clean_value(val):
    """Cleans and converts a nutrition value string to a float."""
    if val is None or val == '':
        return 0.0
    val = str(val).strip()
    if "<" in val:
        return 0.0
    match = re.search(r"([\d\.]+)", val)
    if match:
        return float(match.group())
    return 0.0

def clean_json_to_df(data):
    cleaned = []
    for item in data:
        cleaned.append({
            'date': item.get('date', ''),
            'meal': item.get('meal', ''),
            'food': item.get('food', ''),
            'calories': clean_value(item.get('calories')),
            'fats': clean_value(item.get('fats')),
            'carbs': clean_value(item.get('carbs')),
            'protein': clean_value(item.get('protein'))
        })
        
    df = pd.DataFrame(cleaned)
    return df

list_of_files = glob.glob("nutrition_data_*.json")
if list_of_files:
    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"Loading data from {latest_file}")
    with open(latest_file, 'r', encoding='utf-8') as file:
        raw_data = json.load(file)
    df = clean_json_to_df(raw_data)
    


else:
    print("No nutrition data files found.")
    
available_dates = df['date'].unique()
available_meals = df['meal'].unique()

while True: 
    print("\nAvailable dates:")
    for d in available_dates:
        print(f"- {d}")
    selected_date = input("Enter a date from the above list: ").strip()
    if selected_date in available_dates:
        break
    else:
        print("Invalid date. Please choose from the available dates.\n")
    
while True:
    print("\nAvailable meals:")
    for m in available_meals:
        print(f"- {m}")
    selected_meal = input("Enter a meal from the above list: ").strip()
    if selected_meal in available_meals:
        break
    else:
        print("Invalid meal. Please choose from the available meals.\n")

filtered_df = df[(df['date'] == selected_date) & (df['meal'] == selected_meal)]
    
def get_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a positive number.")
                continue
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


target_calories = get_positive_number("Enter your target calories: ")
target_protein = get_positive_number("Enter your target protein (g): ")
target_fats = get_positive_number("Enter your target fats (g): ")
target_carbs = get_positive_number("Enter your target carbs (g): ")



best_combo = None
best_score = float('inf')

for r in range(2, 5):
    for combo in combinations_with_replacement(filtered_df.to_dict('records'), r):
        total_calories = sum(item['calories'] for item in combo)
        total_protein = sum(item['protein'] for item in combo)
        total_fats = sum(item['fats'] for item in combo)
        total_carbs = sum(item['carbs'] for item in combo)

        score = abs(total_calories - target_calories) \
              + abs(total_protein - target_protein) \
              + abs(total_fats - target_fats) \
              + abs(total_carbs - target_carbs)

        if score < best_score:
            best_score = score
            best_combo = combo
            
print("Best meal plan:")
for item in best_combo:
    print(f"- {item['food']} (Cals: {item['calories']}, P: {item['protein']}, F: {item['fats']}, C: {item['carbs']})")

print("\nTotals:")
print(f"Calories: {sum(i['calories'] for i in best_combo)}")
print(f"Protein: {sum(i['protein'] for i in best_combo)}")
print(f"Fats: {sum(i['fats'] for i in best_combo)}")
print(f"Carbs: {sum(i['carbs'] for i in best_combo)}")


