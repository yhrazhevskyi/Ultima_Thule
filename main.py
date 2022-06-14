from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.core.text import LabelBase

import requests
from bs4 import BeautifulSoup

from kivy.metrics import dp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.properties import StringProperty
import datetime
from datetime import date
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout

import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from kivymd.uix.list import MDList, TwoLineListItem

Window.size = (350, 600)

MainScreen_kv = """
MDScreen:
    name: "menu"
    MDFloatLayout:
        MDLabel:
            text: "[i][b]Ultima Thule[/b][/i]"
            font_size: "42sp"
            markup: True
            halign: "center"
            pos_hint: {"center_x": .5, "center_y": .85}
            size_hint: (1, .3)

        MDRectangleFlatButton:
            text: "[i]Film recommendation[/i]"
            font_size: "18sp"
            markup: True
            pos_hint: {"center_x": .5, "center_y": .65}
            size_hint: (.8, .15)
            on_release: 
                root.manager.transition.direction = "left"
                root.manager.current = "movie"
        MDRectangleFlatButton:
            text: "[i]ToDoList[/i]"
            font_size: "18sp"
            markup: True
            pos_hint: {"center_x": .5, "center_y": .45}
            size_hint: (.8, .15)
            on_release: 
                root.manager.transition.direction = "left"
                root.manager.current = "todo"
        MDRectangleFlatButton:
            text: "[i]Weather[/i]"
            font_size: "18sp"
            markup: True
            pos_hint: {"center_x": .5, "center_y": .25}
            size_hint: (.8, .15)
            on_release: 
                root.manager.transition.direction = "left"
                root.manager.current = "loading"

"""

LoadingScreen_kv = """
MDScreen:
    name: "loading"
    on_enter: app.get_location()
    MDLabel:
        text: "Your data loading"
        halign: "center"
"""

MovieLoadingScreen_kv = """
MDScreen:
    name: "movie_loading"
    # on_enter: app.more_movie_info()
    MDLabel:
        text: "Your data loading"
        halign: "center"
"""

WeatherScreen_kv = """
MDScreen:
    name: "weather"
    temperature: temperature
    weather: weather
    humidity: humidity
    wind_speed: wind_speed
    location: location
    weather_image: weather_image
    city_name: city_name

    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        Image:
            source: "assets/icons/location.png"
            size_hint: .1, .1
            pos_hint: {"center_x": .5, "center_y": .95}
        MDLabel:
            id: location
            text: "Kyiv"
            pos_hint: {"center_x": .5, "center_y": .89}
            halign: "center"
            font_size: "20sp"
            font_name: "BPoppins"
        AsyncImage:
            id: weather_image
            source: ""
            pos_hint: {"center_x": .5, "center_y": .77}
            anim_delay: .1
        MDLabel:
            id: temperature
            text: ""
            markup: True
            pos_hint: {"center_x": .5, "center_y": .62}
            halign: "center"
            font_size: "60sp"
        MDLabel:
            id: weather
            text: ""
            pos_hint: {"center_x": .5, "center_y": .54}
            halign: "center"
            font_size: "20sp"
            font_name: "Poppins"
        MDFloatLayout:
            pos_hint: {"center_x": .25, "center_y": .4}
            size_hint: .22, .1
            Image:
                source: "assets/icons/humidity.png"
                pos_hint: {"center_x": .1, "center_y": .5}
            MDLabel:
                id: humidity
                text: ""
                pos_hint: {"center_x": 1, "center_y": .7}
                font_size: "16sp"
                font_name: "Poppins"
            MDLabel:
                text: "Humidity"
                pos_hint: {"center_x": 1, "center_y": .3}
                font_size: "14sp"
                font_name: "Poppins"
        MDFloatLayout:
            pos_hint: {"center_x": .75, "center_y": .4}
            size_hint: .22, .1
            Image:
                source: "assets/icons/wind.png"
                pos_hint: {"center_x": .1, "center_y": .5}
            MDLabel:
                id: wind_speed
                text: ""
                pos_hint: {"center_x": 1.1, "center_y": .7}
                font_size: "16sp"
                font_name: "Poppins"
            MDLabel:
                text: "Wind"
                pos_hint: {"center_x": 1.1, "center_y": .3}
                font_size: "14sp"
                font_name: "Poppins"
        MDFloatLayout:
            size_hint_y: .3
            canvas:
                Color:
                    rgb: rgba(148, 117, 255, 255)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [10, 10, 0, 0]
            MDFloatLayout:
                pos_hint: {"center_x": .5, "center_y": .71}
                size_hint: .9, .32
                canvas:
                    Color:
                        rgb: rgba(131, 69, 255, 255)
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos
                        radius: [6]
                TextInput:
                    id: city_name
                    hint_text: "Enter City Name"
                    size_hint: 1, None
                    pos_hint: {"center_x": .5, "center_y": .5}
                    height: self.minimum_height
                    multiline: False

                    font_size: "20sp"
                    hint_text_color: 1, 1, 1, 1
                    foreground_color: 1, 1, 1, 1
                    background_color: 1, 1, 1, 0
                    padding: 15
                    cursor_color: 1, 1, 1, 1
                    cursor_width: "2sp"
            Button:
                text: "Get Weather"
                font_name: "BPoppins"
                font_size: "20sp"
                size_hint: .9, .32
                pos_hint: {"center_x": .5, "center_y": .29}
                background_color: 1, 1, 1, 0
                color: rgba(148, 117, 255, 255)
                on_release: app.search_weather()
                canvas.before:
                    Color:
                        rgb: 1, 1, 1, 1
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos
                        radius: [6]
        MDIconButton:
            icon: "arrow-left"
            pos_hint: {"center_y": .95}
            on_release: 
                root.manager.transition.direction = "right"
                root.manager.current = "menu"
        MDIconButton:
            # icon: "book-information-variant"
            icon: "information"
            pos_hint: {"right": 1, "center_y": .95}
            on_release: 
                app.dialog()
"""

