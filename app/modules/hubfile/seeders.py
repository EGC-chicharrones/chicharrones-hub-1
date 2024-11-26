from core.seeders.BaseSeeder import BaseSeeder
from app import db
from app.modules.hubfile.models import Hubfile


class HubfileSeeder(BaseSeeder):
    
    priority = 12
    def run(self):

        data = [
            Hubfile(id=1, name="model1.uvl", checksum="123", size=12, feature_model_id=1),
            Hubfile(id=2, name="model2.uvl", checksum="123", size=12, feature_model_id=2),
            Hubfile(id=3, name="model3.uvl", checksum="123", size=12, feature_model_id=3),
            Hubfile(id=4, name="model4.uvl", checksum="123", size=12, feature_model_id=4)

        ]
        
        self.seed(data)
        db.session.commit()
