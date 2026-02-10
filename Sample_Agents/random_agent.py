from agent_class import AbstractAgent
import numpy as np
import random


class Agent(AbstractAgent):
    """
    Acts randomly but preserves the majority of its balance for future rounds.
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
        total_rounds = 10
        current_round = len(history) + 1
        rounds_remaining = (total_rounds - current_round) + 1

        # 1. Determine a sustainable budget for this round
        # We take our "fair share" and add a bit of randomness to the spend amount
        fair_share = current_balance // rounds_remaining
        round_spend = random.randint(int(fair_share * 0.5), int(fair_share * 2))
        round_spend = min(round_spend, current_balance)  # Safety cap

        if round_spend == 0:
            return [0] * num_fields

        # 2. Randomly distribute the 'round_spend' across fields
        cuts = sorted([random.randint(0, round_spend) for _ in range(num_fields - 1)])
        points = [0] + cuts + [round_spend]
        allocation = [points[i + 1] - points[i] for i in range(num_fields)]

        random.shuffle(allocation)
        return allocation
