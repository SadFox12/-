import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

# Функция для подключения к базе данных
def connect_db():
    return sqlite3.connect('law_database.db')

# ------------------------- Интерфейс Эксперта -------------------------

class ExpertInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Интерфейс Эксперта")

        # Создаем кнопки для ввода данных
        self.create_widgets()

    def create_widgets(self):
        # Кнопки для внесения данных
        self.add_law_btn = tk.Button(self.root, text="Добавить новый закон", command=self.add_law)
        self.add_law_btn.pack(pady=10)

        self.add_chapter_btn = tk.Button(self.root, text="Добавить новую главу", command=self.add_chapter)
        self.add_chapter_btn.pack(pady=10)

        self.add_article_btn = tk.Button(self.root, text="Добавить новую статью", command=self.add_article)
        self.add_article_btn.pack(pady=10)

        self.add_sublaw_btn = tk.Button(self.root, text="Добавить подзаконный акт", command=self.add_sublaw)
        self.add_sublaw_btn.pack(pady=10)

        self.edit_law_btn = tk.Button(self.root, text="Редактировать закон", command=self.edit_law)
        self.edit_law_btn.pack(pady=10)

        self.edit_chapter_btn = tk.Button(self.root, text="Редактировать главу", command=self.edit_chapter)
        self.edit_chapter_btn.pack(pady=10)

        self.edit_article_btn = tk.Button(self.root, text="Редактировать статью", command=self.edit_article)
        self.edit_article_btn.pack(pady=10)

        self.edit_sublaw_btn = tk.Button(self.root, text="Редактировать подзаконный акт", command=self.edit_sublaw)
        self.edit_sublaw_btn.pack(pady=10)

        self.view_laws_btn = tk.Button(self.root, text="Просмотр базы знаний", command=self.view_laws)
        self.view_laws_btn.pack(pady=10)

        self.exit_btn = tk.Button(self.root, text="Выход", command=self.root.quit)
        self.exit_btn.pack(pady=10)

    def add_law(self):
        # Ввод нового закона
        title = simpledialog.askstring("Закон", "Введите название закона:")
        description = simpledialog.askstring("Закон", "Введите описание закона:")
        date_enacted = simpledialog.askstring("Закон", "Введите дату принятия закона (ГГГГ-ММ-ДД):")

        if title and description and date_enacted:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO laws (title, description, date_enacted) VALUES (?, ?, ?)''', (title, description, date_enacted))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Закон успешно добавлен!")
            self.show_affected_relations('law')
        else:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")

    def add_chapter(self):
        # Ввод новой главы
        law_id = simpledialog.askinteger("Глава", "Введите ID закона, к которому добавляется глава:")
        title = simpledialog.askstring("Глава", "Введите название главы:")
        description = simpledialog.askstring("Глава", "Введите описание главы:")

        if law_id and title and description:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO chapters (law_id, title, description) VALUES (?, ?, ?)''', (law_id, title, description))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Глава успешно добавлена!")
            self.show_affected_relations('chapter', law_id)
        else:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")

    def add_article(self):
        # Ввод новой статьи
        chapter_id = simpledialog.askinteger("Статья", "Введите ID главы, к которой добавляется статья:")
        title = simpledialog.askstring("Статья", "Введите название статьи:")
        content = simpledialog.askstring("Статья", "Введите содержание статьи:")

        if chapter_id and title and content:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO articles (chapter_id, title, content) VALUES (?, ?, ?)''', (chapter_id, title, content))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Статья успешно добавлена!")
            self.show_affected_relations('article', chapter_id)
        else:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")

    def add_sublaw(self):
        # Ввод нового подзаконного акта
        chapter_id = simpledialog.askinteger("Подзаконный акт", "Введите ID главы, к которой добавляется подзаконный акт:")
        title = simpledialog.askstring("Подзаконный акт", "Введите название подзаконного акта:")
        description = simpledialog.askstring("Подзаконный акт", "Введите описание подзаконного акта:")

        if chapter_id and title and description:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO sublaws (chapter_id, title, description) VALUES (?, ?, ?)''', (chapter_id, title, description))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Подзаконный акт успешно добавлен!")
            self.show_affected_relations('sublaw', chapter_id)
        else:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")

    def show_affected_relations(self, element_type, element_id=None):
        # Функция для отображения связанных элементов при изменении базы данных
        conn = connect_db()
        cursor = conn.cursor()

        if element_type == 'law':
            # Если добавлен новый закон
            messagebox.showinfo("Связанные элементы", "Новый закон был добавлен. Нет вышестоящих элементов.")
        elif element_type == 'chapter':
            # Если добавлена новая глава
            cursor.execute('SELECT title FROM laws WHERE id = ?', (element_id,))
            law = cursor.fetchone()
            if law:
                messagebox.showinfo("Связанные элементы", f"Эта глава относится к закону: {law[0]}")
        elif element_type == 'article':
            # Если добавлена новая статья
            cursor.execute('SELECT title FROM chapters WHERE id = ?', (element_id,))
            chapter = cursor.fetchone()
            if chapter:
                cursor.execute('SELECT title FROM laws WHERE id = (SELECT law_id FROM chapters WHERE id = ?)', (element_id,))
                law = cursor.fetchone()
                if law:
                    messagebox.showinfo("Связанные элементы", f"Эта статья относится к главе: {chapter[0]}, которая относится к закону: {law[0]}")
        elif element_type == 'sublaw':
            # Если добавлен новый подзаконный акт
            cursor.execute('SELECT title FROM chapters WHERE id = ?', (element_id,))
            chapter = cursor.fetchone()
            if chapter:
                cursor.execute('SELECT title FROM laws WHERE id = (SELECT law_id FROM chapters WHERE id = ?)', (element_id,))
                law = cursor.fetchone()
                if law:
                    messagebox.showinfo("Связанные элементы", f"Этот подзаконный акт относится к главе: {chapter[0]}, которая относится к закону: {law[0]}")

        conn.close()

    def edit_law(self):
        law_id = simpledialog.askinteger("Редактирование закона", "Введите ID закона для редактирования:")
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT title, description, date_enacted FROM laws WHERE id = ?', (law_id,))
        law = cursor.fetchone()

        if law:
            title = simpledialog.askstring("Закон", f"Название закона ({law[0]}):", initialvalue=law[0])
            description = simpledialog.askstring("Закон", f"Описание закона ({law[1]}):", initialvalue=law[1])
            date_enacted = simpledialog.askstring("Закон", f"Дата принятия закона ({law[2]}):", initialvalue=law[2])

            if title and description and date_enacted:
                cursor.execute('''UPDATE laws SET title = ?, description = ?, date_enacted = ? WHERE id = ?''', (title, description, date_enacted, law_id))
                conn.commit()
                messagebox.showinfo("Успех", "Закон успешно обновлен!")
                self.show_affected_relations('law')
            else:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        else:
            messagebox.showerror("Ошибка", "Закон с таким ID не найден!")

        conn.close()

    def edit_chapter(self):
        chapter_id = simpledialog.askinteger("Редактирование главы", "Введите ID главы для редактирования:")
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT title, description, law_id FROM chapters WHERE id = ?', (chapter_id,))
        chapter = cursor.fetchone()

        if chapter:
            title = simpledialog.askstring("Глава", f"Название главы ({chapter[0]}):", initialvalue=chapter[0])
            description = simpledialog.askstring("Глава", f"Описание главы ({chapter[1]}):", initialvalue=chapter[1])
            law_id = simpledialog.askinteger("Глава", f"ID закона ({chapter[2]}):", initialvalue=chapter[2])

            if title and description and law_id:
                cursor.execute('''UPDATE chapters SET title = ?, description = ?, law_id = ? WHERE id = ?''', (title, description, law_id, chapter_id))
                conn.commit()
                messagebox.showinfo("Успех", "Глава успешно обновлена!")
                self.show_affected_relations('chapter', law_id)
            else:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        else:
            messagebox.showerror("Ошибка", "Глава с таким ID не найдена!")

        conn.close()

    def edit_article(self):
        article_id = simpledialog.askinteger("Редактирование статьи", "Введите ID статьи для редактирования:")
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT title, content, chapter_id FROM articles WHERE id = ?', (article_id,))
        article = cursor.fetchone()

        if article:
            title = simpledialog.askstring("Статья", f"Название статьи ({article[0]}):", initialvalue=article[0])
            content = simpledialog.askstring("Статья", f"Содержание статьи ({article[1]}):", initialvalue=article[1])
            chapter_id = simpledialog.askinteger("Статья", f"ID главы ({article[2]}):", initialvalue=article[2])

            if title and content and chapter_id:
                cursor.execute('''UPDATE articles SET title = ?, content = ?, chapter_id = ? WHERE id = ?''', (title, content, chapter_id, article_id))
                conn.commit()
                messagebox.showinfo("Успех", "Статья успешно обновлена!")
                self.show_affected_relations('article', chapter_id)
            else:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        else:
            messagebox.showerror("Ошибка", "Статья с таким ID не найдена!")

        conn.close()

    def edit_sublaw(self):
        sublaw_id = simpledialog.askinteger("Редактирование подзаконного акта", "Введите ID подзаконного акта для редактирования:")
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT title, description, chapter_id FROM sublaws WHERE id = ?', (sublaw_id,))
        sublaw = cursor.fetchone()

        if sublaw:
            title = simpledialog.askstring("Подзаконный акт", f"Название подзаконного акта ({sublaw[0]}):", initialvalue=sublaw[0])
            description = simpledialog.askstring("Подзаконный акт", f"Описание подзаконного акта ({sublaw[1]}):", initialvalue=sublaw[1])
            chapter_id = simpledialog.askinteger("Подзаконный акт", f"ID главы ({sublaw[2]}):", initialvalue=sublaw[2])

            if title and description and chapter_id:
                cursor.execute('''UPDATE sublaws SET title = ?, description = ?, chapter_id = ? WHERE id = ?''', (title, description, chapter_id, sublaw_id))
                conn.commit()
                messagebox.showinfo("Успех", "Подзаконный акт успешно обновлен!")
                self.show_affected_relations('sublaw', chapter_id)
            else:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        else:
            messagebox.showerror("Ошибка", "Подзаконный акт с таким ID не найден!")

        conn.close()

    def view_laws(self):
        # Просмотр базы знаний с выбором по номеру
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, title FROM laws')
        laws = cursor.fetchall()
        conn.close()

        if not laws:
            messagebox.showinfo("Нет данных", "В базе данных нет законов.")
            return

        # Отображаем список законов с номерами
        laws_text = "\n".join([f"{index+1}. {law[1]}" for index, law in enumerate(laws)])
        selected_number = simpledialog.askinteger("Выбор закона", f"Выберите закон по номеру:\n{laws_text}")

        if selected_number:
            # Получаем ID выбранного закона по номеру
            if 1 <= selected_number <= len(laws):
                selected_law_id = laws[selected_number - 1][0]
                # Просмотр глав выбранного закона
                self.view_chapters(selected_law_id)

    def view_chapters(self, law_id):
        # Получаем главы для выбранного закона
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, title FROM chapters WHERE law_id = ?', (law_id,))
        chapters = cursor.fetchall()
        conn.close()

        if not chapters:
            messagebox.showinfo("Нет данных", "Для выбранного закона нет глав.")
            return

        # Отображаем список глав с номерами
        chapters_text = "\n".join([f"{index+1}. {chapter[1]}" for index, chapter in enumerate(chapters)])
        selected_number = simpledialog.askinteger("Выбор главы", f"Выберите главу по номеру:\n{chapters_text}")

        if selected_number:
            # Получаем ID выбранной главы по номеру
            if 1 <= selected_number <= len(chapters):
                selected_chapter_id = chapters[selected_number - 1][0]
                # Просмотр статей и подзаконных актов для выбранной главы
                self.view_articles_and_sublaws(selected_chapter_id)

    def view_articles_and_sublaws(self, chapter_id):
        # Получаем статьи и подзаконные акты для выбранной главы
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT title, content FROM articles WHERE chapter_id = ?', (chapter_id,))
        articles = cursor.fetchall()

        cursor.execute('SELECT title, description FROM sublaws WHERE chapter_id = ?', (chapter_id,))
        sublaws = cursor.fetchall()
        conn.close()

        # Отображаем статьи с номерами
        articles_text = "\n".join([f"{index+1}. {article[0]} - {article[1]}" for index, article in enumerate(articles)])

        # Отображаем подзаконные акты с номерами
        sublaws_text = "\n".join([f"{index+1}. {sublaw[0]} - {sublaw[1]}" for index, sublaw in enumerate(sublaws)])

        # Если есть статьи или подзаконные акты, показываем их
        if articles_text or sublaws_text:
            messagebox.showinfo("Статьи и подзаконные акты", f"{articles_text}\n{sublaws_text}")
        else:
            messagebox.showinfo("Нет данных", "Для выбранной главы нет статей или подзаконных актов.")

