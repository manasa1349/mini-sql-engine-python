
import argparse, sys
from mini_sql.parser import parse, ParseError
from mini_sql.engine import run_query, RunError
from mini_sql.utils import pretty_print
def repl(initial_file=None):
    current = None
    if initial_file: current = initial_file; print(f'Loaded table: {initial_file}')
    while True:
        try: raw = input('mini-sql> ').strip()
        except (EOFError, KeyboardInterrupt): print('\\nBye.'); return
        if not raw: continue
        if raw.lower() in ('exit','quit'): print('Bye.'); return
        if raw.lower().startswith("load "):
            parts = raw.split(None, 1)
            if len(parts) == 2:
                filename = parts[1].strip().rstrip(";")
                if filename.lower().endswith(".csv"):
                    current = filename
                else:
                    current = filename + ".csv"
                print(f"Table set to: {current}")
            else:
                print("Usage: load <csv_file>")
            continue
        if raw.lower() == 'help':
            print('Example: SELECT name, age FROM students_small WHERE age > 20 ORDER BY name DESC LIMIT 10;'); continue
        try: q = parse(raw)
        except ParseError as e: print('Parse error:', e); continue
        try: res = run_query(q, table_path_or_name=q.from_table)
        except RunError as e: print('Execution error:', e); continue
        if isinstance(res, dict) and 'aggregates' in res:
            for k,v in res['aggregates'].items(): print(f'{k}: {v}')
        elif isinstance(res, dict) and 'columns' in res and 'rows' in res:
            pretty_print(res['columns'], res['rows'])
        else: print(res)
def main():
    p = argparse.ArgumentParser(); p.add_argument('--file','-f', default=None); args = p.parse_args()
    try: repl(initial_file=args.file)
    except Exception as e: print('Error:', e); sys.exit(1)
if __name__ == '__main__': main()
