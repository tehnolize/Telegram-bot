from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

import matplotlib.pyplot as plt

# from telegram import Bot
import telebot
from telebot import types

API_TOKEN = '7616140381:AAF62sq_h_ssG7tN---_rWQlXLRIe16izqA'
CHAT_ID = '7616140381'

score_sum = 0               # Сумма баллов анкетирования

credit_sum = 0              # Сумма кредита клиента
T=0                         # Период кредитования
i=0                         # Годовая процентаня ставка
monthly_income=0            # Месячный доход клиента

anketa_scores_list=[1,1,1,1]
anketa_criterias_list = ['Возраст','Наличие детей','Доход','Семейное положение','Сфера деятельности','Квалификация','Стаж работы','Наличие домашнего телефона','Наличие автомобиля и марка']



#----------------------------------------------------------------------------------------------------------------------- Создание Телеграм-бота
bot = telebot.TeleBot(API_TOKEN)

# Пример вывода фото
# @bot.message_handler(commands=['start'])
# def get_graph(message):
#     file = open('metrics.png','rb')
#     bot.send_photo(message.chat.id, file)
#
# bot.polling(none_stop=True, interval=0)

#----------------------------------------------------------------------------------------------------------------------- Ввод данных для кредита
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'Здравствуйте, для скоринговой оценки, пожалуйста, введите свои данные.')
    bot.send_message(message.from_user.id, 'Какова сумма вашего кредита (руб.)?')
    bot.register_next_step_handler(message, get_sum)  # следующий шаг – функция get_name

def get_sum(message):
    global credit_sum
    credit_sum = int(message.text)
    bot.send_message(message.from_user.id, 'Каков ваш срок кредитования (мес.)?')
    bot.register_next_step_handler(message, get_period) #следующий шаг – функция get_name

def get_period(message): #получаем фамилию
    global T
    T = int(message.text)
    bot.send_message(message.from_user.id, 'Какова годовая процентная ставка вашего кредита (%)?')
    bot.register_next_step_handler(message, get_rate)

def get_rate(message):
    global i
    i = int(message.text)
    bot.send_message(message.from_user.id,'Каков ваш месячный доход (руб./мес.)?')
    bot.register_next_step_handler(message, get_income)

def get_income(message):
    global monthly_income
    monthly_income = int(message.text)
    bot.send_message(message.from_user.id, 'Итак, ваши данные: '+str(credit_sum)+str(T)+str(i)+str(monthly_income))
    bot.send_message(message.from_user.id,
                     'Выши данные приняты. Для продолжения введите /next')
    bot.register_next_step_handler(message, anketa)

#----------------------------------------------------------------------------------------------------------------------- Анкетирование

def anketa (message):
    bot.send_message(message.from_user.id, 'Приступаем к первому этапу скоринговой оценки. Пожалуйста заполните следующую анкету')

# --------------------------------------------------------------------------------------------- Возраст
    keyboard_age = types.InlineKeyboardMarkup()
    key_age_1 = types.InlineKeyboardButton(text='20-25 лет', callback_data='20-25')
    keyboard_age.add(key_age_1)
    key_age_2 = types.InlineKeyboardButton(text='25-30 лет', callback_data='25-30')
    keyboard_age.add(key_age_2)
    key_age_3 = types.InlineKeyboardButton(text='30-60 лет', callback_data='30-60')
    keyboard_age.add(key_age_3)
    bot.send_message(message.from_user.id, text='Возраст', reply_markup=keyboard_age)
