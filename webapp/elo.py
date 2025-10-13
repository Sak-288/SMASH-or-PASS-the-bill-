def update_elos(eloA, eloB, resultA, resultB, nbVotes):
    import math
    INDULGENCE_COEFF = 400
    COEFF = round(128 / math.log(int(nbVotes) + math.e), 0) # Begins very fast sinc user-base is small BUT changes get smaller logarithmically as number of votes (like nb of games in chess.com) increases
    probA = 1 / (1 + 10 ** ((eloB - eloA) / INDULGENCE_COEFF))
    probB = 1 - probA

    newEloA = round(eloA + COEFF * (resultA - probA), 0)
    newEloB = round(eloB + COEFF * (resultB - probB), 0)

    return newEloA, newEloB