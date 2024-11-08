"""SQLite helpers."""

from dataclasses import astuple
from sqlite3 import Connection, Cursor
from sqlite3 import Error as SqliteError
from sqlite3 import IntegrityError, connect
from typing import Any

from rich.pretty import pretty_repr

from .classes import CATEGORIES, Resource
from .logger import programLogger

DB_CONNECTION: Connection

sql_create_categories_table: str = """
CREATE TABLE IF NOT EXISTS categories (
    id integer PRIMARY KEY,
    name text NOT NULL
);
"""

sql_create_resources_table: str = """
CREATE TABLE IF NOT EXISTS resources (
    id integer PRIMARY KEY,
    url text NOT NULL,
    category_id int,
    FOREIGN KEY (category_id) REFERENCES users (id)
);
"""


def create_categories() -> None:
    """Set categories in database."""
    cursor: Cursor = DB_CONNECTION.cursor()
    query: str = "INSERT INTO categories (name) VALUES "

    for idx, category in enumerate(CATEGORIES, start=1):
        query += f'("{category.value}")'
        if idx < len(CATEGORIES):
            query += ","

    try:
        cursor.execute(query)
        DB_CONNECTION.commit()
        programLogger.notice("Created categories.")

    except (IntegrityError, SqliteError) as err:
        programLogger.warning(f"Failed creating categories: {err}")


def create_tables() -> None:
    """Create all tables.

    Raises
    ------
    sqlite3.Error

    """
    cursor: Cursor = DB_CONNECTION.cursor()
    programLogger.debug("Creating tables ...")

    cursor.execute(sql_create_categories_table)
    cursor.execute(sql_create_resources_table)
    create_categories()


def init_db_connection(database_path: str) -> None:
    """Initialize database connection.

    Parameters
    ----------
    database_path : str
        Path to database file.

    """
    global DB_CONNECTION
    DB_CONNECTION = connect(database_path)
    create_tables()


def fetch_category(category_id: str) -> str | None:
    """Fetch category by name.

    Parameters
    ----------
    category_id : str
        The category ID.

    Returns
    -------
    str
        The object name.

    """
    cursor: Cursor = DB_CONNECTION.cursor()
    query: str = "SELECT name FROM categories WHERE id=?"

    try:
        result: Cursor = cursor.execute(query, (category_id,))
        first_result: Any | None = result.fetchone()

        if first_result:
            return str(first_result[0])

    except SqliteError as err:
        programLogger.error(f"Failed fetching category: {err}")

    return None


def fetch_category_id(category_name: str) -> int | None:
    """Fetch category by name.

    Parameters
    ----------
    category_name : str
        The category name.

    Returns
    -------
    int or None
        The ID if object was found. Otherwise, None.

    """
    cursor: Cursor = DB_CONNECTION.cursor()
    query: str = "SELECT id FROM categories WHERE name=?"

    try:
        result: Cursor = cursor.execute(query, (category_name,))
        first_result: Any | None = result.fetchone()

        if first_result:
            return int(first_result[0])

    except SqliteError as err:
        programLogger.error(f"Failed fetching category: {err}")

    return None


def fetch_all_resources() -> dict[str, list[str]]:
    """Fetch resources by category if provided.

    Returns
    -------
    list
        The object list.

    """
    cursor: Cursor = DB_CONNECTION.cursor()
    query: str = "SELECT url,category_id FROM resources"
    links: dict[str, list[str]] = {}

    try:
        result: Cursor = cursor.execute(query)

        for row in result.fetchall():
            if row[1] not in links:
                links[row[1]] = []
            links[row[1]].append(row[0])

    except SqliteError as err:
        programLogger.error(f"Failed fetching resources: {err}")

    return links


def fetch_resources(category_name: str) -> list[Any]:
    """Fetch resources by category if provided.

    Parameters
    ----------
    category_name : str
        The category name.

    Returns
    -------
    list
        The object list.

    """
    cursor: Cursor = DB_CONNECTION.cursor()

    try:
        category_id: int | None = fetch_category_id(category_name)
        query: str = "SELECT url FROM resources WHERE category_id=?"

        if not category_id:
            programLogger.error(f"No ID found for category {category_name}")

        else:
            result: Cursor = cursor.execute(query, (str(category_id),))
            return [row[0] for row in result.fetchall()]

    except SqliteError as err:
        programLogger.error(f"Failed fetching resources: {err}")

    return []


def fetch_resource(url: str, category_name: str) -> Any | None:
    """Fetch resource by URL and category.

    Parameters
    ----------
    url : str
        The URL.
    category_name : str
        The category name.

    Returns
    -------
    Any or None
        The object if found.

    """
    cursor: Cursor = DB_CONNECTION.cursor()

    try:
        category_id: int | None = fetch_category_id(category_name)
        query: str = "SELECT * FROM resources WHERE url=? AND category_id=?"

        if not category_id:
            programLogger.error(f"No ID found for category {category_name}")

        else:
            result: Cursor = cursor.execute(
                query,
                (
                    url,
                    str(category_id),
                ),
            )
            return result.fetchone()

    except SqliteError as err:
        programLogger.error(f"Failed fetching resources: {err}")

    return None


def create_resource(url: str, category: str) -> int | None:
    """Insert a new resource row.

    Parameters
    ----------
    url : str
        The URL.
    category : str
        The category name.

    Returns
    -------
    int or None
        The generated ID if object was created. Otherwise, None.

    Raises
    ------
    ValueError
        If resource already exists in database.

    """
    if fetch_resource(url, category):
        raise ValueError("Resource already exist.")

    resource_id: int | None = None
    category_id: int | None = fetch_category_id(category)

    if category_id:
        resource = Resource(url, category_id)
        query: str = "INSERT INTO resources(url,category_id) VALUES(?,?)"
        cursor: Cursor = DB_CONNECTION.cursor()

        try:
            cursor.execute(query, astuple(resource))
            DB_CONNECTION.commit()
            resource_id = cursor.lastrowid
            programLogger.notice(f"Created resource ID: {resource_id}")
            programLogger.debug(pretty_repr(resource))

        except IntegrityError as err:
            programLogger.warning(f"Failed creating resource: {err}")

        except SqliteError as err:
            programLogger.error(f"Failed creating resource: {err}")

    return resource_id
