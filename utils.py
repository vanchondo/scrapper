import json
import os

import requests
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def download_file(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)
    else:
        print(f"Failed to download the image. Status code: {response.status_code}")

def create_pdf(folder_path, output_pdf):
    image_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))])
    pdf = canvas.Canvas(output_pdf, pagesize=letter)

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        img = Image.open(image_path)
        img_width, img_height = img.size
        max_width, max_height = letter
        scale = min(max_width / img_width, max_height / img_height)

        pdf.drawInlineImage(image_path, 0, 0, width=img_width * scale, height=img_height * scale)
        pdf.showPage()

    pdf.save()

def get_all_chapters(url):
    response = requests.get(url)

    if response.status_code == 200:
        page = json.loads(response.text)
        pageData = json.loads(page['data'])
        return pageData['result']
    else:
        print(f"Invalid response {response}")
        return {}

def create_folder(folder):
    os.makedirs(folder, exist_ok=True)

def get_name(name, prefix):
    return (prefix + name)[len(name):]