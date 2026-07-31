import os
import telebot
from telebot import apihelper
from google import genai
from google.genai import types

apihelper.proxy = {'https': 'http://proxy.server:3128'}

# --- НАСТРОЙКИ ---
# Вставь сюда свой токен от Telegram-бота (из BotFather)
TELEGRAM_BOT_TOKEN = '8662145672:AAGvMYxn_dgXM__RQrQj1FksY1C5OTQG3a8'

# Вставь сюда свой API-ключ от Google AI Studio (который ты создал)
GEMINI_API_KEY = 'AQ.Ab8RN6Lq6dhk2XGLJw8y3nL01lNOoescVOQj_mleYidRmVT8cA'
# ------------------

# Инициализируем бота Telegram
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Инициализируем Google Gemini через новый официальный SDK
client = genai.Client(api_key=GEMINI_API_KEY)

print("=========================================")
print("Медицинский ИИ-бот успешно настроен!")
print("Ожидаю сообщений в Telegram...")
print("=========================================")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой медицинский ассистент на базе ИИ. Опиши мне свои симптомы, и я подскажу, к какому врачу обратиться. \n\n*Внимание: я не заменяю реального врача!*")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_query = message.text
    
    # Системная инструкция для ИИ
    system_instruction = (
        "Ты — опытный медицинский консультант. Твоя задача — проанализировать симптомы пользователя, "
        "предположить возможные причины, обязательно направить к конкретному врачу-специалисту "
        "и всегда в конце добавлять строгое предупреждение о необходимости очной консультации."
    )
    
    try:
        # Отправляем запрос к новейшей модели gemini-2.5-flash
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=user_query,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,
            ),
        )
        
        # Отвечаем пользователю в Telegram
        bot.reply_to(message, response.text)
        
    except Exception as e:
        error_msg = f"⚠️ Произошла ошибка при обращении к ИИ:\n{str(e)}"
        print(f"[ОШИБКА]: {str(e)}")
        bot.reply_to(message, error_msg)

# Запуск бота
if __name__ == '__main__':
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Ошибка работы бота: {e}")

