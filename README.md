# 11420CHE240100-Final-Project

## Requirements
- Pygame (install with ```pip install pygame```)
- random

## Execution
To run the game, please run:
```
python run.py
```
An entry screen would be shown, and please choose a playing mode to continue.

## Mass testing (debugging)
For mass testing without GUI, please run the following command with options:
- ```--debug``` activates the debug mode, refer to the following options.
- ```--games``` should be followed by the number of games, default is 10
- ```--p1``` and ```--p2``` should be followed by the agent name, there are four types of agent to choose from: ```minimax``` was a Minimax agent built by Gemini, based on the Minimax and heuristic algorithm, ```rule1``` mimics the moves by 侯佩伶, and ```rule2``` mimics the move by 蔡依憓. Finally, the ```reflex``` agent is a baseline agent that always use up all the rolls and chooses the category of highest score (based on the Greedy algorithm)
Your command line propt should be of form:
```
python run.py --debug --games [number of games] --p1 [agent] --p2 [agent]
```

## Result
We ran a 100 game experiment with minimax and reflex agents, the results are as follows:
```
==================================================
 FINAL STATS
 P1 (minimax) Wins: 94 | P2 (reflex) Wins: 6 | Ties: 0
 P1 Win Rate: 94.0%
 P1 Avg Score: 204.1 | P2 Avg Score: 138.2
==================================================
```
- ```minimax``` agent scores on average 204.2 points
- ```rule1``` agent scores on average 165.1
- ```rule2``` agent scores on average 191.4 points
- ```reflex``` agent scores on average 138.0 points
