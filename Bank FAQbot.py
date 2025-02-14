import pandas as pd
import numpy as np
import pickle
import operator
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split as tts
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder as LE
from sklearn.metrics.pairwise import cosine_similarity
import random
import nltk
from nltk.stem.lancaster import LancasterStemmer
import pyttsx3
import speech_recognition as sr

stemmer = LancasterStemmer()
def cleanup(sentence):
    word_tok = nltk.word_tokenize(sentence)
    stemmed_words = [stemmer.stem(w) for w in word_tok]

    return ' '.join(stemmed_words)


le = LE()

tfv = TfidfVectorizer(min_df=1, stop_words='english')

data = pd.read_csv('BankFAQs.csv')
questions = data['Question'].values

X = []
for question in questions:
    X.append(cleanup(question))

tfv.fit(X)
le.fit(data['Class'])

X = tfv.transform(X)
y = le.transform(data['Class'])


trainx, testx, trainy, testy = tts(X, y, test_size=.25, random_state=42)

model = SVC(kernel='linear')
model.fit(trainx, trainy)
print("SVC:", model.score(testx, testy))


def get_max5(arr):
    ixarr = []
    for ix, el in enumerate(arr):
        ixarr.append((el, ix))
    ixarr.sort()

    ixs = []
    for i in ixarr[-5:]:
        ixs.append(i[1])

    return ixs[::-1]



# Initialize text-to-speech engine
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Index 0 for male voice, 1 for female voice
    engine.setProperty('rate', 150)  # Speed of speech
    VOICE_ENABLED = True
except Exception as e:
    print("Warning: Could not initialize text-to-speech engine:", str(e))
    VOICE_ENABLED = False

# Initialize speech recognition
try:
    recognizer = sr.Recognizer()
    # Test microphone
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
    SPEECH_RECOGNITION_ENABLED = True
except Exception as e:
    print("Warning: Could not initialize speech recognition:", str(e))
    SPEECH_RECOGNITION_ENABLED = False

def speak(text):
    """Function to convert text to speech"""
    if not VOICE_ENABLED:
        print("Text-to-speech is not available")
        return
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Error in text-to-speech:", str(e))

def listen():
    """Function to convert speech to text"""
    if not SPEECH_RECOGNITION_ENABLED:
        print("Speech recognition is not available")
        return ""
    
    with sr.Microphone() as source:
        print("Listening...")
        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5)
            print("Processing speech...")
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text.lower()
        except sr.WaitTimeoutError:
            print("No speech detected")
            return ""
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return ""
        except Exception as e:
            print("Error in speech recognition:", str(e))
            return ""

