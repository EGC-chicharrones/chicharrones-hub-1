from app import db
from app.modules.dataset.models import DSMetaData, DataSet, Author
from core.repositories.BaseRepository import BaseRepository


class ExploreRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)

    def filter_datasets(self, query_string):
        query = db.session.query(DataSet).join(DSMetaData).filter(DSMetaData.dataset_doi.isnot(None))

        filters = query_string.split(';')
        filters = [f.split(':', 1) for f in filters if ':' in f]

        for key, value in filters:
            key = key.strip().lower()
            value = value.strip()

            if key == 'author':
                query = query.join(Author).filter(Author.name.ilike(f'%{value}%'), DSMetaData.anonymized == "false")
            elif key == 'affiliation':
                query = query.join(Author).filter(Author.affiliation.ilike(f'%{value}%'),
                                                  DSMetaData.anonymized == "false")
            elif key == 'orcid':
                query = query.join(Author).filter(Author.orcid.ilike(f'%{value}%'), DSMetaData.anonymized == "false")
            elif key == 'doi':
                query = query.filter(DSMetaData.publication_doi.ilike(f'%{value}%'))
            elif key == 'min_size':
                try:
                    min_size = int(value)
                    query = query.filter(DSMetaData.total_file_size >= min_size)
                except ValueError:
                    continue
            elif key == 'max_size':
                try:
                    max_size = int(value)
                    query = query.filter(DSMetaData.total_file_size <= max_size)
                except ValueError:
                    continue
            elif key == 'rating':
                try:
                    min_rating = float(value)
                    query = query.filter(DSMetaData.rating_avg >= min_rating)
                except ValueError:
                    continue
            elif key == 'tags':
                query = query.filter(DSMetaData.tags.ilike(f'%{value}%'))
            elif key == 'anonymized':
                anon_filter = value.lower() == "true"
                query = query.filter(DSMetaData.anonymized == anon_filter)
            elif key == 'description':
                query = query.filter(DSMetaData.description.ilike(f'%{value}%'))
            elif key == 'date':
                try:
                    query = query.filter(DataSet.created_at >= value)
                except ValueError:
                    continue

        if not filters:
            query = query.filter(DSMetaData.title.ilike(f'%{query_string.strip()}%'))

        query = query.order_by(DataSet.created_at.desc())

        return query.all()
