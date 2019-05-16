#coding=utf-8
from channels.routing import  route
from wxRobot.consumers import ws_connect,ws_disconnect,ws_message

print('hello world')
channel_routing = [
    route('websocket.connect',ws_connect),
    route('websocket.disconnect',ws_disconnect),
    route('websocket.message',ws_message),
]

