import telepot
from telepot.delegate import per_chat_id, per_chat_id_in, create_open, pave_event_space, include_callback_query_chat_id
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from pprint import pprint
import configparser
import random


class Player(telepot.helper.ChatHandler):
    def __init__(self, seed_tuple, stats, players, **kwargs):
        super(Player, self).__init__(seed_tuple, **kwargs)
        # linked to Congress
        self._stats = stats
        self._players = players

        # by chat
        if self.id in self._players:
            self._draft_game = self._players[self.id]['_draft_game']
        else:
            self._draft_game = None

    def _default_reply(self):
        self.sender.sendMessage("你在说啥？")

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
        if command[0] != '/':
            self._default_reply()
            return
        if content_type != 'private' and sender_id not in self._players:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [dict(text='Add me', url='https://t.me/DaVinciCodeBot/')]
            ])
            self.sender.sendMessage('To play the game add me first', reply_markup=markup)


class DaVinciCode(telepot.DelegatorBot):
    def __init__(self, token, player, stat):
        self._stat = stat
        self._player = player

        super(DaVinciCode, self).__init__(token, [
            include_callback_query_chat_id(pave_event_space())(
                per_chat_id(types=['private', 'supergroup', 'group']),
                create_open,
                Player,
                self._stat,
                self._player,
                timeout=200
            )
        ])
