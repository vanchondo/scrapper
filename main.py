import configparser

from download_manager import download_chapter
from utils import create_folder, get_all_chapters

# Read configuration from application.properties
config = configparser.ConfigParser()
config.read('application.properties')

root_folder = config.get('Default', 'rootFolder')
host_url = config.get('Default', 'hostUrl')
base_url = host_url + config.get('Default', 'baseUrl')
one_piece_id = config.get('Default', 'onePieceId')
chapter_start = int(config.get('Default', 'chapterStart'))
chapter_end = int(config.get('Default', 'chapterEnd'))

# Create the root folder
create_folder(root_folder)

print("Get all chapters...")
chapters = get_all_chapters(host_url + "chapter/getall?mangaIdentification=" + one_piece_id)
print(f"Found {len(chapters)} chapters")

# Download chapters within the specified range
download_chapter(root_folder, host_url, base_url, one_piece_id, chapter_start, chapter_end, config)
