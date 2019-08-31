import aiohttp

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


Builder.load_string("""
<Messenger>
	username: username
	open_chat_btn: open_chat_btn
	TextInput:
		id: username
		test: ''
	Button:
		id: open_chat_btn
		text: 'open chat'
		on_press: root.open_chat()


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
		if self.username == '':
			self.open_chat_btn.text = 'open chat\nEnter your name, retard!'
			return
		change_screen('chat')


class ChatWindow(Screen):
	"""docstring for Chat"""
	def __init__(self, **kw):
		super(Chat, self).__init__(**kw)
        self.ws = await session.ws_connect('https://kivymess.herokuapp.com/ws')

	
	def on_enter(self):
        async for msg in self.ws:
            for m in msg.json():
                self.draw_mess(m)
                if msg.data == 'close cmd':
                    await ws.close()
                    break
                else:
                    await ws.send_json(msg.data + '/answer')

    def draw_mess(self, message):
        m = f'{message['sender']}:\n{message['text']}'
        self.messages_area.data.append({'text': m, 'valign': 'top'})

    def send_mess(self):
        url = 'https://kivymess.herokuapp.com/send_mess'
        text = self.message
        self.draw_mess(text)
        self.ws.send_json(data={'sender': MessengerApp.own_name, 'text': text})
        self.message = ''
        # async with session.post(url, json={'sender': MessengerApp.own_name, 'text': text}) as resp:
        #     code = await resp.status
        #     if code == '200':
        #         self.draw_mess(text)




sm =ScreenManager()
sm.add_widget(Messenger(name='main_menu'))
sm.add_widget(ChatWindow(name='chat'))


def change_screen(screen):
    sm.current = screen


class MainApp(App):
	def __init__(self, **kw):
		self.username = ''

	def build(self):
		return sm


if __name__ == '__main__':
	MessengerApp = MainApp()
	MessengerApp.run()