from app.global_db import db

host = '127.0.0.1'
port = 9000
address = f"{host}:{port}"
global_db = db
query = db.query
query2 = db.query2

root_folder = './'
upload_tmp = 'tmp/'
img_folder = 'img/'
video_folder = 'video/'
