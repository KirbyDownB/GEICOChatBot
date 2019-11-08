from flask import Flask, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import random
import requests
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import pickle
import re
import paralleldots
import operator
import config
from pymongo import MongoClient
from music import MusicRecommender

cluster = MongoClient("mongodb+srv://adiach1:1234@cluster0-jgwg7.mongodb.net/geico?retryWrites=true&w=majority")
db = cluster["geico"]
collection=db["users"]
# paralleldots.set_api_key(key.emotion_key)
paralleldots.set_api_key(config.emotion_key)

app = Flask(__name__)
CORS(app)



chatbot = ChatBot(
    "GEICOChatBot",
    storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
    logic_adapters=['chatterbot.logic.BestMatch',{'import_path': 'custom_adapters.JokeAdapter'},{'import_path':'custom_adapters.MovieMusicAdapter'},
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Who made you?',
            'output_text': 'My creators are John, Eric, Aditya, and Will. I was created at the University of California, Riverside in Bourns A171.'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'When is your birthday?',
            'output_text': 'I was born on November 1st, 2019'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'What is the answer to life, the universe, and everything?',
            'output_text': '42'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': '?',
            'output_text': 'I could ask the same of you as well. I don\'t think either of us could give a good answer'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Who\'s that pokemon?',
            'output_text': 'It\'s me'
        }
        ],
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
mrec = MusicRecommender()

@app.route('/api/music', methods=['POST'])
def rec_song():
    data = request.get_json()
    if 'songName' not in data:
        return jsonify({ 'success': False, 'message': 'Missing song name field' })
    result = mrec.recommend(data['songName'])
    result['success'] = True
    return jsonify(result)

