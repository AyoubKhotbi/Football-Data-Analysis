# Football-Data-Analysis

Wyscout-based functions help you define how a football team can score during a match.
They are not fully working, you can only find about 80% of the goals in a season and goals may not be categorized right.

The idea is to split up these kinds of goals INTO:

1. Penalty shot ---> Find every penalty goal

2. Freekick shot ---> Find every freekick that has been kicked to score directly

3. Owngoal ---> Find every own goal

4. Counter attack and Ball recovery ---> Find every ball recovery that leads to a goal, each action can be divided in a counter attack or a ball recovery based on the location of the recovery and the time between it and the goal and the number of events between the recovery and the goal

5. Throw-in shot ---> Find every goal that starts with a throw-in and leads to a goal within a certain amount of events

6. Direct corner shot ---> Find every goal scored directly from the corner kick

7. Corner schema ---> Find every goal scored starting with a corner kick, the category of the goal could be different based on how the action went

8. Freekick schema ---> Find every goal scored starting with a freekick, the category of the goal could be different based on how the action went

9. Positional attack ---> Find every goal scored with a built action that has at least a certain amount of events before the goal

10. Goalkeeper's bounce ---> Find every goal that happens after a goalkeeper's save with the ball still playable

WYSCOUT GLOSSARY: https://dataglossary.wyscout.com/ WYSCOUT API DOCS: https://apidocs.wyscout.com/

Each function returns a pandas dataframe with goals that have the shot type of the function, the number of attempted shots (including both shots and goals) and the number of goals.

TO USE MAIN FUNCTIONS YOU'LL NEED SOME SIDE FUNCTIONS, NOT ALL OF THEM. YOU CAN FIND THEM INSIDE THE PROPER FOLDER.

There are also alternative written functions that do the same work as the other but these are written based on the SoccerAction package. Fucntions based on this package are slitly different from the original ones but the goal is the same. I've tried this package attempting to cover the lack of the true functions but there is still the same problem of accuracy. You can find the SoccerAction based function inside their proper folder.
