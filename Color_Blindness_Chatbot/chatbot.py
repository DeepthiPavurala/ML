import tkinter as tk
from tkinter import messagebox, Button
import requests
import spacy
import subprocess
import re
import random
import uuid
from gtts import gTTS
import os
from playsound import playsound
from langdetect import detect


# spaCy model (one-time execution)
subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])  # Using "en_core_web_sm" for efficiency

user_name = None
user_language = None

# keyword match responses
pattern_responses = [
    (r"\b(?:types|kinds)\b", [
        "There are several types of color blindness, including red-green color blindness and blue-yellow color blindness.",
        "Common types of color blindness include protanopia, deuteranopia, and tritanopia."
    ]),
    (r"\bprotanopia\b", [
        "Protanopia is a type of red-green color blindness where individuals have difficulty perceiving red hues.",
        "People with protanopia may struggle to distinguish between reds and greens, which can affect various aspects of daily life."
    ]),
    (r"\bdeuteranopia\b", [
        "Deuteranopia is another type of red-green color blindness characterized by a weakness in perceiving green hues.",
        "Individuals with deuteranopia may have difficulty distinguishing between greens and reds, which can impact tasks like reading traffic lights or interpreting color-coded information."
    ]),
    (r"\btritanopia\b", [
        "Tritanopia, also known as blue-yellow color blindness, affects how individuals perceive blue and yellow hues.",
        "People with tritanopia may struggle to differentiate between blues and yellows, making tasks like reading traffic lights or identifying certain colors in twilight challenging."
    ]),
    (r"\bred-green color blindness\b", [
        "Red-green color blindness is the most common type, affecting how people perceive reds and greens. There are variations within this category, such as protanopia (weakness in red perception) and deuteranopia (weakness in green perception).",
        "Many people with color blindness have difficulty distinguishing between reds and greens. This can be caused by protanopia, deuteranopia, or other variations of red-green color blindness."
    ]),
    (r"\bblue-yellow color blindness\b", [
        "Blue-yellow color blindness, also known as tritanopia, is a less common type where people have trouble differentiating between blues and yellows. It can make distinguishing certain colors in twilight or under colored lighting difficult.",
        "Tritanopia, or blue-yellow color blindness, affects how someone perceives blue and yellow hues. This can make tasks like reading traffic lights or interpreting color-coded information challenging."
    ]),
    (r"\btest(s)?|diagnosed\b", [
        "There are various tests for color blindness, including the Ishihara color vision test and the Farnsworth-Munsell 100 hue test. I can provide you one for Red Green color blindness, click on the Color Blind Test button to take test.",
        "Color blindness tests like Ishihara color vision test help diagnose color vision deficiencies. I can provide you one for Red Green color blindness, click on the Color Blind Test button to take test."
    ]),
    (r"\btreatment(s)?|cure|treated\b", [
        "Currently, there is no cure for color blindness. However, some aids and tools can help people with color vision deficiency distinguish colors better.",
        "Treatment options for color blindness are limited, but researchers are exploring gene therapy and other interventions."
    ]),
    (r"\bcause(s)?\b", [
        "Color blindness can arise from two main causes:\n 1) Inherited genetic defects in the cone cells of the retina responsible for color vision, and \n 2) Damage to the eye, optic nerve, or parts of the brain responsible for processing color information.",
        "There are two main reasons for color blindness: either genetic faults in the retina's cone cells, or damage to the eye, optic nerve, or brain areas that handle color processing."
    ]),
    (r"\boccupations|professions|businesses\b", [
        "Color blindness can impact job opportunities and career choices in some professions that require precise differentiation of colors. Here are some examples: \n Transportation: \n Pilots, air traffic controllers, and drivers of commercial vehicles all rely on colored lights, markings, and signals for safe navigation.\nEmergency Services: \n Firefighters depend on color coding on equipment to identify tools and respond quickly.\nPolice officers may use colored flares or markings at crime scenes.\nSkilled Trades: \n Electricians work with color-coded wires to ensure proper connections, and plumbers rely on color coding to identify hot and cold water lines.\nDesign and Manufacturing: \nGraphic designers use color extensively for visual communication, and quality control inspectors in some industries rely on color coding to identify defects."
    ]),
    (r"\bliving with color blindness\b", [
        "Living with color blindness involves making adjustments in daily life, such as using color-coded labels and relying on patterns and textures.",
        "People with color blindness can lead fulfilling lives by using adaptive strategies and seeking support when needed."
    ]),
    (r"\b(?:impact|effect|affect)\s+(.*)?(?:daily|everyday) (?:life|activities)\b", [
        "Color blindness can affect daily life in various ways, such as difficulty in distinguishing traffic lights, reading maps, and identifying certain foods.",
        "The impact of color blindness on daily activities depends on the severity and type of color vision deficiency."
    ]),
    (r"\bexamples\b", [
        "Color blindness can impact daily activities in various ways. For instance, distinguishing traffic lights, matching clothes, or reading colored maps can be difficult. Some people might also struggle with ripeness cues of fruits and vegetables based on color.",
        "Imagine trying to pick out ripe tomatoes from a bowl of green and red ones, or matching a blue shirt with a pair of black pants that appear very similar to you. These are some everyday challenges faced by color-blind individuals."
    ]),
    (r"\bprevalence\b", [
        "Color blindness is more common in men than in women. It affects approximately 8% of men and 0.5% of women of Northern European descent.",
        "The prevalence of color blindness varies among different populations and ethnicities."
    ]),
    (r"\binherited|genetic|hereditary\b", [
        "Yes, color blindness is often inherited genetically. It is passed down through the X chromosome, which is why it is more common in men.",
        "Yes, genetic factors play a significant role in the development of color vision deficiency."
    ]),
    (r"\b(?:impact|effect|affect)\s+(.*)?career\b", [
        "The impact of color blindness on a person's career depends on the specific job requirements. Some professions may have restrictions for color-blind individuals.",
        "Certain occupations, such as pilots or electricians, may require color vision testing as part of the hiring process."
    ]),
    (r"\bchallenges\b", [
        "Some challenges of color blindness include difficulties in certain occupations, limitations in perceiving art or design, and potential safety hazards.",
        "Color blindness can pose challenges in everyday tasks, such as driving, cooking, and choosing clothing.",
        "Beyond the physical limitations, color blindness can sometimes lead to social or emotional challenges. Feeling excluded from activities that rely heavily on color vision or misunderstood by others can be frustrating. However, with increased awareness and support, these challenges can be addressed."
    ]),
    (r"\btools\b", [
        "There are various tools and resources available for color-blind individuals, such as color-blind-friendly apps, special glasses, and accessible design guidelines.",
        "Technology has made significant advancements in providing solutions for color vision deficiencies, including mobile apps and digital accessibility features."
    ]),
    (r"\bglasses\b", [
        "Color-blind glasses, also known as color-enhancing glasses like EnChroma Cx30, Hilux, can help individuals with color vision deficiency distinguish colors more effectively.",
        "Specialized glasses for color blindness like EnChroma Cx30, Hilux use filters to adjust color perception and enhance the visibility of certain hues."
    ]),
    (r"\bawareness\b", [
        "Color blindness awareness initiatives aim to educate people about the condition, promote accessibility and inclusion, and reduce stigma associated with color vision deficiency.",
        "Raising awareness about color blindness can help create a more inclusive society and improve support for individuals with color vision deficiencies."
    ]),
    (r"\badvancements in research\b", [
        "Researchers are continuously working on advancements in color blindness treatments, gene therapy, and assistive technologies to improve the quality of life for color-blind individuals.",
        "Recent breakthroughs in genetics and biotechnology have opened up new possibilities for treating color vision deficiencies."
    ]),
    (r"\b(?:art(ist)?)\b", [
        "Color blindness can influence how individuals perceive and create art. Some artists with color blindness develop unique styles or use alternative techniques to express themselves.",
        "Artists with color vision deficiencies may rely on contrast, texture, and form to convey their artistic vision.",
        "An artist with color blindness, don't perceive the full spectrum of colors that others do. But that can also be a source of creativity! One focuses more on shapes, values (light and dark), and textures to create one's art. There's a whole world of expression beyond just color.",
        "Sure, I can share some insights on a color-blind artist. While they might not see all the colors others do, it allows them to experiment with unique color combinations and focus on composition and light. Many famous artists throughout history have had some form of color blindness."
    ]),
    (r"\bsimulation\b", [
        "Color blindness simulators are tools that allow individuals to experience how color-blind individuals perceive the world. They can be helpful in promoting empathy and understanding.",
        "Using color blindness simulators can help raise awareness about the challenges faced by color-blind individuals in daily life."
    ]),
    (r"\bvision accessibility\b", [
        "Vision accessibility refers to designing products, environments, and technologies to be inclusive and accessible to individuals with visual impairments, including color blindness.",
        "Creating vision-accessible designs benefits not only color-blind individuals but also people with other visual impairments."
    ]),
    (r"\bworkplace accommodations\b", [
        "Workplace accommodations for color-blind individuals may include using color-blind-friendly charts and diagrams, providing alternative labeling methods, and ensuring accessible digital interfaces.",
        "Employers can support color-blind employees by implementing inclusive policies, providing training on color vision deficiency, and offering assistive technologies."
    ]),
    (r"\b(?:sports|athletes)\b", [
        "Color blindness can pose challenges in certain sports, such as soccer or tennis, where distinguishing between team colors or tracking fast-moving objects may be important.",
        "Athletes with color vision deficiencies may need to rely on other cues, such as player positions or field markings, to navigate the game effectively."
    ]),
    (r"\beducation\b", [
        "In education, teachers can support color-blind students by using alternative teaching materials, providing verbal descriptions of visual content, and creating accessible learning environments.",
        "Educators play a crucial role in ensuring that students with color vision deficiencies have equal access to educational resources and opportunities."
    ]),
    (r"\bcolor blindness\b", [
        "Color blindness, also known as color vision deficiency, is a condition where a person has difficulty distinguishing certain colors. It affects how individuals perceive colors."
    ]),
    (r"\bthank\s?you\b", [
        "No Worries! I'm happy I was able to assist you.",
        "I'm happy I could assist you."
    ]),
    (r"\b(?:cannot|couldn't|unable).*?(find|identify|recognize).*?(color(?:s?)\s?)\b", [
        "Would you like to learn more about color blindness or try a color blindness test? You may also use the Identify Color button to identify some basic colors.",
        "There are tools and resources available to help individuals with color blindness navigate their surroundings. You may also use the Identify Color button to identify some basic colors."
    ])
]