# --------------------------------------------------------------------------------------------- Наличие детей
    keyboard_children = types.InlineKeyboardMarkup()
    key_children_1 = types.InlineKeyboardButton(text='нет детей', callback_data='no')
    keyboard_children.add(key_children_1)
    key_children_2 = types.InlineKeyboardButton(text='один ребёнок', callback_data='one')
    keyboard_children.add(key_children_2)
    key_children_3 = types.InlineKeyboardButton(text='два ребёнка', callback_data='two')
    keyboard_children.add(key_children_3)
    key_children_4 = types.InlineKeyboardButton(text='три ребёнка', callback_data='three')
    keyboard_children.add(key_children_4)
    key_children_5 = types.InlineKeyboardButton(text='более трех детей', callback_data='more then three')
    keyboard_children.add(key_children_5)
    bot.send_message(message.from_user.id, text='Наличие детей', reply_markup=keyboard_children)
    # --------------------------------------------------------------------------------------------- Доход
    keyboard_income = types.InlineKeyboardMarkup()
    key_income_1 = types.InlineKeyboardButton(text='до 25 тыс. руб.', callback_data='-25')
    keyboard_income.add(key_income_1)
    key_income_2 = types.InlineKeyboardButton(text='25…60 тыс. руб.', callback_data='25-60')
    keyboard_income.add(key_income_2)
    key_income_3 = types.InlineKeyboardButton(text='более 60 тыс. руб.', callback_data='60-')
    keyboard_income.add(key_income_3)
    bot.send_message(message.from_user.id, text='Доход', reply_markup=keyboard_income)
    # --------------------------------------------------------------------------------------------- Семейное положение
    keyboard_family = types.InlineKeyboardMarkup()
    key_family_1 = types.InlineKeyboardButton(text='холост (не замужем)', callback_data='lonely')
    keyboard_family.add(key_family_1)
    key_family_2 = types.InlineKeyboardButton(text='женат (замужем)', callback_data='married')
    keyboard_family.add(key_family_2)
    key_family_3 = types.InlineKeyboardButton(text='женат (замужем), но живет раздельно', callback_data='married distinguished')
    keyboard_family.add(key_family_3)
    key_family_4 = types.InlineKeyboardButton(text='в разводе', callback_data='divorced')
    keyboard_family.add(key_family_4)
    key_family_5 = types.InlineKeyboardButton(text='вдовец (вдова)', callback_data='widow')
    keyboard_family.add(key_family_5)
    bot.send_message(message.from_user.id, text='Семейное положение', reply_markup=keyboard_family)
    # --------------------------------------------------------------------------------------------- Сфера деятельности
    keyboard_sphere = types.InlineKeyboardMarkup()
    key_sphere_1 = types.InlineKeyboardButton(text='государственная или муниципальная служба', callback_data='gosudar')
    keyboard_sphere.add(key_sphere_1)
    key_sphere_2 = types.InlineKeyboardButton(text='коммерческая структура', callback_data='commertional')
    keyboard_sphere.add(key_sphere_2)
    key_sphere_3 = types.InlineKeyboardButton(text='пенсионер', callback_data='pensioner')
    keyboard_sphere.add(key_sphere_3)
    key_sphere_4 = types.InlineKeyboardButton(text='другие сферы деятельности', callback_data='another')
    keyboard_sphere.add(key_sphere_4)
    bot.send_message(message.from_user.id, text='Сфера деятельности', reply_markup=keyboard_sphere)
    # --------------------------------------------------------------------------------------------- Квалификация
    keyboard_kvalific = types.InlineKeyboardMarkup()
    key_kvalific_1 = types.InlineKeyboardButton(text='нет квалификации', callback_data='no kvalif')
    keyboard_kvalific.add(key_kvalific_1)
    key_kvalific_2 = types.InlineKeyboardButton(text='обслуживающий персонал', callback_data='service pers')
    keyboard_kvalific.add(key_kvalific_2)
    key_kvalific_3 = types.InlineKeyboardButton(text='специалист', callback_data='special')
    keyboard_kvalific.add(key_kvalific_3)
    key_kvalific_4 = types.InlineKeyboardButton(text='служащий', callback_data='sluzhasi')
    keyboard_kvalific.add(key_kvalific_4)
    key_kvalific_5 = types.InlineKeyboardButton(text='руководитель', callback_data='rukovod')
    keyboard_kvalific.add(key_kvalific_5)
    bot.send_message(message.from_user.id, text='Квалификация', reply_markup=keyboard_kvalific)
    # --------------------------------------------------------------------------------------------- Стаж работы
    keyboard_stazh = types.InlineKeyboardMarkup()
    key_stazh_1 = types.InlineKeyboardButton(text='до одного года', callback_data='do odnogo goda')
    keyboard_stazh.add(key_stazh_1)
    key_stazh_2 = types.InlineKeyboardButton(text='до двух лет', callback_data='do dvuh let')
    keyboard_stazh.add(key_stazh_2)
    key_stazh_3 = types.InlineKeyboardButton(text='до трех лет', callback_data='do truh let')
    keyboard_stazh.add(key_stazh_3)
    key_stazh_4 = types.InlineKeyboardButton(text='до пяти лет', callback_data='do pyati let')
    keyboard_stazh.add(key_stazh_4)
    key_stazh_5 = types.InlineKeyboardButton(text='более пяти лет', callback_data='bolee pyati')
    keyboard_stazh.add(key_stazh_5)
    bot.send_message(message.from_user.id, text='Стаж работы', reply_markup=keyboard_stazh)
    # --------------------------------------------------------------------------------------------- Наличие домашнего телефона
    keyboard_phone = types.InlineKeyboardMarkup()
    key_phone_1 = types.InlineKeyboardButton(text='есть телефон', callback_data='est phone')
    keyboard_phone.add(key_phone_1)
    key_phone_2 = types.InlineKeyboardButton(text='отсутствует телефон', callback_data='no phone')
    keyboard_phone.add(key_phone_2)
    bot.send_message(message.from_user.id, text='Наличие домашнего телефона', reply_markup=keyboard_phone)
    # --------------------------------------------------------------------------------------------- Наличие автомобиля и марка
    keyboard_auto = types.InlineKeyboardMarkup()
    key_auto_1 = types.InlineKeyboardButton(text='нет автомобиля', callback_data='no auto')
    keyboard_auto.add(key_auto_1)
    key_auto_2 = types.InlineKeyboardButton(text='отечественная, старая', callback_data='otechestv, staraya')
    keyboard_auto.add(key_auto_2)
    key_auto_3 = types.InlineKeyboardButton(text='отечественная, новая', callback_data='otechestv, novaya')
    keyboard_auto.add(key_auto_3)
    key_auto_4 = types.InlineKeyboardButton(text='иномарка, старая', callback_data='inomarka, staraya')
    keyboard_auto.add(key_auto_4)
    key_auto_5 = types.InlineKeyboardButton(text='иномарка, новая', callback_data='inomarka, novaya')
    keyboard_auto.add(key_auto_5)
    bot.send_message(message.from_user.id, text='Наличие автомобиля и марка', reply_markup=keyboard_auto)

    bot.send_message(message.from_user.id,
                     'Для вывода диаграмм и результатов 1 этапа введите /graph_and_result_1')
    bot.register_next_step_handler(message, graph_and_result_1)

