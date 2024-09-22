import json
import os
import time
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from main import handle as send_data_to_server


# Обработчик команды /start
def start(update: Update, context: CallbackContext) -> None:
    context.chat_data.clear()  # Очищаем данные чата при запуске
    update.message.reply_text(
        'Каждый из нас, воплощенных на земле людей, должен знать, из чего складывается его прошлое, настоящее будущее, осознавать свои мысли, действия, поступки. Знать свои кармические задачи и таланты.\n\n'
        'Все это есть в натальной карте. Только нужно правильно ее составить!\n',
        reply_markup=ReplyKeyboardMarkup([['Составить натальную карту']], one_time_keyboard=True, resize_keyboard=True)
    )


def send_photo(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    # Формируем путь к изображению
    photo_path = fr'{os.path.dirname(os.path.abspath(__file__))}/downloads{chat_id}.png'

    if os.path.exists(photo_path):
        # Отправляем изображение
        context.bot.send_photo(chat_id=chat_id, photo=open(photo_path, 'rb'))
        update.message.reply_text(f'{chat_id}, Изображение отправлено.')
    else:
        update.message.reply_text(f'{chat_id}, Изображение не найдено.')


# Валидация имени и фамилии
def validate_name(name: str) -> bool:
    return name.replace(" ", "").isalpha()


# Валидация даты рождения
def validate_date(date: str) -> bool:
    try:
        day, month, year = map(int, date.split('.'))
        if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= datetime.now().year):
            return False
        datetime(year, month, day)  # Проверка на существующую дату
        return True
    except ValueError:
        return False


# Валидация времени рождения
def validate_time(time_str: str) -> bool:
    try:
        hour, minute = map(int, time_str.split(':'))
        return 0 <= hour < 24 and 0 <= minute < 60
    except ValueError:
        return False


