import asyncio
import aiohttp
import requests


async def fetch(urls: list[str], headers: dict = None, timeout: int = 5):
    timeout_setting = aiohttp.ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(timeout=timeout_setting) as session:
        tasks = [fetch_data(session, url, headers) for url in urls]
        return await asyncio.gather(*tasks)


async def fetch_data(session, url, headers):
    try:
        async with session.get(url, headers=headers) as response:
            return await response.json()
    except asyncio.TimeoutError:
        print("error", f"Timeout occurred for {url}")
        raise asyncio.TimeoutError
    except Exception as e:
        print("error", f"An error occurred while fetching {url}: {e}")
        raise e


def sync_fetch(urls: list[str], headers: dict = None, timeout: int = 5):
    result = []
    try:
        for url in urls:
            response = requests.get(url, headers=headers, timeout=timeout)  # Pass timeout to the request
            response.raise_for_status()  # Check for HTTP errors
            result.append(response.json())  # Return the response content
    except requests.Timeout:
        print("Timeout occurred")
        raise requests.Timeout
    except requests.RequestException as e:
        print("An error occurred:", e)
        raise e
    return result