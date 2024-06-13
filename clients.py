import discord
from utils import log, divide_string_by_first_space
import aioconsole
from global_variables import MEMBERS_FILENAME, JARRON_ID
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
        if self.__guild is None:
            log("Received incorrect guild ID")
            raise ValueError(f"Guild with ID {self.__guild_id} not found.")

        if self.__bot_channel is None:
            log("Received incorrect channel ID")
            raise ValueError(f"Channel with ID {self.__bot_channel_id} not found.")
        
        log(f"Client logged in as {self.user.name}")
        await self.run_loop()

    def get_connected_member(self, member_name: str):
        for member in self.get_all_members():
            if member.name.strip() == member_name.strip():
                return member
        return None

    @staticmethod
    def test():
        log("Test run succesfully")

    async def send(self, message):
        log(f"send - Sent '{message.replace('\n', '\t').strip()}'")
        await self.__bot_channel.send(message) 
            
    async def disconnect_member(self, member_name):
        member_to_disconnect = self.get_connected_member(member_name=member_name)
        if member_to_disconnect is None:
            log("disconnect - Attempted to disconnect member who is not connected")
        else:
            try:
                await member_to_disconnect.move_to(None)
                log(f"disconnect - Disconnected user {member_to_disconnect.name}")
            except discord.Forbidden:
                log("disconnect - Attempted to disconnect admin or other privileged member")

    async def give_role(self, role_name: str, user_name: str, color: int = 2303786):
        role_to_give = await self.__guild.create_role(name=role_name, color=discord.Color(color))
        user_id = get_id(member_name=user_name)
        if user_id is None:
            log("role - Attempting to give role to non-cached user")
            return
        user_to_give_role = await self.__guild.fetch_member(user_id)
        if user_to_give_role is None:
            log("role - Attempting to give role to non-existant user existant in cache")
            return
        await user_to_give_role.add_roles(role_to_give)
        log(f'role - Gave role {role_name} to {user_name}')

    async def run_loop(self) -> int:
        while True:
            input_text = await aioconsole.ainput("b> ")
            command, text = divide_string_by_first_space(input_text)

            try:
                if command == "test":
                    self.test()
                elif command == "send":
                    if text.strip() == "":
                        log("Attempted to send empty message")
                    else:
                        await self.send(message=text)
                elif command == "disconnect":
                    await self.disconnect_member(member_name=text)
                elif command == "role":
                    user_name, role_name = divide_string_by_first_space(text)
                    if role_name == "":
                        print("Usage: role <user_name> <role_name>")
                    else:
                        await self.give_role(role_name=role_name, user_name=user_name)
                else:
                    print(f'Unknown command "{command}"')
            except Exception as e:
                log(f"Unexpected error occurred when trying to run operation {command}: {type(e).__name__}: {e}")

    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            try:
                cache_members(self)
                log('Cached members')
            except Exception as e:
                log(f"Failed to cache members, {type(e)}: {e}")