@app.route('/api/chatbot',methods=['GET','POST'])
def chatbot_msg():
    global count
    # global last_question
    # global username
    # global how_was_your_day
    # global favorite_movies
    # global emotion
    username = ''
    last_question = None
    text = ''

    token = request.headers.get('Authorization')
    print(token)
    
    if not token:

        return {"Message":"Token is missing"}
    try:
        token = token.split()[1]
        print(token)
        decToken = jwt.decode(token,"SECRET_KEY",'utf-8')
    except Exception:
        return {"Message":"Failed to decode token"}

    username = decToken.get('username')
    print(username)


    if request.method == 'POST':

        print("HEWWO")
        print(request.json)
        print("I like pie")
        if request.json is not None:
            print("request json is not NOne")
            print("line 61", request.json)
        # username = request.json.get("username")
        # text = request.json.get("text")
        print(bool(request.json))
        if bool(request.json) is False:
            print("request json is false")
            print("Init empty")
            # username = ''
            text = ''
            last_question = None

        if bool(request.json) is not False:
            print("request json is not flase")
            print("Init full")
            # username = request.json.get('username')
            text = request.json.get('text')
            last_question = request.json.get("question")

        print(username)
        print(last_question)



        if username != '' and last_question is None:
            #No response expected
            print("Entry message")
            last_question = {"text":"Welcome back {}. My name is Baut! I recommend movies, music, and do some other stuff as well. Try statements like \"recommend movies\", \"recommend music\", or \"tell a joke \". ".format(username), "type":"bot", "question":"intro","topic":"normal", "username":username}
            count += 1
            return last_question


        print(text)
        print(re.match(r'.*(recommend|suggest).*movie(s?)\.*', text.lower()))
        print(last_question)

        if re.match(r'.*(recommend|suggest).*movie(s?)\.*', text.lower()) and last_question == "intro":

            

            last_question = {"text":"Ok {}, how has your day been? This will give us some idea about what movies to \
                recommend you.".format(username), "type":"bot","question":"day","topic":"normal"}
            return last_question

        if re.match(r'.*(recommend|suggest).*movie(s?)\.*', text.lower()):

            username = request.json.get("username")

            last_question = {"text":"Ok {}, how has your day been? This will give us some idea about what movies to \
                recommend you.".format(username), "type":"bot","question":"day","topic":"normal"}
            return last_question

        if re.match(r'.*(recommend|suggest).*(song(s?)|music)\.*', text.lower()):
            username = request.json.get("username")

            last_question = {"text":"Ok {}. Tell us about yourself. Would you say that you have an Athletic, Sedentary, or Moderate lifestyle?".format(username), "question":"music_lifestyle", "topic":"questions","type":"bot","options":['Athletic','Sedentary','Moderate']}
            return last_question
        if last_question == "music_lifestyle":
            text = request.json.get("text")
            username = request.json.get("username")
            if not(text == "Athletic" or text == "Sedentary" or text == "Moderate"):
                last_question = {"text":"Ok {}. Tell us about yourself. Would you say that you have an Athletic, Sedentary, or Moderate lifestyle?".format(username), "question":"music_lifestyle", "topic":"questions","type":"bot","options":['Athletic','Sedentary','Moderate']}
                return last_question

            collection.find_one_and_update({"username": username}, {"$set": {"lifestyle": text}})

            last_question = {"text":"Great! One more question. Would you say that your hobbies are more Indoor or Outdoor?","question":"music_hobbies", "topic":"questions","type":"bot","options":['Indoor','Outdoor']}
            return last_question

        if last_question == "music_hobbies":
            text = request.json.get("text")

            username = request.json.get("username")

            if not(text == "Indoor" or text == "Outdoor"):
                last_question = {"text":"Let's try that again {}. Would you say that your hobbies are more Indoor or Outdoor?","question":"music_hobbies", "topic":"questions","type":"bot","options":['Indoor','Outdoor']}
                return last_question


            collection.find_one_and_update({"username": username}, {"$set": {"hobbies": text}})
            data = collection.find_one({"username":username})

            #data.get("lifestyle") returns the lifestyle input
            #data.get("hobbies") returns the hobbies input
            #have conditions for if the user puts in junk
            if data.get("lifestyle") == "Athletic" and data.get("hobbies") == "Outdoor":
                print("heahfijdafasdfasdf")
                list = ["EDM", "Dubstep", "Trap"]
                randomNum = random.randint(0, len(list)-1)
                genre = list[randomNum]
                link = "http://ws.audioscrobbler.com/2.0/?format=json&method=tag.gettoptracks&tag=" + genre + "&api_key=" + config.last_key + "&format=json"
                resp = requests.get(link).json()
                store = resp["tracks"]["track"][0]
                mbid = store["mbid"]
                newLink = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=" + config.last_key + "&mbid=" + mbid + "&format=json"
                newResp = requests.get(newLink).json()
                songInfo = newResp["track"]
                songName = songInfo["name"]
                return {"text":"How does the song " + songName + " tickle your ears? ", "question":"general", "topic":"music","type":"bot", "musicInfo": [{"Genre": genre, "Song": songInfo["name"], "Artist": songInfo["artist"]["name"], "Album": songInfo["album"]["title"], "Duration": store["duration"], "Stream": songInfo["url"], "AlbumArt": songInfo["album"]["image"][2]["#text"], "TopTags": songInfo["toptags"]["tag"], "Published": songInfo["wiki"]["published"], "Summary": songInfo["wiki"]["summary"]}]}

            elif data.get("lifestyle") == "Athletic" and data.get("hobbies") == "Indoor":
                list = ["Rap", "Hip-Hop", "House"]
                randomNum = random.randint(0, len(list)-1)
                genre = list[randomNum]
                link = "http://ws.audioscrobbler.com/2.0/?format=json&method=tag.gettoptracks&tag=" + genre + "&api_key=" + config.last_key + "&format=json"
                resp = requests.get(link).json()
                store = resp["tracks"]["track"][0]
                mbid = store["mbid"]
                newLink = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=" + config.last_key + "&mbid=" + mbid + "&format=json"
                newResp = requests.get(newLink).json()
                songInfo = newResp["track"]
                songName = songInfo["name"]
                return {"text":"How does the song " + songName + " tickle your ears? ", "question":"general", "topic":"music","type":"bot", "musicInfo": [{"Genre": genre, "Song": songInfo["name"], "Artist": songInfo["artist"]["name"], "Album": songInfo["album"]["title"], "Duration": store["duration"], "Stream": songInfo["url"], "AlbumArt": songInfo["album"]["image"][2]["#text"], "TopTags": songInfo["toptags"]["tag"], "Published": songInfo["wiki"]["published"], "Summary": songInfo["wiki"]["summary"]}]}

            elif data.get("lifestyle") == "Moderate" and data.get("hobbies") == "Outdoor":
                list = ["Pop", "Musicals", "Rock"]
                randomNum = random.randint(0, len(list)-1)
                genre = list[randomNum]
                link = "http://ws.audioscrobbler.com/2.0/?format=json&method=tag.gettoptracks&tag=" + genre + "&api_key=" + config.last_key + "&format=json"
                resp = requests.get(link).json()
                store = resp["tracks"]["track"][0]
                mbid = store["mbid"]
                newLink = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=" + config.last_key + "&mbid=" + mbid + "&format=json"
                newResp = requests.get(newLink).json()
                songInfo = newResp["track"]
                songName = songInfo["name"]
                return {"text":"How does the song " + songName + " tickle your ears? ", "question":"general", "topic":"music","type":"bot", "musicInfo": [{"Genre": genre, "Song": songInfo["name"], "Artist": songInfo["artist"]["name"], "Album": songInfo["album"]["title"], "Duration": store["duration"], "Stream": songInfo["url"], "AlbumArt": songInfo["album"]["image"][2]["#text"], "TopTags": songInfo["toptags"]["tag"], "Published": songInfo["wiki"]["published"], "Summary": songInfo["wiki"]["summary"]}]}

            elif data.get("lifestyle") == "Moderate" and data.get("hobbies") == "Indoor":
                list = ["Jazz", "Blues", "Swing"]
                randomNum = random.randint(0, len(list)-1)
                genre = list[randomNum]
                link = "http://ws.audioscrobbler.com/2.0/?format=json&method=tag.gettoptracks&tag=" + genre + "&api_key=" + config.last_key + "&format=json"
                resp = requests.get(link).json()
                store = resp["tracks"]["track"][0]
                mbid = store["mbid"]
                newLink = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=" + config.last_key + "&mbid=" + mbid + "&format=json"
                newResp = requests.get(newLink).json()
                songInfo = newResp["track"]
                songName = songInfo["name"]
                return {"text":"How does the song " + songName + " tickle your ears? ", "question":"general", "topic":"music","type":"bot", "musicInfo": [{"Genre": genre, "Song": songInfo["name"], "Artist": songInfo["artist"]["name"], "Album": songInfo["album"]["title"], "Duration": store["duration"], "Stream": songInfo["url"], "AlbumArt": songInfo["album"]["image"][2]["#text"], "TopTags": songInfo["toptags"]["tag"], "Published": songInfo["wiki"]["published"], "Summary": songInfo["wiki"]["summary"]}]}

            elif data.get("lifestyle") == "Sedentary" and data.get("hobbies") == "Outdoor":
                list = ["Country", "BlueGrass", "Folk"]
                randomNum = random.randint(0, len(list)-1)
                genre = list[randomNum]
                link = "http://ws.audioscrobbler.com/2.0/?format=json&method=tag.gettoptracks&tag=" + genre + "&api_key=" + config.last_key + "&format=json"
                resp = requests.get(link).json()
                store = resp["tracks"]["track"][0]
                mbid = store["mbid"]
                newLink = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=" + config.last_key + "&mbid=" + mbid + "&format=json"
                newResp = requests.get(newLink).json()
                songInfo = newResp["track"]
                songName = songInfo["name"]
                return {"text":"How does the song " + songName + " tickle your ears? ", "question":"general", "topic":"music","type":"bot", "musicInfo": [{"Genre": genre, "Song": songInfo["name"], "Artist": songInfo["artist"]["name"], "Album": songInfo["album"]["title"], "Duration": store["duration"], "Stream": songInfo["url"], "AlbumArt": songInfo["album"]["image"][2]["#text"], "TopTags": songInfo["toptags"]["tag"], "Published": songInfo["wiki"]["published"], "Summary": songInfo["wiki"]["summary"]}]}

            elif data.get("lifestyle") == "Sedentary" and data.get("hobbies") == "Indoor":
                list = ["EDM", "Dubstep", "Trap"]
                randomNum = random.randint(0, len(list)-1)
                genre = list[randomNum]
                link = "http://ws.audioscrobbler.com/2.0/?format=json&method=tag.gettoptracks&tag=" + genre + "&api_key=" + config.last_key + "&format=json"
                resp = requests.get(link).json()
                store = resp["tracks"]["track"][0]
                mbid = store["mbid"]
                newLink = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=" + config.last_key + "&mbid=" + mbid + "&format=json"
                newResp = requests.get(newLink).json()
                songInfo = newResp["track"]
                songName = songInfo["name"]
                return {"text":"How does the song " + songName + " tickle your ears? ", "question":"general", "topic":"music","type":"bot", "musicInfo": [{"Genre": genre, "Song": songInfo["name"], "Artist": songInfo["artist"]["name"], "Album": songInfo["album"]["title"], "Duration": store["duration"], "Stream": songInfo["url"], "AlbumArt": songInfo["album"]["image"][2]["#text"], "TopTags": songInfo["toptags"]["tag"], "Published": songInfo["wiki"]["published"], "Summary": songInfo["wiki"]["summary"]}]}


        if last_question == "day":
            #run emotional analysis on the string.
            username = request.json.get("username")
            how_was_your_day = request.json.get('text')
            emotion = "Happy" #placeholder
            response = paralleldots.emotion(how_was_your_day)

            print(response)

            if response.get("emotion") is not None:
                emotion = max(response.get("emotion").items(), key=operator.itemgetter(1))[0]

            print(emotion)
            collection.find_one_and_update({"username": username},
                                {"$set": {"how_was_your_day": how_was_your_day, "emotion":emotion}})

            sentence = ''

            if emotion == "Happy":
                sentence = random.sample(["That's good to hear. ", "Nice to see you in good spirits. ", "I'm glad your chipper. "],1)
            if emotion == "Sad" or emotion == "Angry":
                sentence = random.sample(["I'm sorry your day is going so poorly. ","I hope tomorrow is better. ","Sad reacts only. "],1)
            if emotion == "Excited":
                sentence = random.sample(["Your day sounded AMAZING!!! ","I wish my day was as exciting. ","Sounds like today was a rollercoaster! "],1)
            if emotion == "Fear":
                sentence = random.sample(["I hope your days are calmer in the future. ","We have nothing to fear but fear itself. ","Never fear, the rules are here! "],1)
            if emotion == "Bored":
                sentence = random.sample(["Another day, another dollar I suppose. ", "Back to the old grind. ", "Same tbh. "], 1)

            last_question = {"text":sentence[0] + "What are some of your favorite movies? Separate each one with a \
                comma.", "type":"bot", "question":"favorite_movies", "topic":"normal"}
            return last_question


        if last_question == "favorite_movies":

            #first, create the user object
            # post = {"username":username, "how_was_your_day":how_was_your_day, "emotion":emotion, "favorite_movies":favorite_movies}
            #insert into mongo

            #then, prepend the string with a key phrase and send it to the bot. The corresponding logic adapter should pick it up and send it to Will
            username = request.json.get("username")
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
                return {"type": "bot", "text": "I'm sorry I did not find any movies with those names."}

            resp = requests.post("https://baut-ml.wls.ai/recommend", json={"ids": movieList, "user": username})
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
                if temp["Response"]=="True":
                    listings.append(temp)
            print("listings:", listings)
            return {"type": "bot", "topic": "movie", "text": "Here are some movies I found: " + listings[0]["Title"] + ", " + listings[1]["Title"] + ", " + listings[2]["Title"] + ", and more if you click on me", "movieInfo": listings, "question":"chatbot"}

        else:
            bot_output = chatbot.get_response(text)
            if bot_output.text == "Movie? Movie? I heard Movie! Tell me your favorite movies! Separate each one with a comma.":
                return {"text":bot_output.text, "type":"bot", "question":"favorite_movies", "topic":"normal"}
            elif bot_output.text == "I heard something about songs!":
                last_question = {"text":"Did you say somethings about music or songs? Tell us about yourself. Would you say that you have an Athletic, Sedentary, or Moderate lifestyle?", "question":"music_lifestyle", "topic":"questions","type":"bot","options":['Athletic','Sedentary','Moderate']}
                return last_question
            else:
                num = random.randrange(20)
                if num % 5 == 0:
                    return {"text":"Enough with the shananigans. Type in \"recommend movies\" or \"recommend songs\" to get started.","type":"bot","topic":"normal","question":"general"}
                return {"text":bot_output.text, "type":"bot", "topic":"normal","question":"chatbot"}

    bot_output = chatbot.get_response("tell me a joke")
    return {"text":"Movie? Movie? Did someone say movie? Tell me your favorite movies! Separate each one with a comma.", "type":"bot","topic":"normal", "question":"favorite_movies"}

