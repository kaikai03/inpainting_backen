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
import threading
import time
import asyncio
router = APIRouter()


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
class RabbitManager:
    """每一个worker创建一个管道，不重复创建"""
    def __init__(self):
        self.clis_dic = {}

    @staticmethod
    def cb(worker, message):
        # callback to deal the message from rabbit
        # default is sending to front page
        print("RabbitManager", worker, ":", message)

    def listening_start(self, worker_name: str, call_back=cb):
        if worker_name in self.clis_dic.keys():
            print("RabbitManager this worker is in working:", worker_name)
            return False
        cli = rb.Rabbit_cli(worker_name, call_back)
        cli.connect_init()
        cli.start()
        self.clis_dic[worker_name] = cli
        print("RabbitManager listening_start:", worker_name)
        return True

    def listening_stop(self, worker_name: str):
        try:
            signal_cli = self.clis_dic[worker_name]
            signal_cli.stop()
            signal_cli.close()
            del self.clis_dic[worker_name]
        except Exception as e:
            print(e)


# rabbits_manager = RabbitManager(websoket_manager)
# rabbits.listening_start('worker1')
# signal_listening_start('worker1')

# ------------------- web socket ---------------------------
class ConnectionManager:
    """每一个worker创建一个管道，不重复创建。当一个worker下没有ws连接（没被监听），则关闭管道"""
    def __init__(self):
        # 存放激活的ws连接对象
        self.active_connections: Dict[str, tuple] = {}
        self.ws_in_worker: Dict[str, list] = {}
        self.rabbits_manager = RabbitManager()
        self.last_message_cache = {}
        self.message_dealing_timer = None

    def rabbits_cb(self, worker, message):
        print("get and save")
        wss = self.ws_in_worker[worker]
        for ws in wss:
            self.last_message_cache[self.alter_socket(ws)] = message

    def alter_socket(self, ws: WebSocket):
        socket_str = str(ws)[1:-1]
        socket_list = socket_str.split(' ')
        socket_only = socket_list[3]
        return socket_only

    def get_name_from_connections(self, ws: WebSocket):
        return self.active_connections[self.alter_socket(ws)][1]

    async def connect(self, ws: WebSocket, worker_name: str):
        # TODO 连接时创建管道，将管道广播给对应前端
        # 等待连接
        await ws.accept()
        # 存储ws连接对象
        self.active_connections[self.alter_socket(ws)] = (ws, worker_name)
        ws_list = self.ws_in_worker.get(worker_name, None)
        assert self.rabbits_cb is not None
        self.rabbits_manager.listening_start(worker_name, self.rabbits_cb)
        if ws_list is None:
            self.ws_in_worker[worker_name] = [ws]
        else:
            ws_list.append(ws)
        await ws.send_text("hello")

    def disconnect(self, ws: WebSocket):
        # 关闭时 移除ws对象
        # TODO 如果完全没被监听的worker，关闭管道
        worker_name = self.active_connections[self.alter_socket(ws)][1]
        self.ws_in_worker[worker_name].remove(ws)
        del self.active_connections[self.alter_socket(ws)]
        self.rabbits_manager.listening_stop(worker_name)
        if self.last_message_cache.get(self.alter_socket(ws), False):
            del self.last_message_cache[self.alter_socket(ws)]
        return self.alter_socket(ws), worker_name


        # self.message_dealing_timer = threading.Timer(5.0, self.message_dealing_start)
        # self.message_dealing_timer.start()


    async def send_message_worker(self, message: str, worker_name: str):
        wss = self.ws_in_worker[worker_name]
        for ws in wss:
            await ws.send_text(message)

    async def send_message_ws(self, message: str, ws: WebSocket):
        await ws.send_text(message)

    async def broadcast(self, message: str):
        # 广播消息
        for ws_id in self.active_connections.keys():
            ws = self.active_connections[ws_id][0]
            await ws.send_text(message)


websocket_manager = ConnectionManager()


# websocket_manager.rabbits_cb = lambda worker, message:\
#     (print('ConnectionManager', worker), websocket_manager.send_message_worker(message, worker))


@router.websocket("/ws/data/{worker_called}")
async def websocket_backen(websocket: WebSocket, worker_called: str):
    await websocket_manager.connect(websocket, worker_called)
    try:
        while True:
            message = websocket_manager.last_message_cache.get(websocket_manager.alter_socket(websocket), '')
            if len(message) > 0:
                websocket_manager.last_message_cache[websocket_manager.alter_socket(websocket)] = ''
                await websocket_manager.send_message_ws(message, websocket)
                print('senttttttttttttttttttttttttttttt')
                await asyncio.sleep(5.0)
            else:
                print('stoptoptop')
                await asyncio.sleep(5.0)
            # data = await websocket.receive_text()
            # print(websocket_manager.alter_socket(websocket), ':', data)
    except WebSocketDisconnect:
        disconnect_user = websocket_manager.disconnect(websocket)[0]
        print(f"用户-{disconnect_user}-离开")

# -------------------normal api---------------------------


@router.get("/workers")
async def get_workers():
    return JSONResponse(status_code=status.HTTP_200_OK, content=con.worker_online)





# -------------------test ---------------------------

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
async def websocket_test(websocket: WebSocket, computer: str):
    await websocket_manager.connect(websocket, computer)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket_manager.send_message_ws(f"你说了: {data}", websocket)
            await websocket_manager.broadcast(
                f"用户:{websocket_manager.get_name_from_connections(websocket)} 说: {data}")

    except WebSocketDisconnect:
        disconnect_user = websocket_manager.disconnect(websocket)[0]
        await websocket_manager.broadcast(f"用户-{disconnect_user}-离开")
