import states
import telebot
from states import States
from telebot import types
import user_dicts
from texts import *
import Game
from json import JSONEncoder

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default


token = '1149586230:AAHaOd4fopbl0F_T_fwopykTydRG_F3QylE'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup()
    start_game_button = types.InlineKeyboardButton(text="Начать игру", callback_data="start_game")
    rules_button = types.InlineKeyboardButton(text="Правила игры", callback_data="rules")
    dict_button = types.InlineKeyboardButton(text="Мои словари", callback_data="exist_dics")

    keyboard.add(start_game_button)
    keyboard.add(rules_button)
    keyboard.add(dict_button)

    states.set_state(message.chat.id, States.START)
    bot_msg = bot.send_message(message.chat.id, start_text, reply_markup=keyboard, parse_mode='MARKDOWN')
    if states.get_base(message.chat.id) is not None:
        try:
            bot.delete_message(message.chat.id, states.get_base(message.chat.id))
        except:
            pass
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
    states.set_base(message.chat.id, bot_msg.message_id)


def edit2start(message):
    keyboard = types.InlineKeyboardMarkup()
    start_game_button = types.InlineKeyboardButton(text="Начать игру", callback_data="start_game")
    rules_button = types.InlineKeyboardButton(text="Правила игры", callback_data="rules")
    dict_button = types.InlineKeyboardButton(text="Словари", callback_data="exist_dics")

    keyboard.add(start_game_button)
    keyboard.add(rules_button)
    keyboard.add(dict_button)

    states.set_state(message.chat.id, States.START)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=start_text, reply_markup=keyboard, parse_mode='MARKDOWN')


def game_start(chat_id, new_game = True):
    keyboard = types.InlineKeyboardMarkup()

    if new_game:
        Game.create_game(chat_id)


    back_button = types.InlineKeyboardButton(text="Назад", callback_data="hello")
    keyboard.add(back_button)

    to_dicts_button = types.InlineKeyboardButton(text="Далее", callback_data="choose_dicts")
    keyboard.add(to_dicts_button)

    multi_game_button = types.InlineKeyboardButton(text="Каждый с каждым", callback_data="toggle_multi_mode")
    keyboard.add(multi_game_button)

    pair_game_button = types.InlineKeyboardButton(text="По парам", callback_data="toggle_pair_mode")
    keyboard.add(pair_game_button)


    states.set_state(chat_id, States.BASIC_GAME_SET)

    result_txt = start_game_text
    result_txt = result_txt.replace('режимигры', Game.get_mode(chat_id))
    result_txt = result_txt.replace('длительностьхода', Game.get_duration(chat_id))


    bot.edit_message_text(chat_id=chat_id, message_id=states.get_base(chat_id), text=result_txt,
                          reply_markup=keyboard, parse_mode='MARKDOWN')



toggle_dicts_keyword = "toggle_dicts_keyword"


def choose_dicts(chat_id, uid=0):
    keyboard = types.InlineKeyboardMarkup()
    hello_button = types.InlineKeyboardButton(text="Назад", callback_data="start_game_save")
    keyboard.add(hello_button)

    players_button = types.InlineKeyboardButton(text="Далее", callback_data="players_settings")
    keyboard.add(players_button)

    names = user_dicts.get_dicts_names(uid)
    if names is not None:
        for i in names:
            button = types.InlineKeyboardButton(text=i, callback_data=toggle_dicts_keyword+i)
            keyboard.add(button)
    states.set_state(chat_id, States.CHOOSE_DICTS)

    on_dicts = Game.get_dicts(chat_id)
    msg = choose_dicts_text + '\n' + '\n'.join(['*' + i + '*' for i in on_dicts])
    msg = msg.replace('количествослов', Game.get_wordcount(chat_id))

    bot.edit_message_text(chat_id=chat_id, message_id=states.get_base(chat_id), text=msg,
                          reply_markup=keyboard, parse_mode='MARKDOWN')


def edit2rules(message):
    keyboard = types.InlineKeyboardMarkup()
    hello_button = types.InlineKeyboardButton(text="Назад", callback_data="hello")
    keyboard.add(hello_button)

    states.set_state(message.chat.id, States.RULES)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=rules_text, reply_markup=keyboard, parse_mode='MARKDOWN')


add_words_keyword = "add_words"


def exist_dics(chat_id, uid=0):
    keyboard = types.InlineKeyboardMarkup()
    hello_button = types.InlineKeyboardButton(text="Назад", callback_data="hello")
    keyboard.add(hello_button)

    names = user_dicts.get_dicts_names(uid)
    if names is not None:
        for i in names:
            button = types.InlineKeyboardButton(text=i, callback_data=add_words_keyword+i)
            keyboard.add(button)
    states.set_state(chat_id, States.EXISTING)

    bot.edit_message_text(chat_id=chat_id, message_id=states.get_base(chat_id), text=exist_dics_text,
                          reply_markup=keyboard, parse_mode='MARKDOWN')


