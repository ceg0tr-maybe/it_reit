from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

 
class DataStore:
    polls = {}  
    results = {}  
    user_votes = {}  
    poll_status = {}  

data_store = DataStore()


class UserNameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
    
        layout.add_widget(Label(text="Введите ваше имя:", font_size=24))
        
        self.name_input = TextInput(hint_text="Имя пользователя", multiline=False)
        layout.add_widget(self.name_input)
        
        enter_button = Button(text="Войти")
        enter_button.bind(on_press=self.set_user_name)
        layout.add_widget(enter_button)
        
        self.add_widget(layout)

    def set_user_name(self, instance):
        user_name = self.name_input.text.strip()
        if user_name:
          
            if user_name not in data_store.user_votes:
                data_store.user_votes[user_name] = []  
            self.manager.current = "user"  


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="Выберите пользователя:", font_size=24))
        
        admin_button = Button(text="Администратор", size_hint=(1, 0.3))
        admin_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'admin'))
        layout.add_widget(admin_button)
        
        user_button = Button(text="Жилец", size_hint=(1, 0.3))
        user_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'username'))  
        layout.add_widget(user_button)
        
        self.add_widget(layout)


class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="Администратор: Управление опросами", font_size=24))
        
        create_poll_button = Button(text="Создать опрос")
        create_poll_button.bind(on_press=self.create_poll)
        layout.add_widget(create_poll_button)
        
        view_stats_button = Button(text="Посмотреть статистику")
        view_stats_button.bind(on_press=self.view_stats)
        layout.add_widget(view_stats_button)

       
        finish_poll_button = Button(text="Завершить опрос")
        finish_poll_button.bind(on_press=self.finish_poll)
        layout.add_widget(finish_poll_button)

        back_button = Button(text="Назад в меню")
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu'))
        layout.add_widget(back_button)
        
        self.add_widget(layout)

    def create_poll(self, instance):
        self.manager.current = "create_poll"
    
    def view_stats(self, instance):
        self.manager.current = "stats"
    
    def finish_poll(self, instance):
       
        for poll_title in data_store.polls:
            if data_store.poll_status.get(poll_title, True):  
                data_store.poll_status[poll_title] = False  
                break
        self.manager.current = "admin"

class CreatePollScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.add_widget(Label(text="Создать опрос", font_size=24))
        
        self.poll_title_input = TextInput(hint_text="Название опроса", multiline=False)
        self.layout.add_widget(self.poll_title_input)
        
        self.options_input = TextInput(hint_text="Варианты ответов (через запятую)", multiline=False)
        self.layout.add_widget(self.options_input)
        
        save_button = Button(text="Сохранить")
        save_button.bind(on_press=self.save_poll)
        self.layout.add_widget(save_button)
        
        back_button = Button(text="Назад")
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'admin'))

        self.layout.add_widget(back_button)
        
        self.add_widget(self.layout)

    def save_poll(self, instance):
        title = self.poll_title_input.text.strip()
        options = [opt.strip() for opt in self.options_input.text.split(",") if opt.strip()]
        
        if title and options:
            data_store.polls[title] = options
            data_store.results[title] = {opt: 0 for opt in options}
            data_store.poll_status[title] = True  
            self.poll_title_input.text = ""
            self.options_input.text = ""
            self.manager.current = "admin"

class StatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.add_widget(Label(text="Статистика опросов", font_size=24))
        
        self.add_widget(self.layout)
        back_button = Button(text="Назад")
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'admin'))

        self.layout.add_widget(back_button)
        
    def on_pre_enter(self):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text="Статистика опросов", font_size=24))
        for title, results in data_store.results.items():
            status = " (завершено)" if not data_store.poll_status.get(title, True) else ""
            self.layout.add_widget(Label(text=f"Опрос: {title}{status}"))
            for option, votes in results.items():
                self.layout.add_widget(Label(text=f"{option}: {votes} голосов"))
        back_button = Button(text="Назад")
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'admin'))

        self.layout.add_widget(back_button)


class UserScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.add_widget(Label(text="Выберите опрос", font_size=24))
        
        self.poll_buttons = BoxLayout(orientation='vertical', spacing=10)
        self.layout.add_widget(self.poll_buttons)
        
        back_button = Button(text="Назад")
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu'))

        self.layout.add_widget(back_button)
        
        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.poll_buttons.clear_widgets()
        current_user = list(data_store.user_votes.keys())[-1] 
        for poll_title in data_store.polls:
            if poll_title not in data_store.user_votes.get(current_user, []) and data_store.poll_status.get(poll_title, True): 
                btn = Button(text=poll_title)
                btn.bind(on_press=self.vote)
                self.poll_buttons.add_widget(btn)

    def vote(self, instance):
        poll_title = instance.text
        self.manager.get_screen("vote").poll_title = poll_title
        self.manager.current = "vote"


class VoteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.poll_title = None
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.layout.clear_widgets()
        if not self.poll_title:
            return
        self.layout.add_widget(Label(text=f"Опрос: {self.poll_title}", font_size=24))
       
        for option in data_store.polls[self.poll_title]:
            btn = Button(text=option)
            btn.bind(on_press=self.cast_vote)
            self.layout.add_widget(btn)

    def cast_vote(self, instance):
        option = instance.text
        poll_title = self.poll_title
        current_user = list(data_store.user_votes.keys())[-1]  
        
      
        data_store.results[poll_title][option] += 1
        data_store.user_votes[current_user].append(poll_title) 

       
        self.manager.current = "user"


class PollApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name="main_menu"))
        sm.add_widget(AdminScreen(name="admin"))
        sm.add_widget(CreatePollScreen(name="create_poll"))
        sm.add_widget(StatsScreen(name="stats"))
        sm.add_widget(UserNameScreen(name="username"))  
        sm.add_widget(UserScreen(name="user"))
        sm.add_widget(VoteScreen(name="vote"))
        return sm

if __name__ == "__main__":
    PollApp().run()
           
