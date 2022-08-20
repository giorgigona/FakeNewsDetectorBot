

from itertools import tee
from telethon import TelegramClient
import asyncio

api_id = '9735459'
api_hash = 'ad931188861f97483a2845c2a30c7956'
phone = '+995591708979'
username = 'ggburduli'
telegram_trusted_channels = ['nytimes', 'washingtonpost', 'guardian']
telegram_fake_channels = ['intelslava']
keywords = ['war', 'ukraine', 'russia']

client = TelegramClient('My Session', api_id, api_hash)
client.start()

async def get_data_from_telegram_channel(channels_list, file_name, limit = 100):
    for telegram_channel in channels_list:
        channel = await client.get_entity(telegram_channel)
        messages = await client.get_messages(channel, limit = limit) #pass your own args

        #then if you want to get all the messages text
        for message in messages:
            try:
                text = message.text.lower()

                if len(text) < 10:
                    continue

                for keyword in keywords:
                    if keyword in text:
                        # Open a file with access mode 'a'
                        with open(file_name, "a") as file_object:
                            file_object.write(text)
                        break

            except Exception as e:
                continue



async def main():
    await get_data_from_telegram_channel(telegram_trusted_channels, 'data/truth_sample.txt', limit=5000)
    await get_data_from_telegram_channel(telegram_fake_channels, 'data/fakes_sample.txt', limit=1000)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

