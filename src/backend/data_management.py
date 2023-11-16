class DataManagement:
    def save_high_score(self, score):
        with open('high_scores.txt', 'w') as file:
            file.write(f"{score}\n")
        pass

    def load_high_score(self):
        scores = []
        with open('high_scores.txt', 'r') as file:
            lines = file.readlines()
            scores = [int(score.strip()) for score in lines]
        return scores
