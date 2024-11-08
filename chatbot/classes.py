"""Data models."""

from dataclasses import dataclass

from discord.app_commands import Choice

CATEGORIES: list[Choice] = [
    Choice(name="Cryptography", value="crypto"),
    Choice(name="Dev/IA", value="dev"),
    Choice(name="Forensics", value="forensics"),
    Choice(name="Hardware", value="hardware"),
    Choice(name="Miscellaneous", value="misc"),
    Choice(name="OSINT", value="osint"),
    Choice(name="Pwn", value="pwn"),
    Choice(name="Reverse", value="reverse"),
    Choice(name="System", value="system"),
    Choice(name="Web", value="web"),
    Choice(name="Web3", value="web3"),
]


class Category:
    """Class defining a challenge or resource's category.

    Attributes
    ----------
    name : str
        The category's name.

    """

    name: str


@dataclass
class Resource:
    """Class defining a resource's link.

    Attributes
    ----------
    url : str
        The URL.
    category_id : int
        The category's ID in database.

    """

    url: str
    category_id: int
