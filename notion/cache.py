import threading

import cachetools
from notion_client import Client

from functions.console import log

# Global variables
cache = cachetools.TTLCache(maxsize=200, ttl=600)
fetch_lock = threading.Lock()


def fetch_data_from_notion(
        notion: Client,
        database_id: str,
        filter_params=None):
    """Fetch data from Notion API."""
    all_data = []
    has_more = True
    start_cursor = None

    while has_more:
        database_data = notion.databases.query(
            database_id,
            filter=filter_params,
            start_cursor=start_cursor,
            page_size=100)

        results = database_data["results"]  # type: ignore
        next_cursor = database_data["next_cursor"] or None  # type: ignore

        all_data.extend(results)

        if next_cursor:
            log("fetching next page...", "info")
            start_cursor = next_cursor
        else:
            has_more = False

    return {"results": all_data}


def get_database_data(
        notion: Client,
        database_id: str,
        filter_params=None) -> dict:
    """
    Get data from the cache. If not available, fetch it from Notion API.

    Args:
    notion: notion_client.Client instance.
    database_id: Notion database id.
    filter_params: Filter parameters for the notion query (default is None).

    Returns:
    A dictionary containing the fetched data.
    """
    cache_key = f"{database_id}"
    while True:
        try:
            # If the data is in the cache, return it
            return cache[cache_key]
        except KeyError:
            # Try to acquire the lock to fetch data from Notion API
            with fetch_lock:
                # Check the cache again after acquiring the lock
                if cache_key in cache:
                    return cache[cache_key]

                # If the data is not in the cache, fetch it and store it in the
                # cache
                log("Fetching data from Notion API...", "info")
                cache[cache_key] = fetch_data_from_notion(
                    notion, database_id, filter_params)

                return cache[cache_key]
