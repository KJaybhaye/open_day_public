import os
import sys
import importlib.util
import numpy as np
from agent_class import AbstractAgent


num_fields = 5
field_values = [5, 2, 8, 4, 3]
total_rounds = 5
dummy_name = "your_agent"
dummy_bals = [
    {"random_agent": 100, "uniform_agent": 100, dummy_name: 100},
    {"random_agent": 4, "uniform_agent": 20, dummy_name: 60},
]
dummy_rounds = [1, 5]
dummy_histories = [
    [],
    [
        {
            "random_agent": [0, 5, 5, 10, 1],
            "uniform_agent": [4, 4, 4, 4, 4],
            dummy_name: [4, 4, 4, 4, 4],
        },
        {
            "random_agent": [2, 2, 0, 6, 3],
            "uniform_agent": [4, 4, 4, 4, 4],
            dummy_name: [4, 4, 4, 4, 4],
        },
        {
            "random_agent": [2, 20, 7, 14, 1],
            "uniform_agent": [4, 4, 4, 4, 4],
            dummy_name: [0, 0, 0, 0, 0],
        },
        {
            "random_agent": [3, 7, 0, 1, 7],
            "uniform_agent": [4, 4, 4, 4, 4],
            dummy_name: [0, 0, 0, 0, 0],
        },
    ],
]


def validate_agent_submission(folder_path):
    print(f"--- Validating Agent in: {folder_path} ---")

    agent_file = os.path.join(folder_path, "agent.py")

    # 1. Check if file exists
    if not os.path.exists(agent_file):
        print(f"[ERROR] No 'agent.py' found in {folder_path}")
        return False

    # 2. Dynamically load the module
    try:
        # module_name = "participant_agent"
        # module_name = folder_path
        name = dummy_name
        spec = importlib.util.spec_from_file_location(name, agent_file)
        module = importlib.util.module_from_spec(spec)
        # Add the folder to sys.path so their internal imports work
        sys.path.append(folder_path)
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"[ERROR] Failed to import agent.py: {e}")
        return False

    # 3. Check for 'Agent' class
    if not hasattr(module, "Agent"):
        print("[ERROR] No class named 'Agent' found in agent.py")
        return False

    AgentClass = module.Agent

    # 4. Check Inheritance
    if not issubclass(AgentClass, AbstractAgent):
        print("[ERROR] Class 'Agent' must inherit from 'AbstractAgent'")
        return False

    # 5. Test Instantiation and get_allocation
    try:
        agent_instance = AgentClass(name=name)
        for i in range(len(dummy_rounds)):
            current_balance = dummy_bals[i][dummy_name]
            history = dummy_histories[i]
            balances = dummy_bals[i]
            current_round = dummy_rounds[i]

            print(
                f"[INFO] Testing 'get_allocation' for {name}..for round {current_round}/{total_rounds}..."
            )
            allocation = agent_instance.get_allocation(
                current_balance,
                field_values,
                num_fields,
                history,
                balances,
                total_rounds,
                current_round,
            )

            # 6. Validate Output Structure (Mirroring tournament logic)
            if not isinstance(allocation, (list, np.ndarray)):
                print(
                    f"[ERROR] Output must be a list or numpy array. Got: {type(allocation)}"
                )
                return False

            if len(allocation) != num_fields:
                print(
                    f"[ERROR] Allocation length ({len(allocation)}) doesn't match num_fields ({num_fields})"
                )
                return False

            alloc_sum = sum(allocation)
            if alloc_sum > current_balance:
                print(
                    f"[ERROR] Total allocation ({alloc_sum}) exceeds current balance ({current_balance})"
                )
                return False

            if any(x < 0 for x in allocation):
                print(f"[ERROR] Negative allocations are not allowed: {allocation}")
                return False

            print(f"[SUCCESS] Agent '{name}' passed all local checks!")
            print(f"Sample Output: {allocation}")
        return True

    except Exception as e:
        print(f"[ERROR] Agent crashed during execution: {e}")
        import traceback

        traceback.print_exc()
        return False
    finally:
        # Clean up path
        if folder_path in sys.path:
            sys.path.remove(folder_path)


if __name__ == "__main__":
    import tomllib

    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    # target_folder = "Your_Name"
    target_folder = config["player"]["NAME"]

    if os.path.exists(target_folder):
        validate_agent_submission(target_folder)
    else:
        print(
            f"Directory {target_folder} not found. Please update target_folder in validator.py"
        )
