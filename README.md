# CS410_Proj
### Proposal
The initial proposal and progress report described a more ambitious project that would have collected large amount of text data from users and processed it to analyze sentiment over time. The main source of this data was going to be the [Facebook scraper](https://pypi.org/project/facebook-scraper/) package. However, it no longer works due to some changes to the website. I spent a nontrivial amount of time getting it working. However, Facebook rate limited its interactions so you could at most get 1 post every five seconds it would often disconnect your session after a few thousand posts. 

### Current Tool
Therefore, the tool is much smaller in scale. It currently has the tweet history of some 13 major figures without about 3 thousand posts each. It's still a corpus of about 40 thousand tweets, not bad. This was done using the data scrape [package](https://github.com/vladkens/twscrape) and a small army of twitter accounts. 

To use the data_scrape.py tool to create new data you need to have a series of valid Twitter accounts and create a database connected to the app to pull the tweets. This is described in the package readme. 
The rest of the app is a streamlit app that allows you to find relevant tweets and uses chat gpt to analyze their sentiment. It uses BM25 search to find the most relevant tweet in the text segment of each tweet for every month it has data. 
It then asks chat GPT to asses the sentiment on a scale of 1-10 while 10 is positive vs the query.

This is the link - https://callentest.streamlit.app/-. You can also find the demo video here.

To run the app locally you can clone the repo and hit streamlit run app.py
You will get two errors:
	Not configuring a OpenAi Key 
	Not configuring a github key to read the data 
You must set both of these in the streamlit global variable env as shown here. That is it!
