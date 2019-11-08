import config
import jwt
import operator
import paralleldots
import pickle
import random
import re
import requests

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from library import fetch_response
from flask import Flask, request, jsonify
from flask_cors import CORS
from music import MusicRecommender
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

cluster = MongoClient(
    "mongodb+srv://adiach1:1234@cluster0-jgwg7.mongodb.net/geico?retryWrites=true&w=majority")
db = cluster["geico"]
collection = db["users"]

paralleldots.set_api_key(config.emotion_key)

app = Flask(__name__)
CORS(app)


chatbot = ChatBot(
    "GEICOChatBot",
    storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
    logic_adapters=['chatterbot.logic.BestMatch', {'import_path': 'custom_adapters.JokeAdapter'}, {
        'import_path': 'custom_adapters.MovieMusicAdapter'}],
    database_uri='mongodb+srv://adiach1:1234@cluster0-jgwg7.mongodb.net/test?retryWrites=true&w=majority',
    read_only=True
)

count = 0
last_question = None
username = ''
how_was_your_day = ''
favorite_movies = []
emotion = ''
mrec = MusicRecommender()


@app.route('/api/music', methods=['POST'])
def rec_song():
    data = request.get_json()
    if 'songName' not in data:
        return jsonify({'success': False, 'message': 'Missing song name field'})
    result = mrec.recommend(data['songName'])
    result['success'] = True
    return jsonify(result)


@app.route('/api/chatbot', methods=['POST'])
def chatbot_msg():
    global count
    username = ''
    last_question = None
    text = ''

    token = request.headers.get('Authorization')
    print(token)

    if not token:
        return {"message": "Token is missing"}
    try:
        token = token.split()[1]
        print(token)
        decToken = jwt.decode(token, "SECRET_KEY", 'utf-8')
    except Exception:
        return {"message": "Failed to decode token"}

    username = decToken.get('username')
    print(username)

    if request.json is not None:
        print("request json is not None")

    print(bool(request.json))
    if bool(request.json) is False:
        print("request json is false")
        print("Init empty")
        text = ''
        last_question = None
    else:
        print("request json is not false")
        print("Init full")
        text = request.json.get('text')
        last_question = request.json.get("question")

    print(username)
    print(last_question)

    if username != '' and last_question is None:
        print("Entry message")
        last_question = {"text": "Welcome back {}. My name is Baut! I recommend movies, music, and do some other stuff as well. Try statements like \"recommend movies\", \"recommend music\", or \"tell a joke \". ".format(
            username), "type": "bot", "question": "intro", "topic": "normal", "username": username}
        count += 1
        return last_question

    print(text)
    print(re.match(r'.*(recommend|suggest).*movie(s?)\.*', text.lower()))
    print(last_question)

    if re.match(r'.*(recommend|suggest).*movie(s?)\.*', text.lower()):
        return fetch_response('day', username)

    if re.match(r'.*(recommend|suggest).*(song(s?)|music)\.*', text.lower()):
        return fetch_response('music')

    if last_question == "day":
        # run emotional analysis on the string.
        how_was_your_day = request.json.get('text')
        emotion = "Happy"  # placeholder
        response = paralleldots.emotion(how_was_your_day)

        print(response)
        if response.get("emotion") is not None:
            emotion = max(response.get("emotion").items(),
                          key=operator.itemgetter(1))[0]

        print(emotion)
        collection.find_one_and_update({"username": username},
                                       {"$set": {"how_was_your_day": how_was_your_day, "emotion": emotion}})

        sentence = ''

        if emotion == "Happy":
            sentence = random.sample(
                ["That's good to hear. ", "Nice to see you in good spirits. ", "I'm glad your chipper. "], 1)
        if emotion == "Sad" or emotion == "Angry":
            sentence = random.sample(
                ["I'm sorry your day is going so poorly. ", "I hope tomorrow is better. ", "Sad reacts only. "], 1)
        if emotion == "Excited":
            sentence = random.sample(
                ["Your day sounded AMAZING!!! ", "I wish my day was as exciting. ", "Sounds like today was a rollercoaster! "], 1)
        if emotion == "Fear":
            sentence = random.sample(["I hope your days are calmer in the future. ",
                                      "We have nothing to fear but fear itself. ", "Never fear, the rules are here! "], 1)
        if emotion == "Bored":
            sentence = random.sample(
                ["Another day, another dollar I suppose. ", "Back to the old grind. ", "Same tbh. "], 1)

        return fetch_response('movie_response', sentence[0])

    if last_question == 'music_prompt':
        results = mrec.recommend(text)
        return { 'music': [results], 'question': 'general', 'text': 'Here\'s a song recommenation!', 'type': 'bot', 'topic': 'music' }

    if last_question == "favorite_movies":
        # first, create the user object
        # post = {"username":username, "how_was_your_day":how_was_your_day, "emotion":emotion, "favorite_movies":favorite_movies}
        # insert into mongo

        # then, prepend the string with a key phrase and send it to the bot. The corresponding logic adapter should pick it up and send it to Will
        text = request.json.get("text")
        user = request.json.get("username")
        text = text.split(', ')
        movieList = []

        for movie in text:
            link = "http://www.omdbapi.com/?apikey=" + config.omdb_api+"&s=" + movie
            resp = requests.get(link).json()

            if resp["Response"] == "True":
                movieList.append(resp['Search'][0]["imdbID"])
            else:
                print("failed")
        if len(movieList) == 0:
            return {"type": "bot", "text": "I'm sorry, I did not find any movies with those names."}

        resp = requests.post("https://baut-ml.wls.ai/recommend",
                             json={"ids": movieList, "user": username})
        collection.find_one_and_update({"username": username},
                                       {"$set": {"movies_liked": movieList}})

        response_data = resp.json()["ids"]
        listings = []
        print("response_data", response_data)
        for ids in response_data:
            postLink = "http://www.omdbapi.com/?apikey=" + config.omdb_api + "&i="
            postLink += "tt" + str(ids)
            temp = requests.get(postLink).json()
            print("temp:", temp)
            if temp["Response"] == "True":
                listings.append(temp)
        print("listings:", listings)
        return {"type": "bot", "topic": "movie", "text": "Here are some movies I found: " + listings[0]["Title"] + ", " + listings[1]["Title"] + ", " + listings[2]["Title"] + ", and more if you click on me", "movieInfo": listings, "question": "chatbot"}
    else:
        bot_output = chatbot.get_response(text)
        if bot_output.text == "Movie? Movie? I heard Movie! Tell me your favorite movies! Separate each one with a comma.":
            return {"text": bot_output.text, "type": "bot", "question": "favorite_movies", "topic": "normal"}
        elif bot_output.text == "I heard something about songs!":
            last_question = {"text": "Did you say somethings about music or songs? Tell us about yourself. Would you say that you have an Athletic, Sedentary, or Moderate lifestyle?",
                             "question": "music_lifestyle", "topic": "questions", "type": "bot", "options": ['Athletic', 'Sedentary', 'Moderate']}
            return last_question
        else:
            num = random.randrange(20)
            if num % 5 == 0:
                return fetch_response('bother_user')
            return {"text": bot_output.text, "type": "bot", "topic": "normal", "question": "chatbot"}

    bot_output = chatbot.get_response("tell me a joke")
    return {"text": "Movie? Movie? Did someone say movie? Tell me your favorite movies! Separate each one with a comma.", "type": "bot", "topic": "normal", "question": "favorite_movies"}


