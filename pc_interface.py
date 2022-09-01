import requests
import datetime
import os
import sqlite3
import kivymd.app
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.boxlayout import BoxLayout
from MaxPackMain import Package, MaxPackJson
from kivy.core.window import Window
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
from weather_api_key import api_key
from kivymd.uix.datatables import MDDataTable
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from fpdf import FPDF
from kivy.uix.tabbedpanel import TabbedPanel


Window.size = (1600, 950)
Window.left = (500)
Window.top = (300)


json_db = MaxPackJson()
package = Package()


class MainMenu(BoxLayout):
    font_size = 25                              # Основной размер шрифта
    font_color = "black"                        # Основной цвет шрифта
    label_size = 0.6, 0.03  #
    text_input_size = 0.2, 1                    # Размер шрифта полей ввода текста
    boxlayout_size_hint = 1, 0.9                # Размеры боксов
    entry_box_boxlayout_size_hint = 1, 0.09     # Размеры боксов полей ввода
    menu_button_font_size = 20                  # Размер шрифта кнопок меню
    entry_box_color = 0.51, 0.7, 0.25, 0.7
    weather_size_hint = .7, 1                   # Размеры полей погодного виджета
    weather_font_size = 20                      # Размер шрифта погодного виджета

    @staticmethod
    def get_weather_data(msg):
        """Качаем данные по погоде"""
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/find?q={msg}&appid={api_key}&lang=ru&units=metric")
        data = r.json()
        return data

    def weather_input(self):
        """Заполняем данные по погоде в лейблы"""
        if not self.ids.text_input_weather.focus:
            try:
                data = MainMenu.get_weather_data(self.ids.text_input_weather.text)
                new_data = MainMenu.show_weather(data)
                self.ids.lbl_weather_city.text = new_data[0]
                self.ids.lbl_weather_temp.text = new_data[1]
                self.ids.lbl_weather_state.text = new_data[3]
                self.ids.lbl_weather_date.text = new_data[4]
            except:
                print("something went wrong")

    @staticmethod
    def show_weather(data):
        """Шаблон показа погоды"""
        feels_like = f"Ощущается как {data['list'][0]['main']['feels_like']}"
        name = f"Город :{data['list'][0]['name']}"
        temp = f"Температура : {data['list'][0]['main']['temp']}°"
        description = data["list"][0]["weather"][0]["description"].capitalize()
        time_ = datetime.datetime.now().strftime("%H:%M %d.%m.%Y")
        ans = [name, temp, feels_like, description, time_]
        return ans

    @staticmethod
    def currency_data():
        """Получаем данные по курсам валют"""
        currency = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json")
        data = currency.json()
        return data

    @staticmethod
    def exchange_rate():
        """Парсим и отдаем валюты"""
        try:
            data = MainMenu.currency_data()
            currencies_list = []
            for i in data:
                if i["cc"] in ["USD", "EUR", "PLN"]:
                    idx = data.index(i)
                    text = data[idx]["txt"]
                    rate = data[idx]["rate"]
                    date = data[idx]["exchangedate"]
                    curr_rate = f"{text} / UAH: {rate}, {date}"
                    currencies_list.append(curr_rate)
            what_to_send = "\n".join(currencies_list) + "\n" #+ 3 * "\U0001F601"
            return what_to_send
        except:
            return "Что-то пошло не так"


