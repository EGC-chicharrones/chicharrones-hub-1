from app import db
from app.modules.dataset.models import DSMetaData, DataSet, Author
from core.repositories.BaseRepository import BaseRepository


class ExploreRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)

    def filter_datasets(self, query_string):
        """Aplica filtros a los datasets según los parámetros en la cadena de consulta"""
        # Consulta inicial con join a DSMetaData
        query = db.session.query(DataSet).join(DSMetaData).filter(DSMetaData.dataset_doi.isnot(None))

        # Extraer filtros de la cadena de consulta
        query_filter = query_string.strip()

        # Filtrar por nombre del autor
        if query_filter.startswith('author:'):
            author_filter = query_filter[7:].strip()
            query = query.join(Author).filter(Author.name.ilike(f'%{author_filter}%'), DSMetaData.anonymized == "false")

        # Filtrar por afiliación del autor
        elif query_filter.startswith('affiliation:'):
            affiliation_filter = query_filter[12:].strip()
            query = query.join(Author).filter(Author.affiliation.ilike(f'%{affiliation_filter}%'),
                                              DSMetaData.anonymized == "false")

        # Filtrar por ORCID del autor
        elif query_filter.startswith('orcid:'):
            orcid_filter = query_filter[6:].strip()
            query = query.join(Author).filter(Author.orcid.ilike(f'%{orcid_filter}%'), DSMetaData.anonymized == "false")

        # Filtrar por DOI de publicación
        elif query_filter.startswith('doi:'):
            doi_filter = query_filter[4:].strip()
            query = query.filter(DSMetaData.publication_doi.ilike(f'%{doi_filter}%'))

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

        # Filtrar por descripción
        elif query_filter.startswith('description:'):
            desc_filter = query_filter[12:].strip()
            query = query.filter(DSMetaData.description.ilike(f'%{desc_filter}%'))

        # Filtrar por fecha de creación (igual o posterior) formato yyyy/mm/dd AVERIGUAR HORA
        elif query_filter.startswith('date:'):
            date_filter = query_filter[5:].strip()
            query = query.filter(DataSet.created_at >= date_filter)

        # Filtrar por uvl_filename
        # elif query_filter.startswith('file:'):
        #     uvl_filename_filter = query_filter[5:].strip()
        #     query = query.filter(DataSet.files.fm_meta_data.uvl_filename.ilike(f'%{uvl_filename_filter}%'))

        # Filtrar por título (filtro genérico)
        else:
            query = query.filter(DSMetaData.title.ilike(f'%{query_filter}%'))

        # Ordenar por fecha de creación descendente
        query = query.order_by(DataSet.created_at.desc())

        # Devolver los datasets filtrados
        return query.all()
