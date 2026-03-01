import os
import sys
import importlib.util
import numpy as np
from agent_class import AbstractAgent
from multiprocessing import Process


TIMEOUT = 30  # seconds to wait for output from a get_allocation function
NUM_FIELDS = 5
FIELD_VALUES = [5, 2, 8, 4, 3]
TOTAL_ROUNDS = 5
DUMMY_NAME = "your_agent"
DUMMY_BALANCES = [
    {"random_agent": 100, "uniform_agent": 100, DUMMY_NAME: 100},
    {"random_agent": 4, "uniform_agent": 20, DUMMY_NAME: 60},
]
DUMMY_ROUNDS = [1, 5]
DUMMY_HISTORIES = [
    [],
    [
        {
            "random_agent": [0, 5, 5, 10, 1],
            "uniform_agent": [4, 4, 4, 4, 4],
            DUMMY_NAME: [4, 4, 4, 4, 4],
        },
        {
            "random_agent": [2, 2, 0, 6, 3],
            "uniform_agent": [4, 4, 4, 4, 4],
            DUMMY_NAME: [4, 4, 4, 4, 4],
        },
        {
            "random_agent": [2, 20, 7, 14, 1],
            "uniform_agent": [4, 4, 4, 4, 4],
            DUMMY_NAME: [0, 0, 0, 0, 0],
        },
        {
            "random_agent": [3, 7, 0, 1, 7],
            "uniform_agent": [4, 4, 4, 4, 4],
            DUMMY_NAME: [0, 0, 0, 0, 0],
        },
    ],
]


class FunctionTimeoutError(Exception):
    """Exception raised when a function takes too long."""

    def __init__(self, message="The operation timed out"):
        self.message = message
        super().__init__(self.message)


def validate_output(
    agent_instance, current_balance, history, balances, total_rounds, current_round
):
    allocation = agent_instance.get_allocation(
        current_balance,
        FIELD_VALUES,
        NUM_FIELDS,
        history,
        balances,
        total_rounds,
        current_round,
    )

    # Validate Output Structure (Mirroring tournament logic)
    if not isinstance(allocation, (list, np.ndarray)):
        print(f"[ERROR] Output must be a list or numpy array. Got: {type(allocation)}")
        return False

    if len(allocation) != NUM_FIELDS:
        print(
            f"[ERROR] Allocation length ({len(allocation)}) doesn't match NUM_FIELDS ({NUM_FIELDS})"
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

    print(f"[SUCCESS] Agent '{agent_instance.name}' passed all local checks!")
    print(f"Sample Output: {allocation}")


def validate_agent_submission(folder_path):
    print(f"--- Validating Agent in: {folder_path} ---")

    agent_file = os.path.join(folder_path, "your_agent.py")

    # 1. Check if file exists
    if not os.path.exists(agent_file):
        print(f"[ERROR] No 'your_agent.py' found in {folder_path}")
        return False

    # 2. Dynamically load the module
    try:
        name = DUMMY_NAME
        spec = importlib.util.spec_from_file_location(name, agent_file)
        module = importlib.util.module_from_spec(spec)
        # Add the folder to sys.path so their internal imports work
        # sys.path.append(folder_path)
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"[ERROR] Failed to import your_agent.py: {e}")
        return False

    # 3. Check for 'Agent' class
    if not hasattr(module, "Agent"):
        print("[ERROR] No class named 'Agent' found in your_agent.py")
        return False

    AgentClass = module.Agent

    # 4. Check Inheritance
    if not issubclass(AgentClass, AbstractAgent):
        print("[ERROR] Class 'Agent' must inherit from 'AbstractAgent'")
        return False

    # 5. Test Instantiation and get_allocation function
    try:
        agent_instance = AgentClass(name=name)
        for i in range(len(DUMMY_ROUNDS)):
            current_balance = DUMMY_BALANCES[i][DUMMY_NAME]
            history = DUMMY_HISTORIES[i]
            balances = DUMMY_BALANCES[i]
            current_round = DUMMY_ROUNDS[i]

            print(
                f"[INFO] Testing 'get_allocation' for {name}..for round {current_round}/{TOTAL_ROUNDS}..."
            )

            # 6. Validate output
            p = Process(
                target=validate_output,
                args=(
                    agent_instance,
                    current_balance,
                    history,
                    balances,
                    TOTAL_ROUNDS,
                    current_round,
                ),
            )
            p.start()

            # wait for MAX_T seconds only
            p.join(timeout=TIMEOUT)
            if p.is_alive():
                p.terminate()  # Kill the process
                p.join()
                raise FunctionTimeoutError(
                    "Function is taking too long to return a value!"
                )
                # print("Function timed out and was terminated.")

            # validate_output(
            #     agent_instance,
            #     current_balance,
            #     history,
            #     balances,
            #     TOTAL_ROUNDS,
            #     current_round,
            # )
        return True

    except FunctionTimeoutError as e:
        print(f"[ERROR] : {e}")
        return False

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
