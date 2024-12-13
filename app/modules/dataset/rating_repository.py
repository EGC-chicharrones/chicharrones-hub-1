from app.modules.dataset.models import DatasetRating
from core.repositories.BaseRepository import BaseRepository


class RatingRepository(BaseRepository):
    def __init__(self):
        super().__init__(DatasetRating)

    def get_all_by_user(self, user_id):
        return DatasetRating.query.filter_by(user_id=user_id).all()
