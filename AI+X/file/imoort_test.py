import os
from xml.etree.ElementTree import parse
from exts import db
from models import VideoModel

def import_xml(xml_path='E:/A-10-Temporary_test/last_test/flask-qa-main/AI+X/file/movie.xml',
               movie_folder_path = 'E:/A-10-Temporary_test/last_test/flask-qa-main/AI+X/static/movie'):
    tree = parse(xml_path)
    root = tree.getroot()

    for movie in root.findall('movie'):
        title = movie.findtext('title')
        file = movie.findtext('file')
        count = int(movie.findtext('count'))

        # Generate url path from file name
        url = os.path.join('../static/movie', file)

        # Generate file path from folder path and file name
        file_path = os.path.join(movie_folder_path, file)

        # Check if file exists
        if not os.path.isfile(file_path):
            print(f'File not found: {file_path}')
            continue

        # Create VideoModel instance
        video = VideoModel(title=title, file=file, url=url, count=count)

        # Add to database session
        db.session.add(video)

    # Commit changes to database
    db.session.commit()

