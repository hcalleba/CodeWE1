# Readme

Participation to <https://codeweekend.dev/#/>

I used a simple greedy algorithm with backtracking. It works very poorly on the instances 15, 16 and 17 because I do not look at the experience gained (technically nbFutureMoves can have an impact on it).

I did not do the second part (with the fatigue) but it should be extremely easy to implement and the resulting solutions should still have the same level of optimality as for the first part (might even be better as I assume a greedy heuristic should work better on this problem than the previous one)

Just run the main function, the only parameters you should modify are nbFutureMoves, nbBestGold, nbBestExp and nbRand which are at the last line of the main function

Using nbFutureMoves = 1 is relatively easy to run on any instance. With nbFutureMoves = 2 a lot of instances take quite some time, the other parameters should then be tweaked to avoid testing all the monsters at each iteration.
