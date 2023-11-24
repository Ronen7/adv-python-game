import os


class DataManagement:
    def __init__(self):
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.high_scores_file = os.path.join(self.directory, 'high_scores.txt')

    def save_high_score(self, score, name):
        with open(self.high_scores_file, 'a') as file:
            file.write(f"{name}:{score}\n")

    def load_high_score(self):
        scores = []
        if os.path.exists(self.high_scores_file):
            with open(self.high_scores_file, 'r') as file:
                lines = file.readlines()
                scores = [line.strip().split(':') for line in lines]
                sorted_scores = sorted(scores, key=lambda x: int(x[1]), reverse=True)
                return sorted_scores
        return scores
