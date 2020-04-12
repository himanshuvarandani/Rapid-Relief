from app import app, db, login
from app.forms import LoginForm, RegistrationForm, VolunteerForm
from app.models import User
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/lerner_reg', methods=["GET", "POST"])
def lerner_reg():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are registered user!')
        return redirect(url_for('lerner_login'))

    return render_template('lerner_reg.html', form=form)

@app.route('/login', methods=["GET", "POST"])
@app.route('/lerner_login', methods=["GET", "POST"])
def lerner_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            print(user.username)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('lerner_login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc!='':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('lerner_login.html', form=form)


@app.route('/lerner_dashboard')
def lerner_dashboard():
    return render_template('lerner_dashboard')


@app.route('/lerner_logout')
@login_required
def lerner_logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/aid')
def aid():
    return render_template("firstAid.html")

@app.route('/volunteer', methods=["GET", "POST"])
def volunteer():
    form = VolunteerForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        user.username = form.username.data
        user.email = form.email.data
        user.address = form.address.data
        user.volunteer_status = True
        db.session.commit()
        flash("You are registered as a volunteer")
        return redirect('/index')
    return render_template('volunteer.html', form=form)


englishBot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")

trainer = ChatterBotCorpusTrainer(englishBot)
trainer.train("chatterbot.corpus.english") #train the chatter bot for english

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
