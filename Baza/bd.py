import sqlite3

def add_sample_data_with_sublaws():


    conn = sqlite3.connect('law_database.db')
    cursor = conn.cursor()

    # Добавление законов
    cursor.execute('''
    INSERT INTO laws (title, description, date_enacted) VALUES
    ('Закон о защите прав потребителей', 'Закон, регулирующий отношения между потребителями и поставщиками товаров и услуг.', '2020-01-01'),
    ('Гражданский кодекс', 'Основной закон, регулирующий гражданские правоотношения в стране.', '2023-01-01'),
    ('Закон об охране окружающей среды', 'Закон, регулирующий защиту экологии и охрану природы.', '2022-05-01')
    ''')

    # Получаем ID добавленных законов
    cursor.execute('SELECT id FROM laws WHERE title = "Закон о защите прав потребителей"')
    law_id_1 = cursor.fetchone()[0]

    cursor.execute('SELECT id FROM laws WHERE title = "Гражданский кодекс"')
    law_id_2 = cursor.fetchone()[0]

    cursor.execute('SELECT id FROM laws WHERE title = "Закон об охране окружающей среды"')
    law_id_3 = cursor.fetchone()[0]

    # Добавление глав для первого закона
    cursor.execute('''
    INSERT INTO chapters (law_id, title, description) VALUES
    (?, 'Глава 1: Общие положения', 'Общие положения, регулирующие отношения между потребителями и продавцами'),
    (?, 'Глава 2: Права потребителей', 'Права потребителей в контексте защиты их интересов')
    ''', (law_id_1, law_id_1))

    # Добавление глав для второго закона
    cursor.execute('''
    INSERT INTO chapters (law_id, title, description) VALUES
    (?, 'Глава 1: Общие положения', 'Общие положения гражданского законодательства'),
    (?, 'Глава 2: Договоры', 'Положения о договорах в гражданском праве')
    ''', (law_id_2, law_id_2))

    # Добавление глав для третьего закона
    cursor.execute('''
    INSERT INTO chapters (law_id, title, description) VALUES
    (?, 'Глава 1: Охрана окружающей среды', 'Общие положения по охране окружающей среды'),
    (?, 'Глава 2: Загрязнение воздуха', 'Положения о загрязнении атмосферы')
    ''', (law_id_3, law_id_3))

    # Получаем ID глав
    cursor.execute('SELECT id FROM chapters WHERE law_id = ? AND title = "Глава 1: Общие положения"', (law_id_1,))
    chapter_id_1_1 = cursor.fetchone()[0]

    cursor.execute('SELECT id FROM chapters WHERE law_id = ? AND title = "Глава 2: Права потребителей"', (law_id_1,))
    chapter_id_1_2 = cursor.fetchone()[0]

    cursor.execute('SELECT id FROM chapters WHERE law_id = ? AND title = "Глава 1: Общие положения"', (law_id_2,))
    chapter_id_2_1 = cursor.fetchone()[0]

    cursor.execute('SELECT id FROM chapters WHERE law_id = ? AND title = "Глава 2: Договоры"', (law_id_2,))
    chapter_id_2_2 = cursor.fetchone()[0]

    cursor.execute('SELECT id FROM chapters WHERE law_id = ? AND title = "Глава 1: Охрана окружающей среды"',
                   (law_id_3,))
    chapter_id_3_1 = cursor.fetchone()[0]

    cursor.execute('SELECT id FROM chapters WHERE law_id = ? AND title = "Глава 2: Загрязнение воздуха"', (law_id_3,))
    chapter_id_3_2 = cursor.fetchone()[0]

    # Добавление подзаконных актов для главы 1 первого закона
    cursor.execute('''
    INSERT INTO sublaws (chapter_id, title, description) VALUES
    (?, 'Подзаконный акт 1.1', 'Руководство по применению законодательства о защите прав потребителей'),
    (?, 'Подзаконный акт 1.2', 'Методические рекомендации по защите прав потребителей в торговле')
    ''', (chapter_id_1_1, chapter_id_1_1))

    # Добавление подзаконных актов для главы 2 второго закона
    cursor.execute('''
    INSERT INTO sublaws (chapter_id, title, description) VALUES
    (?, 'Подзаконный акт 2.1', 'Правила заключения договоров в рамках гражданского кодекса'),
    (?, 'Подзаконный акт 2.2', 'Порядок расторжения договоров')
    ''', (chapter_id_2_2, chapter_id_2_2))

    # Добавление подзаконных актов для главы 1 третьего закона
    cursor.execute('''
    INSERT INTO sublaws (chapter_id, title, description) VALUES
    (?, 'Подзаконный акт 3.1', 'Инструкции по охране водных ресурсов'),
    (?, 'Подзаконный акт 3.2', 'Правила охраны атмосферы от загрязнений')
    ''', (chapter_id_3_1, chapter_id_3_1))

    conn.commit()
    conn.close()


# Вызов функции для добавления данных с подзаконными актами
add_sample_data_with_sublaws()