call_count=0
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global score_sum
    global anketa_scores_list

    global call_count
    if call_count==0:
        anketa_scores_list.clear()
        call_count+=1
    else:
        call_count+=1
    # --------------------------------------------------------------------------------------------- Возраст
    if call.data == '20-25':
        score_sum += 100
        anketa_scores_list.append(100) # добавление значения в массив для дашборда
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == '25-30':
        score_sum += 107
        anketa_scores_list.append(107)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == '30-60':
        score_sum += 123
        anketa_scores_list.append(123)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    # --------------------------------------------------------------------------------------------- Наличие детей
    if call.data == 'no':
        score_sum+=100
        anketa_scores_list.append(100)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'one':
        score_sum+=90
        anketa_scores_list.append(90)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'two':
        score_sum+=80
        anketa_scores_list.append(80)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'three':
        score_sum+=70
        anketa_scores_list.append(70)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'more then three':
        score_sum+=30
        anketa_scores_list.append(30)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    # --------------------------------------------------------------------------------------------- Доход
    if call.data == '-25':
        score_sum += 130
        anketa_scores_list.append(130) # добавление значения в массив для дашборда
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == '25-60':
        score_sum += 145
        anketa_scores_list.append(145)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == '60-':
        score_sum += 160
        anketa_scores_list.append(160)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    # --------------------------------------------------------------------------------------------- Семейное положение
    if call.data == 'lonely':
        score_sum+=87
        anketa_scores_list.append(87)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'married':
        score_sum+=115
        anketa_scores_list.append(115)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'married distinguished':
        score_sum+=30
        anketa_scores_list.append(30)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'divorced':
        score_sum+=70
        anketa_scores_list.append(70)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'widow':
        score_sum+=65
        anketa_scores_list.append(65)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    # --------------------------------------------------------------------------------------------- Сфера деятельности
    if call.data == 'gosudar':
        score_sum+=124
        anketa_scores_list.append(124)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'commertional':
        score_sum+=93
        anketa_scores_list.append(93)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'pensioner':
        score_sum+=29
        anketa_scores_list.append(29)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'another':
        score_sum+=37
        anketa_scores_list.append(37)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    # --------------------------------------------------------------------------------------------- Квалификация
    if call.data == 'no kvalif':
        score_sum+=3
        anketa_scores_list.append(3)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'service pers':
        score_sum+=17
        anketa_scores_list.append(17)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'special':
        score_sum+=72
        anketa_scores_list.append(72)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'sluzhasi':
        score_sum+=83
        anketa_scores_list.append(83)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'rukovod':
        score_sum+=122
        anketa_scores_list.append(122)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    # --------------------------------------------------------------------------------------------- Стаж работы
    if call.data == 'do odnogo goda':
        score_sum+=6
        anketa_scores_list.append(6)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'do dvuh let':
        score_sum+=28
        anketa_scores_list.append(28)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'do truh let':
        score_sum+=51
        anketa_scores_list.append(51)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'do pyati let':
        score_sum+=62
        anketa_scores_list.append(62)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'bolee pyati':
        score_sum+=89
        anketa_scores_list.append(89)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    # --------------------------------------------------------------------------------------------- Наличие домашнего телефона
    if call.data == 'est phone':
        score_sum+=36
        anketa_scores_list.append(36)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'no phone':
        score_sum+=7
        anketa_scores_list.append(7)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    # --------------------------------------------------------------------------------------------- Наличие автомобиля и марка
    if call.data == 'no auto':
        score_sum+=70
        anketa_scores_list.append(70)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'otechestv, staraya':
        score_sum+=7
        anketa_scores_list.append(7)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'otechestv, novaya':
        score_sum+=53
        anketa_scores_list.append(53)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'inomarka, staraya':
        score_sum+=60
        anketa_scores_list.append(60)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'inomarka, novaya':
        score_sum+=115
        anketa_scores_list.append(115)
        bot.delete_message(call.message.chat.id, call.message.message_id)



    if call_count == 9:
        bot.send_message(call.message.chat.id, 'Ваш скоринговый балл: ' + str(score_sum))

    # url = 'http://127.0.0.1:8050'
    # webbrowser.open(url)

