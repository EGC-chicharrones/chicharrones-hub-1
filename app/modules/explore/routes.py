from flask import render_template, request, jsonify
from app.modules.explore import explore_bp
from app.modules.explore.forms import ExploreForm
from app.modules.explore.services import ExploreService


@explore_bp.route('/explore', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        query = request.args.get('query', '')  # Obtener la consulta desde la URL
        form = ExploreForm()
        return render_template('explore/index.html', form=form, query=query)

    if request.method == 'POST':
        criteria = request.get_json()
        # Procesamos el 'query' para extraer los filtros
        query_string = criteria.get("query", "")  # Aquí obtenemos el 'query' como string
        # Llamamos al servicio de exploración con el query_string procesado
        datasets = ExploreService().filter(query_string)
        return jsonify([dataset.to_dict() for dataset in datasets])


def process_query(query):
    """
    Procesa el 'query' para convertirlo en filtros utilizables.
    Por ejemplo, 'author:pepe' se convierte en {'author': 'pepe'}.
    """
    filters = {}
    query_parts = query.split()
    for part in query_parts:
        if ':' in part:
            key, value = part.split(":", 1)
            filters[key] = value
    return filters
