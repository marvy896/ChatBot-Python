import asyncio
import socketio
import requests
from chatbot import messageBot

sio = socketio.AsyncClient()

@sio.event
async def connect():
    await sio.emit("currentRoom", 'personal')
    await sio.emit("chat message", ('hello','personal'))
    print('connection established')

@sio.event
async def my_message(data):
    print('message received with ', data)
    await sio.emit('my response', {'response': 'my response'})

@sio.on('chat message')
async def handleChatMessage(msg, UrlRoomId):
    if (msg['username'] != 'bot' and UrlRoomId == 'personal'):
        res = messageBot(msg['message'])
        await sio.emit("chat message", (res,'personal'))
        print(f'I received a message!{msg, UrlRoomId}')


@sio.event
async def disconnect():
    print('disconnected from server')

async def main():
    await sio.connect('http://localhost:3000')
    await sio.wait()

if __name__ == '__main__':
    # sending post request and saving response as response object
    r = requests.post(url='http://localhost:3000/user', json= {'username': 'bot'})
    # extracting response text
    pastebin_url = r.text
    print("The pastebin URL is:%s" % pastebin_url)
    asyncio.run(main())
 