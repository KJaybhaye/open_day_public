import numpy as np
import tomllib
from env import Env
import importlib.util
import os
from agent_class import AbstractAgent


class HumanAgent(AbstractAgent):
    def __init__(self, name="Human"):
        super().__init__(name)

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
        print(f"\n--- YOUR TURN: Round {current_round}/{total_rounds} ---")
        print(f"Current Balance: {current_balance}")
        print(f"Field Values:    {field_values}")

        while True:
            try:
                user_input = input(f"Enter {num_fields} integers separated by spaces: ")
                allocation = [int(x) for x in user_input.split()]

                if len(allocation) != num_fields:
                    print(f"Error: You must provide exactly {num_fields} values.")
                    continue

                if sum(allocation) > current_balance:
                    print(
                        f"Error: Total {sum(allocation)} exceeds your balance of {current_balance}."
                    )
                    continue

                if any(x < 0 for x in allocation):
                    print("Error: Allocations cannot be negative.")
                    continue

                return allocation
            except ValueError:
                print("Error: Please enter valid integers.")


def load_agent(file_path):
    module_name = os.path.basename(file_path)[:-3]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Agent(name=module_name)


def select_agents(folder_path="Sample_Agents"):
    """Lists available agents and lets the user select opponents via input."""
    # 1. Scan the folder for valid .py files
    available_files = [
        f for f in os.listdir(folder_path) if f.endswith(".py") and f != "__init__.py"
    ]

    if not available_files:
        print("No agents found in Sample_Agents!")
        return []

    print("\n--- AVAILABLE OPPONENTS ---")
    for idx, filename in enumerate(available_files):
        print(f"[{idx}] {filename[:-3]}")  # Show name without .py extension

    # 2. Get user selection
    while True:
        try:
            user_input = input(
                "\nEnter the index of 1 or 2 agents (e.g., '0' or '0 1'): "
            )
            indices = [int(i) for i in user_input.split()]

            if not (1 <= len(indices) <= 2):
                print("Please select either 1 or 2 opponents.")
                continue

            if any(i < 0 or i >= len(available_files) for i in indices):
                print("One or more indices are out of range.")
                continue

            # 3. Load and return the selected agent instances
            selected_agents = []
            for i in indices:
                file_path = os.path.join(folder_path, available_files[i])
                selected_agents.append(load_agent(file_path))

            return selected_agents

        except ValueError:
            print("Invalid input. Please enter numbers separated by spaces.")
            return []


def play_game():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    num_fields = config["human_play"]["num_fields"]
    rounds = config["human_play"]["rounds"]
    start_balance = config["human_play"]["start_balance"]
    field_values = [np.random.randint(2, 10) for _ in range(num_fields)]

    opponents = [
        load_agent("Sample_Agents/random_agent.py"),
    ]

    human = HumanAgent(name="You")
    opponents = select_agents()
    if not opponents:
        print("Error: No opponent selected.")
    all_agents = [human] + opponents
    agent_names = [a.name for a in all_agents]

    env = Env(
        agent_names,
        field_values,
        num_fields=num_fields,
        total_rounds=rounds,
        starting_soldiers=start_balance,
    )

    print("=" * 40)
    print("WELCOME TO THE RESOURCE ALLOCATION GAME")
    print("=" * 40)
    print(f"Opponents: {[a.name for a in opponents]}")
    print(f"Field Values: {field_values}")

    for r in range(1, rounds + 1):
        current_state = env.get_state()
        round_allocations = {}

        # Get moves
        for agent in all_agents:
            move = agent.get_allocation(
                current_state["balances"][agent.name],
                env.field_values,
                env.num_fields,
                current_state["history"],
                current_state["balances"],
                env.total_rounds,
                r,
            )
            round_allocations[agent.name] = move

        # Step Environment
        state, winners = env.step(round_allocations)

        # Show Round Summary
        print(f"\n--- ROUND {r} SUMMARY ---")
        header = f"{'Field':<8} | {'Value':<5} | {'Winner':<12} | {'Allocations (You vs Others)'}"
        print(header)
        print("-" * len(header))

        for i in range(num_fields):
            winner_name = agent_names[winners[i]] if winners[i] >= 0 else "TIE"
            allocs = [round_allocations[name][i] for name in agent_names]
            print(f"Field {i:<2} | {field_values[i]:<5} | {winner_name:<12} | {allocs}")

        print(f"\nScores:   {state['scores']}")
        print(f"Balances: {state['balances']}")
        input("\nPress Enter for next round...")

    # Final Result
    final_scores = state["scores"]
    winner = max(final_scores, key=final_scores.get)
    print("\n" + "=" * 40)
    print(f"GAME OVER! WINNER: {winner}")
    print("=" * 40)


if __name__ == "__main__":
    play_game()
