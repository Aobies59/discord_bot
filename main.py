#!/bin/python
import asyncio
from client import ConsoleClient
from global_variables import TOKEN_FILENAME
from private_global_variables import JARRON_ID, BOT_CHANNEL_ID
from utils import init_logs, log


def read_token():
    with open(TOKEN_FILENAME, 'r') as token_file:
        token = token_file.read()
    return token


async def main():
    init_logs()
    console_client = ConsoleClient(guild_id=JARRON_ID, bot_channel_id=BOT_CHANNEL_ID)
    token = read_token()
    try:
        await console_client.start(token)
    except KeyboardInterrupt:
        await console_client.close()
    except Exception as e:
        await console_client.close()
        log(f'Client stopped by unexpected {type(e).__name__}: {e}')
    finally:
        await console_client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log("Client stopped manually")
        print("\nBye!")
