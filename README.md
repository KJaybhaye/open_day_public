

# Agent War

Welcome to the IISc Open Day Game Challenge!

In this competition, you will design a strategy for a multi-agent game. You are a commander with a limited pool of soldiers. Over multiple rounds, you must decide how many soldiers to send to different battlefields and how many to keep in reserve for later rounds. At each round winner of a particular field will win points equal to the value of that field. At end of last round, the player with most points wins.

## 🎮 The Rules
Detailed rules are provided in the [detailed_rules.md](detailed_rules.md) file.

1. **Multiple Battlefields:** There are N battlefields, each with a certain amount of points associated with it. (eg. 5 Fields)
2. **Starting Balance:** Each player starts with same fixed number of soldiers. (eg. 100 Soldirs)
3. **Multiple Rounds:** Game runs for T number of rounds. (e.g 10 rounds)
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
2. Inside that folder, inside the `your_agent.py` file write you code in `get_allocation` function.

## Coniguration of Environment
You are given a sample environment. Note that number of rounds, number of players, number of fileds, field values and starting soldiers may be changed for final tournament. This information will be availble to your agents `get_allocation` function through arguments. 


### ⚠️ Important "DOs" and "Don'ts"

* **Do Not** change the function signature of `get_allocation`.
* **Do Not** rename the class `Agent`.
* **Do** use only standard libraries like numpy and pandas.
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

First change the `NAME` variable in `config.toml` to name of your folder. Run the   `validate.py` to check if your folder strucute and agent code is proper. Then run the `run_tournament.py`. It takes all the agents defined in `Sample_Agents` folder and the agents defined in `Your_name` folder and makes them play against each other.



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
3. Submission method: Will be given soon.

