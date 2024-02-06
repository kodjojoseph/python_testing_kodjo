import json
from flask import Flask,render_template,request,redirect,flash,url_for

#Chargement des clubs
def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs

#Chargement des competitions
def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/',)
def index():
    return render_template('index.html')
    

@app.route('/showSummary',methods=['POST'])
def showSummary():
    entered_email = request.form['email']
    
    if any(club['email'] == entered_email for club in clubs):
        # Si oui, récupère le club correspondant
        club = next(club for club in clubs if club['email'] == entered_email)
        return render_template('welcome.html', club=club, competitions=competitions)
    
    else:
       
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition,club):
    
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    
    # Vérifiez si le nombre de places disponibles est suffisant
    if int(competition['numberOfPlaces']) < placesRequired :
        flash("il n'y a pas assez de places disponibles.")
        return render_template('welcome.html', club=club, competitions=competitions)
    elif placesRequired > 12:
        flash('Désolé, pas plus de 12 places.')
        return render_template('welcome.html', club=club, competitions=competitions)
    
    club ['points'] = int (club ['points']) - placesRequired
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    flash('Génial !! Vous avez réussi à acheter {} places'.format(placesRequired))
    return render_template('welcome.html', club=club, competitions=competitions)

    

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))