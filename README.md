# 11420CHE240100-Final-Project

## Requirements
- Pygame (install with ```pip install pygame```)

## Execution
To run the game, please run:
```
python run.py
```
An entry screen would be shown, and please choose a playing mode to continue.

## Mass testing (debugging)
For mass testing without GUI, please run the following command with options:
```
python run.py --debug --games [number of games] --p1 [minimax, rule, reflex] --p2 [minimax, rule, reflex]
```

## Result
We ran a 100 gamge experiment with minimax and reflex agents, the results are as follows:
```
==================================================
 FINAL STATS
 P1 (minimax) Wins: 94 | P2 (reflex) Wins: 6 | Ties: 0
 P1 Win Rate: 94.0%
 P1 Avg Score: 204.1 | P2 Avg Score: 138.2
==================================================
```
