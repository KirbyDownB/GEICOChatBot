from flask import Flask, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import requests
from flask_cors import CORS
import pickle
import re
import paralleldots
import operator
import keys
from keys import emotion_key
# paralleldots.set_api_key(key.emotion_key)
paralleldots.set_api_key(emotion_key)

app = Flask(__name__)
CORS(app)



chatbot = ChatBot(
    "GEICOChatBot",
    storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
    logic_adapters=['chatterbot.logic.BestMatch',{'import_path': 'custom_adapters.JokeAdapter'}],
    database_uri='mongodb+srv://adiach1:1234@cluster0-jgwg7.mongodb.net/test?retryWrites=true&w=majority',
    read_only=True

)

'''

Leading questions
1. Hey! My name is (GEICO BOT). Please type in your username
{"text":"My name is GEICO BOT. Please type in your username", "type":"leading, "question":"username", "topic":"normal"}
2. How has your day been? This will give us some idea about what movies/songs to recommend you. 
{"text":"How has your day been? This will give us some idea about what movies/songs to recommend you.", "type":"leading","question":"day"}
3. What are some of your favorite movies? Seperate each one with a comma.
{"text":"What are some of your favorite movies? Seperate each one with a comma.", "type":"leading", "question":"favorite_movies", "topic":"normal"}


'''
count = 0
last_question = None
username = ''
how_was_your_day = ''
favorite_movies = []
emotion = ''
@app.route('/api/chatbot',methods=['GET','POST'])
def main():
    global count
    global last_question
    global username
    global how_was_your_day
    global favorite_movies
    global emotion
    if request.method == 'POST':
        print(last_question)
        print(count)
        if count == 0 and last_question is None:
            #No response expected
            last_question = {"text":"My name is GEICO BOT! I recommend movies, music, and do some other stuff as well. First things first, I need a username from you", "type":"bot", "question":"intro","topic":"normal"}
            count += 1
            return last_question
        
        elif count > 0 and last_question is not None:

            #text = request.json.get('text')
            text = request.json.get('text')
            print("TEXXXXT")
            print(text)
            # print(re.match(r'.*(recommend|suggest).*movies\.*', text.lower()))
            if last_question.get("question") == "intro":
                username = request.json.get("text")
                #start the movie flow
                last_question = {"text":"Hi {}! Now we can begin! Try things like \"recommend me some movies\" or \"tell me a joke\".".format(username), "topic":"normal", "type":"bot"}
                return last_question

            if re.match(r'.*(recommend|suggest).*movies\.*', text.lower()):
                

                last_question = {"text":"Ok {}, how has your day been? This will give us some idea about what movies to \
                    recommend you.".format(username), "type":"bot","question":"day","topic":"normal"}
                return last_question
            if last_question.get("question") == "day":
                #run emotional analysis on the string. 

                how_was_your_day = request.form.get('text')
                emotion = "Happy" #placeholder 
                # find_max(requests.post("https://apis.paralleldots.com/v4/emotion",params={"text":how_was_your_day,"api_key":"Ssc7kaGUcIf46xcEc8CPknQZQSAwJAgAQJTSqXnDsoM"}).get("emotion")), where find max finds the key with the highest value
                response = paralleldots.emotion(how_was_your_day)
                
                if response.get("emotion") is not None:
                    emotion = max(response.items(), key=operator.itemgetter(1))[0]

                print(emotion)
                last_question = {"text":"What are some of your favorite movies? Separate each one with a \
                    comma.", "type":"bot", "question":"favorite_movies", "topic":"normal"}

                return last_question

            if last_question.get("question") == "favorite_movies":

                #Go in for the kill lmao

                #first, create the user object
                post = {"username":username, "how_was_your_day":how_was_your_day, "emotion":emotion, "favorite_movies":favorite_movies}
                #insert into mongo

                #then, prepend the string with a key phrase and send it to the bot. The corresponding logic adapter should pick it up and send it to Will
                text = request.form.get("text")
                text = "Movies:" + text

                bot_output = chatbot.get_response(text)
                if bot_output == "junk":
                    return {"text":"Hmmm, those don't sound like any movies I've heard of. Can you give me any more movies you like?"}
                return {"text":bot_output}


            else:
                bot_output = chatbot.get_response(text)
                return {"text":bot_output.text, "type":"bot", "topic":"normal"}

    return {"Hi":"Eric"}

@app.route('/api/user_data', methods=['GET','POST'])
def user_data():

    if request.method == 'POST':

        return {"Hi":"John", "type":"bot"}


    return {"Hi":"John", "type":"bot"}









if __name__ == "__main__":
    app.run(debug=True)

