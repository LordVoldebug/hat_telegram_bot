start_text = '''*Для чего этот бот?*

Этот бот представляет собой удобный интерфейс для игры в шляпу. 
Сейчас вы находитесь в режиме локальной игры.

Подерживается режим игры в чате (для этого необходимо добавить бот в чат). ***(в разработке)***
'''
rules_text = ''' *Правила игры*

Шляпа - игра для компании. Цель игры – за ограниченное время объяснить партнёру или команде как можно больше слов вытянутых из шляпы. В игре в шляпу участвуют две или несколько пар игроков.

Перед стартом каждого кона засекается время - оно будет на экране. Одному из игроков команды на экране показыватеся слово которое он должен объяснить.

При объяснении нельзя:

1. Использовать однокоренные слова
2. Называть переводы слова на иностранных языках
3. Использовать жесты (в том числе показывать на предметы)
4. Называть напрямую слова, похожие по звучанию (например, если вы объясняете слово «этюд» и решили объяснить его как «музыкальное произведение, похожее на «утюг», то в таком случае сначала вам нужно объяснить слово «утюг»)

Партнер выдвигает версии того, какое слово написано на карточке. Если он угадал написанное слово, то команде присуждется очко и первый игрок переходит к объяснению следующего слова в шляпе. Кон длится, пока не закончится время. Если время закончилось, а слово осталось неотгаданным, то слово возвращается в "шляпу".

Имя следующего игрока и того, кому он объясняет слова показывается на экране. 

Игра заканчивается, когда в шляпе не остается бумажек. Победителем становится команда, отгадавшая больше слов.

Также существует версия в которой каждый игрок играет сам за себя и игроки объясняют друг другу каждый каждому.
'''

exist_dics_text = ''' *Список словарей*

Для удаления словоря выберете словарь и соответствующий пункт в меню.
Введите название чтобы создать новый словарь. Добавление словаря, с названием уже имеющегося в библиотеке ни к чему не привидет.
'''

process_dict_text = '''*Работа со словарём*

В этом разделе можно добавлять или удалять слова.
Чтобы добавить одно или несколько слов, пошлите их боту набранные через пробел.
Чтобы удалить слово нажмите на него в списке слов. Чтобы увидеть новые слова нажмите обновить.
Уже имеющеся в словаре слова добавлены не будут.
'''
start_game_text = '''*Начало игры.*

Выбранный режим игры: *режимигры*. Для изменения режима игры выберете соответсвующий режим в списке.

Длительность хода (в секундах): *длительностьхода*. Для изменения длительности пошлите в чат целое число от 1 до 120 - новую длительность. 
'''
choose_dicts_text = ''' *Выбор словарей*

Для выбора/отмены выбора словаря выберете название словаря в меня.

Количество слов в шляпе: *количествослов*. Для изменения количества слов пошлите сообщения с новым количеством в чат
(количество слов должно лежать в пределах от 1 до 1000). Если сумаррный размер словарей меньше обозначенного числа, 
шляпа будет автоматически уменьшена.

Выбранные словари:
'''

process_users_text = '''*Игроки*

Для добавления пользователя пошлите сообщение с его именем. Для удаления пользователя выберете его имя в меню.
Для начала игры нажмите Начать.

'''

pair_text = ''' При удалении пользователя из пары пользователи циклически сдвигаются на один вверх. При добавлении пользователя 
он добавляется в конец списка.
 
*Пары игроков*

'''

odd_number_players_error = '''

*Ошибка:*

Нечётное количество игроков в партии по парам.
'''


one_player_error = '''
    
*Ошибка:*

Слишком мало игроков.
'''

main_game_screen = ''' *Игра в шляпу*
'''

stats_msg = '''*Статистика.*

*Для каждого игрока: (объяснено/угадано).*

'''