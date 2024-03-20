import argparse
import configparser

from download_manager import download_chapter
from utils import create_folder, get_all_chapters

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Process some integers.')

# Add arguments to the parser
parser.add_argument('--mangaName', type=str, help='Manga name', required=True)
parser.add_argument('--mangaId', type=str, help='Manga Id', required=True)
parser.add_argument('--chapterStart', type=int, help='Chapter start', default=0)
parser.add_argument('--chapterEnd', type=int, help='Chapter end', default=0)

# Parse the command-line arguments
args = parser.parse_args()
manga_name = args.mangaName
manga_id = args.mangaId
chapter_start = args.chapterStart
chapter_end = args.chapterEnd

# Read configuration from application.properties
config = configparser.ConfigParser()
config.read('application.properties')

resources_host_url = config.get('Default', 'hostUrl')
base_url = resources_host_url + config.get('Default', 'baseUrl') + manga_name + "/"
inManga_url = config.get('Default', 'inMangaHostUrl')
get_all_url = config.get('Default', 'getAllUrl')

print("Get all chapters...")
chapters = get_all_chapters(inManga_url + get_all_url + manga_id)
print(f"Found {len(chapters)} chapters")

# Download chapters within the specified range
download_chapter(manga_name, inManga_url, resources_host_url, base_url, get_all_url, manga_id, chapter_start, chapter_end)
