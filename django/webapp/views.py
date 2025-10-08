from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path
from types import SimpleNamespace


# get the app's base path
BASE_DIR = Path(__file__).resolve().parent  # points to webapp/

csv_file_path = BASE_DIR / 'data' / 'liste.csv'

def home(request):
    import random as rp
    import csv

    firstRank = rp.randint(1, 575)
    secondRank = rp.choice([i for i in range(1, 575 + 1) if i != firstRank])


    with open(csv_file_path, mode='r', newline='', encoding="utf-8") as file:
        content = list(csv.reader(file))
        firstList = content[firstRank]
        secondList = content[secondRank]   

    firstParty = firstList[5]
    firstColor = ""
    secondParty = secondList[5]
    secondColor = ""

    match firstParty:
        case "La France insoumise - Nouveau Front Populaire":
            firstColor = "#E41B17"  # Rouge vif
        case "Horizons & Indépendants":
            firstColor = "#0066CC"  # Bleu clair
        case "Union des droites pour la République":
            firstColor = "#003366"  # Bleu foncé
        case "Socialistes et apparentés":
            firstColor = "#FF3366"  # Rose / Rouge clair
        case "Rassemblement National":
            firstColor = "#0055A4"  # Bleu marine
        case "Ensemble pour la République":
            firstColor = "#FFD700"  # Or / Jaune
        case "Écologiste et Social":
            firstColor = "#009933"  # Vert
        case "Les Démocrates":
            firstColor = "#FF6600"  # Orange
        case "Droite Républicaine":
            firstColor = "#990000"  # Bordeaux / Rouge foncé
        case "Libertés, Indépendants, Outre-mer et Territoires":
            firstColor = "#66CCCC"  # Bleu turquoise
        case "Non inscrit(e)":
            firstColor = "#808080"  # Gris
        case "Gauche Démocrate et Républicaine":
            firstColor = "#800080"  # Violet
        case _:
            firstColor = "#000000"  # Couleur par défaut si non reconnu

    match secondParty:
        case "La France insoumise - Nouveau Front Populaire":
            secondColor = "#E41B17"  # Rouge vif
        case "Horizons & Indépendants":
            secondColor = "#0066CC"  # Bleu clair
        case "Union des droites pour la République":
            secondColor = "#003366"  # Bleu foncé
        case "Socialistes et apparentés":
            secondColor = "#FF3366"  # Rose / Rouge clair
        case "Rassemblement National":
            secondColor = "#0055A4"  # Bleu marine
        case "Ensemble pour la République":
            secondColor = "#FFD700"  # Or / Jaune
        case "Écologiste et Social":
            secondColor = "#009933"  # Vert
        case "Les Démocrates":
            secondColor = "#FF6600"  # Orange
        case "Droite Républicaine":
            secondColor = "#990000"  # Bordeaux / Rouge foncé
        case "Libertés, Indépendants, Outre-mer et Territoires":
            secondColor = "#66CCCC"  # Bleu turquoise
        case "Non inscrit(e)":
            secondColor = "#808080"  # Gris
        case "Gauche Démocrate et Républicaine":
            secondColor = "#800080"  # Violet
        case _:
            secondColor = "#000000"  # Couleur par défaut si non reconnu


    returnDict = {'firstInf':SimpleNamespace(id=firstList[0], name=firstList[1], surname=firstList[2], department=firstList[3], num=firstList[4], party=firstList[5], color=firstColor), 'secondInf':SimpleNamespace(id=secondList[0], name=secondList[1], surname=secondList[2], department=secondList[3], num=secondList[4], party=secondList[5], color=secondColor)}

    return render(request, "webapp/home.html", returnDict)
