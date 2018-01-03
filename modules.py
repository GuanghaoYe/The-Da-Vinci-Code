import telepot
from telepot.delegate import per_chat_id, per_chat_id_in, create_open, pave_event_space, include_callback_query_chat_id
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, User
from pprint import pprint
import configparser
import random


class Player(telepot.helper.ChatHandler):
    def __init__(self, seed_tuple, games, players, **kwargs):
        super(Player, self).__init__(seed_tuple, **kwargs)
        # linked to Congress
        self._games = games
        self._players = players

        # by chat
        if self.id in self._players:
            self._draft_game = self._players[self.id]['_draft_game']
        else:
            self._draft_game = None

    def _default_reply(self):
        self.sender.sendMessage("你在说啥？")

    def _welcome_reply(self):
        self.sender.sendMessage("欢迎来到达芬奇密码游戏！")

    def _addGame(self, user):
        self.sender.sendMessage('由<{stater_name}>发起的游戏开始了，输入/join 参加游戏'.format(stater_name=user.username))
        return Game()

    def _join(self, user):
        self._draft_game.player_list[user.id] = dict()
        self._draft_game.player_list[user.id]['user_info'] = user

    def _print_draft_player_name(self):
        name_list = set()
        for key, value in self._draft_game.player_list.items():
            name_list.add(value['user_info'].user_name)
        names = ', '.join(str(s) for s in name_list)
        self.sender.sendMessage(names + "have joined game")

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print(content_type, chat_type, chat_id)
        print(self.id)
        pprint(msg)
        if content_type != 'text':
            self._default_reply()
            return

        content = msg['text'].strip().split(' ', 1)
        command = content[0]
        param = content[-1]
        sender_id = msg['from']['id']
        user = msg['from']
        if chat_type == 'private':
            if command == '/start':  #TODO : fix safeDict
                if self._players[sender_id] is None:
                    self._players[sender_id] = dict()
                    self._welcome_reply()
                else:
                    pass
        if content_type != 'private':
            if command[0] != '/':
                self._default_reply()
                return
            if sender_id not in self._players:
                markup = InlineKeyboardMarkup(inline_keyboard=[
                    [dict(text='Add me', url='https://t.me/DaVinciCodeBot/')]
                ])
                self.sender.sendMessage('To play the game add me first', reply_markup=markup)
            if command == '/addGame':
                if len(self._games) > 1 and self._games[-1].is_active:
                    self.sender.sendMessage('Here\'s game running')
                else:
                    self._draft_game = self._addGame(user)
            if command == '/join':
                if self._draft_game is None:
                    self.sender.sendMessage("Here's no game to join")
                else:
                    self._join(user)
                    self._print_draft_player_name()


class Game(object):
    def __init__(self):
        self.id = ''.join(random.choice('0123456789ABCDEF') for i in range(8))
        self.is_active = False
        self.player_list = dict()


class DaVinciCode(telepot.DelegatorBot):
    def __init__(self, token, players, games):
        self._games = games
        self._players = players

        super(DaVinciCode, self).__init__(token, [
            include_callback_query_chat_id(pave_event_space())(
                per_chat_id(types=['private', 'supergroup', 'group']),
                create_open,
                Player,
                self._games,
                self._players,
                timeout=200
            )
        ])
