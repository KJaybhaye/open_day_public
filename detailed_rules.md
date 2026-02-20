# ⚔️ Agent War: IISc Open Day Challenge

## 📜 The Core Rules

### 1. Resources & Battlefields

* **Soldiers:** Every player starts with an identical starting balance of soldiers.
* **Battlefields:** There are `n` number of battlefields. Each has a specific **Gold Value** that remains **constant** throughout the entire game.
* **Deployment:** Each round, you distribute your soldiers across these `n` fields(cannot deploy more than you balance).

### 2. Winning a Field

* **Highest Bidder:** The player who commits the **highest number of soldiers** to a field wins all the gold for that field for that round.
* **The Tie-Break:** If two or more players tie for the highest number of soldiers, **no one wins the gold** (0 gold awarded).
* **Sunk Costs:** Soldiers deployed to battle **do not return**, regardless of whether you win or lose. They are permanently removed from your balance.

### 3. Victory Condition

The game lasts for `T` rounds. The player with the **highest cumulative gold** at the end of the final round is the winner.

---

## 📖 A Walkthrough Example

To understand how **Agent War** plays out, let’s look at a 3-round game with 3 players (**Alpha**, **Beta**, and **Gamma**) across 5 fields.

**Setup:**

* **Starting Soldiers:** 50 each.
* **Field Gold Values:** `[10, 20, 30, 10, 5]` (Total 75 gold available per round).

### Round 1

Players distribute their first set of soldiers.

| Field (Gold Value) | Alpha (Spent) | Beta (Spent) | Gamma (Spent) | Winner | Gold Awarded |
| --- | --- | --- | --- | --- | --- |
| **Field 1 (10)** | 5 | **10** | 2 | **Beta** | Beta +10 |
| **Field 2 (20)** | **15** | 0 | 10 | **Alpha** | Alpha +20 |
| **Field 3 (30)** | 10 | **12** | 10 | **Beta** | Beta +30 |
| **Field 4 (10)** | 5 | 5 | 5 | **TIE** | None (0) |
| **Field 5 (5)** | 0 | 0 | **10** | **Gamma** | Gamma +5 |

* **Round 1 Totals:** Alpha: 20 | Beta: 40 | Gamma: 5
* **Soldiers Remaining:** Alpha: 15 | Beta: 23 | Gamma: 13

---

### Round 2

In this round, Beta tries to dominate again, but Alpha and Gamma adapt.

| Field (Gold Value) | Alpha (Spent) | Beta (Spent) | Gamma (Spent) | Winner | Gold Awarded |
| --- | --- | --- | --- | --- | --- |
| **Field 1 (10)** | 0 | **5** | 0 | **Beta** | Beta +10 |
| **Field 2 (20)** | 0 | **5** | 0 | **Beta** | Beta +20 |
| **Field 3 (30)** | **10** | 10 | 5 | **TIE** | None (0) |
| **Field 4 (10)** | 5 | 3 | **8** | **Gamma** | Gamma +10 |
| **Field 5 (5)** | 0 | 0 | 0 | **TIE** | None (0) |

* **Round 2 Totals:** Alpha: 0 | Beta: 30 | Gamma: 10
* **Soldiers Remaining:** Alpha: 0 | Beta: 0 | Gamma: 0

> **⚠️ Strategic Note:** Alpha and Beta are now **bankrupt** (0 soldiers left). Because they spent everything in Rounds 1 and 2, they cannot participate in the final round!

---

### Round 3

Gamma was the only player who saved a small reserve for the end.

| Field (Gold Value) | Alpha (Spent) | Beta (Spent) | Gamma (Spent) | Winner | Gold Awarded |
| --- | --- | --- | --- | --- | --- |
| **Field 1 (10)** | 0 | 0 | 0 | TIE | 0 |
| **Field 2 (20)** | 0 | 0 | **1** | **Gamma**  | Gamma +20 |
| **Field 3 (30)** | 0 | 0 | 0 | TIE | 0 |
| **Field 4 (10)** | 0 | 0 | 0 | TIE | 0 |
| **Field 5 (5)** | 0 | 0 | **1** | **Gamma** | Gamma +5 |

---

### 🏆 Final Leaderboard

| Rank | Player | Total Gold | Logic |
| --- | --- | --- | --- |
| **1st** | **Beta** | **70** | Dominated early with high spending. |
| **2nd** | **Gamma** | **35** | Strategically saved soldiers to win the final round 
| **3rd** | **Alpha** | **20** | Won one high-value field but tied in others. | unopposed. |




---

## 🖥️ Technical Implementation

Your agent must implement the `get_allocation` method in `your_agent.py`. The environment will call this function every round.

### Function Signature

```python
def get_allocation(
    self,
    current_balance,  # Int: Your remaining soldiers
    field_values,     # List[Int]: Gold values (e.g., [5, 2, 8, 4, 3])
    num_fields,       # Int: Total number of fields
    history,          # List[Dict]: Historical moves (see below)
    balances,         # Dict: Current soldier balances of all players
    total_rounds,     # Int: Total game duration
    current_round,    # Int: Current round (1 to total_rounds)
) -> list:
    # Your logic here
    return [soldiers_f1, soldiers_f2, ... soldiers_fN]

```

### Data Structure: The `history` Variable

The `history` parameter is a list of dictionaries. Each dictionary represents a completed round and contains the allocations made by every agent.

**Example of `history` at Round 3:**

```python
[
    { # Round 1
        "agent_alpha": [10, 5, 0], 
        "agent_beta": [5, 5, 5],
        "your_agent": [0, 10, 5]
    },
    { # Round 2
        "agent_alpha": [2, 2, 2],
        "agent_beta": [10, 0, 0],
        "your_agent": [5, 5, 5]
    }
]

```

---


### 🛠️ Submission Checklist

* [ ] Rename your folder from `Your_name` to your actual name (e.g., `Satish_Kumar`).
* [ ] Ensure `get_allocation` returns a list of **integers**.
* [ ] Ensure the sum of your allocation is  `current_balance`.
* [ ] Test your agent against the provided `random_agent` and `uniform_agent` samples.