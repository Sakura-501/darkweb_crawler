"""
使用Tor代理服务器更换代理IP
"""

from stem import Signal
from stem.control import Controller
import socket
import socks
import requests

controller = Controller.from_port(port=9151)  # ControlPort默认端口9151
controller.authenticate()
socks.set_default_proxy(socks.SOCKS5,'127.0.0.1',9050)
socket.socket = socks.socksocket


for i in range(1,11):
    response = requests.get('https://httpbin.org/ip')
    print(response.text)
    controller.signal(Signal.NEWNYM)  # 更换IP