@app.route('/api/signup', methods=['GET','POST'])
def signup():

    if request.method == 'POST':

        username = request.json.get('username')
        password = request.json.get('password')
        password = generate_password_hash(password)


        if collection.find({"username":username}).count() > 0:
            return {"Message":"User already exists!"}


        post = {"username": username, "password":password}
        token = jwt.encode({'username':username}, "SECRET_KEY")
        token = token.decode('utf-8')
        

        collection.insert_one(post)

        return {"Message":"User inserted successfully", "token":token}

    return {"Message":"You sent a post cheif"}


@app.route('/api/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        
        username = request.json.get('username')
        password = request.json.get('password')

        user_obj = collection.find_one({"username":username})

        if user_obj is None:
            return {"Message":"User was not found"}

        if check_password_hash(user_obj['password'],password):
            token = jwt.encode({'username':user_obj['username']}, "SECRET_KEY")
            token = token.decode('utf-8')
            return {"Message":"Password was correct. Login successful", "token":token}

        else:
            return {"Message":"Password Incorrect. Login unsuccessful"}

    return {"Message":"You did not send a post chief"}


@app.route('/api/save_movie',methods=['GET','POST'])
def save_movie():

    if request.method == 'POST':

        token = request.headers.get('Authorization')
        print(token)
        
        if not token:

            return {"Message":"Token is missing"}
        try:
            token = token.split()[1]
            print(token)
            decToken = jwt.decode(token,"SECRET_KEY",'utf-8')
        except Exception:
            return {"Message":"Failed to decode token"}

        username = decToken.get('username')
        print(username)
        print(request.json)
        imdbID = request.json.get('imdbID')
        print(imdbID)


        collection.find_one_and_update({"username":username,}, {'$push':{'saved_movies':imdbID}})

        return {"Message":"Movie inserted into user document"}


    return {"Message":"You did not send a post chief"}

# @app.route('/api/get_saved_movies',methods=['GET','POST'])
def get_saved_movies(token):

    # if request.method == 'POST':

    # token = request.headers.get('Authorization')
    print(token)
    
    if not token:

        return {"Message":"Token is missing"}
    try:
        # token = token.split()[1]
        print(token)
        decToken = jwt.decode(token,"SECRET_KEY",'utf-8')
    except Exception:
        return {"Message":"Failed to decode token"}

    username = decToken.get('username')
    print(username)
    # print(request.json)



    user_obj = collection.find_one({"username":username})

    listings = []
    for imdbID in user_obj.get('saved_movies'):
        postLink = "http://www.omdbapi.com/?apikey=" + config.omdb_api + "&i="
        postLink += str(imdbID)
        temp = requests.get(postLink).json()
        # print("temp:", temp)
        if temp["Response"]=="True":
            listings.append(temp)
    print("listings:", listings)




    return {"Message":"Movies fetched successfully", "savedIDs":user_obj.get('saved_movies'),"movieInfo":listings}


# return {"Message":"You did not send a post chief"}



if __name__ == "__main__":
    app.run(debug=True)
