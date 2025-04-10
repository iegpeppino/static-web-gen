import os
from pathlib import Path
from .block_converter import extract_title, markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Assign the markdown text to a variable
    with open(from_path, "r") as md:
        markdown_file = md.read()
        md.close()
    # Assign the empty template to a variable 
    with open(template_path, "r") as tmp:
        template = tmp.read()
        tmp.close()
    # Extracting title to display from markdown text
    title = extract_title(markdown_file)
    # Markdown converted to html_node
    converted_md = markdown_to_html_node(markdown_file)
    # html node converted to string
    html_string = converted_md.to_html()
    # Fill the empty template with the html string and extracted title
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    
    # Making sure the destiny directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True) 
    
    # Write the new static page file
    with open(dest_path, "w") as html_file:
        html_file.write(template)
        html_file.close()

    return print("HTML file was created!")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        # Check if is file
        if os.path.isfile(src_path):
            # If file, a static page is generated
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(src_path, template_path, dest_path)
        else:
            # If not, it is a directory and it calls the function recursively
            generate_pages_recursive(src_path, template_path, dest_path)