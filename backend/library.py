TABLE = {
    'day': {"text": "Ok {}, how has your day been? This will give us some idea about what movies to \
            recommend you.", "type": "bot", "question": "day", "topic": "normal"},
    'music_lifestyle': {"text": "TODO", "type": "bot", "question": "TODO", "topic": "normal"}
}


def fetch_response(question, username=None):
    if question not in TABLE:
        print(f'MISSING QUESTION: {question}')
        return None
    res = TABLE[question]
    res['text'] = res['text'].format(username)
    return res
