#!/bin/python
import asyncio
from clients import ConsoleClient
from global_variables import TOKEN_FILENAME, BOT_CHANNEL_ID
from utils import init_logs, log


def read_token_file():
    with open(TOKEN_FILENAME, "r") as TOKEN_file:
        token = TOKEN_file.read()
    return token


async def main():
    init_logs()
    console_client = ConsoleClient(BOT_CHANNEL_ID)
    token = read_token_file()
    try:
        await console_client.start(token)
    except KeyboardInterrupt:
        await console_client.close()
    finally:
        await console_client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log("Client stopped manually")
        print("\nBye!")
