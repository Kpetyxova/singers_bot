import sys
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from pprint import pprint
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import markovify
scopes = ["https://www.googleapis.com/auth/youtube.readonly", 'https://www.googleapis.com/auth/youtube.force-ssl']
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_sec.json"

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
reply = ['Егор Крид', 'Дима Билан', 'Сергей Лазарев', 'Григорий Лепс', 'Тимати', 'Филипп Киркоров',
                      'Стас Михайлов', 'Валерий Меладзе', 'Ольга Бузова', 'Елена Темникова', 'Николай Басков',
                      'Баста', 'Джиган', 'Леонид Агутин', 'Вера Брежнева',
                       'Игорь Николаев', 'ЛСП', 'Элджей', 'Федук', 'Фараон', 'Бульвар Депо', 'Томас Мраз',
                      'Монеточка', 'May Waves', 'Александр Гудков', 'Леша Свик', 'Луна',
                      'Мы', 'Мальбек и Сюзанна', 'Пошлая Молли', 'СБПЧ', 'Basic Boy', 'Big Baby Tape',
                      'ЛАУД', 'Little Big', 'Mnogoznaal']
id_video = ['zWkfvuLatRE', 'MMrmkIiv-L0', 'vzlivwyggUI', '1pZhYACZkb4', '4ufRh9zEXvw', 'VcPigheMWsI', 'ABekKPp38R4', '8x6MLJuSHJg',
           'Ldb6S-eKPdQ', 'U521qbNYnQo', 'Unq0IiLCmx8', 'k1DlwC6pR0w', 'u9uzw28-59M', 'mlhfnvTmaek', 'TU8IZnQ-YdU',
           'hj_ylt0gq0Y', 'h2iSMkq9DVY', 'x0abafHIMdQ', 'dS195rBJhXM', 'l7v8DAbIOx0', 'rZSB8P6Lzj8', 'jK4Q69tN5i0',
           'wzJNIagTnIE', 'GVIyBuJ-KgY', 'GSDij1CVcN8', 'LMTXK2pIHVY', 'Q5pol9j1nDo', 'B1yIJ706i78', '2l1MkA5dSmo',
           '8o7YOiYcNbU', 'k21a-YGIeGc', '7an7SBAuDvw', 'pe3QHDbkeU4', 'wJKBSv6AjBs', 'mDFBTdToRmw', 'tds3XMt8R3E']
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("""Привет, кого из русской эстрады ты хочешь обсудить? Просто напиши мне имя и фамилию (например: Ольга Бузова) или никнейм артиста (например: Элджей)""")

def echo(update, context):
    """Echo the user message."""
    a = update.message.text
    b = reply.index(a)
    c = id_video[b]
    list_comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId = c,
        maxResults=100
    )
    response = request.execute()
    items = response.get('items', [])
    nextPageToken = response.get('nextPageToken')
    i = 0
    while i < 10:
        request = youtube.commentThreads().list(
        part="snippet",
        videoId = c,
        maxResults=100,
        pageToken = nextPageToken
        )
        response = request.execute()
        items = response.get('items', [])
        nextPageToken = response.get('nextPageToken')
        i += 1
        data = []
        for item in items:
            snippet = item.get('snippet')
            snippet2 = snippet.get('topLevelComment', {}).get('snippet', {})
            textOriginal = snippet2.get('textOriginal')
            list_comments.append(textOriginal)
    text = ' '.join(list_comments)
    m = markovify.Text(text)
    update.message.reply_text(m.make_short_sentence(100))

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)
    REQUEST_KWARGS={
    'proxy_url': 'socks5://347738780:IviFTbNi@orbtl.s5.opennetwork.cc:999',
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'username': '',
        'password': '',
        }
    }

    updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, echo))


    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
