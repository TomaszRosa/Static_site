from textnode import *
from htmlnode import *
from BlockType import *
import os
import shutil

def copy_public(src, dest):
    copy_files = os.listdir(src)
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest, exist_ok=True)
    for file in copy_files:
        if os.path.isfile(os.path.join(src, file)):
            shutil.copy(os.path.join(src, file), dest)
        else:
            os.makedirs(os.path.join(dest, file), exist_ok=True)
            copy_public(os.path.join(src, file), os.path.join(dest, file))

def extract_title(markdown):
    markdown = markdown.split("\n")
    for mark in markdown:
        if mark.startswith("# "):
            return mark[2:].strip()
    raise Exception("No title")
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        from_files = file.read()
    with open(template_path, "r") as file:
        template_file = file.read()

    html = markdown_to_html_node(from_files).to_html()
    title = extract_title(from_files)
    output = template_file.replace("{{ Content }}", html).replace("{{ Title }}", title)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(output)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    markdowns = os.listdir(dir_path_content)
    for markdown in markdowns:
        if os.path.isfile(os.path.join(dir_path_content, markdown)) and markdown[-3:] == ".md":
            generate_page(os.path.join(dir_path_content, markdown), template_path, os.path.join(dest_dir_path, markdown.replace(".md", ".html")))
        elif os.path.isdir(os.path.join(dir_path_content, markdown)):
            os.makedirs(os.path.join(dest_dir_path, markdown), exist_ok=True)
            generate_pages_recursive(os.path.join(dir_path_content, markdown), template_path, os.path.join(dest_dir_path, markdown))



def main():

    copy_public('static', 'public')
    generate_pages_recursive('content', 'template.html', 'public')

main()