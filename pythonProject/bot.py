from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
# from telegram import Bot
import telebot
from telebot import types

API_TOKEN = '7616140381:AAF62sq_h_ssG7tN---_rWQlXLRIe16izqA'
CHAT_ID = '7616140381'

score_sum = 0

credit_sum = 0
credit_period=0
interest_rate=0
monthly_income=0

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
    global credit_period
    credit_period = int(message.text)
    bot.send_message(message.from_user.id, 'Какова процентная ставка вашего кредита (%)?')
    bot.register_next_step_handler(message, get_rate)

def get_rate(message):
    global interest_rate
    interest_rate = int(message.text)
    bot.send_message(message.from_user.id,'Каков ваш месячный доход (руб./мес.)?')
    bot.register_next_step_handler(message, get_income)

def get_income(message):
    global monthly_income
    monthly_income = int(message.text)
    bot.send_message(message.from_user.id, 'Итак, ваши данные: '+str(credit_sum)+str(credit_period)+str(interest_rate)+str(monthly_income))
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

bot.polling(none_stop=True, interval=0)

#----------------------------------------------------------------------------------------------------------------------- Конец дашборда
if __name__ == '__main__':
    app.run_server(debug=True)