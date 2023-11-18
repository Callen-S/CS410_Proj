import asyncio
from twscrape import API, gather
from open_ai import calc_vibes
from twscrape.logger import set_log_level


async def main():
    api = API()
    users = []
    q = "trump since:2014-01-01 until:2023-05-31"
    async for tweet in api.search(q, limit=300):

        users.append(tweet.user.id)

    for i, user in enumerate(users):
        await gather(api.followers(user, limit=200))
        print(i)

if __name__ == "__main__":
    asyncio.run(main())
