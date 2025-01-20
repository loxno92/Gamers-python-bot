# Telegram Bot для геймеров

Этот Telegram-бот предоставляет геймерам полезные функции, такие как получение последних игровых новостей, поиск напарников и доступ к игровым гайдам.

## Особенности

* **Новости игр:** Получение последних новостей с популярного игрового сайта. Используйте команду `/news`.
* **Поиск напарников:** Функция для поиска напарников для совместных игр. Используйте команду `/find_teammates` для создания запроса и `/find` для поиска подходящих запросов.
* **Игровые гайды:** Доступ к базовой коллекции гайдов по популярным играм. Используйте команду `/guide [название игры]`.

## Инструкции по использованию

1. **Необходимые библиотеки:**
   Убедитесь, что у вас установлены необходимые библиотеки Python. Вы можете установить их с помощью pip: pip install python-telegram-bot==13.7 requests beautifulsoup4
      
2. **Настройка токена:**
Замените `'YOUR_BOT_TOKEN'` на реальный токен вашего Telegram-бота, полученный от BotFather, в файле `game_bot.py`:
```python
TOKEN = 'YOUR_BOT_TOKEN'
```

## Команды бота

| Команда             | Описание                                                                                                |
|----------------------|---------------------------------------------------------------------------------------------------------|
| `/start`             | Приветственное сообщение и список доступных команд.                                                    |
| `/news`              | Получить последние игровые новости с сайта Igromania.                                                   |
| `/find_teammates`    | Запустить процесс поиска напарников. Бот запросит название игры, платформу и желаемые роли.              |
| `/find`              | Найти подходящие запросы напарников от других пользователей, соответствующих вашему последнему запросу. |
| `/guide [название игры]` | Получить список доступных гайдов для указанной игры (например, `/guide Dota 2`).                          |
| `/cancel`           | Отменить текущий процесс поиска сопартийцев.                                                            |


Автор
loxno92

Лицензия
GNU General Public License v3.0
