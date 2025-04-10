import os
import shutil
from .page_generator import generate_pages_recursive
from .file_management import move_static_to_public

STATIC_DIR_PATH = "./static"
PUBLIC_DIR_PATH = "./public"
CONTENT_DIR_PATH = "./content"
TEMPLATE_PATH = "./template.html"

def main():
    move_static_to_public(STATIC_DIR_PATH, PUBLIC_DIR_PATH)
    generate_pages_recursive(CONTENT_DIR_PATH, TEMPLATE_PATH, PUBLIC_DIR_PATH)
    

if __name__ == "__main__":
    main()
