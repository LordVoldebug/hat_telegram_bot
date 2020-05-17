from tinydb import TinyDB, Query
from texts import pair_text, odd_number_players_error, one_player_error
import random
modes = ["каждый с каждым", "по парам"]


class Game:

    def __init__(self, chat_id):
        self.type = 0
        self.duration = 30
        self.word_count = 20
        self.dicts = []
        self.words = []
        self.usedwords = []
        self.players = []
        self.chat_id = chat_id
        self.pairs_play = []
        self.cur_pair = 0
        self.cur_word = ""
        self.explained = dict()
        self.guessed = dict()


game_id = "game_by_chat_id.json"



def create_game(chat_id):
    with TinyDB(game_id) as db:
        game = Query()
        db.remove(game.chat_id == chat_id)
        db.insert(Game(chat_id).__dict__)


def set_mode(chat_id, value):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            db.update({'type': value}, game.chat_id == chat_id)
            return True
        except:
            return False


def get_mode(chat_id):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            if len(search) != 0:
                return modes[search[0]['type']]
            return True
        except:
            return False


def set_duration(chat_id, value):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            value = int(value)
            if 1 <= value <= 120:
                db.update({'duration': value}, game.chat_id == chat_id)
            return True
        except:
            return False


def get_duration(chat_id):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            if len(search) != 0:
                return str(search[0]['duration'])
            return True
        except:
            return False



def set_wordcount(chat_id, value):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            value = int(value)
            if 1 <= value <= 1000:
                db.update({'word_count': value}, game.chat_id == chat_id)
            return True
        except:
            return False


def get_wordcount(chat_id):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            if len(search) != 0:
                return str(search[0]['word_count'])
            return True
        except:
            return False


def get_dicts(chat_id):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            if len(search) != 0:
                dcts = sorted([i['name'] for i in search[0]['dicts']])
                return dcts
            return True
        except:
            return False


def toggle_dicts(chat_id, value, uid):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            if len(search) != 0:
                dicts = set([tuple(sorted(list(i.items())))  for i in search[0]['dicts']])
                dict_val = tuple(sorted({"name": value, "user_id": uid}.items()))
                if dict_val in dicts:
                    dicts.remove(dict_val)
                else:
                    dicts.add(dict_val)
                dicts = [dict(i) for i in dicts]
                db.update({'dicts': dicts}, game.chat_id == chat_id)
            return True
        except:
            return False



def get_players(chat_id):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            if len(search) != 0:
                return search[0]['players']
            return True
        except:
            return False

def add_player(chat_id, name):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            if len(search) != 0:
                players = search[0]['players']
                if name not in players:
                    players.append(name)
                db.update({'players': players}, game.chat_id == chat_id)
            return True
        except:
            return False


def rem_player(chat_id, name):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            if len(search) != 0:
                players = search[0]['players']
                nplayers = []
                for i in players:
                    if i != name:
                        nplayers.append(i)
                db.update({'players': nplayers}, game.chat_id == chat_id)
            return True
        except:
            return False

def shuffle_players(chat_id):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            if len(search) != 0:
                players = search[0]['players']
                random.shuffle(players)
                db.update({'players': players}, game.chat_id == chat_id)
            return True
        except:
            return False


