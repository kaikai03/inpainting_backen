from app.global_db import db

host = '127.0.0.1'
port = 9000
address = f"{host}:{port}"
global_db = db
query = db.query
query2 = db.query2

root_folder = 'D:\\dev_tmp\\'
upload_tmp = 'tmp\\'
img_folder = 'imgs\\'
video_folder = 'v\\'
trash_folder = 'trash\\'

upload_tmp_full = root_folder + upload_tmp
img_folder_full = root_folder + img_folder
video_folder_full = root_folder + video_folder
trash_folder_full = root_folder + video_folder
