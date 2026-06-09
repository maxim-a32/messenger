import customtkinter as ctk
from client import history, main, messeg
import sqlite3
from tkinter import filedialog
import pyautogui
import json
import logging

logging.basicConfig(
    filename="app_log_client.txt",
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s")

class Play:
    file_path = None
    def __init__(self):
        try:
            with open("settings.json", "r", encoding="utf-8") as file:
                settings = json.load(file)
                self.buton_color = settings["element"]
                self.fon = settings["fon"]
                self.Text_Color = settings["text"]
        except:
            self.buton_color = "blue"
            self.fon = "white"
            self.Text_Color = "white"
        width, height = pyautogui.size()
        width = width // 2
        height = height - 150
        size = str(width) + "x" + str(height)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.app = ctk.CTk(fg_color=self.fon)
        self.app.title("Месенджер")
        self.app.geometry(size)
        self.state = 1
        self.main_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Лівa рамка
        self.top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.top_frame.pack(side="top")
        self.left_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.left_frame.pack(side="left", padx=(0, 20))

        # Права рамка
        self.right_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.right_frame.pack(side="right")
        self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.bottom_frame.pack(side="bottom")

        self.Right_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.Right_frame.pack(side="right", padx=(0, 10))
        #self.app.mainloop()
    def Start(self):
        try:
            self.color = ctk.StringVar(value=self.fon)
            self.color_element = ctk.StringVar(value=self.buton_color)
            self.text_color_element = ctk.StringVar(value=self.Text_Color)
        except:
            self.color = ctk.StringVar(value="white")
            self.color_element = ctk.StringVar(value="blue")
            self.text_color_element = ctk.StringVar(value="white")
        
        self.label = ctk.CTkLabel(self.top_frame, text="Ведіть нік, якщо нік вже існує нічого не вводьте", font=("Helvetica", 20))
        self.label.pack(pady=20)
        self.entry = ctk.CTkEntry(self.top_frame, placeholder_text="Ведіть нік")
        self.entry.pack(pady=10)
        text = self.entry.get()
        self.button = ctk.CTkButton(self.top_frame, text="Підключитися до серверу", fg_color=self.buton_color, text_color=self.Text_Color, command=lambda: self.Conect(self.entry.get()))
        self.button.pack(pady=5)
        
        self.Entry_recipient = ctk.CTkEntry(master=self.left_frame, placeholder_text="Ведіть отримувача")
        self.Entry_text = ctk.CTkEntry(master=self.left_frame, placeholder_text="Ведіть текст")
        self.Button = ctk.CTkButton(self.left_frame, text="Подивитися повідомлення", fg_color=self.buton_color, text_color=self.Text_Color, command=lambda: self.History())
        self.Button_file = ctk.CTkButton(self.left_frame, text="Обрати файл", fg_color=self.buton_color, text_color=self.Text_Color, command=lambda: self.select_file())
        self.Button_send = ctk.CTkButton(self.left_frame, text="відправити повідомлення", fg_color=self.buton_color, text_color=self.Text_Color, command=lambda: self.send())
        self.textbox = ctk.CTkTextbox(self.right_frame, width=400, height=200, corner_radius=8, border_width=2)
        self.textbox.configure(state="disabled")

        self.label_fon = ctk.CTkLabel(self.left_frame, text="колір фону", font=("Helvetica", 10))
        self.label_text = ctk.CTkLabel(self.Right_frame, text="колір тексту на кнопках", font=("Helvetica", 10))
        self.label_element = ctk.CTkLabel(self.right_frame, text="колір кнопок", font=("Helvetica", 10))

        self.radio_fon_color_green = ctk.CTkRadioButton(master=self.left_frame, text="Зелений", variable=self.color, value="green")
        self.radio_fon_color_yellow = ctk.CTkRadioButton(master=self.left_frame, text="жовтий", variable=self.color, value="yellow")
        self.radio_fon_color_blue = ctk.CTkRadioButton(master=self.left_frame, text="блакитний", variable=self.color, value="blue")
        self.radio_fon_color_white = ctk.CTkRadioButton(master=self.left_frame, text="білий", variable=self.color, value="white")
        self.radio_fon_color_black = ctk.CTkRadioButton(master=self.left_frame, text="чорний", variable=self.color, value="black")

        self.radio_element_color_green = ctk.CTkRadioButton(master=self.right_frame, text="Зелений", variable=self.color_element, value="green")
        self.radio_element_color_yellow = ctk.CTkRadioButton(master=self.right_frame, text="жовтий", variable=self.color_element, value="yellow")
        self.radio_element_color_blue = ctk.CTkRadioButton(master=self.right_frame, text="блакитний", variable=self.color_element, value="blue")
        self.radio_element_color_white = ctk.CTkRadioButton(master=self.right_frame, text="білий", variable=self.color_element, value="white")
        self.radio_element_color_black = ctk.CTkRadioButton(master=self.right_frame, text="чорний", variable=self.color_element, value="black")

        self.radio_text_color_green = ctk.CTkRadioButton(master=self.Right_frame, text="Зелений", variable=self.text_color_element, value="green")
        self.radio_text_color_yellow = ctk.CTkRadioButton(master=self.Right_frame, text="жовтий", variable=self.text_color_element, value="yellow")
        self.radio_text_color_blue = ctk.CTkRadioButton(master=self.Right_frame, text="блакитний", variable=self.text_color_element, value="blue")
        self.radio_text_color_white = ctk.CTkRadioButton(master=self.Right_frame, text="білий", variable=self.text_color_element, value="white")
        self.radio_text_color_black = ctk.CTkRadioButton(master=self.Right_frame, text="чорний", variable=self.text_color_element, value="black")

        self.Button_color = ctk.CTkButton(self.bottom_frame, text="закінчити", fg_color=self.buton_color, text_color=self.Text_Color, command=lambda: self.end_settings())
        self.Button_setings = ctk.CTkButton(self.left_frame, text="налаштування", fg_color=self.buton_color, text_color=self.Text_Color, command=lambda: self.settings())
        
        self.PLAY()
        #self.app.mainloop()
    def PLAY(self):
        logging.info("Додаток запущено")
        self.app.mainloop()
        logging.info("Додаток вимкнено")
        try:
            client.close()
            conn.close()
        except:
            pass
    def send(self):
        messeg(self.client, self.conn, self.Entry_recipient.get(), self.Entry_text.get(), self.file_path)
        logging.info("повідомлення відправлено")
    def select_file(self):
        # Відкриває діалогове вікно для вибору файлу
        self.file_path = filedialog.askopenfilename(
            title="Виберіть файл",
            filetypes=(("Усі файли", "*.*"), ("Текстові файли", "*.txt"), ("Фото", "*.bmp"))
        )
        
        if self.file_path:
            # Оновлюємо текст на кнопці або в Label для відображення шляху
            self.Button_file.configure(text=self.file_path)
    def History(self):
        Text = history(self.conn, self.cursor)
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("1.0", Text)
        self.textbox.configure(state="disabled")
    def Conect(self, text):
        i, self.conn, self.client, self.cursor = main(text)
        if i == 1:
            logging.info("підключення успішне")
            self.main()
        elif i == 0:
            self.label.configure(text="попередне ім'я не знайдено будьласка введіть нове")
            logging.warning("Попереднє ім'я користувача не знайдено")
        elif i == 2:
            self.label.configure(text="користувач з таким ім'ям вже існує будьласка ведіть нове ім'я")
            logging.warning("Підключення до серверу не вдалося причина таке ім'я вже існує")
    def main(self):
        self.entry.pack_forget()
        self.button.pack_forget()
        self.radio_element_color_green.pack_forget()
        self.radio_element_color_yellow.pack_forget()
        self.radio_element_color_blue.pack_forget()
        self.radio_element_color_white.pack_forget()
        self.radio_element_color_black.pack_forget()
        
        self.radio_fon_color_green.pack_forget()
        self.radio_fon_color_yellow.pack_forget()
        self.radio_fon_color_blue.pack_forget()
        self.radio_fon_color_white.pack_forget()
        self.radio_fon_color_black.pack_forget()

        self.Button_color.pack_forget()
        
        self.Entry_recipient.pack(pady=(0, 10))
        self.Entry_text.pack(pady=(0, 10))
        self.Button.pack(pady=(0, 10))
        self.Button_file.pack(pady=(0, 10))
        self.Button_send.pack(pady=(0, 10))
        self.textbox.pack()
        
        self.label.configure(text="Головне вікно програми")

        self.Button_setings.pack(pady=(0, 10))
    def settings(self):
        self.cleaning()

        self.Button_color.pack(pady=(0, 10))

        self.label_fon.pack(pady=15)
        self.label_element.pack(pady=15)
        self.label_text.pack(pady=15)

        self.radio_element_color_green.pack(pady=(0, 10))
        self.radio_element_color_yellow.pack(pady=(0, 10))
        self.radio_element_color_blue.pack(pady=(0, 10))
        self.radio_element_color_white.pack(pady=(0, 10))
        self.radio_element_color_black.pack(pady=(0, 10))
        
        self.radio_fon_color_green.pack(pady=(0, 10))
        self.radio_fon_color_yellow.pack(pady=(0, 10))
        self.radio_fon_color_blue.pack(pady=(0, 10))
        self.radio_fon_color_white.pack(pady=(0, 10))
        self.radio_fon_color_black.pack(pady=(0, 10))

        self.radio_text_color_green.pack(pady=(0, 10))
        self.radio_text_color_yellow.pack(pady=(0, 10))
        self.radio_text_color_blue.pack(pady=(0, 10))
        self.radio_text_color_white.pack(pady=(0, 10))
        self.radio_text_color_black.pack(pady=(0, 10))

        self.label.configure(text="Налаштування")
    def end_settings(self):
        self.app.configure(fg_color=self.color.get())
        self.cleaning()
        logging.info("Налаштування були змінені")

        self.buton_color = self.color_element.get()
        self.seting_color()
        settings = {"fon": self.color.get(), "element": self.color_element.get(), "text": self.text_color_element.get()}
        with open("settings.json", "+w", encoding="utf-8") as file:
            json.dump(settings, file)

        self.main()
    def cleaning(self):
        self.radio_element_color_green.pack_forget()
        self.radio_element_color_yellow.pack_forget()
        self.radio_element_color_blue.pack_forget()
        self.radio_element_color_white.pack_forget()
        self.radio_element_color_black.pack_forget()
        
        self.radio_fon_color_green.pack_forget()
        self.radio_fon_color_yellow.pack_forget()
        self.radio_fon_color_blue.pack_forget()
        self.radio_fon_color_white.pack_forget()
        self.radio_fon_color_black.pack_forget()

        self.Entry_recipient.pack_forget()
        self.Entry_text.pack_forget()

        self.Button_color.pack_forget()
        self.Button.pack_forget()
        self.Button_file.pack_forget()
        self.Button_send.pack_forget()
        self.Button_setings.pack_forget()
        
        self.textbox.pack_forget()

        self.label_element.pack_forget()
        self.label_text.pack_forget()
        self.label_fon.pack_forget()
    def seting_color(self):
        self.Button_color.configure(fg_color=self.buton_color, text_color=self.text_color_element.get())
        self.Button.configure(fg_color=self.buton_color, text_color=self.text_color_element.get())
        self.Button_file.configure(fg_color=self.buton_color, text_color=self.text_color_element.get())
        self.Button_send.configure(fg_color=self.buton_color, text_color=self.text_color_element.get())
        self.Button_setings.configure(fg_color=self.buton_color, text_color=self.text_color_element.get())

play = Play()
play.Start()
#app.mainloop()
