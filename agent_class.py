import numpy as np
from abc import ABC, abstractmethod


class AbstractAgent(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
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
        pass
