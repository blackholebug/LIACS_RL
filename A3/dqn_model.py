import numpy as np
import os
import random
import shutil

from logger import Logger
from neural_network import CNN
from replay_memory import ReplayMemory

from args import MEMORY_SIZE, REPLAY_START_NUMBER, EPSILON_MIN, EPSILON_TEST, EPSILON_STEPS

GAMMA = 0.99
BATCH_SIZE = 32
TRAINING_FREQUENCY = 4
TARGET_NETWORK_UPDATE_FREQUENCY = 40000
MODEL_WEIGHT_SAVE_FREQUENCY = 10000

EPSILON_MAX = 1.0


class DQNTrain():
    def __init__(self, game_name, input_shape, action_space, save_log=True, save_weights=True):
        self.action_space = action_space
        self.input_shape = input_shape
        self.epsilon = EPSILON_MAX
        self.memory = ReplayMemory(MEMORY_SIZE, BATCH_SIZE)

        self.ddqn_eval = CNN(self.input_shape, self.action_space).model
        self.ddqn_target = CNN(self.input_shape, self.action_space).model
        self.update_target_weights()

        self.save_log = save_log
        self.save_weights = save_weights
        self.save_path = "./output/train"
        self.model_path = self.save_path + "/models/ddqn/" + self.logger.timestamp() + "/model.h5"
        self.logger = Logger(game_name + "Train", self.save_path + "/logs/ddqn/")

    def get_action(self, state):
        if np.random.uniform() < self.epsilon or len(self.memory.replays) < REPLAY_START_NUMBER:
            return random.randrange(self.action_space)
        else:
            q_values = self.ddqn_eval.predict(np.expand_dims(
                np.asarray(state).astype(np.float64), axis=0), batch_size=1)
            return np.argmax(q_values[0])

    def update_epsilon(self):
        self.epsilon -= (EPSILON_MAX-EPSILON_MIN)/EPSILON_STEPS
        if self.epsilon < EPSILON_MIN:
            self.epsilon = EPSILON_MIN

    def save_model(self):
        if os.path.exists(os.path.dirname(self.model_path)):
            shutil.rmtree(os.path.dirname(self.model_path), ignore_errors=True)
        os.makedirs(os.path.dirname(self.model_path))
        self.ddqn_eval.save_weights(self.model_path)

    def update_target_weights(self):
        self.ddqn_target.set_weights(self.ddqn_eval.get_weights())

    def update(self, total_step):
        if len(self.memory.replays) < REPLAY_START_NUMBER:
            return

        if total_step % TRAINING_FREQUENCY == 0 and self.save_log:
            loss, accuracy = self.learn()
            self.log_model_status(loss, accuracy)

        self.update_epsilon()

        if total_step % MODEL_WEIGHT_SAVE_FREQUENCY == 0 and self.save_weights:
            self.save_model()

        if total_step % TARGET_NETWORK_UPDATE_FREQUENCY == 0:
            self.update_target_weights()

    def learn(self, mode=2015):
        batch = self.memory.gen_batch()

        states = []
        q_values = []

        for record in batch:
            state = np.expand_dims(np.asarray(
                record["state"]).astype(np.float64), axis=0)
            states.append(state)
            next_state = np.expand_dims(np.asarray(
                record["next_state"]).astype(np.float64), axis=0)

            q = list(self.ddqn_eval.predict(state)[0])
            if mode == 2015:
                q[record["action"]] = record["reward"] + (1 - record["terminal"]) * GAMMA * np.max(
                    self.ddqn_target.predict(next_state).ravel())
            elif mode == 2013:
                q[record["action"]] = record["reward"] + \
                    (1 - record["terminal"]) * GAMMA * \
                    np.max(self.ddqn.predict(next_state).ravel())
            elif mode == 2016:
                next_max_action = np.argmax(
                    self.ddqn.predict(next_state).ravel())
                q[record["action"]] = record["reward"] + \
                    (1 - record["terminal"]) * GAMMA * \
                    self.ddqn_target.predict(next_state).ravel()[
                    next_max_action]

            q_values.append(q)

        fit = self.ddqn_eval.fit(np.asarray(states).squeeze(),
                                 np.asarray(q_values).squeeze(),
                                 batch_size=BATCH_SIZE,
                                 verbose=0)

        loss = fit.history["loss"][0]
        accuracy = fit.history["accuracy"][0]
        return loss, accuracy

    def log_game_status(self, score, step, gameover):
        self.logger.add_score(score)
        self.logger.add_step(step)
        self.logger.add_gameover(gameover)

    def log_model_status(self, loss, accuracy):
        self.logger.add_loss(loss)
        self.logger.add_accuracy(accuracy)


class DQNTest():
    def __init__(self, game_name, input_shape, action_space, testing_model_path):
        self.action_space = action_space
        self.ddqn = CNN(input_shape, action_space).model
        self.logger = Logger(game_name + "Test", "./output/test/logs/ddqn/")
        assert os.path.exists(os.path.dirname(
            testing_model_path)), "No testing model in: " + str(testing_model_path)
        if os.path.isfile(testing_model_path):
            self.ddqn.load_weights(testing_model_path)

    def get_action(self, state):
        if np.random.rand() < EPSILON_TEST:
            return random.randrange(self.action_space)
        q_values = self.ddqn.predict(np.expand_dims(
            np.asarray(state).astype(np.float64), axis=0), batch_size=1)
        return np.argmax(q_values[0])

    def log_model_status(self, loss, accuracy):
        self.logger.add_loss(loss)
        self.logger.add_accuracy(accuracy)
