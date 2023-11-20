class DataManagement:
    def save_high_score(self, name, score):
        with open('high_scores.txt', 'a') as file:
            file.write(f"{name}:{score}\n")


    def load_high_score(self):
        scores = []
        with open('high_scores.txt', 'r') as file:
            lines = file.readlines()
            scores = [line.strip().split(':') for line in lines]
            sorted_scores = sorted(scores, key=lambda x: int(x[1]), reverse=True)
            return sorted_scores

