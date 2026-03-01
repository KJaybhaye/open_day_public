from agent_class import AbstractAgent
import numpy as np
import random


class Agent(AbstractAgent):
    """
    puts uniform soldiers for each field in each round.
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
        """
        Spend available units uniformly across all fields and rounds
        On last round spend whole balance
        """
        if current_round == total_rounds:
            round_spending = current_balance
        else:
            round_spending = current_balance // (total_rounds - current_round + 1)
            round_spending = min(current_balance, round_spending)
        average = round_spending // num_fields
        return [average] * num_fields
