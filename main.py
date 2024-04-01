import argparse
import configparser
import random
from datetime import datetime

from download_manager import download_chapter
from utils import get_all_chapters

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Process some integers.')

# Add arguments to the parser
parser.add_argument('--mangaName', type=str, help='Manga name', required=True)
parser.add_argument('--mangaId', type=str, help='Manga Id', required=True)
parser.add_argument('--folderName', type=str, help='Folder Name', default="")
parser.add_argument('--chapterStart', type=int, help='Chapter start', default=0)
parser.add_argument('--chapterEnd', type=int, help='Chapter end', default=0)

# Parse the command-line arguments
args = parser.parse_args()
manga_name = args.mangaName
manga_id = args.mangaId
chapter_start = args.chapterStart
chapter_end = args.chapterEnd
folder_name = args.folderName

if folder_name == '':
    folder_name = manga_name

# Read configuration from application.properties
config = configparser.ConfigParser()
config.read('application.properties')

resources_host_url = config.get('Default', 'hostUrl')
base_url = resources_host_url + config.get('Default', 'baseUrl') + manga_name + "/"
inManga_url = config.get('Default', 'inMangaHostUrl')
get_all_url = config.get('Default', 'getAllUrl')
destination_folder = config.get('Default', 'destinationFolder')

print(f"{datetime.now()} - Starting scrapper")
print("Get all chapters...")
chapters = get_all_chapters(inManga_url + get_all_url + manga_id)
print(f"Found {len(chapters)} chapters")

if len(chapters) == 0 :
    print("get_all_chapters() returned no chapters!")
else :
    random.shuffle(chapters)
    # Download chapters within the specified range
    download_chapter(manga_name, inManga_url, resources_host_url, base_url, get_all_url, manga_id, chapters, chapter_start, chapter_end, destination_folder, folder_name)

print(f"{datetime.now()} - Ending scrapper")