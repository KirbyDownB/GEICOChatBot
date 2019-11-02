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
import config
from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://adiach1:1234@cluster0-jgwg7.mongodb.net/geico?retryWrites=true&w=majority")
db = cluster["geico"]
collection=db["geico"]
# paralleldots.set_api_key(key.emotion_key)
paralleldots.set_api_key(config.emotion_key)

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
        if username is '' and last_question is None:
            #No response expected
            last_question = {"text":"My name is GEICO BOT! I recommend movies, music, and do some other stuff as well. First things first, I need a username from you", "type":"bot", "question":"intro","topic":"normal"}
            count += 1
            return last_question

        elif count > 0 and last_question is not None:

            #text = request.json.get('text')
            username = request.json.get('username')
            text = request.json.get('text')

            print("TEXXXXT")
            print(text)
            # print(re.match(r'.*(recommend|suggest).*movies\.*', text.lower()))
            if last_question.get("question") == "intro":
                username = request.json.get("username")
                text = request.json.get("text")
                #store the username in the database

                if collection.find({"username":username}).count() == 0:
                    collection.insert_one({"username":username})


                #start the movie flow
                last_question = {"text":"Hi {}! Now we can begin! Try things like \"recommend me some movies\" or \"tell me a joke\".".format(username), "topic":"normal", "type":"bot"}
                return last_question

            if re.match(r'.*(recommend|suggest).*movies\.*', text.lower()):

                username = request.json.get("username")

                last_question = {"text":"Ok {}, how has your day been? This will give us some idea about what movies to \
                    recommend you.".format(username), "type":"bot","question":"day","topic":"normal"}
                return last_question


            if last_question.get("question") == "day":
                #run emotional analysis on the string.
                username = request.get.json("username")
                how_was_your_day = request.form.get('text')
                emotion = "Happy" #placeholder
                response = paralleldots.emotion(how_was_your_day)

                if response.get("emotion") is not None:
                    emotion = max(response.get("emotion").items(), key=operator.itemgetter(1))[0]

                print(emotion)
                collection.find_one_and_update({"username": username},
                                 {"$set": {"how_was_your_day": how_was_your_day, "emotion":emotion}})


                last_question = {"text":"What are some of your favorite movies? Separate each one with a \
                    comma.", "type":"bot", "question":"favorite_movies", "topic":"normal"}

                return last_question

            if last_question.get("question") == "favorite_movies":

                #first, create the user object
                # post = {"username":username, "how_was_your_day":how_was_your_day, "emotion":emotion, "favorite_movies":favorite_movies}
                #insert into mongo

                #then, prepend the string with a key phrase and send it to the bot. The corresponding logic adapter should pick it up and send it to Will

                text = request.json.get("text")
                text = text.split(', ')
                movieList = []

                for movie in text:
                    link = "http://www.omdbapi.com/?apikey=" + config.omdb_api+"&s=" + movie
                    resp = requests.get(link).json()

                    if resp["Response"]=="True":
                        movieList.append(resp['Search'][0]["imdbID"])
                    else:
                        print("failed")
                if len(movieList) == 0:
                    return {"text": "I'm sorry I did not find any movies with those names."}
                # movieList = json.dumps()
                resp = requests.post("http://167.172.203.238:5500/recommend", json={"ids": movieList})
                response_data = resp.json()["ids"]

                convertedList = []
                for ids in response_data:
                    postLink = "http://img.omdbapi.com/?apikey=&" + config.omdb_api + "&i="
                    postLink += "tt0" + str(ids)
                    temp = requests.get(link).json()

                    if temp["Response"]=="True":
                        convertedList.append(temp['Search'])

                #return of movie recommendations
                return {"type": "bot", "topic": "movie", "text": convertedList[0][0]}


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
