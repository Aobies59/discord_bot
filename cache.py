import threading
from global_variables import MEMBERS_FILENAME
import discord


members_file_lock = threading.Lock()

# members.csv has all cached members stored as ID;NAME

def is_member_cached(member_name: str = None, member_id: int = None) -> bool:
    if member_name is not None and member_id is not None:
        raise ValueError("Either member_name and member_id must be blank, cannot search with both")

    if member_id is not None:
        split_index = 0
        member_getter = str(member_id)
    elif member_name is not None:
        split_index = 1
        member_getter = member_name.strip().lower()

    with members_file_lock:
        with open(MEMBERS_FILENAME, "r") as members_file:
            cached_members = members_file.readlines()

    for member in cached_members:
        if member_getter == member.split(';')[split_index].strip():
            return True
    return False

def get_id(member_name: str) -> int | None:
    member_name.strip()
    with members_file_lock:
        with open(MEMBERS_FILENAME, "r") as members_file:
            cached_members = members_file.readlines()
    for member in cached_members:
        split_member = member.split(';')
        if len(split_member) != 2:
            continue
        if member_name == member.split(';')[1].strip():
            return int(member.split(';')[0])
    return None

def add_member(member_name: str, member_id: int) -> int:
    if is_member_cached(member_id=member_id):
        return -1
    with members_file_lock:
        with open(MEMBERS_FILENAME, 'a') as members_file:
            members_file.write(f'{member_id};{member_name.lower()}\n')
    return 0

def cache_members(client: discord.Client) -> int:
    for member in client.get_all_members():
        add_member(member_name=member.name, member_id=member.id)  # add_member already checks if member with that id is cached
    return 0
