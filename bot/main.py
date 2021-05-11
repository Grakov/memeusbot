import sys
import logging
import random
import os
import shutil

from elasticsearch import Elasticsearch
import telebot
from telebot import types

import settings
from settings import construct_url

from bot.search import MemeSearch

bot = telebot.TeleBot(settings.BOT_TOKEN, parse_mode=None)
if settings.DEBUG:
    telebot.logger.setLevel(logging.DEBUG)

index_html_path = os.path.join(settings.STATIC_LOCAL_FOLDER, 'index.html')
if not os.path.exists(index_html_path):
    shutil.copy2(os.path.join('../crawler/www', 'index.html'), index_html_path)

es = Elasticsearch([{'host': settings.ES_HOST, 'port': settings.ES_PORT}])

sad_emojis = ['😔', '👀', '🕵️‍♂️', '🦸‍♂️', '🎲', '🔎', '😿', '🪂', '🌠', '☂', '💔', '❌']


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Hi, user!\n\n" +
                     "You can search memes here - I'll give you one random meme for your request.\n\n" +
                     "Or you can type @memeusbot and search for memes without limits in any chat!")


@bot.message_handler(func=lambda m: True)
def query_test(message):
    query = message.text.strip()
    if len(query) < 3:
        bot.reply_to(message, sad_emojis[len(sad_emojis) - 1] + ' Search query is too short')
    else:
        response = MemeSearch(es, index_name=settings.ES_INDEX_NAME, query_text=query,
                              max_results=settings.RESULTS_LIMIT).execute()
        if len(response) == 0:
            bot.reply_to(message, '👀 No results')
        else:
            if settings.DEBUG:
                response_text = f'*Results (total: {len(response)})*\n\n'
                result_number = 1
                for result in response:
                    if result_number > 20:
                        break
                    response_text += f"{str(result_number)} _({result.meta.score})_: [{result.original_url}](Image)\n"
                    response_text += f"{result.article_url}\n\n"
                    result_number += 1

                bot.send_message(message.chat.id, response_text, parse_mode="Markdown",
                                 reply_to_message_id=message.message_id)
            else:
                if len(response) > 20:
                    response = response[0:20]
                hit = random.choice(response)
                if settings.IS_SERVERLESS:
                    photo_url = hit.original_url
                else:
                    photo_url = construct_url(hit.id, hit.file_name)

                bot.send_photo(message.chat.id, photo_url, reply_to_message_id=message.message_id)


@bot.inline_handler(lambda query: len(query.query.strip()) > 2)
def process_query(inline_query):
    try:
        query = inline_query.query.strip()
        user = inline_query.from_user

        meme_search = MemeSearch(es, index_name=settings.ES_INDEX_NAME, query_text=query,
                                 max_results=settings.RESULTS_LIMIT)
        response = meme_search.execute()

        response_images = []

        if not meme_search.is_empty():
            hits = meme_search.hits_count()
            images_count = 0

            for hit in response:
                if settings.RESULTS_LIMIT is not None and images_count == settings.RESULTS_LIMIT:
                    break

                hit_score = hit.meta.score
                file_name = hit.file_name
                file_id = hit.id

                if settings.IS_SERVERLESS:
                    response_images.append(types.InlineQueryResultPhoto(file_id,
                                                                        hit.original_url,
                                                                        hit.original_url))
                else:
                    response_images.append(types.InlineQueryResultPhoto(file_id,
                                                                        construct_url(file_id, file_name),
                                                                        construct_url(file_id, settings.THUMBNAIL_PREFIX + file_name)))
                images_count += 1

            if settings.DEBUG:
                print(f":: Found {images_count} memes for {query}")
        else:
            if settings.DEBUG:
                print(f":: 0 results for {query}")

        if len(response_images) > 0:
            bot.answer_inline_query(inline_query.id, response_images, cache_time=1)
        else:
            message_text = f"{user.first_name} tried to send \"{query}\" meme picture"
            message_title = sad_emojis[random.randint(0, len(sad_emojis) - 1)] + " Nothing found"
            text_response = types.InlineQueryResultArticle(inline_query.id, title=message_title,
                                                           input_message_content=types.InputTextMessageContent(message_text))
            bot.answer_inline_query(inline_query.id, (text_response,), cache_time=1)
    except Exception as e:
        print(e)


while True:
    try:
        bot.polling()
    except KeyboardInterrupt:
        sys.exit()
    except telebot.apihelper.ApiTelegramException as e:
        bot.stop_polling()
        print(e)
