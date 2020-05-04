import gym
import argparse
import numpy as np
# import atari_py

from wrapped_env import Environment
from dqn_model import DQNTrain, DQNTest
from args import MAX_TRAIN_STEP


if __name__ == "__main__":
    # preprocessing & generate env
    game_name = "Breakout"
    env_name = game_name + "Deterministic-v4"
    breakout_env = Environment(env_name)
    breakout_env.gen_wrapped_env()
    env = breakout_env.env
    action_space = env.action_space.n
    img_size = 84
    input_shape = (action_space, img_size, img_size)
    testing_model_path = ""

    # generate model
    is_train = True
    model = DQNTrain(game_name, input_shape, action_space) if is_train else DQNTest(
                        game_name, input_shape, action_space, testing_model_path)

    # iteration of updating the Q table
    gameover = 0
    total_step = 0
    while True:
        step = 0
        score = 0
        state = env.reset()
        while True:
            if total_step >= MAX_TRAIN_STEP:
                print(f"Traning of {MAX_TRAIN_STEP} steps completed!")
                exit(0)
            action = model.get_action(state)
            next_state, reward, terminal, info = env.step(action) 
            reward = np.sign(reward)
            if is_train:
                model.memory.add_replay(
                    state, action, reward, next_state, terminal)

            score += reward
            state = next_state
            total_step += 1
            if is_train:
                model.update(total_step)
            step += 1

            if terminal:
                model.log_game_status(score, step, gameover)
                gameover += 1
                break
