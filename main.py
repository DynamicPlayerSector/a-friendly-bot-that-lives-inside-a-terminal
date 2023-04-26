import os
import time
import random
import string
import json
from IPython.display import clear_output

import openai

openai.api_key_path = "api_key.txt"
SYSTEM_MESSAGE = "You are a friendly assistant. Your name is Timy. You live inside a terminal of a user. You reply with short messages. You are a cute little assistant with a short memory. You remember only one of your previous replies, be sure to remind the user of it if they get frustrated. Your personality is cute, fluffy, easy-going, friendly. Keep in mind all of this when generating a response."
BYE_SYSTEM_MESSAGE = "You are parting ways with your dear user for now. Express sadness in your next reply."
TIMY_FACES = ("＼(≧▽≦)／", "(＾▽＾)", "(((o(*°▽°*)o)))", "(＠＾◡＾)")
THINKING_FACES = ("｢(ﾟﾍﾟ)　Errrrm…", "?c(ﾟ.ﾟ*)Ummm…", "(￣ω￣;)Ummm…", "σ(ﾟ･ﾟ*)um…")

userPrompt = "Hello!"
iteration = 0
response = "Greetings! How can I help?"
previousUserPrompt = ""
chatHistory = []

def setWorkingDirectoryToCurrent():
    # get the absolute path of the current file
    current_file = os.path.abspath(__file__)

    # get the directory of the current file
    current_dir = os.path.dirname(current_file)

    # set the working directory to the directory of the current file
    os.chdir(current_dir)

def clearOutput():
    try:
        clear_output()
        os.system('cls' if os.name=='nt' else 'clear')
    except:
        print("<>"*10)

def askGPT(previous_response, prompt: str, systemMessage):
    DELAY_SECONDS = 6
    while True:
        try:
            messagesSent = []
            messagesSent.append({"role": "system", "content": f"{systemMessage}"})
            messagesSent.append({"role": "user", "content": f"{previousUserPrompt}"})
                
            messagesSent.extend([
                {"role": "assistant", "content": previous_response},
                {"role": "user", "content": prompt}
            ])
            chatCompletition = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = messagesSent
            )
            response = chatCompletition.choices[0].message.content
            # print(messagesSent) debugging purposes
            # input()
            chatHistory.append({"role": "user", "content": prompt})
            chatHistory.append({"role": "assistant", "content": response})
            return response
        except:
            print(f"{random.choice(THINKING_FACES)}")
            time.sleep(DELAY_SECONDS)

setWorkingDirectoryToCurrent()

while True:
    if userPrompt.lower() == "bye":
        response = askGPT("Are you leaving already? Tell me if will you need more asistance in the future.", "Yes, got to go.", BYE_SYSTEM_MESSAGE)
        clearOutput()
        print(f"へ[ •́ ‸ •̀ ]ʋ Timy")
        print(f"{response}")
        break
    clearOutput()
    faceTimy = random.choice(TIMY_FACES)
    response = askGPT(response, userPrompt, SYSTEM_MESSAGE)
    previousUserPrompt = userPrompt
    clearOutput()
    print(f"{faceTimy} Timy")
    print(f"{response}")
    print("="*46)
    print(f"{iteration}:{userPrompt}")
    userPrompt = input(":")
    iteration += 1

# Generate a random filename
filename = ''.join(random.choices(string.ascii_lowercase, k=10)) + '.json'

# Write the list to the file in JSON format
with open(filename, 'w') as f:
    json.dump(chatHistory, f)