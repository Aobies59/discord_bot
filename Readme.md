# Discord bot

Pretty simple bot for testing purposes. It can be controlled from the terminal for some basic commands.

#### What's needed:

> All global variables are stored in *global_variables.py*

- To clone this repository:
```bash
git clone https://github.com/Aobies59/discord_bot
```
- A discord bot token, to be stored in *token.txt*
- The id of the discord server the bot will run in, to be stored in `JARRON_ID` (don't ask why)
- The id of the bot channel in that discord server, to be stored in `BOT_CHANNEL_ID`. The bot will send messages in that channel.
- A logs folder, whose name must be stored in `LOGS_FOLDERNAME` (default is *logs*)
- A file to store member info, whose name must be stored in `MEMBERS_FILENAME` (default is *members.csv*)

#### Getting started:

Once you have everything in **#What's needed**, you only need the following code to start running the bot in your server:

```python
#!/bin/python
import asyncio
from clients import ConsoleClient
from global_variables import JARRON_ID, TOKEN_FILENAME, BOT_CHANNEL_ID
from utils import init_logs, log

# optional, you can just give the token as a parameter to console_client.start
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
    finally:
        await console_client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log("Client stopped manually")
        print("\nBye!")

```

#### But what does it do?:

Right now the functionality of the bot is pretty limited. It can:

> See *#Commands* for info in how to trigger some of these functions

- Automatically cache every member that connects to a voice channel in `MEMBERS_FILENAME`
- Send messages to the bot channel
- Create a role and give it to a user (*user must be cached*)
- Disconnect a user from any voice channel (*user must be connected to a voice channel*)
- Generate log files and log every action made

I am planning on adding the following:

- [ ] A counting minigame in a specific channel
- [ ] Some way to play music with some random API (*maybe*, probably wont get to it ever)
- [ ] More controls with commands

#### Commands

- Send *message* in the bot channel
```bash
send <message>
```
> Any command that asks for *user* is asking for their username
- Disconnect *user* from any voice channel it is connected to
```bash
disconnect <user>
```
- Create *role* and give it to *user*
> Right now the role will always be black, maybe someday I will make it so custom colors can be assigned
```bash
role <user> <role>
```
> User must be cached, so it must have been connected to a voice channel at least once while the bot was running