class MainScreen(Screen):
    panel_id = None
    lbl_text = package.reset_func()
    font_size = 25                               #Основной размер шрифта
    font_color = "black"                         #Основной цвет шрифта
    properties_size = 0.25, 1                    #Размер приписки гр/м2/eur и тд
    properties_font_size = 18                    #Размер шрифта приписного текста
    label_size = 0.6, 0.03                       #
    text_input_size = 0.3, 1                     #Размер шрифта полей ввода текста
    workspace_padding = 10, 8                    #Отступы рабочего пространства
    boxlayout_size_hint = 1, 0.9                 #Размеры боксов
    entry_box_boxlayout_size_hint = 1, 0.09      #Размеры боксов полей ввода
    entry_box_color = 0.51, 0.7, 0.25, 0.7       #Цвет полей ввода
    menu_button_font_size = 20                   #Размер шрифта кнопок меню
    md_button_color = 0.01, 0.01, 0.01, 1        #Цвет шрифта мд кнопы
    md_button_font_size = 20                     #Размер шрифта мд кнопы
    bottom_button_color = 0.51, 0.7, 0.25, 1     #Цвет нижних кнопок

    def change_currency_func(self):
        """Меняем спинером стоимость сырья в зависимости от валюты"""
        if self.ids.change_currency.text == "UAH":
            package.currency = "UAH"
            package.currency_func()
            self.refresh()
        elif self.ids.change_currency.text == "USD":
            package.currency = "USD"
            package.currency_func()
            self.refresh()
        elif self.ids.change_currency.text == "EUR":
            package.currency = "EUR"
            package.currency_func()
            self.refresh()
        else:
            self.ids.bottom_label_text.text = "Выберите валюту"

    def check_focus(self):
        """Проверка фокуса на ентри боксах"""
        list_of_input_text_focus = [self.ids.text_input_p_width.focus, self.ids.text_input_p_height.focus,
                                    self.ids.text_input_p_bottom.focus, self.ids.text_input_first_layer.focus,
                                    self.ids.text_input_second_layer.focus, self.ids.text_input_third_layer.focus,
                                    self.ids.text_input_bottom_raw_gram.focus, self.ids.text_input_raw_paper_cost.focus,
                                    self.ids.text_input_shading_percentages.focus, self.ids.text_input_paint_spend.focus,
                                    self.ids.text_input_paint_cost.focus, self.ids.text_input_exchange_rate_usd.focus,
                                    self.ids.text_input_exchange_rate_eur.focus, self.ids.text_input_handle.focus,
                                    self.ids.text_input_order_amount.focus]

        if list_of_input_text_focus:
            #print("focus checked")
            self.refresh()
        else:
            print("Something went wrong")

    def refresh(self):
        """Обновление данных в классе и в интерфейсе"""
        list_of_text_fields = [self.ids.text_input_p_width.text, self.ids.text_input_p_height.text,
                               self.ids.text_input_p_bottom.text, self.ids.text_input_first_layer.text,
                               self.ids.text_input_second_layer.text, self.ids.text_input_third_layer.text,
                               self.ids.text_input_bottom_raw_gram.text, self.ids.text_input_raw_paper_cost.text,
                               self.ids.text_input_shading_percentages.text, self.ids.text_input_paint_spend.text,
                               self.ids.text_input_paint_cost.text, self.ids.text_input_margin.text,
                               self.ids.text_input_exchange_rate_usd.text, self.ids.text_input_exchange_rate_eur.text,
                               self.ids.text_input_handle.text, self.ids.text_input_order_amount.text]

        if all(list_of_text_fields):
            try:
                package.p_width = int(self.ids.text_input_p_width.text)
                package.p_height = int(self.ids.text_input_p_height.text)
                package.p_bottom = int(self.ids.text_input_p_bottom.text)
                package.first_layer = int(self.ids.text_input_first_layer.text)
                package.second_layer = int(self.ids.text_input_second_layer.text)
                package.third_layer = int(self.ids.text_input_third_layer.text)
                package.bottom_raw_gram = int(self.ids.text_input_bottom_raw_gram.text)
                package.raw_paper_cost = int(self.ids.text_input_raw_paper_cost.text)
                package.shading_percentages = int(self.ids.text_input_shading_percentages.text)
                package.paint_spend = int(self.ids.text_input_paint_spend.text)
                package.paint_cost = int(self.ids.text_input_paint_cost.text)
                package.margin = int(self.ids.text_input_margin.text)
                package.exchange_rate_usd = float(self.ids.text_input_exchange_rate_usd.text)
                package.exchange_rate_eur = float(self.ids.text_input_exchange_rate_eur.text)
                package.handle = float(self.ids.text_input_handle.text)
                package.order_amount = int(self.ids.text_input_order_amount.text)
                package.reload_variables()
                self.ids.text_input_roll_format1.text = str(package.roll_format)
                self.ids.text_input_sleeve_length.text = str(package.sleeve_length)
                self.ids.text_input_squaring.text = str(package.squaring.__round__(3))
                self.ids.text_input_bottom_squaring.text = str(package.bottom_squaring)
                self.ids.text_input_bottom_weight.text = str(package.bottom_weight.__round__(3))
                self.ids.text_input_bottom_cost.text = str(package.bottom_cost.__round__(3))
                self.ids.text_input_weight_first_layer.text = str(package.weight_first_layer.__round__(3))
                self.ids.text_input_weight_second_layer.text = str(package.weight_second_layer.__round__(3))
                self.ids.text_input_weight_third_layer.text = str(package.weight_third_layer.__round__(3))
                self.ids.text_input_cost_first_layer_raw.text = str(package.cost_first_layer_raw.__round__(3))
                self.ids.text_input_cost_second_layer_raw.text = str(package.cost_second_layer_raw.__round__(3))
                self.ids.text_input_cost_third_layer_raw.text = str(package.cost_third_layer_raw.__round__(3))
                self.ids.text_input_paint_cost_one_gram.text = str(package.paint_cost_one_gram)
                self.ids.text_input_painting_cost.text = str(package.painting_cost)
                self.ids.text_input_workpiece_area.text = str(package.workpiece_area.__round__(3))
                #self.ids.text_input_paint_cost_eur.text = str(package.paint_cost_eur.__round__(5))
                self.ids.text_input_paint_cost_uah.text = str(package.paint_cost_uah.__round__(5))
                self.ids.text_input_self_cost_package.text = str(package.self_cost_package.__round__(2))
                self.ids.text_input_margin_sum.text = str(package.margin_sum.__round__(2))
                self.ids.text_input_cost_for_customer.text = str(package.cost_for_customer.__round__(2))
                self.ids.text_input_order_price.text = str(package.order_price.__round__(2))
            except:
                print("nope")
        else:
            print("nope")


    def return_from_orders(self):
        """Переносим значения из выбранной панели заказов обратно в конструктор"""
        panel_id = MainScreen.panel_id
        data = json_db.read()
        self.ids.text_input_p_width.text = data[panel_id]["width"][1]
        self.ids.text_input_p_height.text = data[panel_id]["height"][1]
        self.ids.text_input_p_bottom.text = data[panel_id]["bottom"][1]
        self.ids.text_input_first_layer.text = data[panel_id]["first_layer"][1]
        self.ids.text_input_second_layer.text = data[panel_id]["second_layer"][1]
        self.ids.text_input_third_layer.text = data[panel_id]["third_layer"][1]
        self.ids.text_input_bottom_raw_gram.text = data[panel_id]["bottom_raw_gram"][1]
        self.ids.text_input_raw_paper_cost.text = data[panel_id]["raw_paper_cost"][1]
        self.ids.text_input_shading_percentages.text = data[panel_id]["shading_percentages"][1]
        self.ids.text_input_paint_spend.text = data[panel_id]["paint_spend"][1]
        self.ids.text_input_paint_cost.text = data[panel_id]["paint_cost"][1]
        self.ids.text_input_margin.text = data[panel_id]["margin"][1]
        self.ids.text_input_exchange_rate_usd.text = data[panel_id]["exchange_rate_usd"][1]
        self.ids.text_input_exchange_rate_eur.text = data[panel_id]["exchange_rate_eur"][1]
        self.ids.text_input_handle.text = data[panel_id]["handle"][1]
        self.ids.text_input_order_amount.text = data[panel_id]["order_amount"][1]
        self.refresh()


