import os
import random
from datetime import datetime, timezone
from app.modules.auth.models import User
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from app.modules.hubfile.models import Hubfile
from core.seeders.BaseSeeder import BaseSeeder
from app.modules.dataset.models import (
    DataSet,
    DSMetaData,
    PublicationType,
    DSMetrics,
    DatasetRating,
    Author
)
from app import db

class DataSetSeeder(BaseSeeder):
    priority = 2  # Prioridad más baja

    def run(self):
        # Buscar usuarios, y si no existen, crearlos temporalmente para el seeder
        user1 = User.query.filter_by(email='user1@example.com').first()
        user2 = User.query.filter_by(email='user2@example.com').first()

        if not user1:
            user1 = User(email='user1@example.com', password="hashed_password1")
            db.session.add(user1)
            db.session.flush()  # Inserta sin confirmar la transacción

        if not user2:
            user2 = User(email='user2@example.com', password="hashed_password2")
            db.session.add(user2)
            db.session.flush()  # Inserta sin confirmar la transacción

        # Crear DSMetrics
        ds_metrics = DSMetrics(number_of_models='5', number_of_features='50')
        seeded_ds_metrics = self.seed([ds_metrics])[0]

        # Crear DSMetaData
        ds_meta_data_list = [
            DSMetaData(
                deposition_id=1 + i,
                title=f'Sample dataset {i+1}',
                description=f'Description for dataset {i+1}',
                publication_type=PublicationType.DATA_MANAGEMENT_PLAN,
                publication_doi=f'10.1234/dataset{i+1}',
                dataset_doi=f'10.1234/dataset{i+1}',
                tags='tag1, tag2',
                ds_metrics_id=seeded_ds_metrics.id
            ) for i in range(4)
        ]
        seeded_ds_meta_data = self.seed(ds_meta_data_list)

        authors = [
            Author(
                name=f'Author {i+1}',
                affiliation=f'Affiliation {i+1}',
                orcid=f'0000-0000-0000-000{i}',
                ds_meta_data_id=seeded_ds_meta_data[i % 4].id
            ) for i in range(4)
        ]
        self.seed(authors)

        datasets = [
            DataSet(
                id=i+1,
                user_id=user1.id if i % 2 == 0 else user2.id,
                ds_meta_data_id=seeded_ds_meta_data[i].id,
                created_at=datetime.now(timezone.utc)
            ) for i in range(4)
        ]
        seeded_datasets = self.seed(datasets)

        ratings = []
        for dataset in ds_meta_data_list:
            num_ratings = random.randint(1, 3)
            for _ in range(num_ratings):
                rating = DatasetRating(
                    value=random.randint(1, 5),
                    comment=f"Comentario para el dataset {dataset.id}",
                    user_id=random.choice([user1.id, user2.id]),
                    ds_meta_data_id=dataset.id,
                )
                ratings.append(rating)

        self.seed(ratings)
        db.session.commit() 

        initialize_rating_avg()
        print("Dataset ratings successfully seeded.")

def initialize_rating_avg():
    ds_meta_datas = DSMetaData.query.all()

    for ds_meta_data in ds_meta_datas:
        if ds_meta_data.ratings:
            ds_meta_data.rating_avg = sum(rating.value for rating in ds_meta_data.ratings) / len(ds_meta_data.ratings)
        else:
            ds_meta_data.rating_avg = 0.0
        db.session.add(ds_meta_data)

    db.session.commit()
