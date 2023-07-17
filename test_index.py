from index import gen_index
from main import export_csv_table, load_index_data


def test_index_py():
    # gen_index("python", ".", "")
    pass


def test_summary():
    data = load_index_data()
    export_csv_table(data, "a.csv")
