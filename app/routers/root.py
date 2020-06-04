from typing import List
from typing import Union
from pydantic import BaseModel
import app.constants as con
from fastapi import FastAPI, Path, Query, Header, Request, status, File, UploadFile, Form, HTTPException
# from fastapi.responses import HTMLResponse
from starlette.responses import HTMLResponse, JSONResponse, FileResponse
import app.utils as u


from fastapi.encoders import jsonable_encoder



from fastapi import APIRouter



router = APIRouter()


class task_item(BaseModel):
    item_id: int = None
    index: int = None
    name: str = None
    status: Union['pic', 'video', 'error'] = 'pic'
    description: str = None
    error: str = None
    cover: str
    src: List[str] = None


@router.get("/random/{count}", response_model=List[task_item])
async def rand_tasks(*, count: int):
    items = con.global_db.get_random(count)
    tasks = []
    for index, item in enumerate(items):
        v = task_item(**item)
        v.index = index
        tasks.append(v)
    return tasks


@router.get("/cover/{name}")
async def get_cover(*, name: str):
    return FileResponse(con.root_folder + con.img_folder + name)


@router.get("/v/{v_name}")
async def get_video(*, v_name: str):
    return FileResponse(con.root_folder + con.video_folder + v_name)


@router.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    logs = []
    for index, file in enumerate(files):
        content = await file.read()
        file_name = u.standardization_filename(file.filename)
        addr = con.root_folder + con.upload_tmp + file_name
        with open(addr, 'wb') as f:
            f.write(content)
            logs.append({'index': index, 'origin': file.filename, 'type': file.content_type, 'save_name': file_name})
    return {"filenames": logs}


@router.get("/up.html")
async def main():
    content = """
            <body>
            <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
            <input name="files" type="file" multiple>
            <input type="submit">
            </form>
            </body>
             """
    return HTMLResponse(content=content)



# con.global_db.workqueue.remove(con.query.item_id.exists())
# it = con.global_db.workqueue.search(con.query.doc == '27adb294-a497-11ea-9eb4-2c4d54698d66')
# it[0].get('doc1') is None
# con.global_db.work_finish("26659cf4-a4a8-11ea-8ef0-2c4d54698d66")
#
# #
# # con.global_db.completed.remove(con.query.doc == '27adb294-a497-11ea-9eb4-2c4d54698d66')
# con.global_db.work_drop(['9145d4f4-a495-11ea-8837-2c4d54698d66'])
# con.global_db.completed.get(doc_id=7)
# con.global_db.get_last_item_id()
#
#
# con.global_db.get_random(2)