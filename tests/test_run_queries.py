
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mini_sql.parser import parse
from mini_sql.engine import run_query
def run_smoke():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    small = os.path.join(base, 'sample_data', 'students_small.csv')
    q1 = parse('SELECT * FROM students_small;')
    r1 = run_query(q1, table_path_or_name=small)
    assert 'columns' in r1 and 'rows' in r1
    q2 = parse('SELECT COUNT(*) FROM students_small;')
    r2 = run_query(q2, table_path_or_name=small)
    assert 'aggregates' in r2 and 'COUNT(*)' in r2['aggregates']
    q3 = parse('SELECT COUNT(cc_total_problems) FROM students_small WHERE cc_total_problems > 10;')
    r3 = run_query(q3, table_path_or_name=small)
    assert 'aggregates' in r3
    q4 = parse('SELECT name AS student, lc_easy FROM students_small WHERE lc_easy >= 0 LIMIT 5;')
    r4 = run_query(q4, table_path_or_name=small)
    assert len(r4.get('rows')) <= 5
    q5 = parse('SELECT name FROM students_small ORDER BY name DESC LIMIT 3;')
    r5 = run_query(q5, table_path_or_name=small)
    assert 'rows' in r5
    print('Smoke tests OK')
if __name__ == '__main__': run_smoke()
