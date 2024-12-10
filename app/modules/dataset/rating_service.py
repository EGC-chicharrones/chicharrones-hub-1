from app.modules.dataset.rating_repository import RatingRepository
from core.services.BaseService import BaseService
from app.modules.dataset.models import DatasetRating, DSMetaData


class RatingService(BaseService):
    def __init__(self):
        super().__init__(RatingRepository())

    def get_all_by_user(self, user_id):
        return self.repository.get_all_by_user(user_id)

    def get_ratings(self, ds_meta_data_id: int):
        return DatasetRating.query.filter_by(ds_meta_data_id=ds_meta_data_id).all()

    def create_rating(self, user_id: int, ds_meta_data_id: int, value: int, comment):
        if comment is None:
            comment = ""
        rating = self.repository.create(user_id=user_id, ds_meta_data_id=ds_meta_data_id, value=value, comment=comment)
        ds_meta_data = self.repository.session.query(DSMetaData).get(ds_meta_data_id)
        ratings = ds_meta_data.ratings
        ds_meta_data.rating_avg = sum(rating.value for rating in ratings) / len(ratings) if ratings else 0.0
        self.repository.session.commit()
        return rating
