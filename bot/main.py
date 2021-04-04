import logging
import random

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import telebot
from telebot import types

import settings
from settings import construct_url

bot = telebot.TeleBot(settings.BOT_TOKEN, parse_mode=None)
if settings.DEBUG:
    telebot.logger.setLevel(logging.DEBUG)

es = Elasticsearch([{'host': settings.ES_HOST, 'port': settings.ES_PORT}])

sad_emojis = ['😔', '👀', '🕵️‍♂️', '🦸‍♂️', '🎲', '🔎', '😿', '🪂', '🌠', '☂', '💔', '❌']


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, str(message))


'''
InlineQueryResultPhoto(id, photo_url, thumb_url[, photo_width, photo_height, title, description, caption[str], 
                       reply_markup, input_message_content, parse_mode, caption_entities, **_kwargs])
doc: https://python-telegram-bot.readthedocs.io/en/stable/telegram.inlinequeryresultphoto.html
'''


@bot.inline_handler(lambda query: len(query.query.strip()) > 2)
def process_query(inline_query):
    try:
        query = inline_query.query.strip()
        user = inline_query.from_user

        es_query = Search().index(settings.ES_INDEX_NAME).using(client=es).query("match", tags=query)
        response = es_query.execute()

        if response.success():
            print(response)
            hits = response.hits.total
            images_count = 0

            response_images = []

            for hit in response:
                if settings.RESULTS_LIMIT is not None and images_count == settings.RESULTS_LIMIT:
                    break

                hit_score = hit.meta.score
                file_name = hit.file_name
                file_id = hit.id
                '''
                response_images.append(types.InlineQueryResultPhoto(file_id,
                                                                    construct_url(file_id, file_name),
                                                                    construct_url(file_id, settings.THUMBNAIL_PREFIX + file_name)))
                '''
                response_images.append(types.InlineQueryResultPhoto(file_id,
                                                                    hit.original_url,
                                                                    hit.original_url))
                images_count += 1

        if settings.DEBUG:
            print(f":: Found {images_count} memes for {query}")

        if len(response_images) > 0:
            bot.answer_inline_query(inline_query.id, response_images, cache_time=1)
        else:
            message_text = f"{user.first_name} tried to send \"{query}\" meme picture"
            message_title = "Nothing found " + sad_emojis[random.randint(0, len(sad_emojis))]
            text_response = types.InlineQueryResultArticle(inline_query.id, title=message_title,
                                                           input_message_content=types.InputTextMessageContent(message_text))
            bot.answer_inline_query(inline_query.id, (text_response,), cache_time=1)
    except Exception as e:
        print(e)


bot.polling()
