from app.modules.dataset.models import DSMetaData, DataSet
from flask import render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user

from app import db
from app.modules.profile import profile_bp
from app.modules.profile.forms import UserProfileForm
from app.modules.profile.services import UserProfileService
from app.modules.auth.models import User


@profile_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    profile = current_user.profile
    if not profile:
        return redirect(url_for("public.index"))

    form = UserProfileForm()
    if request.method == "POST":
        service = UserProfileService()
        try:
            service.update_profile(profile.id, **form.data)
        except Exception as exc:
            return render_template("profile/edit.html", form=form, error=f"Error updating profile: {exc}")

    return render_template("profile/edit.html", form=form)


@profile_bp.route('/profile/summary')
@login_required
def my_profile():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    user_datasets_pagination = db.session.query(DataSet) \
        .filter(DataSet.user_id == current_user.id) \
        .order_by(DataSet.created_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    total_datasets_count = db.session.query(DataSet) \
        .filter(DataSet.user_id == current_user.id) \
        .count()

    print(user_datasets_pagination.items)

    return render_template(
        'profile/summary.html',
        user_profile=current_user.profile,
        user=current_user,
        datasets=user_datasets_pagination.items,
        pagination=user_datasets_pagination,
        total_datasets=total_datasets_count,
        is_developer=current_user.profile.user.is_developer
    )


@profile_bp.route('/profile/<int:user_id>')
def user_profile(user_id):
    page = request.args.get('page', 1, type=int)
    per_page = 5

    user = db.session.query(User) \
        .filter(User.id == user_id).first()

    if user is None:
        abort(404)

    user_datasets_pagination = db.session.query(DataSet).join(DSMetaData) \
        .filter(DataSet.user_id == user_id,
                DSMetaData.anonymized.is_(False),
                DSMetaData.dataset_doi != ""
                ) \
        .order_by(DataSet.created_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    total_public_datasets_count = db.session.query(DataSet).join(DSMetaData) \
        .filter(
            DataSet.user_id == user_id,
            DSMetaData.anonymized.is_(False),
            DSMetaData.dataset_doi != ""
        ).count()

    return render_template(
        'profile/view_user_profile.html',
        user_profile=user.profile,
        user=user,
        datasets=user_datasets_pagination.items,
        pagination=user_datasets_pagination,
        total_datasets=total_public_datasets_count,
    )
