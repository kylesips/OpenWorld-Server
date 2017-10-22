from django.http import HttpResponse
from channels.handler import AsgiHandler

# Example consumer for handling HTTP requests as opposed to Django view layer
def http_consumer(message):
    # Make standard HTTP response - access ASGI path attribute directly
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)

# Example WebSockets message consumer
def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.

    # Note that we care also about the order, reply_channel, and path!!

    # Handle plain-text data
    if 'text' in message.content:
      message.reply_channel.send({
        "text": message.content['text'],
      })
    else: # Handle binary data
      print("Binary data received:\n")
      print(message.content['bytes'])

      message.reply_channel.send({
        "bytes": message.content['bytes']
      })
