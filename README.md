# Tandoor2xcookybooky
A tiny script using jinja2 Templating for transscription of recipes into LaTeX documents


- You need to create an api Token first. Visit [tandoor-recipe host and port]/api/access-token/ and create a token. In scope enter "read" (omit quotation marks)
- Enter your IP and port in 2 places where it says [YOUR_TANDOOR_HOST] into start_engl.py
- add [YOUR_TANDOOR_TOKEN] into start_engl.py including tda_
- You may want to adjust pdfauthor={yourname}, \usepackage[nswissgerman]{babel} and maybe adjust the text size in xcookybooky-nswissgerman-11pt.txt
- adjust xcookybooky.cfg to your needs
- run python3 start_engl.py

What does this do?

This script saves one or all (user selection. The ID is the last number shown in URL bar when viewing a recipe) recipes from Tandoor recipes into .tex files using xcookybooky package and downloads its corresponding image. You will need to render these files with a LaTeX interpreter. The simplest way to do this is uploading all of the .tex files and the Picture folder to overleaf.com. In the same folder as .tex files in overleaf add xcookybooky.cfg and edit it to your needs. You can adjust the language of headers here.

Plurals as well as Fractions are supported. If you (like me) like to have empty units for normally unitless items but don't want to miss out on conversion functions, you can create a unit "-" (without quotation marks) in Tandoor recipes. This will be filtered when creating the .tex file.

If you feel like spacing looks a little odd between step paragraphs, try adding more text per step/reducing steps and/or setting the font size to 12pt. At least 3 Lines of text per step are recommended.

![image](https://github.com/user-attachments/assets/a8b35a96-35c9-476d-a85f-af443b45c91d)
