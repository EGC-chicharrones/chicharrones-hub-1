
from app.modules.explore.repositories import ExploreRepository


class ExploreService:
    def __init__(self):
        self.repository = ExploreRepository()

    def filter(self, query_string: str, publication_type: str, sorting: str, models: str, features: str,
               constraints: str):
        """Filtra los datasets a partir de una cadena de consulta."""
        # Llamar al método filter_datasets del repositorio, pasando la cadena de consulta
        return self.repository.filter_datasets(query_string, publication_type, sorting, models, features, constraints)
