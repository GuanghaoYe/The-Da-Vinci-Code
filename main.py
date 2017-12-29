from TOKEN import TOKEN
import telepot
import logging
import sys
import time
from pprint import pprint
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from modules import DaVinciCode

player = telepot.helper.SafeDict()
bot = telepot.Bot(TOKEN)
# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.debug(bot.getMe())
pprint(bot.getMe())
bot = DaVinciCode(TOKEN, [], player)
MessageLoop(bot).run_as_thread()
while 1:
    time.sleep(10)