class SecondScreen(Screen):
    panel_id = None

    def panel_start(self):
        """Создание Експанс панелей второго экрана"""
        if os.path.exists(f"maxpack_db.json"):
            names = json_db.read()
            self.ids.panel_container.clear_widgets()
            for i in names:
                panel = MDExpansionPanel(icon="pocket.png", content=ExpPanel(), panel_cls=MDExpansionPanelThreeLine(
                    text=str(names[i]["name"]),
                    secondary_text=f"Заказ от : {datetime.datetime.fromtimestamp(int(i))}",
                    tertiary_text=i,))
                panel.bind(on_open=self.on_panel_open)
                self.ids.panel_container.add_widget(panel)
        else:
            print("Пока ничего нет")

    def on_panel_open(self, instance_panel):
        """Заполнение содержимого експанс панелей второго экрана"""
        id = instance_panel.panel_cls.tertiary_text
        cls_ids = instance_panel.content.ids
        names = json_db.read()
        if id in names:
            if int(names[id]['shading_percentages'][1]) == 0:
                shading = "Без печати"
            else:
                shading = "С печатью"
            if float(names[id]['handle'][1]) <= 0:
                handle = "Без ручки"
            else:
                handle = "С ручкой"

            cls_ids.exp_panel_size.text = str(names[id]['width'][0] + ": " + \
                                              names[id]['width'][1] + " " + \
                                              names[id]['width'][2] + "\n" + \
                                              names[id]['height'][0] + ": " + \
                                              names[id]['height'][1] + " " + \
                                              names[id]['height'][2] + "\n" + \
                                              names[id]['bottom'][0] + ": " + \
                                              names[id]['bottom'][1] + " " + \
                                              names[id]['bottom'][2]+ "\n" + shading)

            cls_ids.exp_panel_paper_spec.text = str(names[id]['roll_format'][0] + ": " + \
                                                    names[id]['roll_format'][1] + " " + \
                                                    names[id]['roll_format'][2] + "\n" + \
                                                    names[id]['sleeve_length'][0] + ": " + \
                                                    names[id]['sleeve_length'][1] + " " + \
                                                    names[id]['sleeve_length'][2] + "\n" + \
                                                    "Граматура:" + names[id]['first_layer'][1]+ "/" + \
                                                    names[id]['second_layer'][1] + "/" +
                                                    names[id]['third_layer'][1] + "\n" + handle)

            cls_ids.exp_panel_exch.text = str("Посчитано по курсу:" + "\n" + "Евро: " + \
                                              names[id]['exchange_rate_eur'][1] + " грн" + "\n" + \
                                              "Доллар: " + names[id]['exchange_rate_usd'][1] + " " + \
                                              names[id]['exchange_rate_usd'][2] + "\n" + \
                                              names[id]['raw_paper_cost'][0]+ ": " + \
                                              names[id]['raw_paper_cost'][1] + " " + \
                                              names[id]['raw_paper_cost'][2])

            cls_ids.exp_panel_cost.text = str(names[id]['self_cost_package'][0] + ": " + \
                                               str(float(names[id]['self_cost_package'][1]).__round__(2)) + " " + \
                                               names[id]['self_cost_package'][2] + "\n" + \
                                               names[id]['cost_for_customer'][0] + ": " + \
                                               str(float(names[id]['cost_for_customer'][1]).__round__(2)) + " " + \
                                               names[id]['cost_for_customer'][2] + "\n" + \
                                               names[id]['order_amount'][0] + " "+ \
                                               names[id]['order_amount'][1] + " " + \
                                               names[id]['order_amount'][2] + "\n" + \
                                               names[id]['order_price'][0] + " " + \
                                               str(float(names[id]['order_price'][1]).__round__(2)) + " " + \
                                               names[id]['order_price'][2])
        else:
            print("something went wrong")
        MainScreen.panel_id = id
        SecondScreen.panel_id = id

    def delete_record(self):
        """Удаление клиента из вкладки заказов"""
        data = json_db.read()
        del data[SecondScreen.panel_id]
        json_db.write(data)
        self.panel_start()

    def save_to_file_btn(self):
        """Сохраняем заказ в PDF"""
        what_to_write = ["width", "height", 'bottom', 'cost_for_customer', 'order_price']
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("DejaVuSans", style="", fname="DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVuSans", size=10)
        data = json_db.read()
        line = 1
        for i, k in data[SecondScreen.panel_id].items():
            if i in what_to_write:
                txt = f"{k[0]} {float(k[1]).__round__(2)} {k[2]}"
                text = "".join(txt)
                pdf.cell(200, 10, txt=text, ln=line)
                line += 1
        pdf.output(f"{data[SecondScreen.panel_id]['name']}_{datetime.datetime.now().strftime('%d-%m-%y')}.pdf")


