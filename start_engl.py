import requests, re, os
from jinja2 import Environment, FileSystemLoader, Template
from fractions import Fraction

# Convert Decimals into fractions
def decimal_to_nicefrac(value):
    # Convert value to float
    try:
        value = float(value)
    except ValueError:
        return value  # if not number, return value

    # Return if integer
    if value.is_integer():
        return str(int(value))
    
    # Convert Number into fraction
    frac = Fraction(value).limit_denominator(8)  # Limit denominator to 8, for clean fractions such as 1/2, 1/4 
    
    # Extract numerator and denominator
    if frac.numerator > frac.denominator:
        whole_number = frac.numerator // frac.denominator
        fraction_part = frac - whole_number
        return f"{whole_number}\\nicefrac{{{fraction_part.numerator}}}{{{fraction_part.denominator}}}"
    else:
        return f"\\nicefrac{{{frac.numerator}}}{{{frac.denominator}}}"
        
# Define Replacement functions for '°C' und 'Min.'
def replace_celsius(value):
    return value.replace("°C", r"\textcelcius")

def replace_min_space(value):
    if isinstance(value, str):
        value = re.sub(r'(\d+)\s+Min\.', r'\1~Min.', value)
        value = re.sub(r'(\d+)\s+min\.', r'\1~min.', value)
        value = re.sub(r'(\d+)\s+Minuten', r'\1~Minuten', value)
    return value

# Adjustment of jinja2 environment to avoid curly brackets that are heavily used in LaTeX.
env = Environment(
    loader=FileSystemLoader("templates"),
    block_start_string="<<%",
    block_end_string="%>>",
    variable_start_string="<<",
    variable_end_string=">>",
    comment_start_string="<<#",
    comment_end_string="#>>"
)

# Register user defined filters in Jinja2-environment
env.filters['replace_celsius'] = replace_celsius
env.filters['replace_min_space'] = replace_min_space
env.filters['decimal_to_nicefrac'] = decimal_to_nicefrac

# API-URL to fetch total number of recipes
api_url = "[tandoor-recipe host and port]/api/recipe/" #replace with your info
headers = {
    "Authorization": "Bearer tda_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" #your API token goes here
}

# API-call, to fetch total number of recipes
response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    total_count = data['count']  # Get recipe count
    print(f"{total_count} Recipes found.")
else:
    print(f"Error: {response.status_code} - {response.text}")
    total_count = 0

# User choice
choice = input("Would you like to export a certain recipe (enter ID) or all (a)? ")

# Load Template
template = env.get_template('xcookybooky-nswissgerman-11pt.txt')

# Folder for exported LaTeX-Files
output_dir = "exported_recipes"
os.makedirs(output_dir, exist_ok=True)

def fetch_recipe_data(recipe_id):
    """ Gets selected recipe from API """
    recipe_url = f"[tandoor-recipe host and port]api/recipe/{recipe_id}/" #replace with your info
    response = requests.get(recipe_url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Recipe ID {recipe_id} could not be found (Status: {response.status_code}).")
        return None

if choice.lower() == 'a':  # Export all Recipes
    for recipe_id in range(1, total_count + 1):  # Crawl through all IDs
        recipe_data = fetch_recipe_data(recipe_id)  # Fetch recipe Data from recipe
        
        if recipe_data:
            # Name file like recipe (Replace unwanted characters)
            recipe_name = recipe_data['name'].replace(" ", "_").replace("/", "-")  
            output_path = os.path.join(output_dir, f"{recipe_name}.tex")
            
            # Render Template
            latex_content = template.render(recipe=recipe_data)
            
            # Save rendered LaTeX-File
            with open(output_path, 'w') as file:
                file.write(latex_content)
            
            print(f"{recipe_name}.tex wurde erfolgreich exportiert.")
else:
    # User enters recipe ID
    recipe_id = int(choice)
    
    # Fetch recipe Data
    recipe_data = fetch_recipe_data(recipe_id)
    
    if recipe_data:
        # Name file like recipe (Replace unwanted characters)
        recipe_name = recipe_data['name'].replace(" ", "_").replace("/", "-")
        output_path = os.path.join(output_dir, f"{recipe_name}.tex")
        
        # Render Template
        latex_content = template.render(recipe=recipe_data)
        
        # Save rendered LaTeX-File
        with open(output_path, 'w') as file:
            file.write(latex_content)
        
        print(f"{recipe_name}.tex successfully exported.")
    else:
        print(f"Recipe ID {recipe_id} not found.")
