import sqlite3

def add_sample_data():

    conn = sqlite3.connect('law_database.db')
    cursor = conn.cursor()

    # Добавление законов
    cursor.execute('''
    INSERT INTO laws (title, description, date_enacted) VALUES
    ('Закон о защите прав потребителей', 'Закон, регулирующий отношения между потребителями и поставщиками товаров и услуг.', '2020-01-01'),
    ('Гражданский кодекс', 'Основной закон, регулирующий гражданские правоотношения в стране.', '2023-01-01')
    ''')

    # Получаем ID добавленных законов
    cursor.execute('SELECT id FROM laws WHERE title = "Закон о защите прав потребителей"')
    law_id_1 = cursor.fetchone()[0]

    cursor.execute('SELECT id FROM laws WHERE title = "Гражданский кодекс"')
    law_id_2 = cursor.fetchone()[0]

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

    # Получаем ID глав
    cursor.execute('SELECT id FROM chapters WHERE law_id = ? AND title = "Глава 1: Общие положения"', (law_id_1,))
    chapter_id_1_1 = cursor.fetchone()[0]

    cursor.execute('SELECT id FROM chapters WHERE law_id = ? AND title = "Глава 2: Права потребителей"', (law_id_1,))
    chapter_id_1_2 = cursor.fetchone()[0]

    cursor.execute('SELECT id FROM chapters WHERE law_id = ? AND title = "Глава 1: Общие положения"', (law_id_2,))
    chapter_id_2_1 = cursor.fetchone()[0]

    cursor.execute('SELECT id FROM chapters WHERE law_id = ? AND title = "Глава 2: Договоры"', (law_id_2,))
    chapter_id_2_2 = cursor.fetchone()[0]

    # Добавление статей для первой главы первого закона
    cursor.execute('''
    INSERT INTO articles (chapter_id, title, content) VALUES
    (?, 'Статья 1: Права потребителей на информацию', 'Каждый потребитель имеет право на полную информацию о товаре или услуге.'),
    (?, 'Статья 2: Ответственность продавца', 'Продавец обязан возместить ущерб, если товар или услуга не соответствуют заявленным характеристикам.')
    ''', (chapter_id_1_1, chapter_id_1_2))

    # Добавление статей для первой главы второго закона
    cursor.execute('''
    INSERT INTO articles (chapter_id, title, content) VALUES
    (?, 'Статья 1: Определение гражданского права', 'Гражданское право регулирует отношения между физическими и юридическими лицами в области собственности, обязательств и иных сделок.'),
    (?, 'Статья 2: Прекращение гражданских прав', 'Гражданские права прекращаются в случаях, предусмотренных законодательством.')
    ''', (chapter_id_2_1, chapter_id_2_2))

    conn.commit()
    conn.close()


# Вызов функции для добавления данных
add_sample_data()
