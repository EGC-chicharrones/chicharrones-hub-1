from app.modules.dataset.rating_repository import RatingRepository
from core.services.BaseService import BaseService
from app import db 
from app.modules.dataset.models import DatasetRating

class RatingService(BaseService):
    def __init__(self):
        super().__init__(RatingRepository())

    def get_all_by_user(self, user_id):
        return self.repository.get_all_by_user(user_id)
    
    def get_ratings(dataset_id):
        return db.session.query(DatasetRating).filter_by(dataset_id=dataset_id).all()
