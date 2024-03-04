import os
import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By

from utils import (create_folder, create_pdf, download_file, get_all_chapters,
                   get_name)


def download_chapter(root_folder, host_url, base_url, one_piece_id, chapter_start, chapter_end, config):
    chapters = get_all_chapters(host_url + "chapter/getall?mangaIdentification=" + one_piece_id)

    # If chapter_end was not provided, use the latest chapter as end.
    if (chapter_end == 0):
        chapter_end = chapters[-1]['FriendlyChapterNumberUrl']

    print(f"Trying to download from chapter {chapter_start} to {chapter_end}")

    for chapter in chapters:
        chapter_number = chapter['FriendlyChapterNumberUrl']
        current_chapter = float(chapter_number.replace('-', '.'))

        if current_chapter >= float(chapter_start) and current_chapter <= float(chapter_end):
            identification = chapter['Identification']
            page_count = chapter['PagesCount']
            print(f"Chapter={current_chapter} pages={page_count}")

            chapter_folder = root_folder + "/" + get_name(chapter_number, "0000")
            create_folder(chapter_folder)

            driver = webdriver.Firefox()
            driver.implicitly_wait(10)
            driver.maximize_window()
            driver.get(base_url + chapter_number + "/" + identification)
            pages = driver.find_elements(By.CLASS_NAME, "ImageContainer")

            current_page_number = 1

            for page in pages:
                page_id = page.get_attribute("id")
                image_url = f"{host_url}images/manga/One-Piece/chapter/{chapter_number}/page/{current_page_number}/{page_id}"
                print(f"Downloading image from: {image_url}")
                file_name = chapter_folder + "/" + get_name(str(current_page_number), "00") + ".jpeg"
                download_file(image_url, file_name)
                current_page_number += 1

            create_pdf(chapter_folder, chapter_folder + ".pdf")
            shutil.rmtree(chapter_folder)
            driver.close()