ToDoScreen_kv = """
<TodoCard>
    title: title
    description: description
    checkbox: checkbox
    elevation: 10
    md_bg_color: 1, 1, 1, 1
    radius: [8]
    MDFloatLayout:
        id: bar
        size_hint: .01, .9
        pos_hint: {"center_x": .02, "center_y": .5}
        md_bg_color: 1, 170/255, 23/255, 1
    MDLabel:
        id: title
        text: root.title
        markup: True
        # font_name: "Poppins-SemiBold.ttf"
        font_size: "20sp"
        size_hint_x: .8
        pos_hint: {"center_x": .46, "center_y": .8}
    MDCheckbox:
        id: checkbox
        active: False
        size_hint: None, None
        size: "48dp", "48dp"
        unselected_color: 1, 170/255, 23/255, 1
        selected_color: 0, 179/255, 0, 1
        pos_hint: {"center_x": .95, "center_y": .8}
        on_active: app.on_complete(*args, title, description, bar)
    MDLabel:
        id: description
        text: root.description
        # font_name: "Poppins-Regular.ttf"
        markup: True
        size_hint_x: .9
        line_height: .8
        pos_hint: {"center_x": .51, "center_y": .4}
MDScreen:
    date: date
    todo_list: todo_list
    name: "todo"
    on_pre_enter: app.todo_screen_start()
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        MDLabel:
            text: "My Tasks"
            pos_hint: {"center_x": .65, "center_y": .95}
            # font_name: "Poppins-SemiBold.ttf"
            font_size: "35sp"
        MDLabel:
            id: date
            text: ""
            pos_hint: {"center_x": .65, "center_y": .89}
            # font_name: "Poppins-Regular.ttf"
            font_size: "18sp"
        MDIconButton:
            icon: "plus"
            pos_hint: {"center_x": .89, "center_y": .925}
            user_font_size: "30sp"
            md_bg_color: 1, 170/255, 23/255, 1
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            on_release: 
                root.manager.transition.direction = "left"
                root.manager.current = "add_todo"
        ScrollView:
            do_scroll_y: True
            do_scroll_x: False
            size_hint_y: .85
            pos_hint: {"center_x": .5, "y": 0}
            bar_width: 0
            GridLayout:
                id: todo_list
                cols: 1
                height: self.minimum_height
                row_default_height: 80
                size_hint_y: None
                padding: 15, 10
                spacing: 15, 10

        MDIconButton:
            icon: "arrow-left"
            pos_hint: {"center_y": .95}
            on_release: 
                root.manager.transition.direction = "right"
                root.manager.current = "menu"
"""