# shuffle the pattern-response pairs
random.shuffle(pattern_responses)

languages = {
    "Hindi": "hi",
    "Telugu": "te",
    "English": "en"
}

get_language_name = lambda code: {v: k for k, v in languages.items()}.get(code, "Language not found") # language

# greets user and asks for name
def greet_user():
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "Bella: Hi there! Welcome. I'm Bella, your friendly chatbot for color blindness.\n")
    speak("Hi there! Welcome. I'm Bella, your friendly chatbot for color blindness.")
    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)  # Scroll to the bottom of the chat history
    user_entry.focus_set()  # focus on the entry field for easy typing

# speech generation method
def speech(text, language="English"):
  """
  converts text to speech and plays it directly.
  """
  tts = gTTS(text=text, lang=languages[language])
  filename = "speech.mp3"
  tts.save(filename)  # temporary MP3 file for playback
  playsound(filename, block=True)  # play the created MP3 file

  # delete the temporary file after playback
  if os.path.exists(filename):
      os.remove(filename)

# speech generation with some wait so that response is visible first
def speak(text, language="English"):
  """
  Wait to display response first and then speech generation.
  """
  chat_history.update_idletasks()
  chat_history.after(100, lambda: speech(text,language))

# detect the language of user input
def identify_language(text):
    try:
        language = detect(text)
        return language
    except:
        return "Language detection failed"

