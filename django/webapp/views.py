from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path
from types import SimpleNamespace
from django.shortcuts import redirect
import random as rp
import csv
from elo import update_elos

LIST_IDS = list(range(1, 574))

# get the app's base path
BASE_DIR = Path(__file__).resolve().parent  # points to webapp/

csv_file_path = BASE_DIR / 'data' / 'liste.csv'

with open(csv_file_path, mode='r', newline='', encoding="utf-8") as file:
        content = list(csv.reader(file))

def update_value(request):
    if request.method == "POST":
        winSituation = request.POST.get("winSituation")
        winnerRank = request.POST.get("winnerRank")
        loserRank = request.POST.get("loserRank")

        winner = content[winnerRank]
        loser = content[loserRank]
        winnerElo = winner[6]
        loserElo = loser[6]
        winner[8] = int(winner[8]) + 1
        loser[8] = int(loser[8]) + 1

        winnerVotesNumber = int(winner[8])
        loserVotesNumber = int(loser[8])

        if winSituation is "first_wins":
            resultA = 1
            resultB = 0
        else:
            resultB = 1
            resultA = 0

        newWinnerElo = update_elos(winnerElo, loserElo, resultA, resultB, winnerVotesNumber)[0]
        newLoserElo = update_elos(winnerElo, loserElo, resultA, resultB, loserVotesNumber)[1]

        winner[6] = newWinnerElo
        loser[6] = newLoserElo

        
        with open(csv_file_path, "w", encoding="utf-8", newline='') as file:
            file.write(content)

        return redirect(request.META.get('HTTP_REFERER', '/'))

def home(request):
    firstRank = rp.choice(LIST_IDS)
    secondRank = rp.choice(LIST_IDS.pop(firstRank))    
    
    firstList = content[firstRank]
    secondList = content[secondRank]   

    firstParty = firstList[5]
    firstColor = ""
    secondParty = secondList[5]
    secondColor = ""

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

    match secondParty:
        case "La France insoumise - Nouveau Front Populaire":
            secondColor = "#FF0000"  # Rouge vif
        case "Horizons & Indépendants":
            secondColor = "#0066CC"  # Bleu clair
        case "Union des droites pour la République":
            secondColor = "#004991"  # Bleu foncé
        case "Socialistes et apparentés":
            secondColor = "#FF3366"  # Rose / Rouge clair
        case "Rassemblement National":
            secondColor = "#00203E"  # Bleu marine
        case "Ensemble pour la République":
            secondColor = "#FFD700"  # Or / Jaune
        case "Écologiste et Social":
            secondColor = "#009933"  # Vert
        case "Les Démocrates":
            secondColor = "#FF6600"  # Orange
        case "Droite Républicaine":
            secondColor = "#3471FF"  # Bordeaux / Rouge foncé
        case "Libertés, Indépendants, Outre-mer et Territoires":
            secondColor = "#00E1FF"  # Bleu turquoise
        case "Non inscrit(e)":
            secondColor = "#808080"  # Gris
        case "Gauche Démocrate et Républicaine":
            secondColor = "#800080"  # Violet
        case _:
            secondColor = "#000000"  # Couleur par défaut si non reconnu


    returnDict = {'firstInf':SimpleNamespace(id=firstList[0], name=firstList[1], surname=firstList[2], department=firstList[3], num=firstList[4], party=firstList[5], color=firstColor, elo=firstList[6], rank=firstList[7]), 'secondInf':SimpleNamespace(id=secondList[0], name=secondList[1], surname=secondList[2], department=secondList[3], num=secondList[4], party=secondList[5], color=secondColor, elo=secondList[6], rank=secondList[7])}

    return render(request, "webapp/home.html", returnDict)