AddTodo = """
MDScreen:
    title: title
    description: description
    name: "add_todo"
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        MDIconButton:
            icon:"chevron-left"
            user_font_size: "40sp"
            pos_hint: {"center_y": .95}
            theme_text_color: "Custom"
            text_color: 1, 170/255, 23/255, 1
            on_release: 
                root.manager.transition.direction = "right"
                root.manager.current = "todo"
        MDLabel:
            text: "Add Task"
            pos_hint: {"center_x": .6, "center_y": .88}
            # font_name: "Poppins-SemiBold.ttf"
            font_size: "35sp"
        MDFloatLayout:
            size_hint: .85, .08
            pos_hint: {"center_x": .5, "center_y": .78}
            canvas:
                Color:
                    rgb: (238/255, 238/255, 238/255, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [25]
            TextInput:
                id: title
                hint_text: "Title"
                size_hint: 1, None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: self.minimum_height
                multiline: False
                cursor_color: 1, 170/255, 23/255, 1
                cursor_width: "2sp"
                foreground_color: 1, 170/255, 23/255, 1
                background_color: 0, 0, 0, 0
                padding: 15
                # font_name: "Poppins-Regular.ttf"
                font_size: "18sp"
        MDFloatLayout:
            size_hint: .85, .28
            pos_hint: {"center_x": .5, "center_y": .57}
            canvas:
                Color:
                    rgb: (238/255, 238/255, 238/255, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [25]
            TextInput:
                id: description
                hint_text: "Description"
                size_hint: 1, None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: 180
                cursor_color: 1, 170/255, 23/255, 1
                cursor_width: "2sp"
                foreground_color: 1, 170/255, 23/255, 1
                background_color: 0, 0, 0, 0
                padding: 15
                # font_name: "Poppins-Regular.ttf"
                font_size: "18sp"

        Button:
            text: "ADD TASK"
            size_hint: .45, .08
            pos_hint: {"center_x": .5, "center_y": .36}
            background_color: 0, 0, 0, 0
            # font_name: "Poppins-SemiBold.ttf"
            font_size: "18sp"
            color: 1, 1, 1, 1
            on_release:
                app.add_todo(title.text, description.text)
            canvas.before:
                Color:
                    rgb: (1, 170/255, 23/255, 1)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [25]

"""

MovieScreen_kv = """
MDScreen:
    movie_name: movie_name
    movie_rec: movie_rec
    name: "movie"
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        MDLabel:
            text: "Get your recommendation"
            pos_hint: {"center_x": .5, "center_y": .95}
            size_hint_y: 0.15
            halign: "center"
            # font_name: "Poppins-SemiBold.ttf"
            font_size: "20sp"

        MDTextField:
            id: movie_name
            mode: "rectangle"
            hint_text: "Enter movie name"
            helper_text: "Then press on button"
            helper_text_mode: "on_focus"
            icon_right: "movie"
            size_hint_x: 0.9
            size_hint_y: 0.1
            pos_hint: {"center_x": .5, "center_y": .87}

        MDRectangleFlatButton:
            text: "Show"
            size_hint_x: 0.93
            size_hint_y: 0.07
            pos_hint: {"center_x": .5, "center_y": .77}
            on_release: 
                root.manager.transition.direction = "left"
                app.get_movie_recommendation()

        ScrollView:
            do_scroll_y: True
            do_scroll_x: False
            size_hint_y: .725
            # pos_hint: {"center_x": .5, "y": 0}
            bar_width: 0
            GridLayout:
                id: movie_rec
                cols: 1
                height: self.minimum_height
                # row_default_height: 80
                size_hint_y: None
                padding: 15, 10
                spacing: 15, 10
        MDIconButton:
            icon: "arrow-left"
            pos_hint: {"center_y": .95}
            on_release: 
                root.manager.transition.direction = "right"
                root.manager.current = "menu"
"""

