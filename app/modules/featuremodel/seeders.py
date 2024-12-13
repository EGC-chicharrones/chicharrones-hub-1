from core.seeders.BaseSeeder import BaseSeeder
from app.modules.featuremodel.models import FeatureModel
from app.modules.dataset.models import DataSet
from app import db


class FeaturemodelSeeder(BaseSeeder):
    priority = 11

    def run(self):

        datasets = db.session.query(DataSet).all()

        data = []
        for dataset in datasets:
            if dataset.id == 1:
                data.append(FeatureModel(id=1, data_set_id=1))
                data.append(FeatureModel(id=2, data_set_id=1))

            elif dataset.id == 2:
                data.append(FeatureModel(id=3, data_set_id=2))
                data.append(FeatureModel(id=4, data_set_id=2))
                data.append(FeatureModel(id=5, data_set_id=2))
                data.append(FeatureModel(id=6, data_set_id=2))
            elif dataset.id == 3:
                data.append(FeatureModel(id=7, data_set_id=3))
                data.append(FeatureModel(id=8, data_set_id=3))
            else:
                data.append(FeatureModel(id=9, data_set_id=4))
                data.append(FeatureModel(id=10, data_set_id=4))
                data.append(FeatureModel(id=11, data_set_id=4))
                data.append(FeatureModel(id=12, data_set_id=4))
        self.seed(data)
        db.session.commit()
