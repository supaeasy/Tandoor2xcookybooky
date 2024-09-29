# Tandoor2xcookybooky
A tiny script using jinja2 Templating for transscription of recipes into LaTeX documents


- You need to create an api Token first. Visit [tandoor-recipe host and port]/api/access-token/ and create a token. In scope enter "read" (omit quotation marks)
- Enter your IP and token into start_engl.py
- run python3 start_engl.py

What does this do?

This script saves one or all (user selection) recipes from Tandoor recipes into .tex files using xcookybooky package and downloads its corresponding image. You will need to render these files with a LaTeX interpreter. The simplest way is to upload all of the .tex files and the Picture folder to overleaf.com In the same folder as .tex files in overleaf add xcookybooky.cfg and edit it to your needs. Here you can adjust the language.

![image](https://github.com/user-attachments/assets/d5f10d6c-317a-4bde-90d2-39af8683c01d)