MovieInfoScreen_kv = """
MDScreen:
    name: "movie_info"
    poster: poster
    title: title
    release: release
    rate: rate
    runtime: runtime
    genres: genres
    director: director
    writer: writer
    actors: actors
    plot: plot
    language: language
    country: country
    awards: awards
    imd_rate: imd_rate
    rotten_rate: rotten_rate
    movie_scroll: movie_scroll
    metacritic_rate: metacritic_rate
    MDBoxLayout:
        md_bg_color: 1, 1, 1, 1
        orientation: "vertical"
        size_hint_y: None
        size: root.width, root.height
        spacing: 0
        padding: 0
        AsyncImage:
            id: poster
            source: ''
            pos_hint: {'center_x': .5}
            size_hint: (1, .6)
        ScrollView:
            id: movie_scroll
            size_hint: (1, .4)
            pos_hint: {'center_x': .5, 'center_y': .5}
            do_scroll_y: True
            do_scroll_x: False
            bar_width: 0
            MDGridLayout:
                cols: 1
                height: self.minimum_height
                padding: 15, 10
                spacing: 15, 10
                size_hint_y: None
                MDLabel:
                    id: title
                    text: "Title: Shrek"
                    markup: True
                    size_hint: 1, None
                    text_size: self.width, None
                    height: self.texture_size[1]
                MDLabel:
                    id: release
                    markup: True
                    text: "Released: 18 May 2001"
                    size_hint: 1, None
                    text_size: self.width, None
                    height: self.texture_size[1]
                MDLabel:
                    id: rate
                    markup: True
                    text: "Rated: PG"
                    size_hint: 1, None
                    text_size: self.width, None
                    height: self.texture_size[1]
                MDLabel:
                    id: runtime
                    markup: True
                    text: "Runtime: 90 min"
                    size_hint: 1, None
                    text_size: self.width, None
                    height: self.texture_size[1]
                MDLabel:
                    id: genres
                    markup: True
                    text: "Genre: Animation, Adventure, Comedy"
                    size_hint: 1, None
                    text_size: self.width, None
                    height: self.texture_size[1]
                MDLabel:
                    id: director
                    markup: True
                    text: "Director: Andrew Adamson, Vicky Jenson"
                    size_hint: 1, None
                    text_size: self.width, None
                    height: self.texture_size[1]
                MDLabel:
                    id: writer
                    markup: True
                    text: "Writer: William Steig, Ted Elliott, Terry Rossio"
                    size_hint: 1, None
                    text_size: self.width, None
                    height: self.texture_size[1]
                MDLabel:
                    id: actors
                    markup: True
                    text: "Actors: Mike Myers, Eddie Murphy, Cameron Diaz"
                    size_hint: 1, None
                    text_size: self.width, None
                    height: self.texture_size[1]
                MDLabel:
                    id: plot
                    markup: True
                    text: "Plot: A mean lord exiles fairytale creatures to the swamp of a grumpy ogre, who must go on a quest and rescue a princess for the lord in order to get his land back."
                    size_hint: 1, None
                    text_size: self.width, None
                    height: self.texture_size[1]
                MDLabel:
                    id: language
                    markup: True
                    text: "Language: English"
                    size_hint: 1, None
                    text_size: self.width, None
                    height: self.texture_size[1]
                MDLabel:
                    id: country
                    markup: True
                    text: "Country: United States"
                    size_hint: 1, None
                    text_size: self.width, None
                    height: self.texture_size[1]
                MDLabel:
                    id: awards
                    markup: True
                    text: "Awards: Won 1 Oscar. 40 wins & 60 nominations total"
                    size_hint: 1, None
                    text_size: self.width, None
                    height: self.texture_size[1]
                MDLabel:
                    id: imd_rate
                    markup: True
                    text: "Internet Movie Database: N/A"
                    size_hint: 1, None
                    text_size: self.width, None
                    height: self.texture_size[1]
                MDLabel:
                    id: rotten_rate
                    markup: True
                    text: "Rotten Tomatoes: N/A"
                    size_hint: 1, None
                    text_size: self.width, None
                    height: self.texture_size[1]
                MDLabel:
                    id: metacritic_rate
                    markup: True
                    text: "Metacritic: N/A"
                    size_hint: 1, None
                    text_size: self.width, None
                    height: self.texture_size[1]
    MDFloatLayout:
        MDIconButton:
            icon: "arrow-left"
            pos_hint: {"center_y": .95}
            on_release: 
                root.manager.transition.direction = "right"
                root.manager.current = "movie"
"""


