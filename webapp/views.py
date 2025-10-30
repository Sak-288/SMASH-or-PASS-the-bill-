from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path
from types import SimpleNamespace
from django.shortcuts import redirect
import random as rp
import csv
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from . import elo
from .elo import update_elos
from .models import Contact
import numpy as np
from .forms import ContactForm

LIST_IDS = list(range(1, 574))

# get the app's base path
BASE_DIR = Path(__file__).resolve().parent  # points to webapp/

csv_file_path = BASE_DIR / 'data' / 'liste.csv'
csv_party_elos = BASE_DIR / 'data' / 'elos_partis.csv'

def get_party_elo(party_list):
    aggregate = 0
    for deputy in party_list:
        aggregate += float(deputy[6])
    party_avr = round(aggregate / len(party_list), 0)
    return party_avr

WOMEN = []
MEN = []
with open(csv_file_path, mode='r', newline="", encoding='utf-8') as file:
    content = list(csv.reader(file))
    for row in content:
        if row[9] == 'F':
            WOMEN.append(int(row[7]))
        else:
            MEN.append(int(row[7]))

LFI = []
HEI = []
UDR = []
SEA = []
RN = []
EN = []
ES = []
DR = []
DM = []
LIOT = []
NI = []
GDR = []

for row in content:
    match row[5]:
        case "La France insoumise - Nouveau Front Populaire":
            LFI.append(row)
        case "Horizons & Indépendants":
            HEI.append(row)
        case "Union des droites pour la République":
            UDR.append(row)
        case "Socialistes et apparentés":
            SEA.append(row)
        case "Rassemblement National":
            RN.append(row)
        case "Ensemble pour la République":
            EN.append(row)
        case "Écologiste et Social":
            ES.append(row)
        case "Les Démocrates":
            DM.append(row)
        case "Droite Républicaine":
            DR.append(row)
        case "Libertés, Indépendants, Outre-mer et Territoires":
            LIOT.append(row)
        case "Non inscrit(e)":
            NI.append(row)
        case "Gauche Démocrate et Républicaine":
            GDR.append(row)
        case _:
            NI.append(row)

def get_party_color(firstParty):
    match firstParty:
        case "La France insoumise - Nouveau Front Populaire":
            firstColor = "#FF0000"  # Rouge vif
        case "Horizons & Indépendants":
            firstColor = "#0066CC"  # Bleu clair
        case "Union des droites pour la République":
            firstColor = "#004991"  # Bleu foncé
        case "Socialistes et apparentés":
            firstColor = "#FF3366"  # Rose / Rouge clair
        case "Rassemblement National":
            firstColor = "#00203E"  # Bleu marine
        case "Ensemble pour la République":
            firstColor = "#FFD700"  # Or / Jaune
        case "Écologiste et Social":
            firstColor = "#009933"  # Vert
        case "Les Démocrates":
            firstColor = "#FF6600"  # Orange
        case "Droite Républicaine":
            firstColor = "#3471FF"  # Bordeaux / Rouge foncé
        case "Libertés, Indépendants, Outre-mer et Territoires":
            firstColor = "#00E1FF"  # Bleu turquoise
        case "Non inscrit(e)":
            firstColor = "#808080"  # Gris
        case "Gauche Démocrate et Républicaine":
            firstColor = "#800080"  # Violet
        case _:
            firstColor = "#000000"  # Couleur par défaut si non reconnu
    return firstColor

def update_party_elos_dict():
    partyElosDict = {
    'La France insoumise - Nouveau Front Populaire': SimpleNamespace(
        elo=get_party_elo(LFI),
        color=get_party_color('La France insoumise - Nouveau Front Populaire')
    ),
    'Horizons & Indépendants': SimpleNamespace(
        elo=get_party_elo(HEI),
        color=get_party_color('Horizons & Indépendants')
    ),
    'Union des droites pour la République': SimpleNamespace(
        elo=get_party_elo(UDR),
        color=get_party_color('Union des droites pour la République')
    ),
    'Socialistes et apparentés': SimpleNamespace(
        elo=get_party_elo(SEA),
        color=get_party_color('Socialistes et apparentés')
    ),
    'Rassemblement National': SimpleNamespace(
        elo=get_party_elo(RN),
        color=get_party_color('Rassemblement National')
    ),
    'Ensemble pour la République': SimpleNamespace(
        elo=get_party_elo(EN),
        color=get_party_color('Ensemble pour la République')
    ),
    'Écologiste et Social': SimpleNamespace(
        elo=get_party_elo(ES),
        color=get_party_color('Écologiste et Social')
    ),
    'Les Démocrates': SimpleNamespace(
        elo=get_party_elo(DM),
        color=get_party_color('Les Démocrates')
    ),
    'Droite Républicaine': SimpleNamespace(
        elo=get_party_elo(DR),
        color=get_party_color('Droite Républicaine')
    ),
    'Libertés, Indépendants, Outre-mer et Territoires': SimpleNamespace(
        elo=get_party_elo(LIOT),
        color=get_party_color('Libertés, Indépendants, Outre-mer et Territoires')
    ),
    'Non inscrit(e)': SimpleNamespace(
        elo=get_party_elo(NI),
        color=get_party_color('Non inscrit(e)')
    ),
    'Gauche Démocrate et Républicaine': SimpleNamespace(
        elo=get_party_elo(GDR),
        color=get_party_color('Gauche Démocrate et Républicaine')
    ),
}    
    return partyElosDict

