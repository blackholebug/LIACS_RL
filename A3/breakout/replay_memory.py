import numpy as np
import random


class ReplayMemory():
    def __init__(self, memory_size=1000000, batch_size=32):
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.replays = []

    def add_replay(self, state, action, reward, next_state, terminal):
        new_replay = {"state": state,
                      "action": action,
                      "reward": reward,
                      "next_state": next_state,
                      "terminal": terminal}
        self.replays.append(new_replay)
        if len(self.replays) > self.memory_size:
            self.replays.pop(0)

    def gen_batch(self):
        batch = np.asarray(random.sample(self.replays, self.batch_size))
        return batch