rem_word_keyword = "remwordkeyword"


def process_dict(chat_id, uid=0, dict_name=""):
    user_dicts.set_dict(uid, dict_name)

    keyboard = types.InlineKeyboardMarkup()
    hello_button = types.InlineKeyboardButton(text="Назад", callback_data="exist_dics")
    keyboard.add(hello_button)
    rem_button = types.InlineKeyboardButton(text="Удалить словарь", callback_data="rem_dict")
    keyboard.add(rem_button)

    names = user_dicts.get_words(uid, dict_name)
    if names is not None:
        for i in names:
            button = types.InlineKeyboardButton(text=i, callback_data=rem_word_keyword + dict_name + '_' + i)
            keyboard.add(button)
    states.set_state(chat_id, States.PROCESS)

    bot.edit_message_text(chat_id=chat_id, message_id=states.get_base(chat_id), text=process_dict_text,
                          reply_markup=keyboard, parse_mode='MARKDOWN')


def rem_dict(message, uid):
    user_dicts.rem_dict(uid, user_dicts.get_current_dict(uid))
    exist_dics(message.chat.id, uid)


rem_user_keyword = "rem_user_keyword"


def process_users(chat_id, error_message="", new_size = -1):
    keyboard = types.InlineKeyboardMarkup()
    hello_button = types.InlineKeyboardButton(text="Назад", callback_data="choose_dicts")
    keyboard.add(hello_button)

    begin_button = types.InlineKeyboardButton(text="Начать", callback_data="begin_game")
    keyboard.add(begin_button)

    shuffle_button = types.InlineKeyboardButton(text="Перемешать игроков", callback_data="shuffle_players")
    keyboard.add(shuffle_button)

    users = Game.get_players(chat_id)
    if users is not None:
        for i in users:
            button = types.InlineKeyboardButton(text=i, callback_data=rem_user_keyword + i)
            keyboard.add(button)
    states.set_state(chat_id, States.PROCESS_USERS)

    bot.edit_message_text(chat_id=chat_id, message_id=states.get_base(chat_id), text=process_users_text + Game.get_users_text(chat_id) + error_message,
                          reply_markup=keyboard, parse_mode='MARKDOWN')



