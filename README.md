# VIRA-AI-Assistant
VIRA- Virtually Integrated Assistant helps in your Daily tasks with voice and text. Inspired from jarvis
**VIRA is a versatile, full-stack voice assistant built using Python (Flask/Gunicorn) and JavaScript.**
VIRA handles voice, keyboard, and file inputs, and uses the Google Gemini API for powerful, multimodal intelligence.
##  Main Theme of VIRA and Working:
* The Vira was made with the intention to help users on there daily tasks.
* It has wide range of features like pdf-summary, letter writting, email writing, funny convo etc.
* While falling to technical part it can write codes, fix errors, suggest brainstorms etc.
* I kept total of four level search mechanism
    - Memory search
    - Basic commands
    - Api Knowledge
    - LLM model search
* 1st Vira looks into Memory for any past queries if yes gives response for that from it's memo else
* 2nd It fall to basic commands like Hello, Hi, Time, Date etc. To decrease the use of tokens.
* 3rd If the command is not catched, It uses the API knowledge for Real time Knowledge like Weather, News, sports etc.
* 4th The main LLM Brain for Reasoning and Generative quires.

##  Features:
* **Multimodal Input:** Accepts commands via voice (microphone),keyboard text input, and file upload.<br>
* **Secure File Processing:** Analyzes and reviews PDF and Image files based on a user-provided text instruction (e.g., "Summarize this PDF").<br>
* **Typing Animation:** Features a smooth, character-by-character typing animation for VIRA's responses, enhancing UX.
* **Styled Output:** Renders Markdown (bold text, code blocks) directly in the chat log.
* **Core Utility:** Handles weather, definitions, news headlines, jokes, memory recall, and application launching (locally).
* The many other feauters like WMI brightness control, opening Apps, launching Sites, songs are disabled due to Error while Building in Railway production. Please Visit the
  repo in my github to see the full Python file of Vira
##  Technology: 
* **Backend Framework** : Flask (Python)Lightweight, flexible WSGI micro-framework for API handling.
* **Production Server** : GunicornStable, production-grade WSGI server for cloud deployment
* **Intelligence** : Google Gemini 2.5 FlashFast, high-capacity Large Language Model (LLM) for reasoning and summarization.
* **File Handling** : PyMuPDF / PyPDF Library for reliable PDF text extraction.
* **Frontend/UI** : HTML5, CSS3, JavaScript Cross-device compatibility and high-performance client-side logic (Web Speech API).
* **Deployment** : Hugging Face with Docker Images.**
##  Getting Started (Local Setup):
**Follow these instructions to run VIRA locally on your machine.**
#### * Prerequisites:
- Python 3.11+ installed.
- A Gemini API Key (available from Google AI Studio).
#### * Installation Steps:
Clone the Repository:
- ``` git clone https://github.com/rohan45327/VIRA-AI-Assistant.git ```
- cd VIRA-AI-Assistant
#### * Install Dependencies:
- ```pip install -r requirements.txt```
- configure your api keys as gemini-key, openweather as weather, api ninjas as food more refer to the vira.py file for more details
#### * Run the Server:
- ```gunicorn app:app --workers 4 --timeout 120```
- Open your browser and navigate to the URL displayed by Gunicorn (e.g., http://127.0.0.1:8000/static/vira.html).
##  License:
#### This project is licensed under the Apache License 2.0. See the LICENSE file for details.
##  Contact:
#### Creator: K. Satya Rohan
#### GitHub: @rohan45327
#### Email: chandujoshita47@gmail.com
