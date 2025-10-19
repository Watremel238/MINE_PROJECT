import telebot
import sqlite3
import json

API_TOKEN = '7996754173:AAEbldXu9drkQpm4Ios0M7j-2JfKlcAMqsM'

bot = telebot.TeleBot(API_TOKEN)

users = {}

conn = sqlite3.connect("users_db.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users_db(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER UNIQUE,
                       user_data TEXT
               )
               
               ''')  
conn.commit()
##conn.execute('''
##CREATE TABLE IF NOT EXISTS works_db(
##             )''')
cariers_data = [
    # Работа из дома + Технарь + разные возрастные группы
    ('работа из дома', 'технарь', '10 - 17', 'Разработчик игр', 'Создание простых игр и приложений, обучение программированию'),
    ('работа из дома', 'технарь', '17 - 25', 'Веб-разработчик', 'Разработка сайтов и веб-приложений, фриланс'),
    ('работа из дома', 'технарь', '25 - 30', 'Data Scientist', 'Анализ данных, машинное обучение, удаленная работа'),
    ('работа из дома', 'технарь', '30+', 'IT-архитектор', 'Проектирование сложных систем, удаленное руководство'),

    # Работа из дома + Гуманитарий + разные возрастные группы
    ('работа из дома', 'гуманитарий', '10 - 17', 'Блогер', 'Ведение блога, создание контента'),
    ('работа из дома', 'гуманитарий', '17 - 25', 'Копирайтер', 'Написание текстов, статей, рекламных материалов'),
    ('работа из дома', 'гуманитарий', '25 - 30', 'SMM-специалист', 'Продвижение в соцсетях, удаленная работа'),
    ('работа из дома', 'гуманитарий', '30+', 'Онлайн-преподаватель', 'Преподавание через интернет, создание курсов'),

    # Работа не из дома + Технарь + разные возрастные группы
    ('работа не из дома', 'технарь', '10 - 17', 'Стажер в IT-компании', 'Помощь в технических задачах, обучение'),
    ('работа не из дома', 'технарь', '17 - 25', 'Инженер-программист', 'Разработка программного обеспечения в офисе'),
    ('работа не из дома', 'технарь', '25 - 30', 'Системный администратор', 'Обслуживание IT-инфраструктуры компании'),
    ('работа не из дома', 'технарь', '30+', 'IT-директор', 'Руководство IT-отделом, стратегическое планирование'),

    # Работа не из дома + Гуманитарий + разные возрастные группы
    ('работа не из дома', 'гуманитарий', '10 - 17', 'Волонтер', 'Помощь в социальных проектах, мероприятиях'),
    ('работа не из дома', 'гуманитарий', '17 - 25', 'Журналист', 'Работа в редакции, написание статей, репортажи'),
    ('работа не из дома', 'гуманитарий', '25 - 30', 'Менеджер проектов', 'Координация команд, управление проектами'),
    ('работа не из дома', 'гуманитарий', '30+', 'HR-специалист', 'Подбор персонала, работа с сотрудниками'),
]
conn = sqlite3.connect("cariers.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS cariers(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               work_type TEXT NOT NULL,
               personality_type TEXT NOT NULL,
               age_group TEXT NOT NULL,
               carier_name TEXT NOT NULL,
               carier_des TEXT,
               UNIQUE(work_type, personality_type, age_group)
               )
               ''')
cursor.executemany('''
INSERT OR IGNORE INTO cariers (work_type, personality_type, age_group, carier_name, carier_des) VALUES (?, ?, ?, ?, ?)
''', cariers_data)
conn.commit()
class User:
    def __init__(self, id, name, date_of_birth, state, chat, answerrs=None):
        self.id = id
        self.name = name
        self.birthday = date_of_birth
        self.state = state
        if answerrs:
            self.answerrs = answerrs
        else:
            self.answerrs = {}
        self.chat_id = chat
        User.add_to_db(self)
    def to_dict(self):
        return {'id': self.id,
        'name': self.name,
        'birthday': self.birthday,
        'state': self.state,
        'answerrs': self.answerrs,
        'chat_id' :self.chat_id}

    def add_to_db(self):
        conn = sqlite3.connect("users_db.db")
        cursor = conn.cursor()

        user_dict = self.to_dict()
        user_json = json.dumps(user_dict, ensure_ascii=False)

        cursor.execute("""SELECT user_id FROM users_db WHERE user_id = ?""", (self.id,))
        if cursor.fetchone() == None:
            cursor.execute('''INSERT INTO users_db (user_id, user_data) VALUES(?, ?)''',(self.id, user_json))
        else:
            cursor.execute('''UPDATE users_db SET user_data = ? WHERE user_id = ?''',(user_json, self.id))
        conn.commit()
    def get_from_db(user_id):
        try:
            conn = sqlite3.connect("users_db.db")
            cursor = conn.cursor()    
            cursor.execute("""SELECT user_data FROM users_db WHERE user_id = ?""", (user_id,))
            res = cursor.fetchone()
            if res:
                user_data = json.loads(res[0])
                user = User(user_data["id"], user_data["name"], user_data["birthday"], user_data["state"], user_data["chat_id"], user_data["answerrs"])
                return user
        except Exception:
            pass 
    def add_answer(self, question, answerr):
        self.answerrs[question] = answerr
        User.add_to_db(self)   
    def analyse(self):
        if self.answerrs and len(self.answerrs) == 3:
            answ_0 = self.answerrs["question_0"]
            answ_1 = self.answerrs["question_1"]
            answ_2 = self.answerrs["question_2"]
            conn = sqlite3.connect('cariers.db')
            cursor = conn.cursor()
            cursor.execute("""SELECT carier_name, carier_des FROM cariers WHERE work_type = ? AND personality_type = ? AND age_group = ?""", (answ_0, answ_1, answ_2))
            res = cursor.fetchone()
            carier_name = res[0]
            carier_des = res[1]
            bot.send_message(self.chat_id, f'РЕЗУЛЬТАТ, \n{carier_name} \n{carier_des}')
            conn.close()

def user_initialisation(name, b_date, state, chat, id):
    conn = sqlite3.connect("users_db.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT user_id FROM users_db WHERE user_id = ?""", (id,))
    if cursor.fetchone() == None:
        user = User(id, name, b_date, state, chat)
        User.add_to_db(user)
    else:
        user = User.get_from_db(id)
        user.state = state   
        User.add_to_db(user)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привете, я бот для выбора карьеры незнаю что дополнить)\
""")

def question(message, choises, question_name, next_question_state, pretext=None, next_choises=None):
    if message.text.lower() not in choises:
        bot.reply_to(message, 'попробуйте сного')
        return
    user = User.get_from_db(message.from_user.id)
    user.add_answer(question_name, message.text)
    user.state = next_question_state    
    User.add_to_db(user)    
    bot.reply_to(message, f'записали, ваши ответ {list(user.answerrs.values())}')
    if next_choises:
        bot.send_message(message.chat.id, f'{pretext} {next_choises}')
    else:
        bot.send_message(message.chat.id, f'спасибо за прохождение теста ваши ответы: {user.answerrs.values()} ')
        user.analyse()
        
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(commands=['test'])
def test_cuarier(message):
    chat_id = message.chat.id
    user_initialisation(message.from_user.first_name, 0, 'question_0', chat_id, message.from_user.id)
    User.get_from_db(message.from_user.id).answerrs = {}
    bot.send_message(chat_id, "привет) чтобы ты выбрал? [работа из дома, работа не из дома]")

@bot.message_handler(func=lambda m: User.get_from_db(m.from_user.id) and User.get_from_db(m.from_user.id).state == "question_0")     
def question_0_handler(message):
    question(message, ["работа из дома", "работа не из дома"], "question_0", "question_1", "кто вы?", ["технарь", "гуманитарий"])  
@bot.message_handler(func=lambda m: User.get_from_db(m.from_user.id) and User.get_from_db(m.from_user.id).state == "question_1")     
def question_1_handler(message):
    question(message, ["технарь", "гуманитарий"], "question_1", "question_2", "сколько вам лет?\n(записать в формате как написано тоесть 10 - 17 либо другие варианты)",["10 - 17", "17 - 25", "25 - 30", "30+"]) 
@bot.message_handler(func=lambda m: User.get_from_db(m.from_user.id) and User.get_from_db(m.from_user.id).state == "question_2")     
def question_2_handler(message):
    question(message, ["10 - 17", "17 - 25", "25 - 30", "30+"], "question_2", "None")       

bot.infinity_polling()
