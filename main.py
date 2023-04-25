import os
import time
import random
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
            chatCompletition = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"{systemMessage}"},
                    {"role": "assistant", "content": previous_response},
                    {"role": "user", "content": prompt}
                ]
            )
            response = chatCompletition.choices[0].message.content
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
    clearOutput()
    print(f"{faceTimy} Timy")
    print(f"{response}")
    print("="*20)
    print(f"{iteration}:{userPrompt}")
    userPrompt = input(":")
    iteration += 1