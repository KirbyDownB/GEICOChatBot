# trainer = ChatterBotCorpusTrainer(chatbot)
# trainer.train(
#     "chatterbot.corpus.english.greetings",
#     "chatterbot.corpus.english.conversations"
# )


# while True:
#     try:
#         bot_input = chatbot.get_response(input())
#         print(bot_input)

#     except(KeyboardInterrupt, EOFError, SystemExit):
#         break
# jokes = requests.get("https://icanhazdadjoke.com/search",headers={'Accept': 'application/json'},params={"limit":30}).json().get("results")
# print(jokes)
# with open('jokes.pickle','wb') as f:

# pickle.dump(jokes, file_)
# pickle.dump(jokes,open('jokes.pickle','wb'))


            #if username already exists, a different prompt will occur
                #Back for more movie recommendations are you? Do you have any new movies you like or do you just want more like the ones I've recommended to you previously?
            #else, the rest of this code is fine


             

 elif count == 1:
            # Username expected

            username = request.form.get('text')

            last_question = {"text":"How has your day been? This will give us some idea about what movies/songs to recommend you.", "type":"leading","question":"day","topic":"normal"}
            count += 1
            return {"text":"How has your day been? This will give us some idea about what movies/songs to recommend you.", "type":"leading","question":"day","topic":"normal"}
        
        elif count == 2:
            # How was your day expected

            how_was_your_day = request.form.get('text')
            # calculate emotion of how was your day
            last_question = {"text":"What are some of your favorite movies? Seperate each one with a comma.", "type":"leading", "question":"favorite_movies", "topic":"normal"}
            count += 1
            return {"text":"What are some of your favorite movies? Seperate each one with a comma.", "type":"leading", "question":"favorite_movies", "topic":"normal"}

        elif count == 3:
            # Favorite movies expected

            favorite_movies = request.form.get('text').split(',')
            # create user object in mongo


            last_question = {"text":"Thanks! Here are some movie recommendations. I do more than just recommend movies you know. Try saying \"tell me a joke\", or just having a regular conversation.", "type":"leading", "question":"fav_mov_response", "topic":"movies"}
            count += 1
            return {"text":"Thanks! Here are some movie recommendations", "type":"leading", "question":"fav_mov_response", "topic":"movies"}


        else:
            text = request.form.get('text')
        
            bot_output = chatbot.get_response(text)

            return {"text":bot_output, "type":"bot"}
           if last_question.get("question") == "favorite_movies":

                #first, create the user object
                # post = {"username":username, "how_was_your_day":how_was_your_day, "emotion":emotion, "favorite_movies":favorite_movies}
                #insert into mongo

                #then, prepend the string with a key phrase and send it to the bot. The corresponding logic adapter should pick it up and send it to Will

                text = request.json.get("text")
                text = text.split(', ')
                movieList = []

                for movie in text:
                    link = "http://www.omdbapi.com/?apikey="
                    link += config.omdb_api+"&s=" + movie
                    resp = requests.get(link).json()

                    if resp["Response"]=="True":
                        movieList.append(resp['Search'][0]["imdbID"])
                    else:
                        print("failed")
                if len(movieList) == 0:
                    return {"text": "I'm sorry I did not find any movies with those names."}



                # text = "Movies:" + text

                # bot_output = chatbot.get_response(text)
                # if bot_output == "junk":
                #     return {"text":"Hmmm, those don't sound like any movies I've heard of. Can you give me any more movies you like?"}
                # return {"text":bot_output}
                return {"text": "yuhh"}
        if request.json.get('username') == "reset" or request.json.get('username') == "restart" or request.json.get('text') == "reset" or request.json.get('text') == "restart":
            print("RESTART")
            # count = 1
            username = request.json.get("username")

            last_question = {"text":"Ok {}, how has your day been? This will give us some idea about what movies to \
                    recommend you.".format(username), "type":"bot","question":"day","topic":"normal"}
            return last_question


        # if count > 0 and last_question is not None:

        #     print("Entereed movie flow")
        #     #text = request.json.get('text')
        #     username = request.json.get('username')
        #     text = request.json.get('text')
        #     last_question = request.json.get("question")

        #     print("TEXXXXT")
        #     print(text)
        #     # print(re.match(r'.*(recommend|suggest).*movies\.*', text.lower()))
        #     if last_question == "intro":
        #         username = request.json.get("username")
        #         text = request.json.get("text")
        #         #store the username in the database

        #         if collection.find({"username":username}).count() == 0:
        #             collection.insert_one({"username":username})


        #         #start the movie flow
        #         last_question = {"text":"Hi {}! Now we can begin! Try things like \"recommend me some movies\" , \"recommend music\", or \"tell me a joke\".".format(username), "question":"general", "topic":"normal", "type":"bot"}
        #         return last_question

            if last_question == "restart":

                username = request.json.get("username")

                last_question = {"text":"Hey, sorry about that {}. Even though I'm not human, I still make mistakes. If you want to get movie recommendations type \'recommend movies \'. If you want song recommendations you can say '\recommend music\'. We can just talk too.","type":"bot","topic":"normal","question":"general"}
                return last_question
