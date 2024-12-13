import logging
import os
import shutil
import tempfile
import uuid
import requests
from datetime import datetime, timezone
from zipfile import ZipFile


from app.modules.dataset.rating_service import RatingService

from flask import (
    flash,
    redirect,
    render_template,
    request,
    jsonify,
    send_from_directory,
    make_response,
    abort,
    url_for,
)
from flask_login import login_required, current_user
from app.modules.dataset.forms import DataSetForm, RatingForm
from app.modules.dataset.models import DSDownloadRecord
from app.modules.dataset import dataset_bp
from app.modules.dataset.services import (
    AuthorService,
    DSDownloadRecordService,
    DSMetaDataService,
    DSViewRecordService,
    DataSetService,
    DOIMappingService,
)
from app.modules.zenodo.services import ZenodoService

logger = logging.getLogger(__name__)
rating_service = RatingService()

dataset_service = DataSetService()
author_service = AuthorService()
dsmetadata_service = DSMetaDataService()
zenodo_service = ZenodoService()
doi_mapping_service = DOIMappingService()
ds_view_record_service = DSViewRecordService()
dataset_rating_service = RatingService()


@dataset_bp.route("/dataset/upload", methods=["GET", "POST"])
@login_required
def create_dataset():
    form = DataSetForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            return jsonify({"message": form.errors}), 400

        try:
            # Creación del dataset en local
            dataset = dataset_service.create_from_form(form=form, current_user=current_user)
            dataset_service.move_feature_models(dataset)

            # Intento de envío a Zenodo
            try:
                zenodo_response_json = zenodo_service.create_new_deposition(dataset)
                deposition_id = zenodo_response_json.get("id")
                dataset_service.update_dsmetadata(dataset.ds_meta_data_id, deposition_id=deposition_id)

                # Carga de modelos de características y publicación de la deposición
                for feature_model in dataset.feature_models:
                    zenodo_service.upload_file(dataset, deposition_id, feature_model)
                zenodo_service.publish_deposition(deposition_id)

                # Actualización del DOI
                deposition_doi = zenodo_service.get_doi(deposition_id)
                dataset_service.update_dsmetadata(dataset.ds_meta_data_id, dataset_doi=deposition_doi)

            except Exception:
                msg = "it has not been possible upload feature models in Zenodo and update the DOI"
                return jsonify({"message": msg}), 200

            except Exception as exc:
                logger.exception(f"No se pudo subir a Zenodo o actualizar el DOI: {exc}")
                return jsonify({"message": "No se pudo subir los modelos a Zenodo y actualizar el DOI"}), 200

            # Eliminación del folder temporal
            file_path = current_user.temp_folder()
            if os.path.exists(file_path) and os.path.isdir(file_path):
                shutil.rmtree(file_path)

            return jsonify({"message": "¡Todo funcionó correctamente!"}), 200

        except Exception as exc:
            logger.exception(f"Error al crear dataset: {exc}")
            return jsonify({"Exception while create dataset data in local: ": str(exc)}), 400

    return render_template("dataset/upload_dataset.html", form=form)


@dataset_bp.route("/dataset/list", methods=["GET", "POST"])
@login_required
def list_dataset():
    return render_template(
        "dataset/list_datasets.html",
        datasets=dataset_service.get_synchronized(current_user.id),
        local_datasets=dataset_service.get_unsynchronized(current_user.id),
    )


@dataset_bp.route("/dataset/file/upload", methods=["POST"])
@login_required
def upload():
    file = request.files["file"]
    temp_folder = current_user.temp_folder()

    if file.filename.endswith(".zip"):
        try:
            # create temp folder
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)

            file_path = os.path.join(temp_folder, file.filename)
            file.save(file_path)

            with ZipFile(file_path, "r") as zipf:
                # Ignore directory structure
                for member in zipf.namelist():
                    filename = os.path.basename(member)
                    if filename:
                        source = zipf.open(member)
                        # If an extracted file with the same name is already in the temp dir, give it a different name
                        if os.path.exists(os.path.join(temp_folder, filename)):
                            # Generate unique filename (by recursion)
                            base_name, extension = os.path.splitext(member)
                            i = 1
                            while os.path.exists(
                                os.path.join(temp_folder, f"{base_name} ({i}){extension}")
                            ):
                                i += 1
                            new_filename = f"{base_name} ({i}){extension}".split("/")[-1]
                            target = open(os.path.join(temp_folder, new_filename), "wb")
                        else:
                            target = open(os.path.join(temp_folder, filename), "wb")

                        with source, target:
                            shutil.copyfileobj(source, target)

            # Delete all files that are not .uvl
            for file in os.listdir(temp_folder):
                if file[-4:] != ".uvl":
                    os.remove(os.path.join(temp_folder, file))

            return (
                jsonify(
                    {
                        "message": "UVL uploaded and validated successfully",
                        "filenames": os.listdir(temp_folder),
                    }
                ),
                200,
            )

        except Exception as e:
            return jsonify({"message": str(e)}), 500

    else:
        if not file or not file.filename.endswith(".uvl"):
            return jsonify({"message": "No valid file"}), 400

        # create temp folder
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        file_path = os.path.join(temp_folder, file.filename)

        if os.path.exists(file_path):
            # Generate unique filename (by recursion)
            base_name, extension = os.path.splitext(file.filename)
            i = 1
            while os.path.exists(
                os.path.join(temp_folder, f"{base_name} ({i}){extension}")
            ):
                i += 1
            new_filename = f"{base_name} ({i}){extension}"
            file_path = os.path.join(temp_folder, new_filename)
        else:
            new_filename = file.filename

        try:
            file.save(file_path)
        except Exception as e:
            return jsonify({"message": str(e)}), 500

        return (
            jsonify(
                {
                    "message": "UVL uploaded and validated successfully",
                    "filenames": [new_filename],
                }
            ),
            200,
        )


