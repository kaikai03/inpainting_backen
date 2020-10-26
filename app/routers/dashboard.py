# coding:utf-8

from typing import List,Dict

from fastapi.websockets import WebSocketDisconnect
from fastapi import APIRouter, WebSocket
from starlette.responses import HTMLResponse, JSONResponse
from starlette.websockets import WebSocket
from fastapi import Body, Path, Query, Header, Request, status, HTTPException

import operator
import factory.inpainting_task as celery_app
import app.constants as con
import time

import factory.monitor_rabbit_consume as rb

router = APIRouter()
signal_cli_list = {}

# -------------- workers listening background --------------
def update_worker(workers):
    workers.sort()
    if not operator.eq(con.worker_online, workers):
        con.worker_online.clear()
        con.worker_online.extend(workers)
        print('celery worker update')
        print('now worker_online:', con.worker_online)
    else:
        print('workers not change:', con.worker_online,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


celery_app.heart_beat_start(update_worker)

# ------------------- rabbit ---------------------------
def signal_cb(worker, message):
    print(worker, ":", message)


def signal_listening_start(worker_name:str, call_back):
    signal_cli = rb.Rabbit_cli(worker_name, call_back)
    signal_cli.connect_init()
    signal_cli.start()
    if worker_name not in signal_cli_list.keys():
        signal_cli_list[worker_name] = signal_cli


def signal_listening_stop(worker_name:str):
    try:
        signal_cli = signal_cli_list[worker_name]
        signal_cli.stop()
        signal_cli.close()
        del signal_cli_list[worker_name]
    except Exception as e:
        print(e)

# signal_listening_start('worker1',signal_cb)

# ------------------- web socket ---------------------------
class ConnectionManager:
    def __init__(self):
        # 存放激活的ws连接对象
        self.active_connections: Dict[str, WebSocket] = {}
        self.active_names: Dict[str, str] = {}

    def alter_socket(self, websocket):
        socket_str = str(websocket)[1:-1]
        socket_list = socket_str.split(' ')
        socket_only = socket_list[3]
        return socket_only

    async def connect(self, ws: WebSocket, worker_name: str):
        # 等待连接
        await ws.accept()
        # 存储ws连接对象
        self.active_connections[worker_name] = ws
        self.active_names[self.alter_socket(ws)] = worker_name

    def disconnect(self, ws: WebSocket):
        # 关闭时 移除ws对象
        worker_name = self.active_names.pop(self.alter_socket(ws))
        del self.active_connections[worker_name]
        return worker_name

    @staticmethod
    async def send_personal_message(message: str, ws: WebSocket):
        # 发送个人消息
        await ws.send_text(message)

    async def broadcast(self, message: str):
        # 广播消息
        for connection in self.active_connections:
            await connection.send_text(message)
    #TODO 连接时创建管道，将管道接收内容转发给客户端

manager = ConnectionManager()


html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>聊天1</title>
</head>
<body>
<h1>User1 Chat</h1>
<form action="" onsubmit="sendMessage(event)">
    <input type="text" id="messageText" autocomplete="off"/>
    <button>Send</button>
</form>
<ul id='messages'>
</ul>

<script>
    var ws = new WebSocket("ws://127.0.0.1:9000/dashboard/ws/%s");

    ws.onmessage = function(event) {
        var messages = document.getElementById('messages')
        var message = document.createElement('li')
        var content = document.createTextNode(event.data)
        message.appendChild(content)
        messages.appendChild(message)
    };
    function sendMessage(event) {
        var input = document.getElementById("messageText")
        ws.send(input.value)
        input.value = ''
        event.preventDefault()
    }
</script>

</body>
</html>
"""


@router.get("/{computer}")
async def get(computer: str):
    return HTMLResponse(html % computer)


@router.websocket("/ws/{computer}")
async def websocket_endpoint(websocket: WebSocket, computer: str):
    # await websocket.accept()
    # while True:
    #     data = await websocket.receive_text()
    #     await websocket.send_text(f"{computer}-Message text was: {data}")
    await manager.connect(websocket, computer)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"你说了: {data}", websocket)
            await manager.broadcast(f"用户:{manager.active_names[manager.alter_socket(websocket)]} 说: {data}")

    except WebSocketDisconnect:
        disconnect_user = manager.disconnect(websocket)
        await manager.broadcast(f"用户-{disconnect_user}-离开")


@router.websocket("/ws/data/{worker}")
async def websocket_endpoint(websocket: WebSocket, worker: str):
    pass


# -------------------normal api---------------------------


@router.get("/workers")
async def get():
    return JSONResponse(status_code=status.HTTP_200_OK, content=con.worker_online)