# ------------------------- Интерфейс Пользователя -------------------------

class UserInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Интерфейс Пользователя")

        # Кнопка для просмотра базы знаний
        self.view_laws_btn = tk.Button(self.root, text="Просмотр базы знаний", command=self.view_laws)
        self.view_laws_btn.pack(pady=10)

        self.exit_btn = tk.Button(self.root, text="Выход", command=self.root.quit)
        self.exit_btn.pack(pady=10)

    def view_laws(self):
        # Просмотр базы знаний (только для чтения)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, title FROM laws')
        laws = cursor.fetchall()
        conn.close()

        if not laws:
            messagebox.showinfo("Нет данных", "В базе данных нет законов.")
            return

        # Отображаем список законов с номерами
        laws_text = "\n".join([f"{index+1}. {law[1]}" for index, law in enumerate(laws)])
        selected_number = simpledialog.askinteger("Выбор закона", f"Выберите закон по номеру:\n{laws_text}")

        if selected_number:
            # Получаем ID выбранного закона по номеру
            if 1 <= selected_number <= len(laws):
                selected_law_id = laws[selected_number - 1][0]
                # Просмотр глав выбранного закона
                self.view_chapters(selected_law_id)

    def view_chapters(self, law_id):
        # Получаем главы для выбранного закона
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, title FROM chapters WHERE law_id = ?', (law_id,))
        chapters = cursor.fetchall()
        conn.close()

        if not chapters:
            messagebox.showinfo("Нет данных", "Для выбранного закона нет глав.")
            return

        # Отображаем список глав с номерами
        chapters_text = "\n".join([f"{index+1}. {chapter[1]}" for index, chapter in enumerate(chapters)])
        selected_number = simpledialog.askinteger("Выбор главы", f"Выберите главу по номеру:\n{chapters_text}")

        if selected_number:
            # Получаем ID выбранной главы по номеру
            if 1 <= selected_number <= len(chapters):
                selected_chapter_id = chapters[selected_number - 1][0]
                # Просмотр статей и подзаконных актов для выбранной главы
                self.view_articles_and_sublaws(selected_chapter_id)

    def view_articles_and_sublaws(self, chapter_id):
        # Получаем статьи и подзаконные акты для выбранной главы
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT title, content FROM articles WHERE chapter_id = ?', (chapter_id,))
        articles = cursor.fetchall()

        cursor.execute('SELECT title, description FROM sublaws WHERE chapter_id = ?', (chapter_id,))
        sublaws = cursor.fetchall()
        conn.close()

        # Отображаем статьи с номерами
        articles_text = "\n".join([f"{index+1}. {article[0]} - {article[1]}" for index, article in enumerate(articles)])

        # Отображаем подзаконные акты с номерами
        sublaws_text = "\n".join([f"{index+1}. {sublaw[0]} - {sublaw[1]}" for index, sublaw in enumerate(sublaws)])

        # Если есть статьи или подзаконные акты, показываем их
        if articles_text or sublaws_text:
            messagebox.showinfo("Статьи и подзаконные акты", f"{articles_text}\n{sublaws_text}")
        else:
            messagebox.showinfo("Нет данных", "Для выбранной главы нет статей или подзаконных актов.")


# ------------------------- Главная функция -------------------------

def main():
    # Создаем окно для выбора интерфейса
    root = tk.Tk()
    root.geometry("400x400")

    # Появляется выбор: эксперт или пользователь
    user_type = simpledialog.askstring("Выбор интерфейса", "Введите '1' для интерфейса эксперта или '2' для интерфейса пользователя:")

    if user_type == '1':
        expert_interface = ExpertInterface(root)
    elif user_type == '2':
        user_interface = UserInterface(root)
    else:
        messagebox.showerror("Ошибка", "Неизвестный тип интерфейса.")

    root.mainloop()

# Запуск программы
if __name__ == "__main__":
    main()