from app.modules.fakenodo.models import Deposition
from core.repositories.BaseRepository import BaseRepository


class DepositionRepo(BaseRepository):
    # def init(self):
    #     super().init(Deposition)
    
    def __init__(self):
        # Debes pasar el modelo adecuado como argumento al constructor de BaseRepository
        super().__init__(model=Deposition)

    def create_new_deposition(self, dep_metadata):
        return self.create(dep_metadata=dep_metadata)