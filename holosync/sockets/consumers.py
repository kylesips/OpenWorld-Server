from django.http import HttpResponse
from channels import Group
from channels.handler import AsgiHandler
from time import sleep
import json
from .debug import SocketDebugger

sd = SocketDebugger()
sd.toggle_debug_mode()

DEMO_GROUP = "demo"
DEMO_GROUP_LIST = []

####################################################
## HTTP Consumer as per Django Channels tutorial  ##
####################################################


def http_consumer(message):
  # Make standard HTTP response - access ASGI path attribute directly
  response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
  # Encode that response into message format (ASGI)
  for chunk in AsgiHandler.encode_response(response):
    message.reply_channel.send(chunk)

####################################################
##  Echo server as per Django Channels tutorial   ##
####################################################

# Handle initial connection
def ws_echo_service_connect(message):
  # Accept connection
  message.reply_channel.send({"accept": True})
  if(sd.get_debug_mode()):
    message.reply_channel.send({
      "text": sd.get_random_insult()
    })

####################################################
##     Groups as per Django Channels tutorial     ##
####################################################

# Connected to websocket.connect
def ws_add(message):
    # Accept the incoming connection
    message.reply_channel.send({"accept": True})

    # Display message reply channel in console
    print("Message Reply Channel:\n", message.reply_channel)

    # Add them to the chat group
    # Group(DEMO_GROUP).add(message.reply_channel)
    DEMO_GROUP_LIST.append(message.reply_channel)

# Connected to websocket.receive
def ws_message(message):
  # ASGI WebSocket packet-received and send-packet message types
  # both have a "text" key for their textual data.

  # Note that we care also about the order, reply_channel, and path!!

  if 'text' in message.content: # Handle plain-text data
    output = {"text": message.content['text']}
    print("Plain text message received:\n")
    print(message.content['text'])
  else:  # Handle binary data
    print("Binary data received:\n")
    print(message.content['bytes'])
    output = {"bytes": message.content['bytes']}

  print("Sending message to group (excluding sender)...")
  if(len(DEMO_GROUP_LIST) == 1 and DEMO_GROUP_LIST[0].name == message.reply_channel.name): # Base case for single connection testing
    message.reply_channel.send(output)
  else:
    for channel in DEMO_GROUP_LIST:
      if channel.name != message.reply_channel.name: # Send message to all other devices in the group
        channel.send(output)


  #Group(DEMO_GROUP).discard(message.reply_channel)
  #Group(DEMO_GROUP).send(output,immediately=True)
  #Group(DEMO_GROUP).add(message.reply_channel)

# Connected to websocket.disconnect
def ws_disconnect(message):
    #Group(DEMO_GROUP).discard(message.reply_channel)
    try:
      DEMO_GROUP_LIST.remove(message.reply_channel)
    except ValueError:
      pass  # or scream: thing not in some_list!