def show_game_screen(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    hello_button = types.InlineKeyboardButton(text="Закончить игру", callback_data="hello")
    keyboard.add(hello_button)

    if Game.get_hat_words(chat_id) != 0:
        begin_button = types.InlineKeyboardButton(text="Начать обЪяснение", callback_data="explain")
        keyboard.add(begin_button)

    stats_button = types.InlineKeyboardButton(text="Статистика", callback_data="stats")
    keyboard.add(stats_button)


    states.set_state(chat_id, States.MAIN_GAME_SCR)
    msg = main_game_screen + Game.get_cur_pair(chat_id) + '\n' + Game.get_hat_words_message(chat_id)

    if Game.get_hat_words(chat_id) == 0:
        msg = main_game_screen + '\n' + Game.get_hat_words_message(chat_id)

    bot.edit_message_text(chat_id=chat_id, message_id=states.get_base(chat_id), text=msg,
                          reply_markup=keyboard, parse_mode='MARKDOWN')


def show_explanation_screen(chat_id):
    keyboard = types.InlineKeyboardMarkup()

    states.set_state(chat_id, States.EXPLANATION_SCREEN)
    msg = Game.get_hat_words_message(chat_id) + '\n\n' + Game.set_word(chat_id)

    conceed_button = types.InlineKeyboardButton(text="Сдаться", callback_data="conceed")
    keyboard.add(conceed_button)

    error_button = types.InlineKeyboardButton(text="Ошибка", callback_data="error")
    keyboard.add(error_button)

    stats_button = types.InlineKeyboardButton(text="Угадано", callback_data="accepted")
    keyboard.add(stats_button)

    bot.edit_message_text(chat_id=chat_id, message_id=states.get_base(chat_id), text=msg,
                          reply_markup=keyboard, parse_mode='MARKDOWN')


def show_stats(chat_id):
    keyboard = types.InlineKeyboardMarkup()

    states.set_state(chat_id, States.EXPLANATION_SCREEN)
    msg = stats_msg + '\n' + Game.get_stats(chat_id) + '\n' + Game.get_hat_words_message(chat_id)

    back_button = types.InlineKeyboardButton(text="Назад", callback_data="stats_back")
    keyboard.add(back_button)

    bot.edit_message_text(chat_id=chat_id, message_id=states.get_base(chat_id), text=msg,
                          reply_markup=keyboard, parse_mode='MARKDOWN')



@bot.message_handler(func=lambda message: states.get_current_state(message.chat.id) == States.EXISTING)
def existing_dict(message):
    dict_name = message.text
    user_id = message.from_user.id

    user_dicts.add_dict(message.from_user.id, dict_name)
    bot.delete_message(message.chat.id, message.message_id)


    try:
        exist_dics(message.chat.id, user_id)
    except:
        pass

@bot.message_handler(func=lambda message: states.get_current_state(message.chat.id) == States.PROCESS)
def entering_dict(message):
    new_words = message.text.split()
    user_id = message.from_user.id
    user_dicts.add_words(user_id, user_dicts.get_current_dict(user_id), new_words)
    bot.delete_message(message.chat.id, message.message_id)

    try:
        process_dict(message.chat.id, user_id, user_dicts.get_current_dict(user_id))
    except:
        pass

@bot.message_handler(func=lambda message: states.get_current_state(message.chat.id) == States.BASIC_GAME_SET)
def change_duration(message):
    new_dur = message.text
    chat_id = message.chat.id
    bot.delete_message(message.chat.id, message.message_id)

    try:
        Game.set_duration(chat_id, new_dur)
        game_start(chat_id, False)
    except:
        pass

@bot.message_handler(func=lambda message: states.get_current_state(message.chat.id) == States.CHOOSE_DICTS)
def change_word_count(message):
    new_cnt = message.text
    chat_id = message.chat.id
    bot.delete_message(message.chat.id, message.message_id)

    try:
        Game.set_wordcount(chat_id, new_cnt)
        choose_dicts(message.chat.id, message.from_user.id)
    except:
        pass


@bot.message_handler(func=lambda message: states.get_current_state(message.chat.id) == States.PROCESS_USERS)
def add_user(message):
    user_name = message.text
    chat_id = message.chat.id
    bot.delete_message(message.chat.id, message.message_id)

    try:
        Game.add_player(chat_id, user_name)
        process_users(chat_id)
    except:
        pass

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    uid = call.from_user.id
    if call.message:
        if call.data == "hello":
            edit2start(call.message)
        if call.data == "rules":
            edit2rules(call.message)
        if call.data == "exist_dics":
            exist_dics(call.message.chat.id, uid)
        if call.data == "rem_dict":
            rem_dict(call.message, uid)
        if call.data == "start_game":
            game_start(call.message.chat.id)
        if call.data == "start_game_save":
            game_start(call.message.chat.id, False)
        if call.data == "choose_dicts":
            try:
                choose_dicts(call.message.chat.id, uid)
            except:
                pass
        if call.data == "stats":
            show_stats(call.message.chat.id)

        if call.data == "stats_back":
            show_game_screen(call.message.chat.id)
        if call.data == "explain":
            show_explanation_screen(call.message.chat.id)
        if call.data == "conceed":
            Game.next_pair(call.message.chat.id)
            show_game_screen(call.message.chat.id)
        if call.data == "accepted":
            Game.remove_word(call.message.chat.id)
            Game.add_stats(call.message.chat.id)
            if Game.get_hat_words(call.message.chat.id) == 0:
                show_game_screen(call.message.chat.id)
            else:
                show_explanation_screen(call.message.chat.id)

        if call.data == "error":
            Game.remove_word(call.message.chat.id)
            Game.next_pair(call.message.chat.id)
            show_game_screen(call.message.chat.id)

        if call.data == "toggle_multi_mode":
            Game.set_mode(call.message.chat.id, 0)
            try:
                game_start(call.message.chat.id, False)
            except:
                pass
        if call.data == "toggle_pair_mode":
            Game.set_mode(call.message.chat.id, 1)
            try:
                game_start(call.message.chat.id, False)
            except:
                pass
        if call.data == "players_settings":
            process_users(call.message.chat.id)


        if call.data == "begin_game":
            try:
                res = Game.start_game(call.message.chat.id)
                if res[0] != "good":
                    print(res)
                    process_users(call.message.chat.id, res[1])
                else:
                    show_game_screen(call.message.chat.id)
            except:
                pass

        if call.data == "shuffle_players":
            try:
                Game.shuffle_players(call.message.chat.id)
                process_users(call.message.chat.id)
            except:
                pass

        try:
            if call.data[:len(add_words_keyword)] == add_words_keyword:
                dict_name = call.data[len(add_words_keyword):]
                process_dict(call.message.chat.id, uid, dict_name)
            if call.data[:len(rem_word_keyword)] == rem_word_keyword:
                dict_name, word = call.data[len(rem_word_keyword):].split('_')
                user_dicts.rem_word(uid, dict_name, word)
                process_dict(call.message.chat.id, uid, dict_name)

            if call.data[:len(toggle_dicts_keyword)] == toggle_dicts_keyword:
                dict_name = call.data[len(toggle_dicts_keyword):]
                Game.toggle_dicts(call.message.chat.id, dict_name, uid)
                try:
                    choose_dicts(call.message.chat.id, uid)
                except:
                    pass

            if call.data[:len(rem_user_keyword)] == rem_user_keyword:
                user_name = call.data[len(rem_user_keyword):]
                Game.rem_player(call.message.chat.id, user_name)
                try:
                    process_users(call.message.chat.id)
                except:
                    pass
        except:
            pass


bot.infinity_polling()
