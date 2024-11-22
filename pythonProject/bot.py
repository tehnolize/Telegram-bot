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

bot.polling(none_stop=True, interval=0)

#----------------------------------------------------------------------------------------------------------------------- Конец дашборда
if __name__ == '__main__':
    app.run_server(debug=True)