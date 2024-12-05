from core.seeders.BaseSeeder import BaseSeeder
from app.modules.featuremodel.models import FeatureModel
from app.modules.dataset.models import DataSet
from app import db


class FeaturemodelSeeder(BaseSeeder):
    priority = 11
    
    def run(self):
        
        datasets = db.session.query(DataSet).all()
        data = []
        id_fm = 1
        for dataset in datasets:
            data.append(FeatureModel(id=id_fm, data_set_id=dataset.id))
            id_fm += 1
     
        self.seed(data)
        db.session.commit()
