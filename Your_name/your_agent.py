from agent_class import AbstractAgent
import numpy as np
import random


class Agent(AbstractAgent):
    """
    Your agent template.
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
        Write your code here
        """
        return [0] * num_fields