class MainScreen(Screen):
    pass


class MovieScreen(Screen):
    movies = pd.read_csv("assets/dataset/movies.csv")
    ratings = pd.read_csv("assets/dataset/ratings.csv")
    links = pd.read_csv("assets/dataset/links.csv", dtype=str)

    final_dataset = ratings.pivot(index='movieId', columns='userId', values='rating')
    final_dataset.fillna(0, inplace=True)

    no_user_voted = ratings.groupby('movieId')['rating'].agg('count')
    no_movies_voted = ratings.groupby('userId')['rating'].agg('count')

    final_dataset = final_dataset.loc[no_user_voted[no_user_voted > 10].index, :]
    final_dataset = final_dataset.loc[:, no_movies_voted[no_movies_voted > 50].index]

    csr_data = csr_matrix(final_dataset.values)
    final_dataset.reset_index(inplace=True)

    knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
    knn.fit(csr_data)
    recommend_frame = []
    response = {}

    def get_movie_recommendation(self):
        self.recommend_frame = []
        movie_name = screen_manager.get_screen("movie").movie_name.text
        n_movies_to_recommend = 10
        movie_list = self.movies[self.movies['title'].str.contains(movie_name)]
        if len(movie_list) and movie_name != "":
            try:
                movie_idx = movie_list.iloc[0]['movieId']  # get id in movie dataset
                movie_idx = self.final_dataset[self.final_dataset['movieId'] == movie_idx].index[
                    0]  # get id in final_data
                distances, indices = self.knn.kneighbors(self.csr_data[movie_idx],
                                                         n_neighbors=n_movies_to_recommend + 1)
                rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())),
                                           key=lambda x: x[1])[:0:-1]
                # print(rec_movie_indices)
                for val in rec_movie_indices:
                    movie_idx = self.final_dataset.iloc[val[0]]['movieId']
                    # imdb_id = "tt" + self.links[self.links["movieId"] == str(movie_idx)]["imdbId"].iloc[0]
                    idx = self.movies[self.movies['movieId'] == movie_idx].index
                    self.recommend_frame.append({'Title': self.movies.iloc[idx]['title'].values[0],
                                                 'Genres': self.movies.iloc[idx]['genres'].values[0],
                                                 'Id': self.movies.iloc[idx]['movieId'].values[0]})
                # print(self.recommend_frame)
                    # self.recommend_frame.append({'Title': self.movies.iloc[idx]['title'].values[0], 'Distance': val[1]})
                    # self.recommend_frame.append({'Title': self.movies.iloc[idx]['title'].values[0], 'Distance': val[1], "imdbId": imdb_id})
                # df = pd.DataFrame(self.recommend_frame, index=range(1, n_movies_to_recommend + 1))
                # print(distances)
                # return df

                self.set_movie_recommendation(self.recommend_frame)
            except IndexError:
                Snackbar(text="Movie not found, check your input.", snackbar_x="10dp", snackbar_y="10dp",
                         size_hint_y=.08,
                         size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                         bg_color=(66 / 255, 185 / 255, 245 / 255, 1),
                         font_size="18sp",
                         duration=1).open()
        else:
            if movie_name == "":
                Snackbar(text="You cannot leave this field blank.", snackbar_x="10dp", snackbar_y="10dp",
                         size_hint_y=.08,
                         size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                         bg_color=(66 / 255, 185 / 255, 245 / 255, 1),
                         font_size="18sp",
                         duration=1).open()
            else:
                Snackbar(text="Movie not found, check your input.", snackbar_x="10dp", snackbar_y="10dp",
                         size_hint_y=.08,
                         size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                         bg_color=(66 / 255, 185 / 255, 245 / 255, 1),
                         font_size="18sp",
                         duration=1).open()

    def set_movie_recommendation(self, recommend_frame):
        screen_manager.get_screen("movie").movie_rec.clear_widgets()
        list = MDList()
        for val in recommend_frame:
            list.add_widget(
                TwoLineListItem(text=f"{val['Title']}", secondary_text=f"{val['Genres'].replace('|', ', ')}",
                                on_release=self.more_movie_info))
        screen_manager.get_screen("movie").movie_rec.add_widget(list)

    def more_movie_info(self, obj):
        screen_manager.transition.direction = "left"
        # screen_manager.get_screen("movie_info").movie_scroll.do_scroll_y = 0
        screen_manager.current = "movie_loading"
        API_KEY = "f90c4189"
        for val in self.recommend_frame:
            if obj.text == val["Title"]:
                imdb_id = "tt" + self.links[self.links["movieId"] == str(val["Id"])]["imdbId"].iloc[0]
        try:
            url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={API_KEY}"
            self.response = requests.get(url).json()
            if self.response["Response"] != "False":
                screen_manager.get_screen("movie_info").poster.source = self.response["Poster"]
                screen_manager.get_screen("movie_info").title.text = f'[b]Title:[/b] {self.response["Title"]}'
                screen_manager.get_screen("movie_info").release.text = f'[b]Released:[/b] {self.response["Released"]}'
                screen_manager.get_screen("movie_info").rate.text = f'[b]Rated:[/b] {self.response["Rated"]}'
                screen_manager.get_screen("movie_info").runtime.text = f'[b]Runtime:[/b] {self.response["Runtime"]}'
                screen_manager.get_screen("movie_info").genres.text = f'[b]Genres:[/b] {self.response["Genre"]}'
                screen_manager.get_screen("movie_info").director.text = f'[b]Director:[/b] {self.response["Director"]}'
                screen_manager.get_screen("movie_info").writer.text = f'[b]Writer:[/b] {self.response["Writer"]}'
                screen_manager.get_screen("movie_info").actors.text = f'[b]Actors:[/b] {self.response["Actors"]}'
                screen_manager.get_screen("movie_info").plot.text = f'[b]Plot:[/b] {self.response["Plot"]}'
                screen_manager.get_screen("movie_info").language.text = f'[b]Language:[/b] {self.response["Language"]}'
                screen_manager.get_screen("movie_info").country.text = f'[b]Country:[/b] {self.response["Country"]}'
                screen_manager.get_screen("movie_info").awards.text = f'[b]Awards:[/b] {self.response["Awards"]}'
                try:
                    screen_manager.get_screen(
                        "movie_info").imd_rate.text = f'[b]Internet Movie Database:[/b] {self.response["Ratings"][0]["Value"]}'
                except IndexError:
                    screen_manager.get_screen(
                        "movie_info").imd_rate.text = f'[b]Internet Movie Database:[/b] N/A'
                try:
                    screen_manager.get_screen(
                        "movie_info").rotten_rate.text = f'[b]Rotten Tomatoes:[/b] {self.response["Ratings"][1]["Value"]}'
                except IndexError:
                    screen_manager.get_screen(
                        "movie_info").rotten_rate.text = f'[b]Rotten Tomatoes:[/b] N/A'
                try:
                    screen_manager.get_screen(
                        "movie_info").metacritic_rate.text = f'[b]Metacritic:[/b] {self.response["Ratings"][2]["Value"]}'
                except IndexError:
                    screen_manager.get_screen(
                        "movie_info").metacritic_rate.text = f'[b]Metacritic:[/b] N/A'
            else:
                # print("City Not Found")rgba(161, 129, 214, 1)
                Snackbar(text="Movie Not Found!", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                         size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                         bg_color=(161 / 255, 129 / 255, 214 / 255, 1),
                         font_size="18sp",
                         duration=1).open()
        except requests.ConnectionError:
            # print("No Internet Connection!")
            Snackbar(text="No Internet Connection!", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(66 / 255, 185 / 255, 245 / 255, 1),
                     font_size="18sp",
                     duration=1).open()
        screen_manager.current = "movie_info"


