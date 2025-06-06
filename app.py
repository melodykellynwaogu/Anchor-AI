from flask import Flask, render_template, request, redirect, url_for, session import wikipedia import os from datetime import timedelta

wikipedia.set_lang("en")

app = Flask(name) app.secret_key = os.urandom(24)  

qa_pairs = { "hi": "Hello! I am Anchor. How can I help you?", "hello": "Hi my Boss Melody isn't here, but I'm here to help you!", "how are you": "I'm just code, but I'm here and happy to chat!", "what is html": "HTML stands for HyperText Markup Language. It's used to structure web pages.", "what is css": "CSS styles the content of web pages.", "what is your farvorite language": "I love Python! It's versatile and easy to read.", "tell me a history fact": "Did you know the Great Wall of China is over 13,000 miles long? It was built to protect against invasions.", "bye": "Goodbye! Talk to you soon.", "what is python": "Python is a high-level programming language known for its readability and versatility.", "what is your name": "I'm Anchor, your friendly chatbot!", "what can you do": "I can chat, answer questions, and share information. Try asking me something!", "what is the capital of france": "The capital of France is Paris.", "what is the weather like": "I'm not connected to weather services yet. Maybe check a weather app?", "tell me a joke": "Why did the scarecrow win an award? Because he was outstanding in his field!", "who created you": "I was built by Melody Kelly Nwaogu using Python and Flask!", "what's the time": "I don’t have a clock yet, but your device should show the correct time.", "are you a robot": "Yes, but a friendly one programmed to chat with you.", "can you help me with my homework": "Sure! Ask me a specific question and I’ll do my best to help.", "what's your favorite color": "I like blue—it reminds me of clean code and clear skies!", "how old are you": "I was just created recently, so I’m pretty young in bot years!", "okay": "Great to hear! What else can I help you with? Or should I sing you a song? Just say 'sing me a song'.", "sing me a song": "\ud83c\udfb5 I'm a little chatbot, short and smart... Ask me things, I’ll do my part!\ud83c\udfb5", "what is your farvorite food": "I don't eat, but if I did, I would really like pizza.", "tell me something interesting": "Did you know honey never spoils? Archaeologists found 3000-year-old honey in ancient Egyptian tombs that's still edible!", "do you sleep": "Nope, I’m always awake and ready to chat.", "what is ai": "AI stands for Artificial Intelligence. It's technology that enables machines to perform tasks that typically require human intelligence.", "what is machine learning": "Machine Learning is a subset of AI that allows systems to learn from data and improve over time without being explicitly programmed." }

def get_wikipedia_summary(query): try: summary = wikipedia.summary(query, sentences=2) return summary except wikipedia.exceptions.DisambiguationError as e: return f"That topic seems unclear. Try asking about something more specific like '{e.options[0]}'." except wikipedia.exceptions.PageError: return "Sorry, I couldn’t find anything on that topic." except Exception as e: return f"Oops, something went wrong: {e}"

@app.route("/", methods=["GET", "POST"]) def index(): session.permanent = True if "chat_history" not in session: session["chat_history"] = []

chat_history = session["chat_history"]

if request.method == "POST":
    prompt = request.form.get("prompt")
    if prompt:
        user_input = prompt.strip().lower()
        chat_history.append({"role": "user", "content": prompt})

        reply = qa_pairs.get(user_input)
        if not reply:
            reply = get_wikipedia_summary(prompt)

        chat_history.append({"role": "assistant", "content": reply})
        session["chat_history"] = chat_history

    return redirect(url_for("index"))

return render_template("index.html", messages=chat_history)

if name == "main": app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

