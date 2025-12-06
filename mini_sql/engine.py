from typing import List, Dict, Any
from mini_sql.loader import load_table, TableLoadError
from mini_sql.parser import SQLQuery, Condition
from mini_sql.utils import compare_values, aggregate_values

class RunError(Exception):
    pass


def run_query(query: SQLQuery, table_path_or_name: str = None):
    # Load table
    if not table_path_or_name:
        table_path_or_name = query.from_table

    try:
        table_name, records, columns = load_table(table_path_or_name)
    except TableLoadError as e:
        raise RunError(str(e))

    result = records

    # -----------------------------
    # WHERE filtering (AND / OR)
    # -----------------------------
    if query.where:
        filtered = []

        for rec in result:
            evals = []

            for item in query.where:
                if isinstance(item, str):
                    evals.append(item)
                else:
                    if item.col not in columns:
                        raise RunError(f"Column not found: {item.col}")
                    try:
                        ok = compare_values(rec.get(item.col), item.op, item.val)
                    except ValueError as e:
                        raise RunError(str(e))
                    evals.append(bool(ok))
            if not evals:
                keep = True
            else:
                acc = evals[0]
                i = 1
                while i < len(evals):
                    op = evals[i]
                    right = evals[i + 1]
                    if op == "AND":
                        acc = acc and right
                    else:
                        acc = acc or right
                    i += 2

                keep = bool(acc)

            if keep:
                filtered.append(rec)

        result = filtered

    # -----------------------------
    # ORDER BY
    # -----------------------------
    if query.order_by:
        col, direction = query.order_by
        rev = (direction.upper() == "DESC")

        def _coerce_for_sort(val):
            if val is None:
                return (1, None)
            try:
                s = str(val).strip()
                if s == '':
                    return (1, None)
                if '.' in s:
                    return (0, float(s))
                return (0, int(s))
            except Exception:
                return (0, str(val))

        try:
            result.sort(key=lambda r: _coerce_for_sort(r.get(col)), reverse=rev)
        except Exception:
            pass

    # -----------------------------
    # LIMIT
    # -----------------------------
    if query.limit is not None:
        result = result[:query.limit]

    # -----------------------------
    # AGGREGATES (COUNT, SUM, AVG)
    # -----------------------------
    if query.aggregates:
        out = {}

        for func, arg in query.aggregates:
            if arg == "*":
                out[f"{func}(*)"] = len(result)
            else:
                if arg not in columns:
                    raise RunError(f"Aggregate column not found: {arg}")
                out[f"{func}({arg})"] = aggregate_values(result, func, arg)

        return {"aggregates": out}

    # -----------------------------
    # SELECT *
    # -----------------------------
    if len(query.select) == 1 and query.select[0][0] == "*":
        rows = [{c: rec.get(c) for c in columns} for rec in result]
        return {"columns": columns, "rows": rows}

    # -----------------------------
    # SELECT col1, col2, ...
    # -----------------------------
    out_cols = []
    for expr, alias in query.select:
        col_name = alias if alias else expr

        if expr not in columns:
            raise RunError(f"Column not found: {expr}")

        out_cols.append(col_name)
    rows = []
    for rec in result:
        row = {}
        for expr, alias in query.select:
            key = alias if alias else expr
            row[key] = rec.get(expr)
        rows.append(row)
    return {"columns": out_cols, "rows": rows}