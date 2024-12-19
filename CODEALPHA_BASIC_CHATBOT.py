import random
import spacy
import time
import requests
nlp = spacy.load("en_core_web_sm")
chatbot_name = "BOT🤖"
user_name = ""
previous_intent = ""
responses = {
    "greet": [
        f"Hello! I'm {chatbot_name}. How can I assist you today? 😊",
        f"Hi there! {chatbot_name} here. How can I help you? 👋",
        f"Hey! I'm {chatbot_name}. What's on your mind? 🤔"
    ],
    "bye": [
        f"Goodbye! Have a great day! 🌟",
        f"Bye! Take care, {user_name}! 👋",
        f"See you later, {user_name}! 😄"
    ],
    "thanks": [
        f"You're welcome! - {chatbot_name} 🤗",
        f"Glad to help! - {chatbot_name} 👍",
        f"No problem! - {chatbot_name} 😊"
    ],
    "fact": [
        "Did you know? Honey never spoils! 🍯",
        "Octopuses have three hearts! 🐙",
        "Bananas are berries, but strawberries aren’t! 🍌🍓"
    ],
    "small_talk": [
        f"I'm just a chatbot, but I'm feeling great! 😄",
        f"I'm here to make your day brighter! 🌟",
        f"I'm always happy to chat! 🤗"
    ],
    "mood": [
        f"Stay positive, {user_name}! 🌈 You got this! 💪",
        f"Here's a motivational quote: 'The best way to get started is to quit talking and begin doing.' 🌟",
        f"Cheer up, {user_name}! Things always get better. 😊"
    ],
    "default": [
        f"I'm sorry, I didn't understand that. 🤷",
        f"Could you please rephrase? 🧐",
        f"Hmm, I’m not sure I follow. 😕"
    ]
}
def get_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        if response.status_code == 200:
            joke = response.json()
            return f"{joke['setup']} - {joke['punchline']} 😂"
    except:
        return "Sorry, I couldn't fetch a joke right now. Try again later! 🙁"
def typing_effect(text):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(0.03)
    print()
def identify_intent(user_input):
    doc = nlp(user_input.lower())
    if "joke" in user_input.lower() or "funny" in user_input.lower():
        return "joke"
    elif "fact" in user_input.lower() or "interesting" in user_input.lower():
        return "fact"
    elif "sad" in user_input.lower() or "bored" in user_input.lower():
        return "mood"
    elif "how are you" in user_input.lower() or "feeling" in user_input.lower():
        return "small_talk"
    elif any(token.lemma_ in ["hello", "hi", "hey"] for token in doc):
        return "greet"
    elif any(token.lemma_ in ["bye", "goodbye"] for token in doc):
        return "bye"
    elif any(token.lemma_ in ["thank", "thanks","thank you"] for token in doc):
        return "thanks"
    return "default"
def get_response(user_input):
    global previous_intent
    intent = identify_intent(user_input)
    if previous_intent == "joke" and "yes" in user_input.lower():
        intent = "joke"
    if intent == "joke":
        response = get_joke()
    else:
        response = random.choice(responses[intent])
    previous_intent = intent
    return response
def chat():
    global user_name
    typing_effect(f"{chatbot_name}: Hi! I'm BOT🤖. What's your name? 😊")
    user_name = input("You: ")
    typing_effect(f"{chatbot_name}: Nice to meet you, {user_name}! How can I help you today?")
    while True:
        user_input = input(f"{user_name}: ")
        if user_input.lower() in ["exit", "quit","bye"]:
            typing_effect(f"{chatbot_name}: Goodbye, {user_name}! Have a great day! 🌟")
            break
        response = get_response(user_input)
        typing_effect(f"{chatbot_name}: {response}")
chat()
