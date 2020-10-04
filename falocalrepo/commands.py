from os import get_terminal_size
from os.path import isdir
from shutil import move
from sqlite3 import Connection
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from faapi import Journal
from faapi import Sub
from falocalrepo_database import write_setting
from requests import get as req_get


def latest_version(version: str, package: str) -> str:
    try:
        res = req_get(f"https://pypi.org/pypi/{package}/json")
        if not res.ok:
            return ""
        else:
            return res.json()["info"]["version"]
    except (Exception, BaseException):
        return ""


def move_files_folder(db: Connection, folder_old: str, folder_new: str):
    write_setting(db, "FILESFOLDER", folder_new)
    if isdir(folder_old):
        print("Moving files to new location... ", end="", flush=True)
        move(folder_old, folder_new)
        print("Done")


def make_journal(id_: Union[int, str], author: str,
                 title: str, date: str, content: str = ""
                 ) -> Journal:
    assert isinstance(id_, int) or (isinstance(id_, str) and id_.isdigit())
    assert int(id_) > 0
    assert isinstance(author, str) and author
    assert isinstance(title, str) and title
    assert isinstance(date, str) and date
    assert isinstance(content, str)

    journal = Journal()

    journal.id = int(id_)
    journal.author = author
    journal.title = title
    journal.date = date
    journal.content = content

    return journal


def make_submission(id_: Union[int, str], author: str, title: str,
                    date: str, category: str, species: str,
                    gender: str, rating: str, tags: str = "",
                    description: str = "", file_url: str = "",
                    file_local_url: str = ""
                    ) -> Tuple[Sub, Optional[bytes]]:
    assert isinstance(id_, int) or (isinstance(id_, str) and id_.isdigit())
    assert int(id_) > 0
    assert isinstance(author, str) and author
    assert isinstance(title, str) and title
    assert isinstance(date, str) and date
    assert isinstance(category, str) and category
    assert isinstance(species, str) and species
    assert isinstance(gender, str) and gender
    assert isinstance(rating, str) and rating
    assert isinstance(tags, str)
    assert isinstance(description, str)
    assert isinstance(file_url, str)
    assert isinstance(file_local_url, str)

    sub: Sub = Sub()
    sub_file: Optional[bytes] = None

    sub.id = int(id_)
    sub.title = title
    sub.author = author
    sub.date = date
    sub.tags = list(filter(bool, map(str.strip, tags.split(","))))
    sub.category = category
    sub.species = species
    sub.gender = gender
    sub.rating = rating
    sub.description = description
    sub.file_url = file_url

    if file_local_url:
        with open(file_local_url, "rb") as f:
            sub_file = f.read()

    return sub, sub_file


def print_items(subs: List[tuple], indexes: Dict[str, int]):
    space_id: int = 10
    space_user: int = 10
    space_date: int = 10
    space_term: int = 10000
    try:
        space_term = get_terminal_size()[0]
    except IOError:
        pass

    index_id: int = indexes["ID"]
    index_user: int = indexes["AUTHOR"]
    index_date: int = indexes["UDATE"]
    index_title: int = indexes["TITLE"]

    print(f"{'ID':^{space_id}} | {'User':^{space_user}} | {'Date':^{space_date}} | Title")
    for sub in subs:
        print(
            f"{str(sub[index_id])[:space_id].zfill(space_id)} | " +
            f"{sub[index_user][:space_user]:<{space_user}} | " +
            f"{sub[index_date][:space_date]:<{space_date}} | " +
            sub[index_title][:(space_term - space_id - space_user - space_date - 10)]
        )