#----------------------------------------------------------------------------------------------------------------------- Создание Дашборда
# df = pd.DataFrame({
#         # "Date": ["2023-01-01", "2023-01-02", "2023-01-03"],
#         # "Sales": [1000, 1200, 1500],
#         # "Profit": [500, 600, 700]
#         "criteria": anketa_criterias_list, # ['Возраст', 'Наличие детей','Доход','Семейное положение','Сфера деятельности'],
#         "score":  anketa_scores_list # [100, 120, 140, 170, 220]
#
#     })
#
# # Создание Dash-приложения
# app = Dash(__name__)
#
# # Добавление интерфейса дашборда
# app.layout = html.Div([
#     html.H1("Распределение баллов"),
#     dcc.Graph(figure=px.pie(df, names="criteria", values="score", title='Анкета')),
# ])



#----------------------------------------------------------------------------------------------------------------------- Вывод Дашборда
try:
    def graph_and_result_1(message):
        # -------------------------------------------------------------------------------------- Сохранение дашборда как картинки
        # Save plot as image          # Закинуто в функцию, чтобы изменились элементы массива в calllback
        # В противном случае, находясь в основном потоке, значения используются те, что были при объявлении

        plt.pie(anketa_scores_list, labels=anketa_criterias_list, autopct='%1.1f%%')
        plt.title('Распределение баллов (в долях) по критериям')  # нахвание графика
        plt.savefig('pie.png')
        plt.close()

        file_1 = open('.venv/pie.png', 'rb')
        bot.send_photo(message.from_user.id, file_1)

        plt.bar(anketa_criterias_list, anketa_scores_list)
        plt.title('Распределение баллов по критериям')  # нахвание графика
        plt.savefig('histogram.png')
        plt.close()

        file_2 = open('.venv/histogram.png', 'rb')
        bot.send_photo(message.from_user.id, file_2)
        # bot.close()

        if score_sum > 620:
            bot.send_message(message.from_user.id, 'Вы прошли первый этап. Для продолжения введите /next')
            bot.register_next_step_handler(message, expenses_data)
        else:
            bot.send_message(message.from_user.id, 'К сожалению, вы не смогли пройти первый этап')
except UserWarning:
    score_sum=score_sum+1-1

#----------------------------------------------------------------------------------------------------------------------- 2 этап скоринга
max_score=0
TD=0
OD=0
SD=0
K=0
E=[]
P=0

