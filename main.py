from aiohttp import web
import json
import MySQLdb
import os

async def all_news(request):
    print(2)
    result = request.transport.get_extra_info('peername')
    with DataBase() as db:
        print(3)
        db.get_or_create_chat('test')
        db.write_message('test', 'some message', 'artem')
    print(4)
    with DataBase() as db:
        result = db.get_messages('test')

    return web.Response(text=json.dumps(result))


async def second(request):
    print(2)
    result = request.transport.get_extra_info('peername')
    with DataBase() as db:
        print(3)
        db.get_or_create_chat('test')
        db.write_message('test', 'some message', 'artem')
    print(4)
    with DataBase() as db:
        result = db.get_messages('test')

    return web.Response(text=json.dumps(result))


app = web.Application()
app.add_routes([
    web.get('/', all_news),
    web.get('/second', second)
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
        self.db = MySQLdb.connect(user='b0efaf87785c65',passwd='df78bf26',db='eu-cdbr-west-02.cleardb.net')
        self.cur = self.db.cursor()
        return self

    def __exit__(self, *kw):
        self.db.commit()
        self.cur.close()
        self.db.close()

    def add_chat(self, args):
        self.cur.execute(f'INSERT chats(contact, chatname, type, ip) VALUES("{args[0]}", "{args[1]}", {args[2]}, "{args[3]}")')
        # self.cur.execute(ADD_CHAT_QUERY % ', '.join(args))

    def get_all_chats(self):
        GET_ALL_CHATS_QUERY = 'SELECT * FROM chats'
        self.cur.execute(GET_ALL_CHATS_QUERY)
        return self.cur.fetchall()

    def get_chat(self, name):
        GET_CHAT_QUERY = f'SELECT * FROM chats WHERE chatname={name}'
        self.cur.execute(GET_CHAT_QUERY)
        return self.cur.fetchone()

    def get_or_create_chat(self, chat_name):
        CREATE_TABLE_QUERY = f"""
            CREATE TABLE IF NOT EXISTS {chat_name}_chat 
            (id INT PRIMARY KEY AUTO_INCREMENT, 
            contact VARCHAR(30) NOT NULL,
            message TEXT);"""
        self.cur.execute(CREATE_TABLE_QUERY)

    def get_messages(self, chat_name):
        self.cur.execute(f'SELECT * FROM {chat_name}_chat')

    def write_message(self, chat_name, message, sender):
        self.cur.execute(f'INSERT {chat_name}_chat(contact, message) VALUES("{sender}", "{message}")')


if __name__ == '__main__':
    print(1)
    web.run_app(app, port=os.getenv('PORT', 8000))