@dataset_bp.route("/dataset/file/upload_from_github", methods=["POST"])
@login_required
def upload_from_github():
    data = request.get_json()
    url = data.get("url")
    url_split = url.split("/")

    try:
        # Do not accept URLs that are not from GitHub or that contain a file that is not .uvl
        if url_split[2] != "github.com":
            return jsonify({"message": "The file is not from GitHub"}), 400
        if url_split[-1][-4:] != ".uvl":
            return jsonify({"message": "The imported file is not UVL"}), 400

        headers = {"Accept": "application/vnd.github.raw+json", "X-GitHub-Api-Version": "2022-11-28"}
        owner = url_split[3]
        repo = url_split[4]
        path = "/".join(url_split[7:])
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/contents/{path}", headers=headers)
        if response.status_code != 200:
            return jsonify({"message": "GitHub returned an error"}), response.status_code
    except Exception:
        return jsonify({"message": "Malformed URL. Please check that it follows the specified format."}), 400

    contents = response.text
    filename = url_split[-1]
    temp_folder = current_user.temp_folder()
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    file_path = os.path.join(temp_folder, filename)

    if os.path.exists(file_path):
        # Generate unique filename (by recursion)
        base_name, extension = os.path.splitext(filename)
        i = 1
        while os.path.exists(os.path.join(temp_folder, f"{base_name} ({i}){extension}")):
            i += 1
        new_filename = f"{base_name} ({i}){extension}"
        file_path = os.path.join(temp_folder, new_filename)
    else:
        new_filename = filename

    try:
        with open(file_path, "w") as uvl:
            uvl.write(contents)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

    return (
            jsonify(
                {
                    "message": "UVL uploaded and validated successfully",
                    "filenames": [new_filename],
                }
            ),
            200,
        )


@dataset_bp.route("/dataset/file/delete", methods=["POST"])
@login_required
def delete():
    data = request.get_json()
    filename = data.get("file")
    temp_folder = current_user.temp_folder()
    filepath = os.path.join(temp_folder, filename)

    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({"message": "Archivo eliminado correctamente"})

    return jsonify({"error": "Error: Archivo no encontrado"})


@dataset_bp.route("/dataset/download/<int:dataset_id>", methods=["GET"])
def download_dataset(dataset_id):
    dataset = dataset_service.get_or_404(dataset_id)

    file_path = f"uploads/user_{dataset.user_id}/dataset_{dataset.id}/"

    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, f"dataset_{dataset_id}.zip")

    with ZipFile(zip_path, "w") as zipf:
        for subdir, dirs, files in os.walk(file_path):
            for file in files:
                full_path = os.path.join(subdir, file)

                relative_path = os.path.relpath(full_path, file_path)

                zipf.write(
                    full_path,
                    arcname=os.path.join(
                        os.path.basename(zip_path[:-4]), relative_path
                    ),
                )

    user_cookie = request.cookies.get("download_cookie")
    if not user_cookie:
        user_cookie = str(
            uuid.uuid4()
        )
        resp = make_response(
            send_from_directory(
                temp_dir,
                f"dataset_{dataset_id}.zip",
                as_attachment=True,
                mimetype="application/zip",
            )
        )
        resp.set_cookie("download_cookie", user_cookie)
    else:
        resp = send_from_directory(
            temp_dir,
            f"dataset_{dataset_id}.zip",
            as_attachment=True,
            mimetype="application/zip",
        )

    existing_record = DSDownloadRecord.query.filter_by(
        user_id=current_user.id if current_user.is_authenticated else None,
        dataset_id=dataset_id,
        download_cookie=user_cookie
    ).first()

    if not existing_record:
        DSDownloadRecordService().create(
            user_id=current_user.id if current_user.is_authenticated else None,
            dataset_id=dataset_id,
            download_date=datetime.now(timezone.utc),
            download_cookie=user_cookie,
        )

    return resp


