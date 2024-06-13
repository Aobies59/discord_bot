import discord
from utils import log, divide_string_by_first_space, clean_logs, equalize_len
import aioconsole
from global_variables import MEMBERS_FILENAME, MAIN_USER
from private_global_variables import JARRON_ID
from cache import get_id, cache_members

class ConsoleClient(discord.Client):

    def __init__(self, guild_id: int, bot_channel_id: int):
        self.__guild_id = guild_id
        self.__bot_channel_id = bot_channel_id
        self.__guild = None
        self.__bot_channel = None
        super().__init__(intents=discord.Intents.default())


    async def on_ready(self):
        
        self.__bot_channel = self.get_channel(self.__bot_channel_id)
        self.__guild = self.get_guild(self.__guild_id)

        login_command = equalize_len('login')
        if self.__guild is None:
            log('Received incorrect guild ID')
            raise ValueError(f'Guild with ID {self.__guild_id} not found.')

        if self.__bot_channel is None:
            log('Received incorrect channel ID')
            raise ValueError(f'Channel with ID {self.__bot_channel_id} not found.')
        
        log(f'Client logged in as {self.user.name}')
        await self.run_loop()

    def get_connected_member(self, member_name: str):
        for member in self.get_all_members():
            if member.name.strip() == member_name.strip():
                return member
        return None

    def test(self):
        # TODO add something to check if the bot is running properly
        return 'Passed without errors'

    async def send(self, message):
        await self.__bot_channel.send(message)
        return f'Sent message: "{message.replace('\n', '\t').strip()}"'
            
    async def disconnect_member(self, member_name):
        if member_name == '':
            member_name = MAIN_USER

        member_to_disconnect = self.get_connected_member(member_name=member_name)

        if member_to_disconnect is None:
            return 'Attempted to disconnect member who is not connected'

        try:
            await member_to_disconnect.move_to(None)
            return f'Disconnected user "{member_to_disconnect.name}"'
        except discord.Forbidden:
            return 'Attempted to disconnect admin or other privileged member'

    async def give_role(self, role_name: str, user_name: str, color: int = 2303786):
        member_id = get_id(member_name=user_name)

        if member_id is None:
            return f'Attempted to give role to non-cached member: "{user_name}"'

        user_to_give_role = await self.__guild.fetch_member(member_id)
        if user_to_give_role is None:
            return f'Attempted to give role to member in cache that does not exist: "{user_name}"'

        role_to_give = await self.__guild.create_role(name=role_name, color=discord.Color(color))
        await user_to_give_role.add_roles(role_to_give)
        
        return f'Gave role "{role_name}" to user "{user_name}"'

    async def execute_command(self, command, text):
        log_text = f'{equalize_len(command=command)} - '

        if command == 'test':
            log_text += self.test()
        elif command == 'send':
            if text.strip() == '':
                log_text += 'Attempted to send empty message'
            else:
                log_text += await self.send(message=text)
        elif command == 'disconnect':
            log_text += await self.disconnect_member(member_name=text)
        elif command == 'role':
            user_name, role_name = divide_string_by_first_space(text)
            if role_name == '':
                print('Usage: role <user_name> <role_name>')
                log_text += 'Incorrect usage of command'
            else:
                log_text += await self.give_role(role_name=role_name, user_name=user_name)
        elif command == 'cleanlogs':
            clean_logs()
            log_text += 'Logs cleaned succesfully'
        else:
            print(f'Unknown command "{command}"')
            log_text += 'Unknown command'

        log(log_text)

    async def run_loop(self) -> int:
        while True:
            input_text = await aioconsole.ainput('b> ')
            command, text = divide_string_by_first_space(input_text)

            try:
                await self.execute_command(command, text)
            except Exception as e:
                log(f'{equalize_len(command)} - Unexpected {type(e).__name__}: {e}')

    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            try:
                cache_members(self)
                log(f'{equalize_len('cache')} - Connection of member "{member.name}" triggered member caching')
            except Exception as e:
                log(f'{equalize_len('cache')} - Unexpected error {type(e)}: {e}')

