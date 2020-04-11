from flask import Flask, render_template, request, redirect
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/lerner_reg')
def lerner_reg():
    return render_template('lerner_reg.html')

@app.route('/lerner_login')
def lerner_login():
    return render_template('lerner_login.html')

@app.route('/lerner_dashboard')
def lerner_dashboard():
    return render_template('lerner_dashboard')

englishBot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")


# trainer = ChatterBotCorpusTrainer(englishBot)
# trainer.train("chatterbot.corpus.english") #train the chatter bot for english

disaster_words = ["disaster","calamity" , "help", "require", "danger", "catastrophe","adversity"]
accident_words = ["accident", "injured", "fall","bleeding","save", "blood", "bleed", "car-accident"]

disasters = "1. Flood  2.Tsunami  3. Earthquake  4.Hurricane   5. Cyclones   6. Mudslides" 

@app.route("/Chatbot")
def Chatbot():
    return render_template("ChatBot.html")

@app.route("/get")

#function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    # userText = input("Enter something")
    if any(word in userText for word in disaster_words):
        help = "Sending for help ... You are in a disaster SELECT THE DISASTER " , disasters
     
        return str(help) # calling Aid
    if str(userText.lower()) == "flood":
        return "Precautions of flood"    
    elif str(userText.lower()) == "tsunami":
        return "Precautions of tsunami"
    elif str(userText.lower()) == "earthquake":
        return  "Precautions of eathquake"
    elif str(userText.lower()) == "cyclones":
        return "Precautions of Cyclones"
    elif str(userText.lower()) == "mudslides":    
        return "Precautions of mudslides"
             # bool = Fals
    elif any(word in userText for word in accident_words):
        help = "Sending for help ....You met an accident"
        return str(help)
            # print ('U met an accident')
            # print('Sending for help ')
            # print('info...')
            # bool = False
    else:
        return str(englishBot.get_response(userText))


if __name__ == "__main__":
    app.run()
