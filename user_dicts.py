from tinydb import TinyDB, Query

class UserDict:

    def __init__(self, dict_name):
        self.name = dict_name
        self.words = []
        self.difficulty = 50

    def add_word(self, word):
        word = word.lower()
        if word not in self.words:
            self.words.append(word)
    def to_json(self):
        return self.__dict__


user_dicts = "dicts.json"


def get_dicts_names(user_id):
    res = []
    with TinyDB(user_dicts) as db:
        qid = Query()
        user_d = db.search(qid.id == user_id)
        for item in user_d:
            res.append(item['dict']['name'])
    return sorted(res)


def add_dict(user_id, name):
    ndict = UserDict(name)
    with TinyDB(user_dicts) as db:
        qid = Query()
        user_d = db.search(qid.dict.name == name)
        if user_d is None or len(user_d) == 0:
            db.insert({"id": user_id, "dict": ndict})

def rem_dict(user_id, name):
    with TinyDB(user_dicts) as db:
        qid = Query()
        db.remove(qid.id == user_id and qid.dict.name == name)


def get_words(user_id, dict_name):
    res = []
    with TinyDB(user_dicts) as db:
        qid = Query()
        user_d = db.search(qid.id == user_id and qid.dict.name == dict_name)
        for item in user_d:
            res.extend(item['dict']['words'])
    return res


def rem_word(user_id, dict_name, word):
    with TinyDB(user_dicts) as db:
        qid = Query()
        user_d = db.search(qid.id == user_id and qid.dict.name == dict_name)
        if user_d is None or len(user_d) == 0:
            return
        tmpwords = user_d[0]['dict']['words']
        nwords = []
        for i in tmpwords:
            if i != word:
                nwords.append(i)
        user_d[0]['dict']['words'] = nwords
        db.update({'dict' : user_d[0]['dict']}, qid.id == user_id and qid.dict.name == dict_name)


def add_words(user_id, dict_name, words):
    with TinyDB(user_dicts) as db:
        qid = Query()
        user_d = db.search(qid.id == user_id and qid.dict.name == dict_name)
        if user_d is None or len(user_d) == 0:
            return
        nwords = user_d[0]['dict']['words']
        nwords.extend(words)
        nwords = sorted(list(set(nwords)))

        user_d[0]['dict']['words'] = nwords
        db.update({'dict': user_d[0]['dict']}, qid.id == user_id and qid.dict.name == dict_name)


def set_dict(user_id, value):
    with TinyDB(user_dicts) as db:
        person = Query()
        try:
            db.update({'cur_dict': value}, person.id == user_id)
            return True
        except:
            return False


def get_current_dict(user_id):
    with TinyDB(user_dicts) as db:
        person = Query()
        search = db.search(person.id == user_id)
        if len(search) != 0:
            return search[0]['cur_dict']