import csv
from io import StringIO


def generate_csv_data(items):
    csv_data = StringIO()
    csv_writer = csv.DictWriter(
        csv_data, fieldnames=["id", "name", "description"]
    )
    csv_writer.writeheader()
    for item in items:
        csv_writer.writerow(
            {"id": item.id, "name": item.name, "description": item.description}
        )
    csv_data.seek(0)
    return csv_data
