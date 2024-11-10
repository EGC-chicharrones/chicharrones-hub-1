import os
import shutil
from app.modules.auth.models import User
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from app.modules.hubfile.models import Hubfile
from core.seeders.BaseSeeder import BaseSeeder
from app.modules.dataset.models import (
    DataSet,
    DSMetaData,
    PublicationType,
    DSMetrics,
    Author)
from datetime import datetime, timezone
from dotenv import load_dotenv

import random

class DataSetSeeder(BaseSeeder):

    priority = 2  # Lower priority

    def run(self):
        # Retrieve users
        user1 = User.query.filter_by(email='user1@example.com').first()
        user2 = User.query.filter_by(email='user2@example.com').first()

        if not user1 or not user2:
            raise Exception("Users not found. Please seed users first.")

        # Create DSMetrics instance
        ds_metrics = DSMetrics(number_of_models='5', number_of_features='50')
        seeded_ds_metrics = self.seed([ds_metrics])[0]

        # Create DSMetaData instances
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

        # Create Author instances and associate with DSMetaData
        authors = [
            Author(
                name=f'Author {i+1}',
                affiliation=f'Affiliation {i+1}',
                orcid=f'0000-0000-0000-000{i}',
                ds_meta_data_id=seeded_ds_meta_data[i % 4].id
            ) for i in range(4)
        ]
        self.seed(authors)

        # Create DataSet instances
        datasets = [
            DataSet(
                user_id=user1.id if i % 2 == 0 else user2.id,
                ds_meta_data_id=seeded_ds_meta_data[i].id,
                created_at=datetime.now(timezone.utc)
            ) for i in range(4)
        ]
        seeded_datasets = self.seed(datasets)

        # Create DatasetRating instances for each DataSet
        ratings = []
        for dataset in seeded_datasets:
            # Genera entre 1 y 3 valoraciones por dataset
            num_ratings = random.randint(1, 3)
            for _ in range(num_ratings):
                rating = DatasetRating(
                    value=random.randint(1, 5),  # Valoración aleatoria entre 1 y 5
                    comment=f"Comentario para el dataset {dataset.id}",
                    user_id=random.choice([user1.id, user2.id]),  # Usuario aleatorio entre los dos
                    dataset_id=dataset.id,
                    created_at=datetime.now(timezone.utc)
                )
                ratings.append(rating)

        # Seed ratings to the database
        self.seed(ratings)

        # (Continuación de creación de FeatureModels y Hubfiles aquí...)

        print("Dataset ratings successfully seeded.")