# Обработчик текстовых сообщений
def text_handler(update: Update, context: CallbackContext) -> None:
    text = update.message.text

    if text == "test":
        update.message.reply_photo(photo='', caption="Твоя натальная карта:")

    if text == 'Составить натальную карту':
        time.sleep(1)
        update.message.reply_text('Отлично, тогда отправь сейчас Имя и Фамилию (по желанию)')

    elif text == 'Изменить данные':
        update.message.reply_text('Какое поле вы хотите изменить?', reply_markup=ReplyKeyboardMarkup([
            ['Имя и фамилия', 'Пол'], ['Дата рождения', 'Время рождения'], ['Город рождения'], ['В меню']
        ], one_time_keyboard=True, resize_keyboard=True))

    elif text in ['Имя и фамилия', 'Пол', 'Дата рождения', 'Время рождения', 'Город рождения']:
        context.chat_data['field_to_change'] = text
        if text == 'Пол':
            update.message.reply_text('Выберите ваш пол.', reply_markup=ReplyKeyboardMarkup([['М', 'Ж'], ['Назад']], one_time_keyboard=True, resize_keyboard=True))
        elif text == "Дата рождения":
            update.message.reply_text("Введите дату рождения через точку (пример: 15.06.1987)", reply_markup=ReplyKeyboardMarkup([['Назад']], one_time_keyboard=True, resize_keyboard=True))
        else:
            update.message.reply_text(f'Введите новое значение для поля "{text}"', reply_markup=ReplyKeyboardMarkup([['Назад']], one_time_keyboard=True, resize_keyboard=True))

    elif text == 'Назад':
        update.message.reply_text('Какое поле вы хотите изменить?', reply_markup=ReplyKeyboardMarkup([
            ['Имя и фамилия', 'Пол'], ['Дата рождения', 'Время рождения'], ['Город рождения'], ["В меню"]
        ], one_time_keyboard=True, resize_keyboard=True))
    elif text == "В меню":
        update.message.reply_text(
            f'Хотите изменить еще что-то?\n'
            f'Имя и фамилия: {context.chat_data.get("name", "не указано")}\n'
            f'Пол: {context.chat_data.get("sex", "не указано")}\n'
            f'Дата рождения: {context.chat_data.get("date", "не указано")}\n'
            f'Время рождения: {context.chat_data.get("date_born", "не указано")}\n'
            f'Город рождения: {context.chat_data.get("city", "не указано")}',
            reply_markup=ReplyKeyboardMarkup([['Все верно', 'Изменить данные']], one_time_keyboard=True,
                                             resize_keyboard=True)
        )
    elif 'field_to_change' in context.chat_data:
        field_map = {
            'Имя и фамилия': 'name',
            'Пол': 'sex',
            'Дата рождения': 'date',
            'Время рождения': 'date_born',
            'Город рождения': 'city'
        }
        field = context.chat_data['field_to_change']
        is_valid = True
        if field == 'Имя и фамилия':
            is_valid = validate_name(text)
            if not is_valid:
                update.message.reply_text('Имя и фамилия должны содержать только буквы. Пожалуйста, попробуйте снова.')
        elif field == 'Дата рождения':
            is_valid = validate_date(text)
            if not is_valid:
                update.message.reply_text('Неправильный формат даты или неверная дата. Пожалуйста, введите в формате дд.мм.гггг и попробуйте снова.')
        elif field == 'Время рождения':
            is_valid = validate_time(text)
            if not is_valid:
                update.message.reply_text('Неправильный формат времени. Пожалуйста, введите в формате чч:мм и попробуйте снова.')

        if is_valid:
            context.chat_data[field_map[field]] = text
            del context.chat_data['field_to_change']
            update.message.reply_text(
                f'Поле успешно обновлено! Хотите изменить еще что-то?\n'
                f'Имя и фамилия: {context.chat_data.get("name", "не указано")}\n'
                f'Пол: {context.chat_data.get("sex", "не указано")}\n'
                f'Дата рождения: {context.chat_data.get("date", "не указано")}\n'
                f'Время рождения: {context.chat_data.get("date_born", "не указано")}\n'
                f'Город рождения: {context.chat_data.get("city", "не указано")}',
                reply_markup=ReplyKeyboardMarkup([['Все верно', 'Изменить данные']], one_time_keyboard=True, resize_keyboard=True)
            )

    elif 'name' not in context.chat_data:
        time.sleep(1)
        if validate_name(text):
            context.chat_data['name'] = text
            update.message.reply_text('Запомнила, теперь давай запишем пол',
                                      reply_markup=ReplyKeyboardMarkup([['М', 'Ж']], one_time_keyboard=True,
                                                                       resize_keyboard=True))
        else:
            update.message.reply_text('Имя и фамилия должны содержать только буквы. Пожалуйста, попробуйте снова.')

    elif 'sex' not in context.chat_data:
        time.sleep(1)
        context.chat_data['sex'] = text
        update.message.reply_text('Прекрасно! Теперь дату рождения через точку (пример: 15.06.1987)')

    elif 'date' not in context.chat_data:
        time.sleep(1)
        if validate_date(text):
            context.chat_data['date'] = text
            update.message.reply_text('Время рождения: (если неизвестно, 12:00)')
        else:
            update.message.reply_text('Неправильный формат даты или неверная дата. Пожалуйста, введите в формате дд.мм.гггг и попробуйте снова.')

    elif 'date_born' not in context.chat_data:
        time.sleep(1)
        if validate_time(text):
            context.chat_data['date_born'] = text
            update.message.reply_text('Теперь город рождения')
        else:
            update.message.reply_text('Неправильный формат времени. Пожалуйста, введите в формате чч:мм и попробуйте снова.')

    elif 'city' not in context.chat_data:
        time.sleep(1)
        context.chat_data['city'] = text
        update.message.reply_text(
            f'Всё ли верно введено?:\n\n'
            f'Имя и фамилия: {context.chat_data["name"]}\n'
            f'Пол: {context.chat_data["sex"]}\n'
            f'Дата рождения: {context.chat_data["date"]}\n'
            f'Время рождения: {context.chat_data["date_born"]}\n'
            f'Город рождения: {context.chat_data["city"]}',
            reply_markup=ReplyKeyboardMarkup([['Все верно', 'Изменить данные']], one_time_keyboard=True,
                                             resize_keyboard=True)
        )

    elif text == 'Все верно':
        # Отправляем данные на сервер и получаем ссылку на картинку
        context.chat_data['chat_id'] = update.message.chat_id
        image_url = (context.chat_data)
        update.message.reply_text("Составляю карту. Обычно нужно подождать 15-20 секунд для получения карты")
        acs, moon, chat_id = send_data_to_server(image_url)
        # Отправляем ссылку на картинку пользователю
        if moon:
            # Формируем путь к изображению
            print(acs,moon,chat_id)
            photo_path = fr'{os.path.dirname(os.path.abspath(__file__))}\downloads\{chat_id}.png'
            print(photo_path, os.path.exists(photo_path))
            if os.path.exists(photo_path):
                # Отправляем изображение
                context.bot.send_photo(chat_id=chat_id, photo=open(photo_path, 'rb'))
                update.message.reply_text(f'Готово!\nТвоя натальная карта:')
                update.message.reply_text(f"Восходящий знак - {acs} \n Лунный знак - {moon}")

            update.message.reply_text('Хотите создать новую натальную карту?\n\n Если пропали кнопки,напишите '
                                      '```Copy "Составить новую карту", или "Да"```',
                                      parse_mode=ParseMode.MARKDOWN_V2,reply_markup=ReplyKeyboardMarkup([['Составить новую карту']],
                                                                       one_time_keyboard=True, resize_keyboard=True))
        else:
            update.message.reply_text('Произошла ошибка при получении натальной карты. Попробуйте позже.')

    elif text == 'Составить новую карту' or 'Да' or 'да' or 'дА':
        context.chat_data.clear()
        update.message.reply_text('Давайте начнем сначала. Отправьте Имя и Фамилию (по желанию)',
                                  reply_markup=ReplyKeyboardMarkup([], remove_keyboard=True))


def main() -> None:
    updater = Updater("6544498233:AAGYlGd75G9pWyrROfW-vL0wQtSDK9jIQ_w")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_handler))
    dispatcher.add_handler(CommandHandler('send_photo', send_photo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()