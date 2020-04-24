import gym
from openai_wrapper import NoopResetEnv, FireResetEnv, ProcessFrame84, ChannelsFirstImageShape, FrameStack


class Environment():
    def __init__(self, env_name, is_video=False):
        self.env = gym.make(env_name)
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space
        if is_video:
            self.env = gym.wrappers.Monitor(
                self.env, "./output/video/", force=True)

    def gen_wrapped_env(self):
        self.env = NoopResetEnv(self.env, noop_max=30)
        if 'FIRE' in self.env.unwrapped.get_action_meanings():
            self.env = FireResetEnv(self.env)
        self.env = ProcessFrame84(self.env)
        self.env = ChannelsFirstImageShape(self.env)
        self.env = FrameStack(self.env, 4)