class LoadingScreen(Screen):
    # def test(self, text):
    #     print(text)
    #     screen_manager.get_screen("weather").temperature.text = "10"
    #     screen_manager.get_screen("weather").humidity.text = "10"
    #     screen_manager.current = "weather"
    API_KEY = "ed7cda7616fd06ff20dae0d6b4036bf6"

    def get_location(self):
        screen_manager.current = 'weather'
        # print(f'current location:{weather["location"]}')
        if weather["location"] == "":
            try:
                soup = BeautifulSoup(
                    requests.get(f"https://www.google.com/search?q=weather+at+my+current+location").text,
                    "html.parser")
                # print(soup)
                temp = soup.find("span", class_="BNeawe tAd8D AP7Wnd")
                location = "".join(filter(lambda item: not item.isdigit(), temp.text)).split(",", 1)
                weather["location"] = location[0]
            except requests.ConnectionError:
                Snackbar(text="No Internet Connection.", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                         size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                         bg_color=(161 / 255, 129 / 255, 214 / 255, 1),
                         font_size="18sp",
                         duration=1).open()
                exit()
            except AttributeError:
                Snackbar(text="Cant get your location, do it by yourself.", snackbar_x="10dp", snackbar_y="10dp",
                         size_hint_y=.08,
                         size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                         bg_color=(161 / 255, 129 / 255, 214 / 255, 1),
                         font_size="18sp",
                         duration=1).open()
                weather["location"] = "Kyiv"

        self.get_weather(weather["location"])

    def get_weather(self, city_name):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.API_KEY}&units=metric"
            response = requests.get(url).json()
            # print(response)
            if response["cod"] != "404":
                weather["temperature"] = round(response["main"]["temp"])
                weather["humidity"] = response["main"]["humidity"]
                weather["weather"] = response["weather"][0]["main"]
                weather["icon"] = str(response["weather"][0]["icon"])
                weather["wind_speed"] = round(response["wind"]["speed"] * 18 / 5)
                weather["location_caption"] = f'{response["name"]}, {response["sys"]["country"]}'
                # print(weather)
            else:
                # print("City Not Found")rgba(161, 129, 214, 1)
                Snackbar(text="City Not Found!", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                         size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                         bg_color=(161 / 255, 129 / 255, 214 / 255, 1),
                         font_size="18sp",
                         duration=1).open()
        except requests.ConnectionError:
            # print("No Internet Connection!")
            Snackbar(text="No Internet Connection!", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(161 / 255, 129 / 255, 214 / 255, 1),
                     font_size="18sp",
                     duration=1).open()
        self.set_weather()

    def set_weather(self):
        screen_manager.get_screen("weather").temperature.text = f'[b]{weather["temperature"]}[/b]°'
        screen_manager.get_screen("weather").weather.text = weather["weather"]
        screen_manager.get_screen("weather").humidity.text = f'{weather["humidity"]}%'
        screen_manager.get_screen("weather").wind_speed.text = f'{weather["wind_speed"]} m/s'
        screen_manager.get_screen("weather").location.text = weather["location_caption"]
        screen_manager.get_screen(
            "weather").weather_image.source = f'http://openweathermap.org/img/wn/{weather["icon"]}@2x.png'
        screen_manager.current = 'weather'