class ThirdScreen(Screen):
    """Таблица готовой продукции на складе"""
    def create_data_table(self):
        self.ids.package_data_container.clear_widgets()
        table_font_size = dp(43)
        con = sqlite3.connect("C:/Users/Maks/Desktop/db_creating/sqlite-tools/maxpack_storage.db")
        cur = con.cursor()
        db = cur.execute("""SELECT * FROM Package;""")
        self.data_tables = MDDataTable(
            use_pagination=True,
            rows_num=12,
            column_data=[
                ("№", dp(15)),
                ("Размер", table_font_size),
                ("Граматура", table_font_size),
                ("Производитель", table_font_size),
                ("Цвет", table_font_size),
                ("Ручка", table_font_size),
                ("В наличии", table_font_size)
            ],
            row_data=db)
        self.ids.package_data_container.add_widget(self.data_tables)
        con.close()



class FourthScreen(Screen):
    """Таблица наличия сырья"""
    def create_data_table(self):
        self.ids.paper_data_container.clear_widgets()
        table_font_size = dp(50)
        con = sqlite3.connect("C:/Users/Maks/Desktop/db_creating/sqlite-tools/maxpack_storage.db")
        cur = con.cursor()
        db = cur.execute("""SELECT * FROM Paper;""")
        self.data_tables = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            rows_num=12,
            column_data=[
                ("№", dp(15)),
                ("Размер", table_font_size),
                ("Граматура", table_font_size),
                ("Производитель", table_font_size),
                ("Цвет", table_font_size),
                ("В наличии (кг)", table_font_size)
            ],
            row_data=db,
        )
        self.ids.paper_data_container.add_widget(self.data_tables)
        con.close()