@dataset_bp.route("/dataset/download/all", methods=["GET"])
def download_all_datasets():
    # Obtener todos los IDs de datasets
    dataset_ids = dataset_service.get_datasets_ids()

    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "all_datasets.zip")

    # Crear el archivo ZIP
    with ZipFile(zip_path, "w") as zipf:
        for dataset_id in dataset_ids:
            dataset = dataset_service.get_or_404(dataset_id)

            # Ruta del dataset
            file_path = f"uploads/user_{dataset.user_id}/dataset_{dataset.id}/"

            for subdir, dirs, files in os.walk(file_path):
                for file in files:
                    full_path = os.path.join(subdir, file)
                    relative_path = os.path.relpath(full_path, file_path)

                    # Añadir al ZIP
                    zipf.write(full_path, arcname=relative_path)

    user_cookie = request.cookies.get("download_cookie")
    if not user_cookie:
        user_cookie = str(uuid.uuid4())

    resp = make_response(
        send_from_directory(
            temp_dir,
            "all_datasets.zip",
            as_attachment=True,
            mimetype="application/zip",
        )
    )
    resp.set_cookie("download_cookie", user_cookie)

    # Registrar descarga en la base de datos
    for dataset_id in dataset_ids:
        existing_record = DSDownloadRecord.query.filter_by(
            user_id=current_user.id if current_user.is_authenticated else None,
            dataset_id=dataset_id,
            download_cookie=user_cookie
        ).first()

        if not existing_record:
            DSDownloadRecordService().create(
                user_id=current_user.id if current_user.is_authenticated else None,
                dataset_id=dataset_id,
                download_date=datetime.now(timezone.utc),
                download_cookie=user_cookie,
            )

    return resp


@dataset_bp.route("/doi/<path:doi>/", methods=["GET"])
def subdomain_index(doi):
    new_doi = doi_mapping_service.get_new_doi(doi)
    if new_doi:
        return redirect(url_for('dataset.subdomain_index', doi=new_doi), code=302)

    ds_meta_data = dsmetadata_service.filter_by_doi(doi)
    if not ds_meta_data:
        abort(404)

    dataset = ds_meta_data.data_set
    user_cookie = ds_view_record_service.create_cookie(dataset=dataset)
    resp = make_response(render_template("dataset/view_dataset.html", dataset=dataset))
    resp.set_cookie("view_cookie", user_cookie)

    return resp


@dataset_bp.route("/dataset/unsynchronized/<int:dataset_id>/", methods=["GET"])
@login_required
def get_unsynchronized_dataset(dataset_id):
    dataset = dataset_service.get_unsynchronized_dataset(current_user.id, dataset_id)
    if not dataset:
        abort(404)
    return render_template("dataset/view_dataset.html", dataset=dataset)


@dataset_bp.route('/dataset/rate/<int:dataset_id>/', methods=['GET'])
@login_required
def view_rating_form(dataset_id):
    form = RatingForm()
    dataset = dataset_service.get_or_404(dataset_id)
    ds_meta_data_id = dataset.ds_meta_data.id
    ratings = rating_service.get_ratings(ds_meta_data_id)

    return render_template('dataset/view_ratings.html', form=form, dataset=dataset, ratings=ratings)


@dataset_bp.route("/datasets/<int:dataset_id>/create/rating", methods=["GET", "POST"])
@login_required
def create_rating(dataset_id):
    user_id = current_user.id
    value = request.form.get('value')
    comment = request.form.get('comment')

    if not value or not value.isdigit() or not (1 <= int(value) <= 5):
        flash("La puntuación es obligatoria y debe estar entre 1 y 5.", "error")
        return redirect(url_for('dataset.view_rating_form', dataset_id=dataset_id))

    dataset = dataset_service.get_or_404(dataset_id)
    ds_meta_data_id = dataset.ds_meta_data.id

    rating_service.create_rating(user_id, ds_meta_data_id, int(value), comment or None)

    flash("Valoración creada con éxito.", "success")
    return redirect(url_for('dataset.view_rating_form', dataset_id=dataset_id))


@dataset_bp.route("/dataset/anonymize/<int:dataset_id>/", methods=["GET", "POST"])
@login_required
def change_anonymize_sync(dataset_id):
    # Get dataset
    dataset = dataset_service.get_synchronized_dataset(current_user.id, dataset_id)

    return change_anonymize(dataset)


@dataset_bp.route("/dataset/anonymize/unsync/<int:dataset_id>/", methods=["GET", "POST"])
@login_required
def change_anonymize_unsync(dataset_id):
    # Get dataset
    dataset = dataset_service.get_unsynchronized_dataset(current_user.id, dataset_id)

    return change_anonymize(dataset)


@dataset_bp.route('/dataset/chatbot', methods=['GET'])
def chatbot():
    return render_template('dataset/chatbot.html')


def change_anonymize(dataset):
    # Coger el actual
    current_anonymize = dataset.ds_meta_data.anonymized
    changes = {
        "anonymized": not current_anonymize
    }

    # Cambiarlo y subirlo
    dsmetadata_service.update(dataset.id, **changes)

    # Redirigir al listado de datasets
    return redirect(url_for('dataset.list_dataset'))
