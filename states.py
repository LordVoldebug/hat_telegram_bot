from tinydb import TinyDB, Query
state_by_chat_id = "state_by_chat_id.json"

class States:
    START = 0
    RULES = 1
    MANAGE = 2
    EXISTING = 3
    PROCESS = 4
    BASIC_GAME_SET = 5
    CHOOSE_DICTS = 6
    PROCESS_USERS = 7
    MAIN_GAME_SCR = 8
    EXPLANATION_SCREEN = 9
    STATS = 10


def set_state(chat_id, value):
    with TinyDB(state_by_chat_id) as db:
        person = Query()
        try:
            db.update({'state': value}, person.id == chat_id)
        except:
            db.insert({'id': chat_id, 'state': States.START})


def get_current_state(chat_id):
    with TinyDB(state_by_chat_id) as db:
        person = Query()
        search = db.search(person.id == chat_id)
        if len(search) != 0:
            return search[0]['state']
        else:
            db.insert({'id': chat_id, 'state': States.START})


def set_base(chat_id, mes_id):
    with TinyDB(state_by_chat_id) as db:
        person = Query()
        try:
            db.update({'mes_id': mes_id}, person.id == chat_id)
        except:
            db.insert({'mes_id': mes_id, 'state': States.START})


def get_base(chat_id):
    with TinyDB(state_by_chat_id) as db:
        person = Query()
        search = db.search(person.id == chat_id)
        if len(search) != 0:
            return search[0]['mes_id']
        else:
            return None