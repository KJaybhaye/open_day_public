

# Agent War

Welcome to the IISc Open Day Game Challenge!

In this competition, you will design a strategy for a multi-agent game. You are a commander with a limited pool of soldiers. Over multiple rounds, you must decide how many soldiers to send to different battlefields and how many to keep in reserve for later rounds. At each round winner of a particular field will win gold equalt ot the value of that field. At end of last round player with most gold wins.

## 🎮 The Rules

1. **Multiple Battlefields:** There are  battlefields, each with a different point value.
2. **Allocation:** In each round, you distribute some of your remaining soldiers across these battlefields.
3. **Winning:** For each battlefield, the player who sends the most soldiers wins the points for that field. In the event of a tie, the points are split.
4. **Resource Management:** Soldiers sent to battle **do not return**. You must manage your total budget across all rounds of the tournament.
5. **Information:** You can see the history of what other agents did in previous rounds to adapt your strategy.

---


## 🛠️ How to Write Your Agent

1. Change the name of `Your_Name` folder to your name (e.g., `Alice_Smith_Agent`).
2. Inside that folder, inside the `agent.py` file write you code in `get_allocation` function.

## Coniguration of Environment
You are given a sample environment. Note that number of rounds, number of players, number of fileds, field values and starting soldiers may be changed for final tournament. This information will be availble to your agents `get_allocation` function through arguments. 


### ⚠️ Important "Don'ts"

* **Do Not** change the function signature of `get_allocation`.
* **Do Not** rename the class `Agent`.
* **Do Not** attempt to modify the `history` or `balances` dictionaries (we pass you copies, but play fair!).
* **Do Not** use external libraries other than `numpy`.

### Example Template (`agent.py`):

```python
from agent_class import AbstractAgent
import numpy as np

class Agent(AbstractAgent):
    def get_allocation(self, my_balance, field_values, num_fields, history, current_balances, total_rounds, current_round):
        # Example strategy: Distribute remaining soldiers equally across all fields
        # but only spend 20% of the current balance per round.
        
        move = np.zeros(num_fields)
        budget_for_this_round = my_balance * 0.2
        
        share = budget_for_this_round / num_fields
        move.fill(share)
        
        return move.tolist()

```

---

## 🚀 How to Run the Experimentation Sandbox

Before submitting, you should test your agent against the baseline bots provided in the `Sample_Agents` folder. You can add more agents here to try against each other.

First change the `YOUR_NAME` variable in `run_tournament.py` to name of your folder. Then run the `run_tournament.py` as follow:


### Option 1: Using `pip` (Standard)

1. Install the requirements:
```bash
pip install numpy

```


2. Run the tournament:
```bash
python tournament_runner.py

```



### Option 2: Using `uv` (Fast / Recommended for 2026)

If you have `uv` installed, you can run the tournament without manually managing environments:

```bash
uv run tournament_runner.py

```

*(This will automatically handle dependencies and execution in a transient environment.)*

---

## 📤 Submission Instructions

Once you are happy with your strategy:

1. Submit `Your_Name` folder.
2. If you used helper files, include them in the same folder.
3. Submission method: Will be given later.

**Note:** Our final tournament script will dynamically scan your folder and load your `Agent` class. If the folder structure or class name is incorrect, your agent will be unable to join the battle!

