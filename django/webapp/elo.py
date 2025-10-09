def update_elos(eloA, eloB, resultA, resultB, nbVotes):
    import math
    INDULGENCE_COEFF = 1000 # Very forgiving since very subjective choice
    COEFF = round(64 / math.log(int(nbVotes) + math.e)) # Begins very fast sinc user-base is small BUT changes get smaller logarithmically as number of votes (like nb of games in chess.com) increases
    probA = 1 / (1 + 10 ** ((int(eloB) - int(eloA)) / INDULGENCE_COEFF))
    probB = 1 - probA

    newEloA = int(eloA) + COEFF * (resultA - probA)
    newEloB = int(eloB) + COEFF * (resultB - probB)

    return newEloA, newEloB
