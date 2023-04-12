from reviews.models import Review

def get_avg_score(self):
    title_id = self.kwargs.get("title_id")
    score = self.kwargs.get("score_id")