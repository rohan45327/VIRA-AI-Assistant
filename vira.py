import google.generativeai as genai
import os
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
import datetime
import requests
import os
import webbrowser
import wmi
import random
import json
import re
import wikipedia
import smtplib
from email.message import EmailMessage
import fitz
load_dotenv()
GEMINI_API=os.getenv("gemini-api")
if GEMINI_API:
    genai.configure(api_key=GEMINI_API)
    GEMINI_MODEL = genai.GenerativeModel('gemini-2.5-flash')
else:
    GEMINI_MODEL = None
API_KEY=os.getenv("weather")
COUNTRY ='IN'
hippocampus="memory.json"
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
engine = pyttsx3.init()
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-AU_James_11.0')
engine.setProperty('rate', 179)
engine.setProperty('volume', 100)
def speak(text):
    engine.say(text)
    engine.runAndWait()
def listen(timeout_val=4, phrase=5):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"{Colors.YELLOW}Listening...{Colors.RESET}")
        r.pause_threshold = 1.5 #breaks
        try:
            audio = r.listen(source, timeout=timeout_val, phrase_time_limit=phrase) #lis
            print(f"{Colors.BLUE}Recognizing...{Colors.RESET}")
            query = r.recognize_google(audio, language='English')
            print(f"{Colors.CYAN}You said: {Colors.RESET}{Colors.WHITE}{query}{Colors.RESET}\n")
            return query.lower()
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout.")
            return ""
        except sr.UnknownValueError:
            print("Sorry, I could not understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""
def get_weather(city, country_code, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city},{country_code}&appid={api_key}&units=metric"
    print(f"Fetching weather from: {complete_url}")
    try:
        response = requests.get(complete_url)
        data = response.json()
        if data["cod"] != "404":
            main_data = data["main"]
            weather_data = data["weather"][0]

            temperature = main_data["temp"]
            feels_like = main_data["feels_like"]
            description = weather_data["description"]
            humidity = main_data["humidity"]

            return (f"The temperature in {city} is {temperature:.1f} degrees Celsius, "
                    f"but it feels like {feels_like:.1f} degrees Celsius. "
                    f"The weather is {description} with {humidity}% humidity.")
        else:
            return "Sorry, I couldn't find weather information for that city."
    except requests.exceptions.ConnectionError:
        return "Sorry, I can't connect to the internet to get weather information."
    except Exception as e:
        print(f"An error occurred while fetching weather: {e}")
        return "Sorry, something went wrong while getting the weather."
def date():
    now=datetime.datetime.now
    return now().strftime("%A, %B %d, %Y")
def define_word(word):
    if not word:
        return "Please tell me a word"

    api = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    speak(f"Fetching definition for: {word}")
    try:
        response = requests.get(api)
        data = response.json()

        if isinstance(data, dict) and data.get('title') == 'No Definitions Found':
            return f"Sorry, I couldn't find a definition for '{word}'."

        if isinstance(data, list) and len(data) > 0:
            first_entry = data[0]
            if 'meanings' in first_entry and len(first_entry['meanings']) > 0:
                first_meaning = first_entry['meanings'][0]

                if 'definitions' in first_meaning and len(first_meaning['definitions']) > 0:
                    definition = first_meaning['definitions'][0].get('definition')
                    example = first_meaning['definitions'][0].get('example')

                    response = f"The definition of {word} is: {definition}."
                    if example:
                        response += f" For example: {example}."
                    return response
        else:
            return f"Sorry, something unexpected happened while looking up '{word}'."

    except requests.exceptions.ConnectionError:
        return "Sorry, I can't connect to the internet to define words."
    except Exception as e:
        print(f"An error occurred while defining word: {e}")
        return "Sorry, something went wrong while trying to define that word."
def open_app(app_name):
    app_name=app_name.lower()
    if(os.name=='nt'):
        if "chrome" in app_name:
            os.startfile("chrome.exe")
            return "opening chrome"
        elif "notepad" in app_name:
            os.startfile("notepad.exe")
            return "opening notepad"
        elif "calculator" in app_name:
            os.startfile("calc.exe")
            return "opening calculator"
        elif "calendar" in app_name:
            os.startfile("HxCalendarAppImm.exe")
            return "opening calendar . Say cheese!!."
        else:
            return f"I dont know how to open {app_name}"
def brightness(value):
    if not 0<=value<=100:
        return "THE BRIGHTNESS LEVEL SHOULD BE BETWEEN 0 to 100"
    try:
        m= wmi.WMI(namespace='root\\WMI')
        times=m.WmiMonitorBrightnessMethods()
        for n in times:
            n.WmiSetBrightness(value, 1)
        return f"BRIGHTNESS OF YOUR DEVICE IS SUCCESSFULLY SET TO {value} percent"
    except Exception as e:
        return "SORRY . PLEASE CHECK THAT YOU INSTALLED THE WINDOWS MANAGEMENT INSTRUMENTATION ON YOUR DEVICE"
def crack_jack():
    url = "https://official-joke-api.appspot.com/jokes/random"
    response = requests.get(url)
    response.raise_for_status()
    joke_data = response.json()
    if "setup" in joke_data and "punchline" in joke_data:
            return f"{joke_data['setup']} ...... {joke_data['punchline']}"
    elif "joke" in joke_data:
            return joke_data["joke"]
    else:
        print("Unexpected response from Official Joke API:", joke_data)
        return "I couldn't fetch a joke right now. My joke circuitry is feeling down."
def food_recipe(food_item: str) -> str:
    api=os.getenv("food")
    if not api:
        return "Invalid Api key"
    url = "https://api.api-ninjas.com/v1/recipe"
    sparams = {
        "query": food_item,
    }
    headers = {
        "X-Api-Key": api}
    try:
        response = requests.get(url, params=sparams, headers=headers)
        response.raise_for_status()
        data = response.json()

        if not data:
            return f"I couldn't find any recipes for '{food_item}' using API-Ninjas. Please try a different food item or a more general search term."

        recipe_info = data[0]
        
        meal_name = recipe_info.get('title')
        ingredients_1 = recipe_info.get('ingredients', '') 
        instructions_1 = recipe_info.get('instructions', '')
        
        ingredients = [ing.strip() for ing in ingredients_1.split('\n') if ing.strip()]
        if not ingredients and ',' in ingredients_1:
             ingredients = [ing.strip() for ing in ingredients_1.split(',') if ing.strip()]
        if not ingredients:
            ingredients = [ingredients_1] if ingredients_1 else ["No ingredients listed."]
        response_string = f"Here's the recipe for {meal_name}: \n\n"
        response_string += "Ingredients:\n" + "\n".join([f"- {ing}" for ing in ingredients]) + ".\n\n"
        response_string += "Instructions: " + instructions_1
        if len(response_string) > 1000:
            spoken_ingredients = ", ".join(ingredients[:5]) + ("..." if len(ingredients) > 5 else "")
            spoken_instructions_for_speak = instructions_1[:500]
            if len(instructions_1) > 500:
                 spoken_instructions_for_speak += "...."
                 response_string_for_speak = f"Here's the recipe for {meal_name}. Ingredients: {spoken_ingredients}. Instructions: {spoken_instructions_for_speak}. Check the chat log for full details and link."
                 return {response_string_for_speak}
        else:
            return response_string
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 402:
            return "My recipe search quota for Spoonacular is exhausted for today. Please try again tomorrow or check your API key usage."
        elif http_err.response.status_code == 401:
            return "Spoonacular API key is invalid or unauthorized. Please check your API key in jarvis.py."
        else:
            print(f"HTTP error fetching recipe: {http_err}")
            return "I'm having trouble with the recipe API. Please check your internet connection or API key."       
def song(song_query: str) -> str:
    key=os.getenv("youtube")
    if not key:
        return "YouTube API key is not set. Please set it in jarvis.py to play songs."

    search_url = "https://www.googleapis.com/youtube/v3/search"
    sparams = {
        "part": "snippet",
        "q": song_query,
        "maxResults": 1,
        "type": "video",
        "key": key
    }
    try:
        response = requests.get(search_url, params=sparams)
        response.raise_for_status()
        data = response.json()
        items = data.get('items')
        if items[0]['id']['kind'] == 'youtube#video':
            video_id = items[0]['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            return  webbrowser.open(video_url)
        else:
            return f"I couldn't find a video for '{song_query}' on YouTube."
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error fetching YouTube video: {http_err}")
        return "I'm having trouble accessing YouTube right now. Please check your internet connection or API key."
    except Exception as e:
        print(f"An unexpected error occurred while fetching a YouTube video: {e}")
        return "I encountered an error while trying to find that song on YouTube."
def news():
    url= f"https://newsapi.org/v2/everything?q='India'&sortBy=popularity&apiKey=033fcf197b9d44858cacc937574da967"
    try:
        response=requests.get(url)
        response.raise_for_status()
        data=response.json()
        news=data.get('articles',[])
        if not news:
            return "sorry could fetch results for that"
        headlines=[]
        for i, article in enumerate(news[:5]):
            title = article.get('title', 'No title')
            source = article.get('source', {}).get('name', 'Unknown Source')
            headlines.append(f"{i+1}. {title} (Source: {source})")
        spoken = "Here are the top headlines: " + ", ".join([f"{i+1}. {article.get('title', '')}" for i, article in enumerate(news[:5])]) + ". For more details, please check the news."
        return spoken
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return "Sorry, I'm having trouble accessing the news service right now.", "Sorry, I'm having trouble accessing the news service right now."
    except Exception as e:
        return "An error occured while processing the news Please try again. Or check your Internet connection"
def wiki(query , sentences=2):
    try:
        wikipedia.set_lang("en")
        page=wikipedia.search(query)
        if not page:
            return "Error Not found that thing"
        summary=wikipedia.summary(page[0],sentences=sentences)
        summary = summary.split(' (listen)')[0]
        summary = summary.split(' (/')[0]
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        options = ", ".join(e.options[:5])
        return f"Your query is ambiguous. Do you mean: {options}, or something else?"
    except wikipedia.exceptions.PageError:
        return f"Sorry, I couldn't find a Wikipedia page matching '{query}'."
def fact():
    api=os.getenv("food")
    url="https://api.api-ninjas.com/v1/facts"
    headers={'X-Api-Key': api}
    try:
        response=requests.get(url,headers=headers)
        response.raise_for_status()
        data=response.json()
        if data and isinstance(data,list) and len(data)>0 and 'fact' in data[0]:
            return data[0]['fact']
        else:
            return "Sorry, I couldn't fetch a random fact right now."
    except requests.exceptions.RequestException as e:
        print(f"Error fetching fact: {e}")
        return "Sorry, I'm having trouble accessing the fact service right now."
    except Exception as e:
        print(f"An unexpected error occurred while fetching a fact: {e}")
        return "An unexpected error occurred while fetching a fact."
def convert(text):
    ssml_text = re.sub(r'\*\*(.*?)\*\*',' ',text)
    ssml_text = re.sub(r'\*(.*?)\*', ' ',ssml_text)
    return ssml_text
def write_email(to,sub,body):
    email=EmailMessage()
    email['From']='chandujoshita47@gmail.com'
    email['To']=to
    email['Subject']=sub
    email.set_content(body)
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login('chandujoshita47@gmail.com','chandu@123456',True)
        smtp.send_message(email)
    return "mail Sent Sucessfully"
def get_summary(inst,pdf_file):
    try:
        pdf_file.seek(0)
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        if GEMINI_MODEL:
            prompt = f"{inst}:\n" + text
            response = GEMINI_MODEL.generate_content(prompt)
            return f"{inst} for {response.text.replace('*','\n')}"
        else:
            return "Gemini API is not configured to summarize text."
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return "Sorry, I had trouble processing that PDF."
def load():
    if os.path.exists(hippocampus):
        try:
            with open(hippocampus, 'r') as h:
                content = h.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except json.JSONDecodeError:
            return {}
def save(data):
    with open(hippocampus,'w') as h:
        return json.dump(data,h,indent=4)
    print(f"[Memory Saved] → {os.path.abspath(hippocampus)}")
def update(key,val):
    memo=load()
    memo[key]=val
    save(memo)
def get(key):
    memo=load()
    return memo.get(key)
def forget(key):
    memo = load()
    if key in memo:
        del memo[key]
        save(memo)
        return f"I Deleted {key} from my storage.."
    return f"I don't remember anything about {key}."
def web_command(command):
    command = command.lower()
    cur = datetime.datetime.now().strftime("%p")
    if cur == "PM":
        word = "AFTERNOON "
    else:
        word = "MORNING "
    respond = ["Yes sir!!", "How can I help you?", "Yeah tell me.", f"Good {word} sir!"]
    wake = random.choice(respond)
    command_map = {
        "hello vira": lambda: f"{wake}",
        "search wikipedia for": lambda q: f"According to Wikipedia, {wiki(q)}",
        "play": lambda q: f"Playing {q} from Youtube. {song(q)}",
    }
    if "weather" in command:
        city_match = re.search(r'(?:in|for)\s+([a-zA-Z\s]+)', command)
        if city_match:
            city_name = city_match.group(1).strip()
            return  get_weather(city_name, COUNTRY, API_KEY)
        else:
            return f"What city's weather would you like to know?"
    elif re.search(r'\b(what\'s|what is|tell me)\s+today\'s|the\s+date\b|(\bcurrent\s+date)|date\b', command):
        return f"Today's date is {date()}."
    elif re.search(r'\b(what\'s|what is|tell me)\s+the\s+time\b|\bcurrent\s+time|time\b', command):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."
    elif re.search(r'define\s+(.+)|meaning\s+of\s+(.+)', command):
        word_match = re.search(r'define\s+(.+)', command)
        if not word_match:
            word_match = re.search(r'meaning\s+of\s+(.+)', command)
        
        if word_match:
            word_to_define = word_match.group(1) if word_match.group(1) else word_match.group(2)
            return f"{define_word(word_to_define.strip())}"
        else:
            return "Please tell me which word you would like to define."
    elif re.search(r'open\s+(notepad|chrome|web browser|google chrome|calculator|calendar|youtube|google|whatsapp)\b', command):
        app = re.search(r'open\s+(notepad|chrome|web browser|google chrome|calculator|calendar|youtube|google|whatsapp)\b', command)
        if app:
            app_name = app.group(1)
            return open_app(app_name)
    elif "launch " in command:
        sd=command.replace("launch","").strip()
        return webbrowser.open(f"https://www.google.com/search?q={sd}.com"),f"OPENING {sd}"
    elif  re.search(r'set (?:screen )?brightness to (\d{1,3})(?: percent|%)?', command):
        brightness_match = re.search(r'set (?:screen )?brightness to (\d{1,3})(?: percent|%)?', command)
        if brightness_match:
            try:
                level = int(brightness_match.group(1))
                return brightness(level)
            except ValueError:
                return "I didn't understand the brightness level ☀. Please say a number like 'set brightness to 70 percent'."
        else:
            return "Sorry, I can only set the screen brightness to a specific percentage."
    elif "stop" in command or "exit" in command or "quit" in command or "go to sleep" in command:
        return "Goodbye! It was nice interacting with you."
    elif re.search(r'jarvis\s+(roll the dice|roll a dice)|(roll a dice\s|roll the dice\s)+(jarvis)|roll a dice\b', command):
       dice=["1","2","3","4","5","6"]
       val=random.choice(dice)
       return f"it is {val}"
    elif re.search(r'jarvis\s+(tell me a joke|crack a joke)|tell me a joke\s|crack a joke\s+(jarvis)|crack a joke\b',command):
        krack=crack_jack()
        phrase=["Okay the joke is ","Get Ready to laugh "]
        lumi=random.choice(phrase)
        return f"{lumi} . {krack}"
    elif "flip a coin" in command:
        coin=["Heads","Tails"]
        return f"it was :{random.choice(coin)}"
    elif "recipe for" in command or "how to make an" in command:
        if "recipe for" in command:
            item=command.split("recipe for ", 1)
        else:
            item=command.split("how to make an ",1)
        if len(item)>1:
            food_item = item[1].strip()
            if food_item:
                recipe_result = f"{food_recipe(food_item)}"
        else:
            return "Please tell me what food item you want a recipe for."
        return f"{recipe_result}"
    elif "news" in command or "headlines" in command:
        eric=news()
        return f"{eric}"
    elif re.search(r'send mail\s + subject\s+(.+)\s +body\s+(.+)', command):
        mail_match = re.search(r'send mail\s + subject\s+(.+)\s +body\s+(.+)', command)
        if mail_match:
            tomail = "chandujoshita47@gmail.com"
            subject = mail_match.group(1).strip()
            body = mail_match.group(2).strip()
            full_body = GEMINI_MODEL.generate_content(f"Give me body of an mail for this scenario {body}")
            if "@" in tomail and "." in tomail:
                response = write_email(tomail, subject, full_body)
                return response
            else:
                return "The email address seems invalid. Please provide a full email address."
        else:
            return "Sorry, I couldn't understand the command. Please say 'send mail to [email] as subject [subject] and body as [message]'."
    elif "wikipedia" in command or "search wikipedia" in command:
        query = command.replace("search wikipedia for", "").replace("wikipedia", "").strip()
        if query:
            summary = wiki(query, sentences=2)
            w=["According to my reach","The results are","Thats interesting here is all about"]
            word=random.choice(w)
            return f"{word}. {summary}"
        else:
            return "What would you like to search on Wikipedia?"
    elif "tell me a fun fact" in command or "give me a fact" in command or "random fact" in command or "fact" in command:
        facts = fact()
        return f"The fact is :{facts}"
    elif "story of jarvis" in command or "your journey" in command:
        return " I am jarvis an Speech assistant from normal if else commands To large NPL language. I have Faced many rejections but now I was Updated to provide powerfull and impactfull solutions. Thanks for trusting and choosing me as your Assistant."
    elif "who are you" in command or "about yourself" in command:
        return "I am Jarvis an Powerfull Speech Assistant. I can answer any queries asked by you."
    elif "created you" in command:
        return "I was created by Rohan on May 2025."
    elif "remember" in command:
        text = command.replace("remember", "", 1).strip()
        if " is " in text:
            key, value = text.split(" is ", 1)
            key, value = key.strip(), value.strip()
            memo=load()
            save(memo)
            update(key, value)
            if "my" in key:
                key= key.replace('my','your')
            return f"Okay, I will remember that {key} is {value}."
        return "Please tell me in the format => Key is Value"
    elif "when is" in command or "what is" in command:
        key = command.replace("what is", "").replace("when is", "").strip()
        value = get(key)
        print(f"[Memory Saved] → {os.path.abspath(hippocampus)}")
        if value:
            if key.startswith("my "):
                phrase = key.replace("my", "your", 1).capitalize()
            elif key.startswith("your "):
                phrase = key.replace("your", "my", 1).capitalize()
            else:
                phrase = key.capitalize()
            return f"{phrase} is {value}."
        else:
            gemini_response = GEMINI_MODEL.generate_content(command)
            if gemini_response or hasattr(gemini_response, 'text'):
                return f"{convert(gemini_response.text)}"
            else:
                return "Error calling Api"
    elif "forget" in command or "forgot" in command:
        key = command.replace("forget", "").replace("forgot","").strip()
        memo = load()
        if key in memo:
            del memo[key]
            save(memo)
            if "my" in key:
               key= key.replace('my','your',1)
               return f"Okay, I forgot {key}."
        else:
            gemini_response = GEMINI_MODEL.generate_content(command)
            if gemini_response or hasattr(gemini_response, 'text'):
                return f"{convert(gemini_response.text)}"
            else:
                return "Error calling api"
    for trigger, func in command_map.items():
        if trigger in command:
            query = command.replace(trigger, "").strip()
            if query and func.__code__.co_argcount > 0:
                return func(query)
            elif func.__code__.co_argcount == 0:
                return func()
    if GEMINI_MODEL:
        try:
            print(f"No specific command matched. Searching for : {command}")
            gemini_response = GEMINI_MODEL.generate_content(command)
            if gemini_response or hasattr(gemini_response, 'text'):
                return f"{convert(gemini_response.text)}"
        except Exception as e:
            return f"Error calling API: {e}"
    return "I'm not sure how to respond to that. My advanced AI brain is not configured."