def chat():
    cnt = 0
    print("PRESS Q to QUIT")
    print("TYPE \"DEBUG\" to Display Debugging statements.")
    print("TYPE \"STOP\" to Stop Debugging statements.")
    print("TYPE \"TOP5\" to Display 5 most relevent results")
    print("TYPE \"CONF\" to Display the most confident result")
    print("TYPE \"VOICE\" to toggle voice mode")
    print()
    print()
    DEBUG = False
    TOP5 = False
    VOICE_MODE = False

    welcome_message = "Hi, Welcome to our bank!"
    print("Bot:", welcome_message)
    if VOICE_ENABLED:
        speak(welcome_message)
    else:
        print("Note: Voice features are not available. Please check if you have the required packages installed:")
        print("- pyttsx3 (for text-to-speech)")
        print("- SpeechRecognition (for speech recognition)")
        print("- pyaudio (for microphone input)")
        print("Install them using: pip install pyttsx3 SpeechRecognition pyaudio")

    while True:
        try:
            if VOICE_MODE:
                if not SPEECH_RECOGNITION_ENABLED:
                    print("Speech recognition is not available. Switching to text mode.")
                    VOICE_MODE = False
                    usr = input("You: ")
                else:
                    usr = listen()
            else:
                usr = input("You: ")
            
            if not usr:
                continue

            if usr.lower() == 'q':
                goodbye_message = "Thank you for using our service. Goodbye!"
                print("Bot:", goodbye_message)
                if VOICE_MODE and VOICE_ENABLED:
                    speak(goodbye_message)
                break

            if usr.lower() == 'voice':
                if not VOICE_ENABLED or not SPEECH_RECOGNITION_ENABLED:
                    print("Voice features are not available. Please check if required packages are installed.")
                    continue
                
                VOICE_MODE = not VOICE_MODE
                mode_message = "Voice mode " + ("activated" if VOICE_MODE else "deactivated")
                print("Bot:", mode_message)
                if VOICE_MODE:
                    speak(mode_message)
                continue

            if usr.lower() == 'yes':
                response = "Yes!"
                print("Bot:", response)
                if VOICE_MODE:
                    speak(response)
                continue

            if usr.lower() == 'no':
                response = "No?"
                print("Bot:", response)
                if VOICE_MODE:
                    speak(response)
                continue

            if usr == 'DEBUG':
                DEBUG = True
                response = "Debugging mode on"
                print(response)
                if VOICE_MODE:
                    speak(response)
                continue

            if usr == 'STOP':
                DEBUG = False
                response = "Debugging mode off"
                print(response)
                if VOICE_MODE:
                    speak(response)
                continue

            if usr == 'TOP5':
                TOP5 = True
                response = "Will display 5 most relevent results now"
                print(response)
                if VOICE_MODE:
                    speak(response)
                continue

            if usr == 'CONF':
                TOP5 = False
                response = "Only the most relevent result will be displayed"
                print(response)
                if VOICE_MODE:
                    speak(response)
                continue

            t_usr = tfv.transform([cleanup(usr.strip().lower())])
            prediction = model.predict(t_usr)
            class_ = le.inverse_transform([prediction])[0]
            questionset = data[data['Class']==class_]

            if DEBUG:
                print("Question classified under category:", class_)
                print("{} Questions belong to this class".format(len(questionset)))

            cos_sims = []
            for question in questionset['Question']:
                sims = cosine_similarity(tfv.transform([question]), t_usr)
                cos_sims.append(sims)
                
            ind = cos_sims.index(max(cos_sims))

            if DEBUG:
                question = questionset["Question"][questionset.index[ind]]
                print("Assuming you asked: {}".format(question))

            if not TOP5:
                response = data['Answer'][questionset.index[ind]]
                print("Bot:", response)
                if VOICE_MODE:
                    speak(response)
            else:
                inds = get_max5(cos_sims)
                for ix in inds:
                    print("Question: "+data['Question'][questionset.index[ix]])
                    response = "Answer: "+data['Answer'][questionset.index[ix]]
                    print(response)
                    if VOICE_MODE:
                        speak(response)
                    print('-'*50)

            print("\n"*2)
            feedback_question = "Was this answer helpful? Yes/No: "
            print(feedback_question, end='')
            if VOICE_MODE:
                speak(feedback_question)
                outcome = listen()
            else:
                outcome = input().lower().strip()

            if outcome == 'yes':
                cnt = 0
            elif outcome == 'no':
                inds = get_max5(cos_sims)
                suggestion_question = "Do you want me to suggest you questions? Yes/No: "
                print("Bot:", suggestion_question, end='')
                if VOICE_MODE:
                    speak(suggestion_question)
                    sugg_choice = listen()
                else:
                    sugg_choice = input().lower()

                if sugg_choice == 'yes':
                    q_cnt = 1
                    for ix in inds:
                        print(q_cnt,"Question: "+data['Question'][questionset.index[ix]])
                        if VOICE_MODE:
                            speak(f"Question {q_cnt}: "+data['Question'][questionset.index[ix]])
                        print('-'*50)
                        q_cnt += 1
                    
                    number_question = "Please say or enter the question number you find most relevant: "
                    print(number_question, end='')
                    if VOICE_MODE:
                        speak(number_question)
                        while True:
                            num_str = listen()
                            try:
                                num = int(num_str)
                                if 1 <= num <= 5:
                                    break
                                speak("Please say a number between 1 and 5")
                            except ValueError:
                                speak("Please say a valid number")
                    else:
                        num = int(input())
                    
                    response = data['Answer'][questionset.index[inds[num-1]]]
                    print("Bot:", response)
                    if VOICE_MODE:
                        speak(response)

        except EOFError:
            goodbye_message = "\nBot: Goodbye! Thank you for using our service."
            print(goodbye_message)
            if VOICE_MODE:
                speak(goodbye_message)
            break
        except KeyboardInterrupt:
            goodbye_message = "\nBot: Goodbye! Thank you for using our service."
            print(goodbye_message)
            if VOICE_MODE:
                speak(goodbye_message)
            break
        except Exception as e:
            error_message = "I'm sorry, I couldn't process that. Could you please try again?"
            print("Bot:", error_message)
            if VOICE_MODE:
                speak(error_message)
            if DEBUG:
                print("Error:", str(e))
            continue

if __name__ == "__main__":
    chat()
