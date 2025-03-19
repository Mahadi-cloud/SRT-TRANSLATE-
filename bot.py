# bot.py

import telebot
from config import TELEGRAM_BOT_TOKEN
from utils import translate_text, parse_srt, generate_srt

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Please send me an .srt file.")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("subtitle.srt", "wb") as file:
        file.write(downloaded_file)
    bot.reply_to(message, "File received. Please enter the target languages separated by commas (e.g., en,es,fr).")

@bot.message_handler(func=lambda message: True)
def handle_languages(message):
    languages = message.text.split(',')
    with open("subtitle.srt", "r") as file:
        content = file.read()
    subtitles = parse_srt(content)
    for lang in languages:
        translated_subtitles = []
        for sub in subtitles:
            translated_text = translate_text(sub['text'], lang)
            translated_subtitles.append({
                'index': sub['index'],
                'time': sub['time'],
                'text': translated_text
            })
        srt_content = generate_srt(translated_subtitles)
        with open(f"subtitle_{lang}.srt", "w") as file:
            file.write(srt_content)
        with open(f"subtitle_{lang}.srt", "rb") as file:
            bot.send_document(message.chat.id, file)
    bot.reply_to(message, "All translations have been sent.")

if __name__ == "__main__":
    bot.polling()
