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

disasters = "1. Flood   2.Tsunami   3. Earthquake   4.Hurricane   5. Cyclones   6. Mudslides" 

@app.route("/Chatbot")
def Chatbot():
    return render_template("ChatBot.html")

@app.route("/get")

#function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    # userText = input("Enter something")
    if any(word in userText for word in disaster_words):
        help = "Searching for avaliable help ... Are are in a disaster?  SELECT THE DISASTER  Or met an accident " ,disasters
        msg = str(help)
        
        return msg # calling Aid
    if str(userText.lower()) == "flood":
        return """FLOOD PRECAUTIONS : Do not walk, swim, or drive through flood waters. 
                Turn Around, Don't Drown! ...  \n
                If you are on a bridge or near it: stay off of bridges and fast-moving water.\n
                Turn off electricity and gas supply when evacuating\n
                Do not walk through flooded areas. ...
                Help is on the way....
                Contacting the nearest rescue man
                """    
    elif str(userText.lower()) == "tsunami":
        return """ TAKE THESE PRECAUTIONS: - First, protect yourself from an Earthquake. ...
                    Get to high ground as far inland as possible
                    Listen to emergency information and alerts.
                    Move to higher ground.
                    Stay away from coast, tidal estuaries, rivers and streams; 
                    if at sea, stay there until “all clear” is issued.      Help is on its way...."""
    
    elif str(userText.lower()) == "earthquake":
        return  """FOLLOW   THESE  TO  BE  SAFE , Mind Me
        Drop down and take cover under a desk or table. ...
        Stay inside until the shaking stops and it is safe to exit.
        Try to keep your cool and don't run around here and there, come out of the building if you can safely.
        Tip: A doorway is the safest place to be during an earthquake if you have a somewhat old house!
        Help is on its way , meanwhile you can talk to me :) """
    
    elif str(userText.lower()) == "cyclones":
        return """ Cyclones : Don't go outside until officially advised it is safe. 
        Check for gas leaks.  Beware of damaged POWER LINES, bridges, BUILDINGS, trees, and don't enter FLOODWATER.
        REQUEST SENT :)  for your help!  DO NOT PANIC ,
        HELP ON ITS WAY!
        """
    
    
    elif str(userText.lower()) == "mudslides":    
        return """FOLLOW THESE STEPS: Move away quickly from the path of the mudflow or landslide to another location.
        Do not try to stay close and take photographs. Landslide debris move from uphill to downhill, therefore, avoid low-lying areas or valleys.
        If there is a way to sound an alarm, do so.
        Listen and look out for signs of further flows in that area, as the flowing debris often knock against surrounding slopes and sets off new flows.
        """
            
    
    
    elif any(word in userText for word in accident_words):
        help = "Sending help request .... you met an accident!"

        return """Do not panic , Stay Calm ... Help on its way...
        If injured too much try to talk and breathe calmly..."""
            
    else:
        return str(englishBot.get_response(userText))


if __name__ == "__main__":
    app.run()
