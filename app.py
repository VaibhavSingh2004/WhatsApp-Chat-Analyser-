import streamlit as st
import preprocessing
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue() 
    data = bytes_data.decode("utf-8")
    df = preprocessing.preprocess(data)
    # for removing group notification
    df = df[df["user"] != "group_notification"]
    user_list = df["user"].unique().tolist()
    # user_list.remove("group_notification") 
    # df["user"] = user_list
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt",user_list)
    num_msg , words , num_media_msg ,num_links = helper.fetch_stats(selected_user,df)
    st.title("Top Statistics")
    if st.sidebar.button("Show Analysis"):
        col1,col2,col3,col4 = st.columns(4)
        with col1 :
            st.header("Total Messages")
            st.title(num_msg)
        with col2 :
            st.header("Total Words")
            st.title(words)
        with col3 :
            st.header("Media Shared")
            st.title(num_media_msg)
        with col4 :
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(timeline["time"],timeline["message"],color="Green")
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        # ax.figure(figsize=(18,10))
        ax.plot(daily_timeline["only_date"],daily_timeline["message"],color="brown")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user,df) 
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color="orange")
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)

        # activity map
        st.title("Weekly Activity Map")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
            

        # finding the busiest user in the group
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x , new_df = helper.fetch_most_busy_user(df)
            fig , ax = plt.subplots()
            col1 , col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index,x.values,color="Green")
                plt.xticks(rotation = "vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax =plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user,df)
        st.title("Most common Words")
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        # st.dataframe(most_common_df)


        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1 , col2 =st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2 :
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(10),labels=emoji_df[0].head(10),autopct="%0.2f")
            st.pyplot(fig)
    
         