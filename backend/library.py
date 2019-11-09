TABLE = {
    'day': {"text": "Ok {}, how has your day been? This will give us some idea about what movies to \
            recommend you.", "type": "bot", "question": "day", "topic": "normal"},
    'bother_user': {"text": "Enough with the shananigans. Type in \"recommend movies\" or \"recommend songs\" to get started.", "type": "bot", "topic": "normal", "question": "general"},
    'music_prompt': {"text": "Give me a song that you like and I'll try to find some similar ones!", "type": "bot", "question": "music_prompt", "topic": "normal"},
    'movie_response': {"text": "{} What are some of your favorite movies? Separate each one with a \
            comma.", "type": "bot", "question": "favorite_movies", "topic": "normal"}
}

def fetch_response(question, username=None):
    if question not in TABLE:
        print(f'MISSING QUESTION: {question}')
        return None
    res = TABLE[question]
    res['text'] = res['text'].format(username)
    return res
