from typing import List
from typing import Union
from pydantic import BaseModel
import app.constants as con
from fastapi import FastAPI, Path, Query, Header, Request, status, File, UploadFile, Form, HTTPException
# from fastapi.responses import HTMLResponse
from starlette.responses import HTMLResponse, JSONResponse, FileResponse
import app.utils as u


from fastapi.encoders import jsonable_encoder

import shutil, os

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

class task_param(BaseModel):
    fps: int
    frames: int
    scan: int
    track: Union['double-straight-line', 'straight-line', 'circle']
    postfix: List[str]
    zoomx: List[float]
    zoomy: List[float]
    zoomz: List[float]
    goods: List[str]




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
    return FileResponse(con.img_folder_full + name)


@router.get("/v/{v_name}")
async def get_video(*, v_name: str):
    return FileResponse(con.video_folder_full + v_name)


@router.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    logs = []
    for index, file in enumerate(files):
        content = await file.read()
        if len(content) > 0:
            file_name = u.standardization_filename(file.filename)
            addr = con.upload_tmp_full + file_name
            with open(addr, 'wb') as f:
                f.write(content)
                logs.append({'index': index, 'origin': file.filename, 'type': file.content_type, 'save_name': file_name})
        else:
            logs.append({'index': index, 'status': 'isn`t file'})
    return {"filenames": logs}


@router.post("/uploadimg/")
async def create_upload_file(img: UploadFile = File(...)):
    content = await img.read()
    if len(content) > 0:
        file_name = u.standardization_filename(img.filename)
        addr = con.upload_tmp_full + file_name
        with open(addr, 'wb') as f:
            f.write(content)
            return {'origin': img.filename, 'type': img.content_type, 'save_name': file_name}
    return {"error": "1"}


@router.get("/up.html")
async def main():
    content = """
            <body>
            <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
            <input name="files" type="file" multiple />
            <input name="tx" type="text" value="22222" style="display:none;"/>
            <textarea  name="tx" type="text" style="display:none;"> 222</textarea>
            <input type="submit" />
            </form>
            </body>
             """
    return HTMLResponse(content=content)

@router.post("/uploadtask/")
async def create_task(upload: task_param):
    # 接受到任务，根据图片数量分解成单个图片的任务
    print("uploadtask:", jsonable_encoder(upload))

    upload_dic = jsonable_encoder(upload)
    tasks = []
    for img in upload_dic['goods']:
        task = upload_dic.copy()
        del task['goods']
        task['img'] = img
        tasks.append(task)

    if len(tasks) > 0:
        result = con.global_db.work_create(tasks)

    # 检查任务入库状态，如果发现存在入库失败，则手工回滚，并返回存储失败。
    for id_ in result:
        if not type(id_) is int:
            con.global_db.work_drop(doc_ids=[tmp for tmp in result if type(tmp) is int])
            return JSONResponse(status_code=status.HTTP_507_INSUFFICIENT_STORAGE)

    # 将任务图片移出临时文件夹，并返回最终生成的实际任务。
    tasks_results = []
    for id_ in result:
        task = con.global_db.workqueue.get(doc_id=id_)
        img_name = task['img']

        # 如果图片在tmp，则移动到img文件夹
        # 某些意外情况，如果图片不在tmp，但img里有，则任务继续
        # 如果tmp与img都没有，报错。
        if os.path.exists(con.upload_tmp_full+img_name):
            shutil.move(con.upload_tmp_full+img_name, con.img_folder_full+img_name)
        elif os.path.exists(con.img_folder_full+img_name):
            continue
        else:
            con.global_db.work_drop(doc_ids=[tmp for tmp in result if type(tmp) is int])
            return JSONResponse(status_code=status.HTTP_507_INSUFFICIENT_STORAGE)
        tasks_results.append(task)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=tasks_results)


@router.post("/droptask/")
async def drop_task(task: task_param):
    # todo 文件标记，图片移动等
    pass


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