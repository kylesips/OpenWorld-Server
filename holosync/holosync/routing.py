from channels.routing import route
from sockets.consumers import ws_add, ws_message, ws_disconnect

channel_routing = [
  route("websocket.connect", ws_add),
  route("websocket.receive", ws_message),
  route("websockets.disconnect", ws_disconnect)
]