# greet user and ask name
def greet_and_ask_name():
    greet_user()
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "Bella: What's your name? Please give your full name.\n")
    speak("What's your name? Please give your full name.")
    chat_history.config(state=tk.DISABLED)

# get name from user input
def get_name_from_input(input_text):
    global user_name
    nlp = spacy.load('en_core_web_sm')
    input_text = input_text.title()
    input_text = input_text.replace("I'M", "I Am")  # replace "I'm" with "I am"
    doc = nlp(input_text)

    user_name = ""
    for token in doc:
        if token.pos_ == "PROPN" or token.pos_ == "NOUN":
            user_name += token.text + " "  # concatenate proper nouns

    user_name = user_name.strip()  # remove whitespaces
    if user_name:
        return user_name
    else:
        return False

# initiate color blind test
def run_blind_test_gui():
    subprocess.call(["python", "test.py"])
    messagebox.showinfo("Blind Test", "Hope your test went well.")

# initiate color identification
def identify_color():
    subprocess.call(["python", "identify_c.py"])
    messagebox.showinfo("Identify Color", "I hope you were able to recognize the colors that you couldn't.")

# confirm chatbot exit
def confirm_quit():
    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to quit?")
    if confirmation:
        root.destroy()

# to get a matched response based on pattern
def get_matched_response(user_input):
    matched_responses = []
    for pattern, responses in pattern_responses:
        if re.search(pattern, user_input, re.IGNORECASE):
            matched_responses.extend(responses)
    if matched_responses:
        return random.choice(matched_responses)
    else:
        return None

