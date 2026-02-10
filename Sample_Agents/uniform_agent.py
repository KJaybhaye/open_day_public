from agent_class import AbstractAgent
import numpy as np
import random


class Agent(AbstractAgent):
    """
    puts uniform soldirs for each field in each round.

    You can access name of your own agent using self.name which is a string value
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
        remaining_rounds = total_rounds - current_round
        round_spending = current_balance // remaining_rounds
        average = round_spending // num_fields
        return [average] * num_fields
