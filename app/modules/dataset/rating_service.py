from app.modules.dataset.rating_repository import RatingRepository
from core.services.BaseService import BaseService

class RatingService(BaseService):
    def __init__(self):
        super().__init__(RatingRepository())

    def get_all_by_user(self, user_id):
        return self.repository.get_all_by_user(user_id)
