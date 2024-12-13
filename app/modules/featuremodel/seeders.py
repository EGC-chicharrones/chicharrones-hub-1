import os
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
                data.append(FeatureModel(id=1, data_set_id=1, features=self.counting_uvl_file("file1.uvl")[0],
                                         constraints=self.counting_uvl_file("file1.uvl")[1]))
                data.append(FeatureModel(id=2, data_set_id=1, features=self.counting_uvl_file("file2.uvl")[0],
                                         constraints=self.counting_uvl_file("file2.uvl")[1]))

            elif dataset.id == 2:
                data.append(FeatureModel(id=3, data_set_id=2, features=self.counting_uvl_file("file3.uvl")[0],
                                         constraints=self.counting_uvl_file("file3.uvl")[1]))
                data.append(FeatureModel(id=4, data_set_id=2, features=self.counting_uvl_file("file4.uvl")[0],
                                         constraints=self.counting_uvl_file("file4.uvl")[1]))
                data.append(FeatureModel(id=5, data_set_id=2, features=self.counting_uvl_file("file5.uvl")[0],
                                         constraints=self.counting_uvl_file("file5.uvl")[1]))
                data.append(FeatureModel(id=6, data_set_id=2, features=self.counting_uvl_file("file6.uvl")[0],
                                         constraints=self.counting_uvl_file("file6.uvl")[1]))

            elif dataset.id == 3:
                data.append(FeatureModel(id=7, data_set_id=3, features=self.counting_uvl_file("file7.uvl")[0],
                                         constraints=self.counting_uvl_file("file7.uvl")[1]))
                data.append(FeatureModel(id=8, data_set_id=3, features=self.counting_uvl_file("file8.uvl")[0],
                                         constraints=self.counting_uvl_file("file8.uvl")[1]))
            else:
                data.append(FeatureModel(id=9, data_set_id=4, features=self.counting_uvl_file("file9.uvl")[0],
                                         constraints=self.counting_uvl_file("file9.uvl")[1]))
                data.append(FeatureModel(id=10, data_set_id=4, features=self.counting_uvl_file("file10.uvl")[0],
                                         constraints=self.counting_uvl_file("file10.uvl")[1]))
                data.append(FeatureModel(id=11, data_set_id=4, features=self.counting_uvl_file("file11.uvl")[0],
                                         constraints=self.counting_uvl_file("file11.uvl")[1]))
                data.append(FeatureModel(id=12, data_set_id=4, features=self.counting_uvl_file("file12.uvl")[0],
                                         constraints=self.counting_uvl_file("file12.uvl")[1]))
        self.seed(data)
        db.session.commit()

    def counting_uvl_file(self, file_name):

        feature_count = 0  # Contador de las características
        constraint_count = 0  # Contador de restricciones
        base_path = 'app/modules/dataset/uvl_examples'

        # Recorremos los directorios y subdirectorios en busca del archivo específico
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file == file_name:  # Compara el nombre del archivo
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            lines = f.readlines()

                            counting_features = False  # Flag para saber si estamos contando características
                            counting_constraints = False  # Flag para saber si estamos contando restricciones

                            for line in lines:
                                stripped_line = line.strip()  # Elimina los espacios en blanco al principio y al final

                                if not stripped_line:  # Si la línea está vacía, la ignoramos
                                    continue

                                indent_level = len(line) - len(stripped_line)  # Número de caraceres blancos al inicio
                                indent_level = indent_level // 4  # Suponemos 4 espacios por tabulación

                                # Si encontramos "features", empezamos a contar
                                if not counting_features and "features" in stripped_line.lower():
                                    counting_features = True
                                    continue

                                # Si encontramos "constraints", empezamos a contar
                                if not counting_constraints and "constraints" in stripped_line.lower():
                                    counting_constraints = True
                                    continue

                                if counting_features:
                                    if counting_constraints is False and indent_level == 1:
                                        feature_count += 1

                                if counting_constraints:
                                    if indent_level == 1:
                                        constraint_count += 1

                    except Exception as e:
                        print(f"Error leyendo el archivo {file_path}: {e}")
                    return feature_count, constraint_count

        # Si el archivo no fue encontrado, devuelve 0
        return 0, 0
