import streamlit as st
import streamlit.components.v1 as components
import requests
import html2text

# Page title
st.markdown("""
# Tweet Embedder
This simple app displays tweets using the url provided. Paste the tweet url in the text box below and view the results.
""")

# Get html version of the tweet
def getTweet(tweet_url):
    tweet_url = tweet_url.replace('https://x', 'https://twitter')
    url = f"https://publish.twitter.com/oembed?url={tweet_url}"
    response = requests.get(url)
    res = response.json()
    author_name = res["author_name"]
    tweet_html = html2text.html2text(res["html"])
    return res, tweet_html, author_name

# Create function that extracts information automatically
def getData(text, name):
    # Clean text
    text = text.replace(">", "")
    
    # Get tweet
    tweet_end = text.find(f"-- {name} (@")
    tweet = text[:tweet_end]
    
    # Remaining text to parse
    text = text[tweet_end+3:]
    text = text[len(name)+1:]
    
    # Get username
    bb, eb = text.find("("), text.find(")")
    username = text[bb+1: eb]
    
    # Get date
    bd, ed = text.find("["), text.find("]")
    date = text[bd+1:ed]
    date = date.replace("\n", "")
    
    return tweet, username, date

# Get url from user
input = st.text_input("Enter the url of the tweet here")
if input and st.button("Get result"):
    try:
        res, data, name = getTweet(input)
        st.subheader("Name")
        st.write(name)
        tweet, username, date = getData(data, name)
        st.subheader("Tweet")
        st.write(tweet)
        st.subheader("Username")
        st.write(username)
        st.subheader("Date")
        st.write(date)
        components.html(res['html'], height=1000, width=1000, scrolling=True)
    except Exception as error:
        st.write(error)
