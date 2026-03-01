import os
import importlib.util
import numpy as np
from env import Env
import tomllib
import sys

with open("config.toml", "rb") as f:
    config = tomllib.load(f)


def load_agents(folder_path="Sample_Agents"):
    """Dynamically loads all Agent classes from the Agents folder."""
    agents = []
    paths = [folder_path]
    for f_path in paths:
        for filename in os.listdir(f_path):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                spec = importlib.util.spec_from_file_location(
                    module_name, os.path.join(f_path, filename)
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Create an instance of the 'Agent' class inside the module
                if hasattr(module, "Agent"):
                    # We use the filename (without .py) as the unique agent name
                    agent_instance = module.Agent(name=module_name)
                    agents.append(agent_instance)
    name = config["player"]["NAME"]
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(name, "your_agent.py")
    )
    module = importlib.util.module_from_spec(spec)
    # sys.path.append(name)
    spec.loader.exec_module(module)

    # Create an instance of the 'Agent' class inside the module
    if hasattr(module, "Agent"):
        # We use the filename (without .py) as the unique agent name
        agent_instance = module.Agent(name="Your Agent")
        agents.append(agent_instance)

    return agents


def validate_allocation(allocation, n, t, name):
    """
    Validates the allocation list based on:
    1. Length must be exactly N.
    2. All values must be non-negative integers.
    3. The sum of values must be strictly less than T.

    Returns: The original list if valid, otherwise a list of N zeros.
    """
    fallback = np.zeros(n, dtype=int)

    # 1. Check if input is list-like and has correct length
    if not isinstance(allocation, (list, np.ndarray)) or len(allocation) != n:
        return fallback

    try:
        # Convert to numpy array for vectorized checks
        arr = np.array(allocation)

        # 2. Check for integer types (or floats that are equivalent to integers)
        # and ensure all values are positive (>= 0)
        # Change to (arr > 0) if 0 is strictly forbidden.
        is_integer_type = np.issubdtype(arr.dtype, np.integer) or np.all(
            np.equal(np.mod(arr, 1), 0)
        )
        is_positive = np.all(arr >= 0)

        if not (is_integer_type and is_positive):
            print(f"Invalid move from {name}. Disqualifying round.")
            return fallback

        # 3. Check if sum is smaller than T
        if np.sum(arr) > t:
            print(f"Invalid move from {name}. Disqualifying round.")
            return fallback

        # Return as a standard list of integers
        return arr.astype(int)

    except Exception as e:
        # Catch-all for unexpected data types within the list (e.g., strings)
        print(f"Invalid move from {name}. Disqualifying round.")
        return fallback


def run_round_logic(env, agents):
    """Referees the round: Gets moves, validates them, and calls env.step."""
    current_state = env.get_state()
    round_allocations = {}
    field_allocations = [[] for i in range(env.num_fields)]
    # print(field_allocations)

    for agent in agents:
        # Get raw move from participant code
        try:
            move = agent.get_allocation(
                current_state["balances"][agent.name],
                env.field_values,
                env.num_fields,
                current_state["history"],
                current_state["balances"],
                env.total_rounds,
                current_state["current_round"] + 1,
            )
            move = validate_allocation(
                move, env.num_fields, current_state["balances"][agent.name], agent.name
            )
            move = np.array(move)
        except Exception as e:
            print(f"Agent {agent.name} crashed: {e}")
            move = np.zeros(env.num_fields)

        round_allocations[agent.name] = move.tolist()
        for n in range(env.num_fields):
            field_allocations[n].append(int(move[n]))

    state, winners = env.step(round_allocations)
    return state, winners, field_allocations


def start_tournament():
    # Setup
    num_fields = config["env"]["num_fields"]
    rounds = config["env"]["rounds"]
    start_balance = config["env"]["start_balance"]
    field_values = [np.random.randint(2, 10) for _ in range(num_fields)]
    agents = load_agents()
    agent_names = [a.name for a in agents]

    env = Env(
        agent_names,
        field_values,
        num_fields=num_fields,
        total_rounds=rounds,
        starting_soldiers=start_balance,
    )

    print("--- Tournament Start ---")
    print(f"Fields: {num_fields} | Values: {field_values}")
    print(f"Participants: {', '.join(agent_names)}\n")

    for r in range(1, env.total_rounds + 1):
        state, winners, field_allocations = run_round_logic(env, agents)

        print(f"ROUND {r} RESULTS:")
        for i, w in enumerate(winners):
            print(
                f"  Field {i} (Val {field_values[i]}): Winner -> {agent_names[w] if w >= 0 else 'Tie'}  Allocations: {field_allocations[i]}"
            )

        print(f"Scores: {state['scores']}")
        print(f"Balances: {state['balances']}")
        print("-" * 30)
        print("Press ENTER to continue.....")
        input()

    # Final Result
    # state["scores"] = {"random_agent": 51, "uniform_agent": 122, "Your Agent": 122}
    max_score = max(state["scores"].values())
    winners = [k for k in state["scores"].keys() if state["scores"].get(k) == max_score]
    if len(winners) > 1:
        print(
            f"\n TOURNAMENT OVER. RESULT: Tie between {','.join(winners[:-1])} and {winners[-1]}"
        )
    else:
        print(f"\n🏆 TOURNAMENT OVER. WINNER: {winners[0]} 🏆")

    if config["player"]["NAME"] in sys.path:
        sys.path.remove(config["player"]["NAME"])


if __name__ == "__main__":
    start_tournament()
