import os
import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from utils import (create_folder, create_pdf, download_file, get_all_chapters,
                   get_name)


def download_chapter(manga_name, inManga_url, resources_host_url, base_url, get_all_url, manga_id, chapter_start, chapter_end, destination_folder, folder_name):
    chapters = get_all_chapters(inManga_url + get_all_url + manga_id)

    # If chapter_end was not provided, use the latest chapter as end.
    if (chapter_end == 0):
        chapter_end = chapters[-1]['FriendlyChapterNumberUrl']

    # If chapter_start was not provided, use the latest chapter as end.
    if (chapter_start == 0):
        chapter_start = chapters[-1]['FriendlyChapterNumberUrl']

    print(f"Trying to download from chapter {chapter_start} to {chapter_end}")

    for chapter in chapters:
        chapter_number = chapter['FriendlyChapterNumberUrl']
        current_chapter = float(chapter_number.replace('-', '.'))

        if current_chapter >= float(chapter_start) and current_chapter <= float(chapter_end):
            identification = chapter['Identification']
            page_count = chapter['PagesCount']
            print(f"Chapter={current_chapter} pages={page_count}")

            chapter_folder_tmp = folder_name + " v" + get_name(chapter_number, "0000")
            create_folder(chapter_folder_tmp)

            options = Options()
            options.add_argument("-headless")
            with webdriver.Firefox(options=options) as driver:
                driver.implicitly_wait(10)
                driver.get(base_url + chapter_number + "/" + identification)
                pages = driver.find_elements(By.CLASS_NAME, "ImageContainer")

                current_page_number = 1

                for page in pages:
                    page_id = page.get_attribute("id")
                    image_url = f"{resources_host_url}images/manga/{manga_name}/chapter/{chapter_number}/page/{current_page_number}/{page_id}"
                    print(f"Downloading image from: {image_url}")
                    file_name = chapter_folder_tmp + "/" + get_name(str(current_page_number), "00") + ".jpeg"
                    download_file(image_url, file_name)
                    current_page_number += 1

            output_folder = destination_folder + folder_name + "/"
            create_folder(output_folder)
            create_pdf(chapter_folder_tmp, output_folder + chapter_folder_tmp + ".pdf")
            shutil.rmtree(chapter_folder_tmp)