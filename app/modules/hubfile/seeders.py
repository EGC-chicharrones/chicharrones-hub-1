from core.seeders.BaseSeeder import BaseSeeder
from app import db
from app.modules.hubfile.models import Hubfile


class HubfileSeeder(BaseSeeder):

    priority = 12

    def run(self):

        data = [
            Hubfile(id=1, name="file1.uvl", checksum="123", size=12, feature_model_id=1),
            Hubfile(id=2, name="file2.uvl", checksum="123", size=12, feature_model_id=2),
            Hubfile(id=3, name="file3.uvl", checksum="123", size=12, feature_model_id=3),
            Hubfile(id=4, name="file4.uvl", checksum="123", size=12, feature_model_id=4),
            Hubfile(id=5, name="file5.uvl", checksum="123", size=12, feature_model_id=5),
            Hubfile(id=6, name="file6.uvl", checksum="123", size=12, feature_model_id=6),
            Hubfile(id=7, name="file7.uvl", checksum="123", size=12, feature_model_id=7),
            Hubfile(id=8, name="file8.uvl", checksum="123", size=12, feature_model_id=8),
            Hubfile(id=9, name="file9.uvl", checksum="123", size=12, feature_model_id=9),
            Hubfile(id=10, name="file10.uvl", checksum="123", size=12, feature_model_id=10),
            Hubfile(id=11, name="file11.uvl", checksum="123", size=12, feature_model_id=11),
            Hubfile(id=12, name="file12.uvl", checksum="123", size=12, feature_model_id=12),
        ]

        self.seed(data)
        db.session.commit()