def expenses_data(message):
    global max_score
    global TD
    global OD
    global SD
    global K
    global E
    global P

    max_score = (123 + 100 + 160 + 115 + 124 + 122 + 89 + 36 + 115)  # Максимальный скориинговый балл
    if monthly_income == 0:
        print('line 415', i, T, monthly_income)
        exit()
    TD = float(monthly_income) * 0.6  # Текущий доход
    OD = TD * (score_sum / max_score)  # Ожидаемый доход
    SD = 0  # Свободный доход
    K = 0  # Коэффициент минимальных расходов, зависящий от количества членов семьи физического лица
    E = []  # Массив фиксированных платежей (аренда жилья, образование и т.п.)
    P = 0  # Ежемесячный платёж по кредиту


    bot.send_message(message.from_user.id, 'Приступаем ко второму этапу скоринговой оценки.')
    bot.send_message(message.from_user.id, 'Укажите количество членов семьи, проживающих совместно с вами')
    bot.register_next_step_handler(message, get_k)

def get_k(message):
    global K
    K = int(message.text)
    if K==0:
        K=0.3
    elif K==1:
        K=0.35
    elif K==2:
        K=0.4
    elif K==3:
        K=0.45
    elif K==4:
        K=0.5
    elif K>=5:
        K=0.7
    bot.send_message(message.from_user.id, 'Укажите ежемесячные фиксированные платежи вашей семьи (в руб.)')
    bot.send_message(message.from_user.id, '1) Арендные платежи')
    bot.register_next_step_handler(message, get_arenda)

def get_arenda(message):
    global E
    E.append(int(message.text))
    bot.send_message(message.from_user.id, '2) Платежи по кредитам')
    bot.register_next_step_handler(message, get_credits)

def get_credits(message):
    global E
    E.append(int(message.text))
    bot.send_message(message.from_user.id, '3) Платежи за образование')
    bot.register_next_step_handler(message, get_education)

def get_education(message):
    global E
    E.append(int(message.text))
    bot.send_message(message.from_user.id, '4) Алименты')
    bot.register_next_step_handler(message, get_aliments)

def get_aliments(message):
    global E
    E.append(int(message.text))
    bot.send_message(message.from_user.id, '5) Почие')
    bot.register_next_step_handler(message, get_another)

def get_another(message):
    global E
    E.append(int(message.text))
    bot.send_message(message.from_user.id, 'Для продолжения введите /next')
    bot.register_next_step_handler(message, income_calculation)

def income_calculation(message):
    global SD
    global OD
    global E
    SD = OD * (1.0 - K)-float(sum(E))
    bot.send_message(message.from_user.id, 'SD= ' + str(SD)+'   OD= ' + str(OD) + '   K= '+ str(K) + '   E= ' + str(float(sum(E))) +'   TD= ' + str(TD) +'   monthly_income= '+ str(monthly_income)  )
    bot.send_message(message.from_user.id, 'Укажите вашу схему кредитования: 1. Аннуитетная 2. Дифференцированная (ввести номер)')
    bot.register_next_step_handler(message, payment_calculation)

def payment_calculation(message):
    global P
    global i
    global T
    i/=100
    if message.text=='1':
        P = credit_sum*( (i/12)/(1 - (1+i/12)**(-T) )  )   # расчёт аннуитетного платежа
    elif message.text == '2':
        P = credit_sum/T + credit_sum*i/12   # расчёт максимального дифференцированного платежа
    bot.send_message(message.from_user.id, 'Для вывода графиков и результатов 2 этапа введите /graph_and_result_2')
    bot.register_next_step_handler(message, graph_and_result_2)

def graph_and_result_2(message):
    # ... графики
    global SD
    global P
    if SD>=P:
        bot.send_message(message.from_user.id, 'Вы прошли 2 этап скоринговой оценки. Теперь вы признаётесь кредитоспособным клиентом для банка')
    else:
        bot.send_message(message.from_user.id, 'К сожалению, вы не прошли 2 этап скоринговой оценки')

    bot.send_message(message.from_user.id, 'Ваш свободный доход: ' + str(SD))
    bot.send_message(message.from_user.id, 'Ваш ежемесячный платёж по кредиту: ' + str(P))




bot.polling(none_stop=True, interval=0)

#----------------------------------------------------------------------------------------------------------------------- Конец дашборда
if __name__ == '__main__':
    app.run_server(debug=True)