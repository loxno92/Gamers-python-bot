import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import requests
from bs4 import BeautifulSoup
import random

TOKEN = ''

GAME, PLATFORM, ROLE = range(3)

teammate_requests = {}

guides = {
    "Dota 2": ["Как фармить эффективно", "Гайд по герою Invoker"],
    "CS:GO": ["Тактики на карте Mirage", "Секретные позиции"],
    "Valorant": ["Как играть за агента Jett", "Раскидки гранат на Haven"],
}

def get_game_news(update, context):
    try:
        url = "https://www.igromania.ru/news/"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = soup.find_all('div', class_='aubli_item')[:5]
        news_text = "📰 Последние игровые новости:\n\n"
        for item in news_items:
            title_element = item.find('a', class_='aubli_name')
            link_element = title_element['href']
            title = title_element.text.strip()
            news_text += f"[{title}]({link_element})\n"
        update.message.reply_text(news_text, parse_mode=telegram.ParseMode.MARKDOWN)
    except requests.exceptions.RequestException as e:
        update.message.reply_text(f"Ошибка при получении новостей: {e}")
    except Exception as e:
        update.message.reply_text(f"Произошла ошибка: {e}")

def find_teammates_start(update, context):
    update.message.reply_text("🎮 В какую игру вы ищете напарников?")
    return GAME

def game_input(update, context):
    context.user_data['game'] = update.message.text
    update.message.reply_text("🕹️ На какой платформе вы играете? (PC, PS, Xbox и т.д.)")
    return PLATFORM

def platform_input(update, context):
    context.user_data['platform'] = update.message.text
    update.message.reply_text("🎯 Какие роли или задачи вам нужны в команде?")
    return ROLE

def role_input(update, context):
    context.user_data['role'] = update.message.text
    game = context.user_data['game']
    platform = context.user_data['platform']
    role = context.user_data['role']

    user_id = update.message.from_user.id
    teammate_requests[user_id] = context.user_data

    update.message.reply_text(
        f"🔎 Вы ищете напарников для игры {game} на платформе {platform} с ролями: {role}. "
        f"Ожидайте, пока другие пользователи не откликнутся."
    )
    return ConversationHandler.END

def find_matching_requests(update, context):
    if not teammate_requests:
        update.message.reply_text("На данный момент нет активных запросов на поиск напарников.")
        return

    user_data = context.user_data
    if not user_data:
        update.message.reply_text("Пожалуйста, сначала создайте запрос на поиск напарников с помощью команды /find_teammates.")
        return

    matches = []
    for user_id, request_data in teammate_requests.items():
        if user_id != update.message.from_user.id and \
           request_data['game'].lower() == user_data['game'].lower() and \
           request_data['platform'].lower() == user_data['platform'].lower():
            matches.append(user_id)

    if matches:
        matched_user_id = random.choice(matches)
        matched_user = context.bot.get_chat(matched_user_id)
        update.message.reply_text(
            f"✅ Найден потенциальный напарник! Свяжитесь с пользователем @{matched_user.username} для координации."
        )
    else:
        update.message.reply_text("К сожалению, пока не найдено подходящих напарников с такими же параметрами.")

def cancel_find_teammates(update, context):
    update.message.reply_text("Поиск напарников отменен.")
    return ConversationHandler.END

def find_guide(update, context):
    game_name = ' '.join(context.args)
    if not game_name:
        update.message.reply_text("Введите название игры, для которой хотите найти гайд, например: /guide Dota 2")
        return

    if game_name in guides:
        guides_list = "\n- ".join(guides[game_name])
        update.message.reply_text(f"📚 Гайды для игры '{game_name}':\n- {guides_list}")
    else:
        update.message.reply_text(f"К сожалению, гайды для игры '{game_name}' пока не найдены.")

def start(update, context):
    update.message.reply_text(
        "Привет! Я бот для геймеров. Вот что я умею:\n"
        "/news - Получить последние игровые новости\n"
        "/find_teammates - Найти сопартийцев для игры\n"
        "/find - Поиск подходящих запросов напарников\n"
        "/guide [название игры] - Найти гайды по игре"
    )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("news", get_game_news))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('find_teammates', find_teammates_start)],
        states={
            GAME: [MessageHandler(Filters.text & ~Filters.command, game_input)],
            PLATFORM: [MessageHandler(Filters.text & ~Filters.command, platform_input)],
            ROLE: [MessageHandler(Filters.text & ~Filters.command, role_input)],
        },
        fallbacks=[CommandHandler('cancel', cancel_find_teammates)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("find", find_matching_requests))
    dp.add_handler(CommandHandler("guide", find_guide))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()