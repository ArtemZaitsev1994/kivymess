from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.lang import Builder 
from kivy.config import ConfigParser
from kivy.core.image import Image
import socket
import urllib.request


Builder.load_string("""
<Messenger>
    username: username
    open_chat_btn: open_chat_btn
    BoxLayout:
        orientation: 'vertical'
        TextInput:
            id: username
            test: ''
        Button:
            id: open_chat_btn
            text: 'open chat'
            on_release: root.open_chat()


<ChatWindow>
    messages_area: messages_area
    message: message
    send_button: send_button
    BoxLayout:
        orientation: 'vertical'
        RecycleView:
            id: messages_area
            viewclass: 'Label'
            RecycleBoxLayout:
                default_size: None, dp(56)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
        BoxLayout:
            size_hint: 1, 0.2
            TextInput:
                id: message
            Button:
                size_hint: 0.3, 1
                id: send_button
                text: 'Отправить'
                on_release: root.send_mess()
""")


class Messenger(Screen):
    def __init__(self, **kw):
        super(Messenger, self).__init__(**kw)

    def open_chat(self):
        if self.username.text == '':
            self.open_chat_btn.text = 'open chat\nEnter your name, retard!'
            return
        MessengerApp.username = self.username
        change_screen('chat')


class ChatWindow(Screen):
    s = socket.socket()
    host = 'https://kivymess.herokuapp.com'
    port = 443
    """docstring for Chat"""
    def __init__(self, **kw):
        super(ChatWindow, self).__init__(**kw)

    def connect(self):
        self.s.connect((self.host, self.port))
        data = self.s.recv(4096).decode()
        strdata = str(data)
        print(strdata)

    def send_message(self):
        text = self.message
        self.s.send(text)
        self.message.text = ''
        self.draw_mess({'text': text, 'sender':MessengerApp.username} )
        self.receive_message()

    def receive_message(self):
        reply = self.s.recv(4096).decode()
        strreply = str(reply)
        print(strreply)
        # self.draw_mess(s)


    def on_enter(self):
        
        response = urllib.request.urlopen('https://kivymess.herokuapp.com/messages')
        print(response.read())
        

    def draw_mess(self, message):
        m = f'{message["sender"]}:\n{message["text"]}'
        self.messages_area.data.append({'text': m, 'valign': 'top'})

    # def send_mess(self):
    #     url = 'https://kivymess.herokuapp.com/send_mess'
    #     text = self.message
    #     self.draw_mess(text)
    #     self.ws.send_json(data={'sender': MessengerApp.username, 'text': text})
    #     self.message = ''
# async with session.post(url, json={'sender': MessengerApp.own_name, 'text': text}) as resp:
# code = await resp.status
# if code == '200':
# self.draw_mess(text)




sm =ScreenManager()
sm.add_widget(Messenger(name='main_menu'))
sm.add_widget(ChatWindow(name='chat'))
sm.current = 'main_menu'


def change_screen(screen):
    sm.current = screen


class MainApp(App):
    def __init__(self, **kw):
        super(MainApp, self).__init__(**kw)
        self.config = ConfigParser()
        self.username = ''

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'user_data', '{}')

    def build(self):
        return sm


if __name__ == '__main__':
    MessengerApp = MainApp()
    MessengerApp.run()