class WeatherScreen(Screen):
    def search_weather(self):
        location = screen_manager.get_screen("weather").city_name.text
        if location != "":
            weather["location"] = location
            Ultima_ThuleApp.get_weather(self, location)
            Ultima_ThuleApp.set_weather(self)
        else:
            Snackbar(text="You must specify the city", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(161 / 255, 129 / 255, 214 / 255, 1),
                     font_size="18sp",
                     duration=1).open()


class TodoCard(FakeRectangularElevationBehavior, MDFloatLayout):
    title = StringProperty()
    description = StringProperty()


class ToDoScreen(Screen):
    def todo_screen_start(self):
        today = date.today()
        wd = date.weekday(today)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().strftime("%b"))
        day = str(datetime.datetime.now().strftime("%d"))
        screen_manager.get_screen("todo").date.text = f'{days[wd]}, {day} {month} {year}'

    def on_complete(self, checkbox, value, title, description, bar):
        if value:
            description.text = f"[s]{description.text}[/s]"
            bar.md_bg_color = 0, 179 / 255, 0, 1
        else:
            remove = ["[s]", "[/s]"]
            for i in remove:
                description.text = description.text.replace(i, "")
                bar.md_bg_color = 1, 170 / 255, 23 / 255, 1

    def add_todo(self, title, description):
        title = title.replace("\n", " ").replace(":", " ")
        description = description.replace("\n", " ").replace(":", " ")
        if title != "" and description != "" and len(title) < 21 and len(description) < 61:
            screen_manager.current = "todo"
            screen_manager.transition.direction = "right"
            card = TodoCard(title=title, description=description)
            screen_manager.get_screen("todo").todo_list.add_widget(card)
            todo_list.append(card)
            screen_manager.get_screen("add_todo").title.text = ""
            screen_manager.get_screen("add_todo").description.text = ""
        elif title == "":
            Snackbar(text="Title is missing!", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp",
                     duration=1).open()
        elif description == "":
            Snackbar(text="Description is missing", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp",
                     duration=1).open()
        elif len(title) > 21:
            Snackbar(text="Title length should be < 20!", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp",
                     duration=1).open()
        elif len(description) > 61:
            Snackbar(text="Description length should be < 61!", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp",
                     duration=1).open()


