from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user,df):

    if selected_user != "Overall" :
        df = df[df["user"] == selected_user]
    
    num_messages = df.shape[0]
    words =[]
    for msg in df["message"]:
        words.extend(msg.split(" "))

    # fetch number of media messages
    num_media_msg = df[df["message"] == "<Media omitted>\n"].shape[0]

    
    extractor = URLExtract()
    links=[]
    for msg in df["message"]:
        links.extend(extractor.find_urls(msg))
        num_links = len(links)
    return num_messages,len(words),num_media_msg , num_links   
    
def fetch_most_busy_user(df):
    
    x=df["user"].value_counts().head(10)
    new_df=round((df["user"].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={"index":"name","user":"percent"})
    return x,new_df

def create_wordcloud(selected_user , df):
    f = open('stop_hinglish.txt',"r")
    stop_words = f.read()
    if selected_user != "Overall" :
        df = df[df["user"] == selected_user]

    # for leaving ommited message word
    extra_df = df[df["message"] != "<Media omitted>\n"]

    def remove_stopwords(msg):
        y=[]
        for word in msg.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color="white")
    df_wc = wc.generate(extra_df["message"].apply(remove_stopwords).str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt',"r")
    stop_words = f.read()
    if selected_user != "Overall" :
        df = df[df["user"] == selected_user]
    temp_df = df[df["message"] != "<Media omitted>\n"]
    # for removing stop words
    words=[]
    for msg in temp_df["message"]:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
    
def emoji_helper(selected_user,df):
    emojis=[]
    for msg in df["message"]:
        emojis.extend(emoji.distinct_emoji_list(msg))
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != "Overall" :
        df = df[df["user"] == selected_user]
    
    timeline = df.groupby(["year","month_num","months"]).count()["message"].reset_index()
    time =[]
    for i in range(timeline.shape[0]):
        time.append(timeline["months"][i]+"-"+str(timeline["year"][i]))
    timeline["time"] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != "Overall" :
        df = df[df["user"] == selected_user]
    daily_timeline = df.groupby("only_date").count()["message"].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != "Overall" :
        df = df[df["user"] == selected_user]
    return df["day_name"].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != "Overall" :
        df = df[df["user"] == selected_user]
    return df["months"].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != "Overall" :
        df = df[df["user"] == selected_user]
        
    activity_heatmap_table = df.pivot_table(index="day_name",columns="period",values="message",aggfunc="count").fillna(0)
    return activity_heatmap_table