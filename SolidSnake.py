# regex replacement table from assignment

pronoun_replacements = [
    (r'\b([Tt]hey|[Ww]e)\'re\b', r'\1 are'),
    (r'\b[Ii]t\'s\b', r'it is'),
    (r'\b[Tt]hat\'s\b', r'that is'),
    (r'\b[Ii] am\b', 'you are'),
    (r'\b[Ii]\'m\b', 'you are'),
    (r'\b([Ii]|me)\b', 'you'),
    (r'\b[Mm]y\b', 'your'),
    (r'\b[Mm]ine\b', 'yours')
]

import csv
import spacy
nlp = spacy.load('en_core_web_sm', disable=['parser','ner'])

# you need the brysbaert csv for this to work
def read_concreteness(f='brysbaert_concreteness.csv'):
    concreteness = {}
    
    with open(f, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            word = row['Lemma']
            value = float(row['Conc.M'])
            
            concreteness[word] = value
    
    return concreteness


import re

def snake_method(file_path):
    concreteness = read_concreteness()

    # always treat input as a file, breaks if try to do both
    with open(file_path, encoding='utf-8') as f:
        text = f.read()

    for pattern, replace in pronoun_replacements:
        text = re.sub(pattern, replace, text)
    # spacy text -> tokens
    doc = nlp(text)

    scored = []

    # run all words through concreteness
    for token in doc:
        # lemmatize all words
        lemma = token.lemma_.lower()
        if lemma in concreteness:
            score = concreteness[lemma]
        else:
        # give stuff like names a score so they at least show up
            score = 2

        scored.append((token.text, score))

    # brute force if nothing works and just use the original phrase
    if not scored:
        phrase = text
    else:
        # sort by concreteness
        scored.sort(key=lambda x: x[1], reverse=True)

        # take top few unique words
        words = []
        # scored is tuple but we only care about first element and if we've used it
        for word, blah in scored:
            if word.lower() not in [w.lower() for w in words]:
                words.append(word)

        phrase = " ".join(words)

    # flip pronoun with regex replacement table
    for pattern, replace in pronoun_replacements:
        phrase = re.sub(pattern, replace, phrase)
    phrase = phrase.strip()
    if phrase:
        phrase = phrase[0].upper() + phrase[1:].lower()

    return phrase + ", huh?"

# UNUSED. I was able to get a chat loop going if the input was purely text, but it breaks if I try to make it text file OR text input.
def talk_to_snake():
    while True:
        user_input = input("You: ")

        # Type quit to quit.
        if user_input.lower() == 'quit':
            print("Snake: The Colonel needs me.")
            break

        # now user_input is expected to be a file path
        response = snake_method(user_input)
        print("Snake:", response)