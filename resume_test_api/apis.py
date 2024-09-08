# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
a = os.getenv('g1')
b = os.getenv('g2')
c = os.getenv('g3')
d = os.getenv('g4')
e = os.getenv('g5')
f = os.getenv('g6')
g = os.getenv('g7')
h = os.getenv('g8')
i = os.getenv('g9')



groq_keys = [a,c,e,f,g,h,i]

#542, ,y3,y1sh,billionare,jugad,03872,trillion
# eurotech,c2c
api = None
import numpy as np
def keys():
    number = np.random.randint(len(groq_keys))
    models = np.random.randint(0,2)
    return number,models
# def gemini(input,key):
#     llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",google_api_key=key, temperature=0)
#     return llm.invoke(input)
def API_func(api_key):
    global api
    api = api_key
    return api


def groq(input):
    chat = ChatGroq(
        temperature=0,
        # model="llama3-70b-8192",
        model = "llama-3.1-70b-versatile",
        # api_key=groq_keys[keys()[0]], # Optional if not set as an environment variable
        # api_key = "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",
        api_key = api
    )
    return chat.invoke(input)


def final(Input,name):
    

    print("Processing from groq")
    
    output = groq(Input).content
    print("done",name)
    return output
    