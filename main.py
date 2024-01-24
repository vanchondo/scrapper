import configparser
import shutil
import uuid

from flask import Flask, send_file

from download_manager import download_chapter
from utils import create_folder, get_name

app = Flask(__name__)

# Read configuration from application.properties
config = configparser.ConfigParser()
config.read('application.properties')

host_url = config.get('Default', 'hostUrl')
base_url = host_url + config.get('Default', 'baseUrl')

@app.route('/download/name/<name>/id/<mangaId>/chapter/<chapter>', methods=['POST'])
def download(name, mangaId, chapter):
    print(f"Received request to download name={name}, mangaId={mangaId}, chapter={chapter}")

    url = base_url + name + "/"

    # Generate a UUID
    new_uuid = uuid.uuid4()
    # Convert the UUID to a string
    uuid_string = str(new_uuid)

    root_folder = name + "-" + uuid_string
    # Download chapters within the specified range
    download_chapter(root_folder, host_url, url, name, mangaId, int(chapter), int(chapter))

    # Specify the path to your PDF file
    pdf_path = root_folder + "/" + get_name(chapter, "0000") + ".pdf"

    # Return the PDF file as a response
    response = send_file(pdf_path, as_attachment=True)

    # Delete folder
    shutil.rmtree(root_folder)

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6066)
