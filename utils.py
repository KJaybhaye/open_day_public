import os
import importlib.util


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
        print(f"No agents found in {folder_path}!")
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
