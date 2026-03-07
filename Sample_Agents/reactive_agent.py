from agent_class import AbstractAgent
import numpy as np


class Agent(AbstractAgent):
    """Example: Looks at what happened last round and adds 1 to each field."""

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
        if not history:
            return [
                int((current_balance / total_rounds) // (num_fields * 2))
            ] * num_fields

        last_round = history[-1]
        # Find the max deployed by anyone last round on each field
        all_deployments = np.array(list(last_round.values()), dtype=int)
        max_last_round = np.max(all_deployments, axis=0)

        my_move = max_last_round + 1
        if sum(my_move) > current_balance:
            round_spending = current_balance // (total_rounds - current_round + 1)
            round_spending = min(current_balance, round_spending)
            return [round_spending // num_fields] * num_fields
        # To-do if still remaining soldiers put all on high value field

        return my_move.tolist()
