#importing all nesscessry packages
import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
from pymongo import MongoClient

st.set_page_config(page_title="Home page")
#heading on the page
st.sidebar.title("Scrape")
st.header('Please fill in the required details and click on the SCRAPE button to run this app')


#No. of tweeter count to be fetched
number = st.number_input("Enter the Number of tweets to retrieve.!")

#Keywod or hashtag in which the tweets to be generated
key_or_hashtag = st.text_input("Enter the keyword or hashtag to retrieve.!")
#st.write('The current movie title is', key_or_hashtag)

#date limit
F_date = st.date_input("Enter the Start Date")
T_date = st.date_input("Enter the End Date")

#combaining all input data to fetch the tweet accordingly
query1=str(key_or_hashtag)+" "+"until:"+str(T_date)+" "+"since:"+str(F_date)

#empty list to store the fetched tweets
tweeterlist=[]

#fetching tweets
for tweet in sntwitter.TwitterSearchScraper(query1).get_items():
    if len(tweeterlist)==number:#check the lenght of the list which meets the no. of count
        break
    else:
        #appending each tweets into empty list
        tweeterlist.append([tweet.date,
                       tweet.id,
                       tweet.url,
                       tweet.rawContent,
                       tweet.user.username,
                       tweet.replyCount,
                       tweet.retweetCount,
                       tweet.lang,
                       tweet.source,
                       tweet.likeCount])

#converting into Data frame
df=pd.DataFrame(tweeterlist,columns=['date',
                                'id',
                                'url',
                                'tweet content',
                                'user','reply count',
                                'retweet count',
                                'language',
                                'source',
                                'like count'])


#scrape button to fetch and display
scrape= st.button("Scrape")
if scrape:
    st.dataframe(df)


#converting the dataframe into dictionary data
df.reset_index(inplace=True )
data_dict=df.to_dict("records")

#button to upload data into mongoDB server
st.header("Click here to upload the data to Database")
upload= st.button("Upload")

#importing dict into mongodb data base
if upload:

    client = MongoClient('localhost', 27017)
    db = client.database
    collection = db.data_1
    collection.insert_many(data_dict)


st.header("Click here to download  the data as CSV file")

#button to download the data in CSV file format
st.download_button(label="Download CSV",
                   data=df.to_csv(), mime='text/csv')

st.header("Click here to download  the data as JSON file")

#button to download the data in json  file format
st.download_button(label="Download json",data=df.to_json(),mime="text/json")


