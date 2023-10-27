import json
import requests
from flask import Flask, request, jsonify


def get_data(filters, ordering, page, page_size):
    """API'ye bir istek gönderir ve yanıtı bir JSON nesnesi olarak döndürür."""
    url = "https://api-dev.massbio.info/assignment/query"
    headers = {"Content-Type": "application/json"}
    data = {"filters": filters, "ordering": ordering, "page": page, "page_size": page_size}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return json.loads(response.content)


def filter_data(data, filters):
    """Verileri filtreler."""
    for column, value in filters.items():
        if isinstance(value, list):
            # Birden çok değer için eşleşme.
            data = [d for d in data if d[column] in value]
        else:
            # Tek bir değer için eşleşme.
            data = [d for d in data if d[column] == value]
    return data


def sort_data(data, ordering):
    """Verileri sıralar."""
    for order in ordering:
        column = list(order.keys())[0]
        direction = order[column]
        data.sort(key=lambda d: d[column], reverse=direction == "DESC")
    return data


def get_page(data, page, page_size):
    """Belirli bir sayfayı döndürür."""
    return data[(page - 1) * page_size: page * page_size]


app = Flask(__name__)


@app.route("/")
def index():
    """Ana sayfa."""
    filters = request.args.get("filters", type=dict, default={})
    ordering = request.args.get("ordering", type=list, default=[])
    page = request.args.get("page", type=int, default=1)
    page_size = request.args.get("page_size", type=int, default=10)

    # Verileri filtreler.
    data = get_data(filters, ordering, page, page_size)

    # Verileri sıralar.
    data = sort_data(data, ordering)

    # Belirli bir sayfayı döndürür.
    data = get_page(data, page, page_size)

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
