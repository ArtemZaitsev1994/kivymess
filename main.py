from aiohttp import web
import json
import MySQLdb
import os


async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    with DataBase() as db:
        async for msg in ws:
            text = msg.data
            print(text)

    return ws

async def get_messages(request):
    with DataBase() as db:
        data = db.get_messages()
    print(data)
    return web.Response(text=data)


app = web.Application()
app.add_routes([
    web.get('/', websocket_handler),
    web.get('/messages', get_messages)
])


class DataBase:
    """
        create table chats 
        (id INT PRIMARY KEY AUTO_INCREMENT, 
        contact VARCHAR(30) NOT NULL, 
        chatname VARCHAR(30) UNIQUE NOT NULL, 
        type INT DEFAULT 0,
        ip VARCHAR(15));
    """

    def __enter__(self):
        self.db = MySQLdb.connect(
        	user='b0efaf87785c65',
        	passwd='df78bf26',
        	host='eu-cdbr-west-02.cleardb.net',
        	db='heroku_dd313defe6a3ba0'
        )
        self.cur = self.db.cursor()
        return self

    def __exit__(self, *kw):
        self.db.commit()
        self.cur.close()
        self.db.close()


    def get_messages(self):
        self.cur.execute(f'SELECT * FROM test_chat')

    def write_message(self, chat_name, message, sender):
        self.cur.execute(f'INSERT test_chat(contact, message) VALUES("{sender}", "{message}")')


if __name__ == '__main__':
    web.run_app(app, port=os.getenv('PORT', 8000))