
import csv, os
class TableLoadError(Exception): pass
def load_table(path_or_name: str):
    paths = [path_or_name, os.path.abspath(path_or_name), os.path.join(os.getcwd(),'sample_data', path_or_name)]
    if not path_or_name.lower().endswith('.csv'):
        paths += [path_or_name + '.csv', os.path.abspath(path_or_name + '.csv'), os.path.join(os.getcwd(),'sample_data', path_or_name + '.csv')]
    for p in paths:
        if p and os.path.exists(p) and os.path.isfile(p):
            try:
                with open(p, newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    records = [dict(r) for r in reader]
                    columns = reader.fieldnames or []
                    columns = [c.strip() for c in columns]
                    table_name = os.path.splitext(os.path.basename(p))[0]
                    return table_name, records, columns
            except Exception as e:
                raise TableLoadError(f'Failed to read CSV {p}: {e}')
    raise TableLoadError(f'CSV not found: {path_or_name}')
