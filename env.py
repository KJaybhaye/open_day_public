import numpy as np
import copy


class Env:
    def __init__(
        self,
        agent_names,
        field_values,
        num_fields=5,
        total_rounds=5,
        starting_soldiers=100,
    ):
        self.agent_names = agent_names
        self.field_values = field_values
        self.num_fields = num_fields
        self.total_rounds = total_rounds
        self.starting_soldiers = starting_soldiers
        self.reset()

    def reset(self):
        """Resets the environment state for a new tournament."""
        self.current_round = 0
        self.balances = {name: self.starting_soldiers for name in self.agent_names}
        self.history = []
        self.scores = {name: 0 for name in self.agent_names}
        return self.get_state()

    def get_state(self):
        """Returns the current state of the environment."""
        return {
            "balances": copy.deepcopy(self.balances),
            "history": copy.deepcopy(self.history),
            "scores": copy.deepcopy(self.scores),
            "current_round": self.current_round,
        }

    def step(self, round_allocations):
        """
        Processes one round of moves.
        round_allocations: dict {agent_name: [list of soldiers per field]}
        """
        self.current_round += 1

        # 1. Deduct resources
        for name, move in round_allocations.items():
            self.balances[name] -= sum(move)

        # 2. Determine winners per field
        # Matrix shape: (num_agents, num_fields)
        alloc_matrix = np.array([round_allocations[name] for name in self.agent_names])
        round_winners = []

        for f in range(self.num_fields):
            field_troops = alloc_matrix[:, f]
            max_val = np.max(field_troops)

            if max_val > 0:
                # Find all indices that tied for the max
                winners_idx = np.where(field_troops == max_val)[0]
                if len(winners_idx) == 1:
                    self.scores[self.agent_names[winners_idx[0]]] += int(
                        self.field_values[f]
                    )
                    round_winners.append(winners_idx[0])
                else:
                    round_winners.append(-1)
            else:
                round_winners.append(-1)

        # 3. Update history
        self.history.append(copy.deepcopy(round_allocations))

        return self.get_state(), round_winners
