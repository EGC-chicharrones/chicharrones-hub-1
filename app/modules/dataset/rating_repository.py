from app.modules.dataset.models import DatasetRating
from core.repositories.BaseRepository import BaseRepository
from typing import Optional
from sqlalchemy import  func


class RatingRepository(BaseRepository):
    def __init__(self):
        super().__init__(DatasetRating)

    def get_all_by_user(self, user_id):
        return DatasetRating.query.filter_by(user_id=user_id).all()

def get_ratings_by_dataset_id(self, ds_meta_data_id: int) -> list[DatasetRating]:
    return DatasetRating.query.filter_by(ds_meta_data_id=ds_meta_data_id).all()


def calculate_avg_rating(self, ds_meta_data_id: int) -> float:
        avg_rating = self.model.query.with_entities(func.avg(self.model.value)).filter_by(ds_meta_data_id=ds_meta_data_id).scalar()
        return avg_rating if avg_rating is not None else 0.0