class AdminScreen(Screen):
    label_font_size = 20
    label_text_color = "black"


    def change_to_admin(self):
        self.ids.admin_paper_data_container.clear_widgets()
        con = sqlite3.connect("C:/Users/Maks/Desktop/db_creating/sqlite-tools/maxpack_storage.db")
        cur = con.cursor()
        db = cur.execute("""SELECT * FROM Package ORDER BY Size;""")

        for i in db:
            box = BoxLayout()
            lbl1 = Label(text=str(i[0]), font_size=20, color="black")
            entry1 = TextInput(text=str(i[1]), multiline=False, font_size=18)
            entry2 = TextInput(text=str(i[2]), multiline=False, font_size=18)
            entry3 = TextInput(text=str(i[3]), multiline=False, font_size=18)
            entry4 = TextInput(text=str(i[4]), multiline=False, font_size=18)
            entry5 = TextInput(text=str(i[5]), multiline=False, font_size=18)
            entry6 = TextInput(text=str(i[6]), multiline=False, font_size=18)
            box.add_widget(lbl1)
            box.add_widget(entry1)
            box.add_widget(entry2)
            box.add_widget(entry3)
            box.add_widget(entry4)
            box.add_widget(entry5)
            box.add_widget(entry6)
            self.ids.admin_paper_data_container.add_widget(box)


class TabForAdmin(TabbedPanel):
    label_font_size = 20
    label_text_color = "black"


class ExpPanel(BoxLayout):
    exp_label_font_size = 20
    exp_label_size_hint = 1, None
    md_button_color = 0.01, 0.01, 0.01, 1


class FirstWindowDialog(BoxLayout):
    pass


class ThirdWindowDialog(BoxLayout):
    pass


class MaxPackDesktopApp(kivymd.app.MDApp):
    dialog = None

    def build(self):
        """Создаем скрин менеджер"""
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(ThirdScreen(name='third'))
        sm.add_widget(FourthScreen(name='fourth'))
        sm.add_widget(AdminScreen(name='admin'))
        return sm

    def show_dialog_save_to_db(self):
        """Диалоговое окно при сохранении в заказы"""
        if not self.dialog:
            self.dialog = MDDialog(
                title="Название фирмы или имя клиента:",
                type="custom",
                content_cls=FirstWindowDialog(),
                buttons=[
                   MDFillRoundFlatButton(
                       text="Отменить",
                       theme_text_color="Custom",
                       text_color=(0.01, 0.01, 0.01, 1),
                       md_bg_color=(0.51, 0.7, 0.25, 1),
                       on_release=self.dialog_cancel_btn
                   ),
                   MDFillRoundFlatButton(
                       text="Сохранить",
                       theme_text_color="Custom",
                       text_color=(0.01, 0.01, 0.01, 1),
                       md_bg_color=(0.51, 0.7, 0.25, 1),
                       on_release=self.dialog_save_to_db_btn
                   ),
                ],
            )
        self.dialog.open()


    def dialog_save_to_db_btn(self, obj):
        """Кнопка сохранения диалогового окна"""
        new_value = {}
        id = int(datetime.datetime.now().timestamp())
        if self.dialog.content_cls.ids.text_input_dialog.text:
            if os.path.exists(f"maxpack_db.json"):
                new = json_db.read()
                new_value[id] = package.reset_func()
                new_value[id]["name"] = self.dialog.content_cls.ids.text_input_dialog.text
                new.update(new_value)
                json_db.write(new)
            else:
                new_value[id] = package.reset_func()
                new_value[id]["name"] = self.dialog.content_cls.ids.text_input_dialog.text
                json_db.write(new_value)
            self.dialog.content_cls.ids.text_input_dialog.text = ""
            self.dialog.dismiss()
        else:
            print("nea")

    def dialog_cancel_btn(self, obj):
        """Закрытие диалогового окна"""
        self.dialog.dismiss()


MaxPackDesktopApp().run()