def get_color(deputy):
    firstParty = deputy[5]
    match firstParty:
        case "La France insoumise - Nouveau Front Populaire":
            firstColor = "#FF0000"  # Rouge vif
        case "Horizons & Indépendants":
            firstColor = "#0066CC"  # Bleu clair
        case "Union des droites pour la République":
            firstColor = "#004991"  # Bleu foncé
        case "Socialistes et apparentés":
            firstColor = "#FF3366"  # Rose / Rouge clair
        case "Rassemblement National":
            firstColor = "#00203E"  # Bleu marine
        case "Ensemble pour la République":
            firstColor = "#FFD700"  # Or / Jaune
        case "Écologiste et Social":
            firstColor = "#009933"  # Vert
        case "Les Démocrates":
            firstColor = "#FF6600"  # Orange
        case "Droite Républicaine":
            firstColor = "#3471FF"  # Bordeaux / Rouge foncé
        case "Libertés, Indépendants, Outre-mer et Territoires":
            firstColor = "#00E1FF"  # Bleu turquoise
        case "Non inscrit(e)":
            firstColor = "#808080"  # Gris
        case "Gauche Démocrate et Républicaine":
            firstColor = "#800080"  # Violet
        case _:
            firstColor = "#000000"  # Couleur par défaut si non reconnu
    return firstColor

def choose_setting(request):
    if request.method == "POST":
        genderSetting = request.POST.get("gd_setting")
        if genderSetting == "men":
            return redirect('/home_men')
        elif genderSetting == "women":
            return redirect('/home_women')
        else:
            return redirect('/home')