# translate text
def translate_text(text,input_dest, dest_language="en"):
    """Translate input text to the destination language."""
    key = "88807704d85a4e74ae21b1c92d697882"
    endpoint = "https://api.cognitive.microsofttranslator.com/"
    location = "eastus"

    path = '/translate'
    constructed_url = endpoint + path
    params = {
        'api-version': '3.0',
        'from': [input_dest],
        'to': [dest_language] #user preferred language
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    #  translated text
    translated_text = response[0]['translations'][0]['text']
    return translated_text

# get user preferred language
def get_language_choice(input_text):
    if input_text.lower() == "english" or input_text == "1":
        return "en"
    elif input_text.lower() == "hindi" or input_text == "2":
        return "hi"
    elif input_text.lower() == "telugu" or input_text == "3":
        return "te"
    # Add more languages and their corresponding codes here
    else:
        return None

# accept user input and give response
def send_message():
    global user_language  # Move the global declaration here
    user_input = user_entry.get()
    user_entry.delete(0, tk.END)  # Clear the input field
    if not user_input:
        messagebox.showinfo("Error", "Please type something.")
        return

    if user_input.lower() in ['quit', 'bye', 'exit']:
        confirm_quit()
        return

    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"You: {user_input}\n")

    if not user_name:
        get_name_from_input(user_input)
        if user_name:
            chat_history.insert(tk.END, f"Bella: Nice to meet you, {user_name}! Please select your preferred language.\n")
            speak(f"Nice to meet you, {user_name}! Please select your preferred language.")
            chat_history.insert(tk.END, "1. English\n2. Hindi\n3. Telugu\n")  # Add more languages as needed
            chat_history.config(state=tk.DISABLED)
        else:
            chat_history.insert(tk.END, "Bella: I couldn't find your name. Can you tell me again?\n")
            speak("I couldn't find your name. Can you tell me again?")
    else:
        if not user_language:
            language_choice = get_language_choice(user_input)
            if language_choice:
                user_language = language_choice
                chat_history.insert(tk.END,
                                    f"Bella: Language set to {get_language_name(user_language)}. Please start typing your message.\n")
                speak(f"Language set to {get_language_name(user_language)}. Please start typing your message.")
            else:
                chat_history.insert(tk.END, "Bella: Please select a valid language option.\n")
                speak("Please select a valid language option.")
        else:
            matched_response = get_matched_response(user_input)
            if not matched_response:
                # Translate user input to English and attempt matching again
                input_dest = identify_language(user_input)
                translated_input = translate_text(user_input, input_dest,dest_language="en")
                print(translated_input)
                matched_response = get_matched_response(translated_input)
                if not matched_response:
                    chat_history.insert(tk.END, f"Bella: Sorry I cannot understand. Can you rephrase it?\n")
                    speak(f"Sorry I cannot understand. Can you rephrase it?")
                else:
                    translated_response = translate_text(matched_response,'en', dest_language=user_language)
                    chat_history.insert(tk.END, f"Bella: {translated_response}\n")
                    speak(translated_response)
            else:
                translated_response = translate_text(matched_response, 'en',dest_language=user_language)
                chat_history.insert(tk.END, f"Bella: {translated_response}\n")
                speak(translated_response)

    chat_history.config(state=tk.DISABLED)
    chat_history.see(tk.END)


# Create the GUI window
root = tk.Tk()
root.title("Chatbot for color blindness")

# Chat history display
chat_history = tk.Text(root, state=tk.DISABLED)
chat_history.pack(expand=True, fill=tk.BOTH)

# User input field
user_entry = tk.Entry(root)
user_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
user_entry.bind("<Return>", send_message)  # Send message on Enter key press

# Send button (optional, for users who prefer clicking)
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

greet_and_ask_name()

# Blind test button
blind_test_button = Button(root, text="Color Blind Test", command=run_blind_test_gui)
blind_test_button.pack()

# Color detection button
color_detection_button = Button(root, text="Identify Color", command=identify_color)
color_detection_button.pack()

# Start the GUI event loop
root.mainloop()
