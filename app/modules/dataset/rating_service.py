from app.modules.dataset.rating_repository import RatingRepository
from core.services.BaseService import BaseService
from app import db 
from app.modules.dataset.models import DatasetRating

class RatingService(BaseService):
    def __init__(self):
        super().__init__(RatingRepository())

    def get_all_by_user(self, user_id):
        return self.repository.get_all_by_user(user_id)
    
    def get_avg_rating(self, ds_meta_data_id):
        return self.repository.calculate_avg_rating(ds_meta_data_id)
    
    def get_ratings(self, ds_meta_data_id: int):
        return DatasetRating.query.filter_by(ds_meta_data_id=ds_meta_data_id).all()
    
    def create_rating(self, user_id:int, ds_meta_data_id:int, value:int, comment):
        if comment is None:
            comment = ""
        rating=self.repository.create(user_id=user_id, ds_meta_data_id=ds_meta_data_id, value=value, comment=comment)
        self.repository.session.commit()
        return rating
