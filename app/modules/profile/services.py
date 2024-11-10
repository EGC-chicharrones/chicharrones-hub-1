from app.modules.auth.repositories import UserRepository
from app.modules.profile.repositories import UserProfileRepository
from core.services.BaseService import BaseService
from flask_login import current_user


class UserProfileService(BaseService):
    def __init__(self):
        super().__init__(UserProfileRepository())
        self.user_repo = UserRepository()

    def update_profile(self, user_profile_id, form, **kwargs):

        try:
            is_developer = form.is_developer.data
            github_username = form.github_username.data

            if is_developer and github_username == "":
                raise ValueError("Developer must have a github username.")

            user_data = {
                "is_developer": is_developer,
                "github_username": github_username
            }
            profile_data = {
                "name": form.name.data,
                "surname": form.surname.data,
                "affiliation": form.affiliation.data,
                "orcid": form.orcid.data
            }

            self.user_repo.update(current_user.profile.user.id, **user_data)
            updated_instance = self.update(user_profile_id, **profile_data)

            self.user_repo.session.commit()
            self.repository.session.commit()

        except Exception as exc:
            self.repository.session.rollback()
            self.user_repo.session.rollback()
            raise exc

        return updated_instance, None
