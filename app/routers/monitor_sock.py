# coding:utf-8

from typing import List

from fastapi.websockets import WebSocketDisconnect
from fastapi import APIRouter, WebSocket
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        # 存放激活的ws连接对象
        self.active_connections: List[WebSocket] = []
        self.active_name: dict = {}

    def alter_socket(self, websocket):
        socket_str = str(websocket)[1:-1]
        socket_list = socket_str.split(' ')
        socket_only = socket_list[3]
        return socket_only

    async def connect(self, ws: WebSocket, computer: str):
        # 等待连接
        await ws.accept()
        # 存储ws连接对象
        self.active_connections.append(ws)
        self.active_name[self.alter_socket(ws)] = computer

    def disconnect(self, ws: WebSocket):
        # 关闭时 移除ws对象
        self.active_connections.remove(ws)
        return self.active_name.pop(self.alter_socket(ws))

    @staticmethod
    async def send_personal_message(message: str, ws: WebSocket):
        # 发送个人消息
        await ws.send_text(message)

    async def broadcast(self, message: str):
        # 广播消息
        for connection in self.active_connections:
            await connection.send_text(message)


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
    var ws = new WebSocket("ws://127.0.0.1:9000/monitor/ws/%s");

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
            await manager.broadcast(f"用户:{manager.active_name[manager.alter_socket(websocket)]} 说: {data}")

    except WebSocketDisconnect:
        disconnect_user = manager.disconnect(websocket)
        await manager.broadcast(f"用户-{disconnect_user}-离开")


import operator
import factory.inpainting_task as celery_app
import app.constants as con


def update_worker(workers):
    if not operator.eq(con.worker_online, workers):
        con.worker_online.clear()
        con.worker_online.extend(workers)
        print('celery worker update')
        print('now worker_online:', con.worker_online)

celery_app.heart_beat_start(update_worker)