def update_value(request):
    with open(csv_file_path, mode='r', newline='', encoding="utf-8") as file:
        content = list(csv.reader(file))

    if request.method == "POST":
        winSituation = request.POST.get("winSituation")
        winnerRank = request.POST.get("winnerRank")
        loserRank = request.POST.get("loserRank")

        winner = content[int(winnerRank) - 1]
        loser = content[int(loserRank) - 1]
        winnerElo = float(winner[6])
        loserElo = float(loser[6])
        winner[8] = int(winner[8]) + 1
        loser[8] = int(loser[8]) + 1

        winnerVotesNumber = int(winner[8])
        loserVotesNumber = int(loser[8])

        if winSituation == "first_wins":
            resultA = 1
            resultB = 0
            newWinnerElo = update_elos(winnerElo, loserElo, resultA, resultB, winnerVotesNumber)[0]
            newLoserElo = update_elos(winnerElo, loserElo, resultA, resultB, loserVotesNumber)[1]
        else:
            resultB = 1
            resultA = 0
            newWinnerElo = update_elos(winnerElo, loserElo, resultA, resultB, winnerVotesNumber)[1]
            newLoserElo = update_elos(winnerElo, loserElo, resultA, resultB, loserVotesNumber)[0]

        winner[6] = newWinnerElo
        loser[6] = newLoserElo

        with open(csv_file_path, "w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in content:
                writer.writerow(row)

        return redirect(request.META.get('HTTP_REFERER', '/'))

def home(request):
    with open(csv_file_path, mode='r', newline='', encoding="utf-8") as file:
        content = list(csv.reader(file))

    firstRank = rp.choice(LIST_IDS)
    tempChoices = [x for x in LIST_IDS if x != firstRank]
    tempCriteria = float(content[firstRank - 1][6])
    secondChoices = []
    for choice in tempChoices:
        if abs(float(content[choice - 1][6]) - tempCriteria) <= 50:
            secondChoices.append(choice)
    secondRank = rp.choice(secondChoices)
    
    firstList = content[firstRank - 1]
    secondList = content[secondRank - 1]   

    firstColor = get_color(firstList)
    secondColor = get_color(secondList)

    returnDict = {'firstInf':SimpleNamespace(id=firstList[0], name=firstList[1], surname=firstList[2], department=firstList[3], num=firstList[4], party=firstList[5], color=firstColor, elo=firstList[6], rank=firstList[7]), 'secondInf':SimpleNamespace(id=secondList[0], name=secondList[1], surname=secondList[2], department=secondList[3], num=secondList[4], party=secondList[5], color=secondColor, elo=secondList[6], rank=secondList[7])}

    return render(request, "webapp/home.html", returnDict)

def home_women(request):
    with open(csv_file_path, mode='r', newline='', encoding="utf-8") as file:
        content = list(csv.reader(file))

    firstRank = rp.choice(WOMEN)
    tempChoices = [x for x in WOMEN if x != firstRank and x != 575]
    tempCriteria = float(content[firstRank - 1][6])
    secondChoices = []
    for choice in tempChoices:
        if abs(float(content[choice - 1][6]) - tempCriteria) <= 50:
            secondChoices.append(choice)
    secondRank = rp.choice(secondChoices)
    
    firstList = content[firstRank - 1]
    secondList = content[secondRank - 1] 

    firstColor = get_color(firstList)
    secondColor = get_color(secondList)

    returnDict = {'firstInf':SimpleNamespace(id=firstList[0], name=firstList[1], surname=firstList[2], department=firstList[3], num=firstList[4], party=firstList[5], color=firstColor, elo=firstList[6], rank=firstList[7]), 'secondInf':SimpleNamespace(id=secondList[0], name=secondList[1], surname=secondList[2], department=secondList[3], num=secondList[4], party=secondList[5], color=secondColor, elo=secondList[6], rank=secondList[7])}

    return render(request, "webapp/home.html", returnDict)

def home_men(request):
    with open(csv_file_path, mode='r', newline='', encoding="utf-8") as file:
        content = list(csv.reader(file))

    firstRank = rp.choice(MEN)
    tempChoices = [x for x in MEN if x != firstRank]
    tempCriteria = float(content[firstRank - 1][6])
    secondChoices = []
    for choice in tempChoices:
        if abs(float(content[choice - 1][6]) - tempCriteria) <= 50:
            secondChoices.append(choice)
    secondRank = rp.choice(secondChoices)
    
    firstList = content[firstRank - 1]
    secondList = content[secondRank - 1]   

    firstColor = get_color(firstList)
    secondColor = get_color(secondList)

    returnDict = {'firstInf':SimpleNamespace(id=firstList[0], name=firstList[1], surname=firstList[2], department=firstList[3], num=firstList[4], party=firstList[5], color=firstColor, elo=firstList[6], rank=firstList[7], gender=firstList[9]), 'secondInf':SimpleNamespace(id=secondList[0], name=secondList[1], surname=secondList[2], department=secondList[3], num=secondList[4], party=secondList[5], color=secondColor, elo=secondList[6], rank=secondList[7], gender=secondList[9])}

    return render(request, "webapp/home.html", returnDict)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get cleaned data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            
            # Create email content
            email_subject = f"Contact Form from SMASH OR PASS - Edition Assemnblée National"
            email_message = f"""
            Name: {name}
            Email: {email}
            
            Message:
            {subject}
            """
            # Send email
            send_mail(
                email_subject,
                settings.DEFAULT_EMAIL,  # From email
                [settings.DEFAULT_EMAIL],     # To email
                fail_silently=False,
            )
        return redirect('/home')
    return render(request, 'webapp/contact.html')

def rankings(request):
    with open(csv_file_path, mode='r', newline="", encoding='utf-8') as file:
        content = list(csv.reader(file))

    copiedList = content.copy()
    for row in copiedList:
        row.append(get_color(row))

    rankingsList = []
    max = 0
    item = 0
    for row in copiedList:
        if float(row[6]) > max:
            max = float(row[6])
    for i in np.arange(int(max) + 1, 0, -0.5):
        for row in copiedList:
            if float(row[6]) == i:
                if item == 0:
                    rankingsList.append(row)
                else:
                    rankingsList.insert(item, row)
                item += 1
    return render(request, "webapp/rankings.html", {"rankingsList": rankingsList})
    
def rankings_parties(request):
    return render(request, "webapp/rankings_parties.html", {"rankingsPartiesList" : update_party_elos_dict()})
