import numpy as np
from agent_class import AbstractAgent


class Agent(AbstractAgent):
    """
    Saves resources for later rounds. Identifies weak fields
    and only wins them if the cost is below the 'fair share' budget.
    """

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
        rounds_left = (total_rounds - current_round) + 1

        # 1. Budgeting: Only spend a fraction of remaining balance
        # We spend slightly more as rounds progress (aggressive finish)
        spend_ratio = 1 / (rounds_left + 0.5)
        round_budget = int(current_balance * spend_ratio)

        if not history:
            # Start very lean to save for later
            return [round_budget // num_fields] * num_fields

        # 2. Analyze 'Heat' (same as before)
        all_maxes = [np.max(list(r.values()), axis=0) for r in history]
        historical_heat = np.mean(all_maxes, axis=0)
        least_contested = np.argsort(historical_heat)

        # 3. Allocation
        my_move = np.zeros(num_fields, dtype=int)
        remaining_round_pool = round_budget

        for idx in least_contested:
            # Target cost = historical max + 1
            cost_to_win = int(historical_heat[idx]) + 1

            # Only take the field if it's "affordable" within this round's budget
            if remaining_round_pool >= cost_to_win:
                my_move[idx] = cost_to_win
                remaining_round_pool -= cost_to_win
            else:
                break  # Save the remaining_round_pool for other rounds

        return my_move.tolist()
