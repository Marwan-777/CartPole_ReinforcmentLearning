import gym
import numpy as np
import math


class CartPoleQAgent():
    def __init__(self, buckets=(1, 1, 6, 12), num_episodes=1000, min_lr=0.1, min_explore=0.1, discount=1.0, decay=25):
        self.buckets = buckets
        self.num_episodes = num_episodes
        self.min_lr = min_lr
        self.min_explore = min_explore
        self.discount = discount
        self.decay = decay
        self.env = gym.make('CartPole-v1')
        self.upper_bounds = [self.env.observation_space.high[0], 0.5, self.env.observation_space.high[2], math.radians(50) / 1.]
        self.lower_bounds = [self.env.observation_space.low[0], -0.5, self.env.observation_space.low[2], -math.radians(50) / 1.]
        self.Q_table = np.zeros(self.buckets + (self.env.action_space.n,))

    def get_explore_rate(self, t):
        return max(self.min_explore, min(1., 1. - math.log10((t + 1) / self.decay)))

    def get_lr(self, t):
        return max(self.min_lr, min(1., 1. - math.log10((t + 1) / self.decay)))

    def update_q(self, state, action, reward, new_state,n):
        self.Q_table[new_state][action] = self.Q_table[state][action] + 1/n * (reward - self.Q_table[state][action])

    def SARSA_update_q(self, state, action, reward, new_state, n, new_action):
        self.Q_table[state][action] = self.Q_table[state][action] + self.lr * (reward + self.discount * self.Q_table[new_state][new_action] - self.Q_table[state][action])

        # Write your code here

    def choose_action(self, state):
        if np.random.uniform() < self.explore_rate:
            return self.env.action_space.sample()
        else:
            return np.argmax(self.Q_table[state])
        # Write your code here

    def discretize_state(self, obs):
        discretized = list()
        for i in range(len(obs)):
            scaling = (obs[i] + abs(self.lower_bounds[i])) / (self.upper_bounds[i] - self.lower_bounds[i])
            new_obs = int(round((self.buckets[i] - 1) * scaling))
            new_obs = min(self.buckets[i] - 1, max(0, new_obs))
            discretized.append(new_obs)
        return tuple(discretized)

    def train(self):
        action = 0
        new_state = 0
        new_action = 0
        for e in range(self.num_episodes):
            current_state = self.discretize_state(self.env.reset())
            self.lr = self.get_lr(e)
            self.explore_rate = self.get_explore_rate(e)
            done = False
            r=0
            n=0
            action = self.choose_action(current_state)
            while not done:
                obs, reward, done, _ = self.env.step(action)

                new_state = self.discretize_state(obs)
                n+=1
                new_action = self.choose_action(new_state)

                self.SARSA_update_q(current_state, action, reward, new_state, self.lr,new_action)

                action = new_action
                current_state=new_state

        print('Finished training!')

    def run(self):
        for e in range(self.num_episodes):
            current_state = self.discretize_state(self.env.reset())
            done = False
            while not done:
                action = self.choose_action(current_state)
                obs, reward, done, _ = self.env.step(action)
                self.env.render()
                current_state = self.discretize_state(obs)
        print('Finished running!')
        # Write your code here


agent = CartPoleQAgent()
agent.train()
agent.run()