class Ultima_ThuleApp(MDApp, LoadingScreen, WeatherScreen, ToDoScreen, MovieScreen):
    title = "Ultima Thule"

    def build(self):
        global todo_list
        todo_list = []
        global weather
        weather = {"location": "",
                   "temperature": "",
                   "humidity": "",
                   "weather": "",
                   "icon": "",
                   "wind_speed": 0,
                   "location_caption": ""}
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_string(MainScreen_kv))
        screen_manager.add_widget(Builder.load_string(LoadingScreen_kv))
        screen_manager.add_widget(Builder.load_string(WeatherScreen_kv))
        screen_manager.add_widget(Builder.load_string(ToDoScreen_kv))
        screen_manager.add_widget(Builder.load_string(AddTodo))
        screen_manager.add_widget(Builder.load_string(MovieScreen_kv))
        screen_manager.add_widget(Builder.load_string(MovieLoadingScreen_kv))
        screen_manager.add_widget(Builder.load_string(MovieInfoScreen_kv))
        # screen_manager.add_widget(Builder.load_file("WeatherScreen.kv"))

        try:
            pre_todo_list = open("assets/todo/todo.txt", "r").readlines()
            year = str(datetime.datetime.now().year)
            month = str(datetime.datetime.now().strftime("%b"))
            day = str(datetime.datetime.now().strftime("%d"))
            today = f"{day}:{month}:{year}\n"
            if pre_todo_list[-1] == today:
                pre_todo_list.pop()
                for elem in pre_todo_list:
                    task = elem.replace("\n", "").split(":")
                    if task[2] == "True ":
                        card = TodoCard(title=task[0], description=f"[s]{task[1]}[/s]")
                        card.checkbox.active = True
                        screen_manager.get_screen("todo").todo_list.add_widget(card)
                        todo_list.append(card)
                    else:
                        card = TodoCard(title=task[0], description=f"{task[1]}")
                        screen_manager.get_screen("todo").todo_list.add_widget(card)
                        todo_list.append(card)
        except FileNotFoundError:
            pass
        except IndexError:
            pass

        return screen_manager

    def on_stop(self):
        todo_txt = open("assets/todo/todo.txt", "w")
        remove = ["[s]", "[/s]"]
        for elem in todo_list:
            for i in remove:
                elem.description = elem.description.replace(i, "")
            todo_txt.write(f"{str(elem.title)}:{str(elem.description)}:{str(elem.checkbox.active)} \n")
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().strftime("%b"))
        day = str(datetime.datetime.now().strftime("%d"))
        todo_txt.write(f"{day}:{month}:{year}\n")

    LabelBase.register(name="Poppins", fn_regular="assets/fonts/Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="assets/fonts/Poppins-SemiBold.ttf")

    def dialog(self):
        if weather["temperature"] >= 18:
            recommendation = "It's pretty hot outside, dress lightly"
        elif weather["temperature"] >= 8:
            recommendation = "It's pretty chill outside, dress moderately"
        elif weather["temperature"] >= -5:
            recommendation = "It's pretty cold outside, dress warmly"
        else:
            recommendation = "It's very cold outside, dress in your warmest clothes"

        self.weather_dialog = MDDialog(title="Clothes recommendation", text=recommendation,
                                       buttons=[MDFlatButton(text="Close", on_release=self.close_dialog)])
        self.weather_dialog.open()

    def close_dialog(self, obj):
        self.weather_dialog.dismiss()

if __name__ == "__main__":
    Ultima_ThuleApp().run()