@app.route('/api/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.json.get('username')
        password = request.json.get('password')
        password = generate_password_hash(password)

        if collection.find({"username": username}).count() > 0:
            return {"message": "User already exists!"}

        post = {"username": username, "password": password}
        token = jwt.encode({'username': username}, "SECRET_KEY")
        token = token.decode('utf-8')

        collection.insert_one(post)

        return {"message": "User inserted successfully", "token": token}

    return {"message": "You sent a post cheif"}


@app.route('/api/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.json.get('username')
        password = request.json.get('password')

        user_obj = collection.find_one({"username": username})

        if user_obj is None:
            return {"message": "User was not found"}

        if check_password_hash(user_obj['password'], password):
            token = jwt.encode(
                {'username': user_obj['username']}, "SECRET_KEY")
            token = token.decode('utf-8')
            return {"message": "Password was correct. Login successful", "token": token}

        else:
            return {"message": "Password Incorrect. Login unsuccessful"}

    return {"message": "You did not send a post chief"}


@app.route('/api/save_movie', methods=['GET', 'POST'])
def save_movie():

    if request.method == 'POST':

        token = request.headers.get('Authorization')
        print(token)

        if not token:

            return {"message": "Token is missing"}
        try:
            token = token.split()[1]
            print(token)
            decToken = jwt.decode(token, "SECRET_KEY", 'utf-8')
        except Exception:
            return {"message": "Failed to decode token"}

        username = decToken.get('username')
        print(username)
        print(request.json)
        imdbID = request.json.get('imdbID')
        print(imdbID)

        collection.find_one_and_update({"username": username, }, {
                                       '$push': {'saved_movies': imdbID}})

        return {"message": "Movie inserted into user document"}

    return {"message": "You did not send a post chief"}


@app.route('/api/get_saved_movies', methods=['GET', 'POST'])
def get_saved_movies():

    if request.method == 'POST':

        token = request.headers.get('Authorization')
        print(token)

        if not token:

            return {"message": "Token is missing"}
        try:
            token = token.split()[1]
            print(token)
            decToken = jwt.decode(token, "SECRET_KEY", 'utf-8')
        except Exception:
            return {"message": "Failed to decode token"}

        username = decToken.get('username')
        print(username)
    # print(request.json)

        user_obj = collection.find_one({"username": username})

        listings = []
        for imdbID in user_obj.get('saved_movies'):
            postLink = "http://www.omdbapi.com/?apikey=" + config.omdb_api + "&i="
            postLink += str(imdbID)
            temp = requests.get(postLink).json()
            # print("temp:", temp)
            if temp["Response"] == "True":
                listings.append(temp)
        print("listings:", listings)

        return {"message": "Movies fetched successfully", "savedIDs": user_obj.get('saved_movies'), "movieInfo": listings}

    return {"message": "You did not send a post chief"}


if __name__ == "__main__":
    app.run(debug=True)
