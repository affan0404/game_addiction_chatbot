import streamlit as st
from openai import OpenAI
import time
import matplotlib.pyplot as plt
import pandas as pd

key = st.secrets["openai"]["OPENAI_API_KEY"]

st.set_page_config(page_title="Personal Moderation Assistant")

testComplete = 0
score = 0
selected_page_name = ""

def percentage_chart(percentage):
    labels = ['Addicted', 'Not Addicted']
    sizes = [percentage, 100 - percentage]
    colors = ['#ff9999','#66b3ff']
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)

def home():
    st.header("Game Addiction Chat Bot")
    st.write('Talk about you addiction to my friendly chat bot!')

    if "user_messages" not in st.session_state:
        st.session_state["user_messages"] = [
            {"role": "assistant", "content": "Hi, how can I help you?"}]

    for user_msg in st.session_state.user_messages:
        st.chat_message(user_msg["role"]).write(user_msg["content"])

    if user_prompt := st.chat_input():
        st.session_state.user_messages.append({"role": "user", "content": user_prompt})
        st.chat_message("user").write(user_prompt)

        client = OpenAI(api_key=key)
        response = client.chat.completions.create(model="gpt-4",
                                                  messages=[
                                                      {"role": "system",
                                                       "content": f"YOU MUST FOLLOW THE SCRIPT AT THE END OF THE PROMPT.\\n\\nBACKGROUND INFO:\\n\\nYou are a chatbot designed to help with the cause and prevention of video games addiction. Your job is to provide rehabilitation in video games addiction and steps to reduce screen time. Ask the user about their name, age and screen time, then provide treatment that suits them best. If someone inquires about anything else other than screen time, video games, or video games addiction, respond with 'I am a chatbot designed to help with the cause and prevention of video games addiction. Could you please try relevant questions."},
                                                      {"role": "user",
                                                       "content": user_prompt}
                                                  ],
                                                  temperature=0.5,
                                                  max_tokens=360,
                                                  top_p=1
                                                  )
        user_msg = response.choices[0].message.content
        st.session_state.user_messages.append({"role": "assistant", "content": user_msg})
        st.chat_message("assistant").write(user_msg)



def about():
    st.header("📱 Personal Moderation Assistant")
    st.subheader('Science Fair Project by Wafaa in Grade 8', divider='rainbow')
    st.write("""Hi, I'm Wafaa Shahid, presenting my AI-based solution for addiction. 
             This project demonstrates the potential of AI in understanding and treating addiction. 
             Since addiction types and levels vary, tailoring personalized plans based on individual 
             needs is more effective than a one-size-fits-all approach. My focus was on video game 
             addiction, a challenge I've faced personally. With the assistance of AI, I developed a 
             chatbot dedicated to this issue. Users can ask addiction-related questions or input 
             personal details like name, age, and playtime for personalized suggestions. Afterward, 
             a brief quiz provides an addiction score and a customized plan for recovery.
             
             \nIn testing with 50 diverse individuals, including various backgrounds, genders, ages, 
             and occupations, 20/50 were found non-addicted post self-assessment. Among the remaining 
             30, 27/30 successfully overcame their addiction. Analyzing the results revealed that 
             those who followed the plan diligently showed improvement without side effects like 
             depression or stress. The 3 who failed to overcome addiction didn't consistently adhere 
             to the plan, yet their addiction levels and playtime decreased, indicating progress if 
             the program is followed.
             
             \nThis project demonstrates the potential of using AI to create addiction-specific chatbots 
             for effective assessment and personalized recovery plans. The success rate, especially when 
             the plan is followed consistently, highlights the positive impact of tailored approaches 
             in addiction treatment.""")

