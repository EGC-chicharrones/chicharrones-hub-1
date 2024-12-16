import re
from sqlalchemy import and_, any_, or_
import unidecode
from app import db
from app.modules.dataset.models import DSMetaData, DataSet, Author, PublicationType
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from app.modules.hubfile.models import Hubfile
from core.repositories.BaseRepository import BaseRepository
from sqlalchemy import func


class ExploreRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)

    def filter_datasets(self, query_string, publication_type_string, sorting, models, features, constraints):
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
            elif key == 'date':  # Formato yyyy/mm/dd
                try:
                    query = query.filter(DataSet.created_at >= value)
                except ValueError:
                    continue

        if not filters:
            query = query.filter(DSMetaData.title.ilike(f'%{query_string.strip()}%'))

        # Publication type filter
        publication_filter = publication_type_string.split(':', 1)[0].strip()
        if publication_filter != "any":
            matching_type = None
            for member in PublicationType:
                if member.value.lower() == publication_filter:
                    matching_type = member
                    break

            if matching_type is not None:
                query = query.filter(DSMetaData.publication_type == matching_type.name)

        # Number of models, features and constraints filter
        models_filter = models.split(':', 1)[0].strip()
        features_filter = features.split(':', 1)[0].strip()
        constraints_filter = constraints.split(':', 1)[0].strip()

        if models_filter != "" or features_filter != "" or constraints_filter != "":
            query = query = query.join(FeatureModel).join(Hubfile).group_by(DataSet.id)

            # Construir condiciones dinámicamente
            having_conditions = []

            if models_filter != "":
                having_conditions.append(func.count(Hubfile.id) == int(models_filter))
            if features_filter != "":
                having_conditions.append(func.sum(FeatureModel.features) == int(features_filter))
            if constraints_filter != "":
                having_conditions.append(func.sum(FeatureModel.constraints) == int(constraints_filter))

            # Aplicar condiciones con `and_` si hay alguna
            if having_conditions:
                query = query.having(and_(*having_conditions))

        # Order by created_at
        if sorting == "oldest":
            query = query.order_by(self.model.created_at.asc())
        else:
            query = query.order_by(self.model.created_at.desc())

        return query.all()

    """
    Old filtering method. This is not used in UVLHUB.IO and is only kept for the basic functionality of the Discord bot.
    """
    def filter_old(self, query="", sorting="newest", publication_type="any", tags=[], **kwargs):
        # Normalize and remove unwanted characters
        normalized_query = unidecode.unidecode(query).lower()
        cleaned_query = re.sub(r'[,.":\'()\[\]^;!¡¿?]', "", normalized_query)

        filters = []
        for word in cleaned_query.split():
            filters.append(DSMetaData.title.ilike(f"%{word}%"))
            filters.append(DSMetaData.description.ilike(f"%{word}%"))
            filters.append(Author.name.ilike(f"%{word}%"))
            filters.append(Author.affiliation.ilike(f"%{word}%"))
            filters.append(Author.orcid.ilike(f"%{word}%"))
            filters.append(FMMetaData.uvl_filename.ilike(f"%{word}%"))
            filters.append(FMMetaData.title.ilike(f"%{word}%"))
            filters.append(FMMetaData.description.ilike(f"%{word}%"))
            filters.append(FMMetaData.publication_doi.ilike(f"%{word}%"))
            filters.append(FMMetaData.tags.ilike(f"%{word}%"))
            filters.append(DSMetaData.tags.ilike(f"%{word}%"))

        datasets = (
            self.model.query
            .join(DataSet.ds_meta_data)
            .join(DSMetaData.authors)
            .join(DataSet.feature_models)
            .join(FeatureModel.fm_meta_data)
            .filter(or_(*filters))
            .filter(DSMetaData.dataset_doi.isnot(None))  # Exclude datasets with empty dataset_doi
        )

        if publication_type != "any":
            matching_type = None
            for member in PublicationType:
                if member.value.lower() == publication_type:
                    matching_type = member
                    break

            if matching_type is not None:
                datasets = datasets.filter(DSMetaData.publication_type == matching_type.name)

        if tags:
            datasets = datasets.filter(DSMetaData.tags.ilike(any_(f"%{tag}%" for tag in tags)))

        # Order by created_at
        if sorting == "oldest":
            datasets = datasets.order_by(self.model.created_at.asc())
        else:
            datasets = datasets.order_by(self.model.created_at.desc())

        return datasets.all()
