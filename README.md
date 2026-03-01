

# Code & Conquer

Welcome to the IISc Open Day Game Challenge!

In this competition, you will design a strategy for a multi-agent game. You are a commander with a limited pool of soldiers. Over multiple rounds, you must decide how many soldiers to send to different battlefields and how many to keep in reserve for later rounds. In each round, the winner of a particular field earns points equal to the value of that field. At the end of the last round, the player with the most points wins.

## 🎮 The Rules
Detailed rules are provided in the [detailed_rules.md](detailed_rules.md) file.

1. **Multiple Battlefields:** There are `N` battlefields, each with a certain amount of points associated with it. (e.g., 5 Fields)
2. **Starting Balance:** Each player starts with the same fixed number of soldiers. (e.g., 100 Soldiers)
3. **Multiple Rounds:**The game runs for `T` rounds. (e.g., 10 rounds)
4. **Allocation:** In each round, you distribute some of your remaining soldiers across these battlefields.
5. **Winning:** For each battlefield, the player who sends the most soldiers wins the points corresponding to that field. In the event of a tie, everyone gets zero points.
6. **Resource Management:** Soldiers sent to battle **do not return**. You must manage your total budget across all rounds of the tournament. Fields start as empty at each round.
7. **Information:** You can see the history of what other agents did in previous rounds to adapt your strategy.

---
## Structure
- `env.py`: Game environment
- `agent_class.py`: Abstract class to be inherited for creation of agents
- `validate.py`: Validates the structure of `Your_name\your_agent.py` file and validates the values returned by `get_allocation` function
- `Sample_Agents`: Folder containing sample agents
- `Your_name`: Folder for your code
- `run_tournament.py`: Runs tournament between all the agents in `Sample_Agents` and the agent defined in `Your_name\your_agent.py`


## 🛠️ How to Write Your Agent

1. Change the name of `Your_name` folder to your name (e.g., `Alice_Bob`).
2. Inside that folder, write your code in the `get_allocation` function within `your_agent.py`.
3. **Important**: Keep your code inside a single file. Using multiple files and relative imports may lead to errors when running on different systems. 

## Configuration of Environment
You are given a sample environment. Note that the number of rounds, players, fields, field values, and starting soldiers may change for the final tournament. This information will be available to your agent’s `get_allocation` function through its arguments. 


### ⚠️ Important "DOs" and "Don'ts"

* **Do Not** change the function signature of `get_allocation`.
* **Do Not** rename the class `Agent`.
* **Do** use only standard libraries like numpy and pandas.
* **Do** run `validate.py` file to do some validation checks
<!-- * **Do Not** use external libraries other than `numpy`. -->

### Example Template (`your_agent.py`):

```python
from agent_class import AbstractAgent
import numpy as np

class Agent(AbstractAgent):
    def get_allocation(
        self,
        current_balance,
        field_values,
        num_fields,
        history,
        balances,
        total_rounds,
        current_round,
    ) -> list:
        """
        Spend available units uniformly across all fields and rounds
        On last round spend whole balance
        """
        if current_round == total_rounds:
            round_spending = current_balance
        else:
            round_spending = current_balance // (total_rounds - current_round + 1)
            round_spending = min(current_balance, round_spending)
        average = round_spending // num_fields
        return [average] * num_fields

```

---

## How to Run the Experimentation

You can test your agent against the baseline bots provided in the `Sample_Agents` folder. You can add more agents here to try against each other. Environment configuration is in `config.toml` file.

First, change the `NAME` variable in `config.toml` to the name of your folder. Run the   `validate.py` to check if your folder structure and agent code is proper. Then run the `run_tournament.py`. It loads all the agents defined in `Sample_Agents` folder and the agent defined in `Your_name` folder and runs matches between them.



### Option 1: Using `pip`

1. Install the requirements:
```bash
pip install numpy

```


2. Run the tournament:
```bash
python run_tournament.py

```



### Option 2: Using `uv`

If you have `uv` installed, you can run the tournament without manually managing environments:

```bash
uv run run_tournament.py

```

*(This will automatically handle dependencies and execution in a transient environment.)*

---

## 📤 Submission Instructions

Once you are happy with your strategy:

1. Submit `Your_name` folder.
2. If you used helper files, include them in the same folder.
3. Submission method: To be announced.