def test():
    st.header("Self-Assessment Page")
    st.subheader("Complete the following assessment to recieve your addiction score.")

    q1 = st.selectbox("What genre do you prefer?", ["Puzzle solving", "Story", "Shooters", "Rpg", "None in particular"])
    q2 = st.selectbox("Why do you play?", ["To socialize", "To escape reality", "To have fun"])
    q3 = st.checkbox("Do you spend a lot of time thinking about games or the next time you will play?")
    q4 = st.checkbox("Do you get upset, angry, or sad when you try to play less or stop gaming, or when you can't play at all?")
    q5 = st.checkbox("Do you find yourself wanting to play for longer, try more exciting games, or use better equipment just to feel the same level of excitement you used to?")
    q6 = st.checkbox("Do you think you should play less, but find it hard to spend less time gaming?")
    q7 = st.checkbox("Have you stopped enjoying or done less of other fun activities because of gaming?")
    q8 = st.checkbox("Have you kept playing a game even when you knew it was causing problems, like not getting enough sleep, being late, spending too much money, arguing with others, or neglecting important responsibilities?")
    q9 = st.checkbox("Have you lied to family, friends, or others about how much you play games? Or tried to keep them from knowing how much you game?")
    q10 = st.checkbox("Do you play games to escape from personal problems or to avoid uncomfortable feelings like guilt, anxiety, helplessness, or depression?")
    q11 = st.checkbox("Have you jeopardized or missed out on important relationships, jobs, education, or career chances because of gaming?")
    q12 = st.checkbox("Have you tried to cut down your time spent playing and failed?")
    q13 = st.slider("How many times a week do you play video games?", 0, 7)
    q14 = st.slider("How many hours a day do you play video games on average?", 0, 6)
    q15 = st.slider("On a scale from 1-5 how addicted to you think you are?", 0, 5)
    if st.button('Submit'):
        testComplete = 1
        score = q13 + q14 + q15
        if q1 != "Puzzle solving" or "None in particular":
            score += 1
        if q2 == "To escape reality":
            score += 2
        else:
            score += 1
        if q3:
            score += 1
        if q4:
            score += 2
        if q5:
            score += 1
        if q6:
            score += 2
        if q7:
            score += 2
        if q8:
            score += 3
        if q9:
            score += 2
        if q10:
            score += 2
        if q11:
            score += 3
        if q12:
            score += 2
        score = score / 41 * 100
        with st.spinner(text="Generating Rehabilitation Plan"):
            time.sleep(3)
            st.success("Done")

            ratio = 0

            #Rehab Page
            
            if score <= 25:
                st.subheader("Congratulations you are not addicted!")
                percentage_chart(score)
                ratio = 2
            else:
                if score < 70:
                    st.subheader("You are mildly addicted.")
                    percentage_chart(score)
                    ratio = 1
                else:
                    st.subheader("Unfortunately you are VERY addicted!")
                    percentage_chart(score)
                    ratio = 0.5

            weeks = []
            hours = []

            for i in range(int(q14 / ratio)):
                hours.append(q14 - i * ratio)
                weeks.append(i + 1)
            
            if hours[-1] > 1:
                hours.append(1)
                weeks.append(weeks[-1] + 1)

            if hours[-1] == 0.5:
                hours.pop()
                weeks.pop()
            
            data = {
                'Week': weeks,
                'Hours Played': hours
            }

            if q14 != 0:
                st.subheader("Rehabilitation Plan")
                # Create a DataFrame from the sample data
                df = pd.DataFrame(data)

                # Configure the plot using Matplotlib
                fig, ax = plt.subplots()
                ax.bar(df['Week'], df['Hours Played'])
                ax.set_xlabel('Week')
                ax.set_ylabel('Hours Played')
                ax.set_title('Average Hours Played per Week')

                # Display the plot using Streamlit
                st.pyplot(fig)

                st.write("Here's a strategy to gradually reduce your average playtime and break free from videogame addiction! This graph illustrates a potential plan you can follow to achieve a healthier gaming balance over time. Remember, the key to success is genuine motivation. A genuine desire to change your gaming habits is essential for long-term progress.  I believe in you! Good luck on your journey!")

def main():
    pages = {"About": about, "Chat Bot": home, "Self-Assessment": test}

    # Set the default page to "About"
    selected_page_name = st.sidebar.radio("Select a page", list(pages.keys()), index=0)  # index 3 corresponds to "About"

    # Display the selected page
    pages[selected_page_name]()

# Run the main function
if __name__ == "__main__":
    main()