
import random
import pickle
import math
from time import sleep

class QAgent:
    def __init__(self, actions):
        self.q_table = self.load_table('q_table.pkl')
        self.actions = actions 
        self.alpha = 0.8 # learning rate
        self.gamma = 0.95 # discount fact
        self.temperature = 1.5 # softmax temp

    def get_state(self, hider, seeker):
        return (seeker.row, seeker.col)
    
    def choose_action(self, state, temperature=None):
        if state not in self.q_table:
            self.q_table[state] = [0.0 for _ in range(len(self.actions))]
        
        q_values = self.q_table[state]
        T = self.temperature if temperature is None else temperature
        mx = max(q_values)

        # convert to positive "probabilities" using softmax
        exp_q = [math.exp((qi - mx) / max(T, 1e-6)) for qi in q_values]
        total = sum(exp_q)
        probs = [v / total for v in exp_q]
        
        action_index = random.choices(range(len(self.actions)), weights=probs)[0]
        return action_index


    def update(self, state, action, reward, next_state, done):
        if state not in self.q_table:
            self.q_table[state] = [0.0 for _ in range(len(self.actions))]
        if next_state not in self.q_table:
            self.q_table[next_state] = [0.0 for _ in range(len(self.actions))]

        best_next = max(self.q_table[next_state])
        old_value = self.q_table[state][action]
        target = reward if done else (reward + self.gamma * best_next)
        self.q_table[state][action] = old_value + self.alpha * (target - old_value)

    def decay_temperature(self, min_T=0.2, rate=0.95):
        self.temperature = max(min_T, self.temperature * rate)


    def save_table(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
        
    def load_table(self, filename):
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}
