from app import db
from app.modules.dataset.models import DSMetaData, DataSet, Author
from core.repositories.BaseRepository import BaseRepository


class ExploreRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)

    def filter_datasets(self, query_string):
        """Aplica filtros a los datasets según los parámetros en la cadena de consulta"""
        # Consulta inicial con join a DSMetaData
        query = db.session.query(DataSet).join(DSMetaData)

        # Extraer filtros de la cadena de consulta
        query_filter = query_string.strip()

        # Filtrar por autor
        if query_filter.startswith('author:'):
            author_filter = query_filter[7:].strip()
            query = query.join(Author).filter(Author.name.ilike(f'%{author_filter}%'), DSMetaData.anonymized == "false")

        # Filtrar por tamaño mínimo de archivo
        elif query_filter.startswith('min_size:'):
            try:
                min_size = int(query_filter[9:].strip())  # Valor mínimo después de 'min_size:'
                query = query.filter(DSMetaData.total_file_size >= min_size)  # Asegúrate de tener esta columna en la BD
            except ValueError:
                pass  # Manejo de errores si no es un número válido

        # Filtrar por tamaño máximo de archivo
        elif query_filter.startswith('max_size:'):
            try:
                max_size = int(query_filter[9:].strip())  # Valor máximo después de 'max_size:'
                query = query.filter(DSMetaData.total_file_size <= max_size)  # Igual que arriba
            except ValueError:
                pass

        # Filtrar por rating mínimo
        elif query_filter.startswith('rating:'):
            try:
                min_rating = float(query_filter[7:].strip())
                query = query.filter(DSMetaData.rating_avg >= min_rating)
            except ValueError:
                pass

        # Filtrar por etiquetas
        elif query_filter.startswith('tags:'):
            tags_filter = query_filter[5:].strip()
            query = query.filter(DSMetaData.tags.ilike(f'%{tags_filter}%'))

        # Filtrar por anonimato
        elif query_filter.startswith('anonymized:'):
            anon_filter = query_filter[11:].strip().lower() == "true"
            query = query.filter(DSMetaData.anonymized == anon_filter)

        # Filtrar por título (filtro genérico)
        else:
            query = query.filter(DSMetaData.title.ilike(f'%{query_filter}%'))

        # Ordenar por fecha de creación descendente
        query = query.order_by(DataSet.created_at.desc())

        # Devolver los datasets filtrados
        return query.all()
