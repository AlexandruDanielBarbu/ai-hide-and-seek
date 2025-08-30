
import random
import pickle

class QAgent:
    def __init__(self, actions):
        self.q_table = self.load_table('q_table.pkl')
        self.actions = actions 
        self.alpha = 0.8 # learning rate
        self.gamma = 0.95 # discount fact
        self.epsilon = 0.85 # exploration rate

    def get_state(self, hider, seeker):
        return (hider.row, hider.col, seeker.row, seeker.col)

    def choose_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = [0.0 for _ in range(len(self.actions))]
    
        if random.random() < self.epsilon or state not in self.q_table:
            return random.choice(self.actions)
        # index of max Q-value
        return self.q_table[state].index(max(self.q_table[state]))
    
    def update(self, state, action, reward, next_state):
        if state not in self.q_table:
                self.q_table[state] = [0.0 for _ in range(len(self.actions))]
        if next_state not in self.q_table:
            self.q_table[next_state] = [0.0 for _ in range(len(self.actions))]

        best_next = max(self.q_table[next_state])
        self.q_table[state][action] += self.alpha * (reward + self.gamma * best_next - self.q_table[state][action])

    def save_table(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
        
    def load_table(self, filename):
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}