def get_users_text(chat_id):
    if get_mode(chat_id) == modes[1]:

        text = pair_text
        players = get_players(chat_id)
        for i in range(len(players) // 2):
            text += '\n'
            text += players[i * 2] + ' - ' + players[i * 2 + 1]
        if len(players) % 2 == 1:
            text += '\n'
            text += players[-1] + ' - ?'
        return text

        pass
    else:
        text = "*Игроки:*\n"
        players = get_players(chat_id)
        for i in players:
            text += '\n'
            text += i
        return text


user_dicts = "dicts.json"


def start_game(chat_id):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            if len(search) != 0:
                dicts = search[0]['dicts']
                words = []
                with TinyDB(user_dicts) as dicts_db:
                    for dct in dicts:
                        qid = Query()
                        user_d = dicts_db.search(qid.id == dct['user_id'] and qid.dict.name == dct['name'])
                        for item in user_d:
                            words.extend(item['dict']['words'])
                words = list(set(words))
                random.shuffle(words)
                db.update({'word_count': min(search[0]['word_count'], len(words))}, game.chat_id == chat_id)

                if len(search[0]['players']) % 2 == 1 and search[0]['type'] == 1:
                    return ("odd_number_players_error", odd_number_players_error)
                if len(search[0]['players']) < 2:
                    return ("one_player_error", one_player_error)

                db.update({'words': words[:search[0]['word_count']]}, game.chat_id == chat_id)
                db.update({'usedwords': []}, game.chat_id == chat_id)

                pairs_play = []

                if search[0]['type'] == 1:
                    us = search[0]['players']
                    for i in range(len(us) // 2):
                        pairs_play.append((us[i * 2], us[i * 2 + 1]))
                    for i in range(len(us) // 2):
                        pairs_play.append((us[i * 2 + 1], us[i * 2]))
                else:
                    us = search[0]['players']
                    for i in range(1, len(us)):
                        for one in range(len(us)):
                            pairs_play.append((us[one], us[(one + i) % len(us)]))
                db.update({'pairs_play': pairs_play}, game.chat_id == chat_id)
                db.update({'cur_pair': 0}, game.chat_id == chat_id)

                explained = dict()
                guessed = dict()
                for i in us:
                    explained[i] = guessed[i] = 0

                db.update({'explained': explained}, game.chat_id == chat_id)
                db.update({'guessed': guessed}, game.chat_id == chat_id)


                return ("good", "")
        except:
            return ("", "")


def get_cur_pair(chat_id):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            if len(search) != 0:
                players_pairs = search[0]['pairs_play']
                cur = search[0]['cur_pair']
                cur_pair =  players_pairs[cur % len(players_pairs)]
                text = "\n*Объясняет:* \n\n" + cur_pair[0] + "\n\n*Угадывает:*\n\n" + cur_pair[1]
                return text
        except:
            return False

def get_hat_words(chat_id):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            if len(search) != 0:
                return len(search[0]['words'])
        except:
            return False


def get_hat_words_message(chat_id):
    try:
        return "\n*Cлов в шляпе:* " + str(get_hat_words(chat_id))
    except:
        return ""


def set_word(chat_id):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            word = random.choice(search[0]['words'])
            db.update({'cur_word': word}, game.chat_id == chat_id)
            return word
        except:
            return ""


def next_pair(chat_id):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            cur_pair = search[0]['cur_pair'] + 1
            db.update({'cur_pair': cur_pair}, game.chat_id == chat_id)
        except:
            return ""

def remove_word(chat_id):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            cur_word = search[0]['cur_word']
            words = search[0]['words']
            nwords = []
            usedwords = search[0]['usedwords']
            usedwords.append(cur_word)
            for i in words:
                if i != cur_word:
                    nwords.append(i)
            db.update({'cur_word': ""}, game.chat_id == chat_id)
            db.update({'usedwords': usedwords}, game.chat_id == chat_id)
            db.update({'words': nwords}, game.chat_id == chat_id)

        except:
            return ""


def add_stats(chat_id):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            if len(search) != 0:
                players_pairs = search[0]['pairs_play']
                cur = search[0]['cur_pair']
                cur_pair = players_pairs[cur % len(players_pairs)]
                explained = search[0]['explained']
                guessed = search[0]['guessed']
                explained[cur_pair[0]] = explained[cur_pair[0]] + 1
                guessed[cur_pair[1]] = guessed[cur_pair[1]] + 1
                db.update({'explained': explained}, game.chat_id == chat_id)
                db.update({'guessed': guessed}, game.chat_id == chat_id)

        except:
            return False

def get_stats(chat_id):
    with TinyDB(game_id) as db:
        game = Query()
        try:
            search = db.search(game.chat_id == chat_id)
            if len(search) != 0:
                players = search[0]['players']
                explained = dict(search[0]['explained'])
                guessed = dict(search[0]['guessed'])
                players.sort(key=lambda i: -(explained[i] + guessed[i]))
                text = ''
                cnt = 1
                length = max([len(i) for i in players]) + 2
                for i in players:
                    if i not in explained:
                        explained[i] = 0
                    if i not in guessed:
                        guessed[i] = 0
                    text += "*" + i + ":*" + " " * (length - len(i)) * 2 + str(explained[i] + guessed[i]) + " (" + str(explained[i]) + "/" + str(guessed[i]) + ')\n'
                    cnt += 1
                if search[0]['type'] == 1:
                    text += '\n'
                    text += '*Рейтинг пар*\n\n'
                    pairs = search[0]['pairs_play']
                    pairs = pairs[:len(pairs) // 2]
                    pairs_output = []
                    max_leng = 0
                    for i in pairs:
                        name = '*' +  i[0] + ' - ' + i[1] + '*'
                        max_leng = max(max_leng, len(name))
                        score = explained[i[0]] + explained[i[1]]
                        pairs_output.append((score, name))
                    max_leng += 4
                    pairs_output.sort(reverse=True)
                    for i in pairs_output:
                        text += i[1] + " " * (max_leng - len(i[1])) * 2 + str(i[0]) + '\n'
                return text


        except:
            return ''
