import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os

# Файл для хранения истории
HISTORY_FILE = "quotes_history.json"

# Предопределённый список цитат
quotes = [
    {"text": "Будь тем изменением, которое хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "Мотивация"},
    {"text": "Жизнь — это 10% того, что с тобой происходит, и 90% того, как ты на это реагируешь.", "author": "Чарльз Р. Свиндолл", "topic": "Мотивация"},
    {"text": "Образование — это самое мощное оружие, которое ты можешь использовать, чтобы изменить мир.", "author": "Нельсон Мандела", "topic": "Образование"},
    {"text": "Только те, кто рискуют идти слишком далеко, могут узнать, как далеко можно зайти.", "author": "Т. С. Элиот", "topic": "Мотивация"},
    {"text": "Будущее принадлежит тем, кто верит в красоту своей мечты.", "author": "Элеонор Рузвельт", "topic": "Мотивация"},
]

# Загрузка истории из файла
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Сохранение истории в файл
def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

class QuoteGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Random Quote Generator")
        self.history = load_history()

        # Текущая цитата
        self.current_quote = None

        # Создание элементов интерфейса
        self.quote_text = tk.Text(master, height=4, width=60, wrap='word', state='disabled', bg='light yellow')
        self.quote_text.pack(pady=10)

        self.generate_button = tk.Button(master, text="Сгенерировать цитату", command=self.generate_quote)
        self.generate_button.pack(pady=5)

        # Фильтры
        filter_frame = tk.Frame(master)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Автор:").grid(row=0, column=0, padx=5)
        self.author_filter = tk.Entry(filter_frame)
        self.author_filter.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Тема:").grid(row=0, column=2, padx=5)
        self.topic_filter = tk.Entry(filter_frame)
        self.topic_filter.grid(row=0, column=3, padx=5)

        self.filter_button = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        self.filter_button.grid(row=0, column=4, padx=5)

        self.reset_filter_button = tk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter)
        self.reset_filter_button.grid(row=0, column=5, padx=5)

        # История
        tk.Label(master, text="История:").pack()
        self.history_listbox = tk.Listbox(master, width=80, height=10)
        self.history_listbox.pack(pady=5)

        self.update_history_listbox()

        # Меню
        menubar = tk.Menu(master)
        master.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Добавить цитату", command=self.add_quote)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=master.quit)

    def generate_quote(self):
        filtered_quotes = self.get_filtered_quotes()
        if not filtered_quotes:
            messagebox.showinfo("Информация", "Нет цитат по текущему фильтру.")
            return
        self.current_quote = random.choice(filtered_quotes)
        self.display_quote(self.current_quote)
        self.history.append(self.current_quote)
        save_history(self.history)
        self.update_history_listbox()

    def display_quote(self, quote):
        self.quote_text.config(state='normal')
        self.quote_text.delete(1.0, tk.END)
        display_text = f"\"{quote['text']}\"\n\n- {quote['author']} ({quote['topic']})"
        self.quote_text.insert(tk.END, display_text)
        self.quote_text.config(state='disabled')

    def update_history_listbox(self):
        self.history_listbox.delete(0, tk.END)
        for idx, q in enumerate(self.history, 1):
            self.history_listbox.insert(tk.END, f"{idx}. \"{q['text']}\" - {q['author']} ({q['topic']})")

    def get_filtered_quotes(self):
        author_filter = self.author_filter.get().strip().lower()
        topic_filter = self.topic_filter.get().strip().lower()
        filtered = []
        for q in quotes:
            if author_filter and author_filter not in q['author'].lower():
                continue
            if topic_filter and topic_filter not in q['topic'].lower():
                continue
            filtered.append(q)
        return filtered

    def apply_filter(self):
        self.generate_quote()

    def reset_filter(self):
        self.author_filter.delete(0, tk.END)
        self.topic_filter.delete(0, tk.END)
        self.generate_quote()

    def add_quote(self):
        author = simpledialog.askstring("Добавить цитату", "Введите автора:")
        if author is None or not author.strip():
            messagebox.showerror("Ошибка", "Автор не может быть пустым.")
            return

        text = simpledialog.askstring("Добавить цитату", "Введите текст цитаты:")
        if text is None or not text.strip():
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым.")
            return

        topic = simpledialog.askstring("Добавить цитату", "Введите тему:")
        if topic is None or not topic.strip():
            messagebox.showerror("Ошибка", "Тема не может быть пустой.")
            return

        new_quote = {"text": text.strip(), "author": author.strip(), "topic": topic.strip()}
        quotes.append(new_quote)
        messagebox.showinfo("Успех", "Цитата добавлена.")
        self.generate_quote()

# Создаем окно
root = tk.Tk()
app = QuoteGeneratorApp(root)
root.mainloop()
