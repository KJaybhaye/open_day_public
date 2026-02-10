import os
import importlib.util
import numpy as np
from env import Env

YOUR_NAME = "Your_Name"


def load_agents(folder_path="Sample_Agents"):
    """Dynamically loads all Agent classes from the Agents folder."""
    agents = []
    paths = [folder_path, YOUR_NAME]
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
    return agents


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
            move = np.array(move)
        except Exception as e:
            print(f"Agent {agent.name} crashed: {e}")
            move = np.zeros(env.num_fields)

        if (
            np.any(move < 0)
            or np.sum(move) > current_state["balances"][agent.name]
            or len(move) != env.num_fields
        ):
            print(f"Invalid move from {agent.name}. Disqualifying round.")
            move = np.zeros(env.num_fields)

        round_allocations[agent.name] = move.tolist()
        for n in range(env.num_fields):
            field_allocations[n].append(int(move[n]))

    state, winners = env.step(round_allocations)
    return state, winners, field_allocations


def start_tournament():
    # Setup
    num_fields = 5
    field_values = [np.random.randint(2, 10) for _ in range(num_fields)]
    agents = load_agents()
    agent_names = [a.name for a in agents]

    env = Env(
        agent_names,
        field_values,
        num_fields=num_fields,
        total_rounds=10,
        starting_soldiers=200,
    )

    print(f"--- Tournament Start ---")
    print(f"Fields: {num_fields} | Values: {field_values}")
    print(f"Participants: {', '.join(agent_names)}\n")

    for r in range(1, env.total_rounds + 1):
        state, winners, field_allocations = run_round_logic(env, agents)

        print(f"ROUND {r} RESULTS:")
        for i, w in enumerate(winners):
            print(
                f"  Field {i} (Val {field_values[i]}): Winner -> {agent_names[w] if w >= 0 else 'Tie'}  Allocation: {field_allocations[i]}"
            )

        print(f"Scores: {state['scores']}")
        print(f"Balances: {state['balances']}")
        print("-" * 30)

    # Final Result
    winner_name = max(state["scores"], key=state["scores"].get)
    print(f"\n🏆 TOURNAMENT OVER. WINNER: {winner_name} 🏆")


if __name__ == "__main__":
    start_tournament()
