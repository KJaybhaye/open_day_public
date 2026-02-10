from agent_class import AbstractAgent
import numpy as np
import random


class Agent(AbstractAgent):
    """
    Acts randomly.
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
        rounds_remaining = (total_rounds - current_round) + 1

        share = current_balance // rounds_remaining
        round_spend = random.randint(int(share * 0.5), int(share * 2))
        round_spend = min(round_spend, current_balance)

        if round_spend == 0:
            return [0] * num_fields

        cuts = sorted([random.randint(0, round_spend) for _ in range(num_fields - 1)])
        points = [0] + cuts + [round_spend]
        allocation = [points[i + 1] - points[i] for i in range(num_fields)]

        random.shuffle(allocation)
        return allocation
