import requests
import re
import os
from jinja2 import Environment, FileSystemLoader, Template
from fractions import Fraction
from urllib.parse import urlparse

def extract_domain(url):
    if not url:
        return None
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    # Remove "www." Prefix
    domain = re.sub(r'^www\.', '', domain)
    return domain if domain else None

def fetch_recipe_data(recipe_id):
    """Fetches recipe Data from API and extracts domain from source_url"""
    recipe_url = f"[YOUR_TANDOOR_HOST]/api/recipe/{recipe_id}/"
    response = requests.get(recipe_url, headers=headers)
    if response.status_code == 200:
        recipe_data = response.json()
        if 'source_url' in recipe_data and recipe_data['source_url']:
            extracted_domain = extract_domain(recipe_data['source_url'])
            recipe_data['source_domain'] = extracted_domain if extracted_domain else recipe_data['source_url']
        else:
            recipe_data['source_domain'] = None
        return recipe_data
    else:
        print(f"Recipe-ID {recipe_id} could not be found (Status: {response.status_code}).")
        return None

def decimal_to_nicefrac(value):
    try:
        value = float(value)
    except ValueError:
        return value
    if value.is_integer():
        return str(int(value))
    frac = Fraction(value).limit_denominator(8)
    if frac.numerator > frac.denominator:
        whole_number = frac.numerator // frac.denominator
        fraction_part = frac - whole_number
        return f"{whole_number}\\nicefrac{{{fraction_part.numerator}}}{{{fraction_part.denominator}}}"
    else:
        return f"\\nicefrac{{{frac.numerator}}}{{{frac.denominator}}}"

def replace_celsius(value):
    return value.replace("°C", r"\textcelcius")

def replace_min_space(value):
    if isinstance(value, str):
        value = re.sub(r'(\d+)\s+Min\.', r'\1~Min.', value)
        value = re.sub(r'(\d+)\s+min\.', r'\1~min.', value)
        value = re.sub(r'(\d+)\s+Minuten', r'\1~Minuten', value)
    return value

env = Environment(
    loader=FileSystemLoader("templates"),
    block_start_string="<<%",
    block_end_string="%>>",
    variable_start_string="<<",
    variable_end_string=">>",
    comment_start_string="<<#",
    comment_end_string="#>>"
)

env.filters['replace_celsius'] = replace_celsius
env.filters['replace_min_space'] = replace_min_space
env.filters['decimal_to_nicefrac'] = decimal_to_nicefrac

api_url = "[YOUR_TANDOOR_HOST]/api/recipe/"
headers = {
    "Authorization": "Bearer [YOUR_TANDOOR_TOKEN]"
}

response = requests.get(api_url, headers=headers)
if response.status_code == 200:
    data = response.json()
    total_count = data['count']
    print(f"{total_count} Recipes found.")
else:
    print(f"Error: {response.status_code} - {response.text}")
    total_count = 0

choice = input("Would you like to export a certain recipe (enter ID) or all (a)? ")

template = env.get_template('xcookybooky-nswissgerman-11pt.txt')

def download_recipe_image(recipe_data, recipe_name):
    if 'image' in recipe_data and recipe_data['image']:
        image_url = recipe_data['image']
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            image_extension = os.path.splitext(image_url)[1]
            image_path = os.path.join(pictures_dir, f"{recipe_name}{image_extension}")
            with open(image_path, 'wb') as image_file:
                image_file.write(image_response.content)
            print(f"Picture for {recipe_name} downloaded successfully.")
        else:
            print(f"Picture could not be downloaded: {image_url}")
    else:
        print(f"No picture found for {recipe_name}.")

output_dir = "exported_recipes"
os.makedirs(output_dir, exist_ok=True)

pictures_dir = os.path.join(output_dir, "Pictures")
os.makedirs(pictures_dir, exist_ok=True)

if choice.lower() == 'a':
    for recipe_id in range(1, total_count + 1):
        recipe_data = fetch_recipe_data(recipe_id)
        if recipe_data:
            recipe_name = recipe_data['name'].replace("/", "-")
            output_path = os.path.join(output_dir, f"{recipe_name}.tex")
            latex_content = template.render(recipe=recipe_data)
            with open(output_path, 'w') as file:
                file.write(latex_content)
            download_recipe_image(recipe_data, recipe_name)
            print(f"{recipe_name}.tex exported successfully.")
else:
    recipe_id = int(choice)
    recipe_data = fetch_recipe_data(recipe_id)
    if recipe_data:
        recipe_name = recipe_data['name'].replace("/", "-")
        output_path = os.path.join(output_dir, f"{recipe_name}.tex")
        latex_content = template.render(recipe=recipe_data)
        with open(output_path, 'w') as file:
            file.write(latex_content)
        download_recipe_image(recipe_data, recipe_name)
        print(f"{recipe_name}.tex exported successfully.")
    else:
        print(f"Recipe ID {recipe_id} not found.")
