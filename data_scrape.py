import asyncio
from twscrape import API, gather
import pandas as pd
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")


async def main():
    api = API()
    user_id = 16129920
    cols = ["Name", "Text", "Time"]
    data = {col: [] for col in cols}

    async for tweet in api.user_tweets(user_id, limit=5000):
        data['Name'].append(tweet.user.displayname)
        data['Text'].append(tweet.rawContent)
        data['Time'].append(tweet.date)

    df = pd.DataFrame(data)
    df.to_csv('maddow' +'.csv')

if __name__ == "__main__":
    asyncio.run(main())
