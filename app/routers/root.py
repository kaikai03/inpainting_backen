from typing import List
from typing import Union
from pydantic import BaseModel
import app.constants as con
from fastapi import FastAPI, Path, Query, Header, Request, status, File, UploadFile, Form, HTTPException
# from fastapi.responses import HTMLResponse
from starlette.responses import HTMLResponse, JSONResponse


from fastapi.encoders import jsonable_encoder



from fastapi import APIRouter



router = APIRouter()


class video_item(BaseModel):
    item_id: int = None
    index: int = None
    name: str = None
    status: Union['pic', 'video', 'error'] = 'pic'
    description: str = None
    error: str = None
    cover: str
    src: List[str] = None


@router.get("/random/{count}", response_model=List[video_item])
async def rand_video(*, count: int):
    items = con.global_db.get_random(count)
    videos = []
    for index, item in enumerate(items):
        v = video_item(**item)
        v.index = index
        videos.append(v)
    return videos


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