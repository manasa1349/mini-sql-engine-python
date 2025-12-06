from typing import Any, List, Dict

def coerce_number(val):
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return val
    s = str(val).strip()
    if s == '':
        return None
    try:
        if '.' in s:
            return float(s)
        return int(s)
    except:
        return None

def compare_values(left_raw: Any, op: str, right_raw: Any) -> bool:
    right_val = right_raw
    if right_val is None:
        if op == '=':
            return left_raw is None or str(left_raw).strip().upper() == 'NULL' or str(left_raw).strip() == ''
        if op == '!=':
            return not (left_raw is None or str(left_raw).strip().upper() == 'NULL' or str(left_raw).strip() == '')
        raise ValueError('Cannot use inequality/ordering with NULL')

    left_num = coerce_number(left_raw)
    right_num = coerce_number(right_val)

    if op in (">", "<", ">=", "<=") and (left_num is None or right_num is None):
        raise ValueError(f"Invalid numeric comparison: {left_raw} {op} {right_raw}")

    if left_num is not None and right_num is not None:
        if op == '=': return left_num == right_num
        if op == '!=': return left_num != right_num
        if op == '>': return left_num > right_num
        if op == '<': return left_num < right_num
        if op == '>=': return left_num >= right_num
        if op == '<=': return left_num <= right_num

    ls = '' if left_raw is None else str(left_raw)
    rs = str(right_val)

    if op == '=': return ls == rs
    if op == '!=': return ls != rs
    if op == '>': return ls > rs
    if op == '<': return ls < rs
    if op == '>=': return ls >= rs
    if op == '<=': return ls <= rs

    raise ValueError('Unsupported operator: ' + op)

def pretty_print(columns: List[str], records: List[Dict], max_width=30):
    if not columns:
        print('(no columns)')
        return
    col_widths = {}
    for c in columns:
        maxlen = len(str(c))
        for r in records:
            v = r.get(c, '')
            l = 0 if v is None else len(str(v))
            if l > maxlen:
                maxlen = l
        col_widths[c] = min(max_width, maxlen)

    sep = '+' + '+'.join('-' * (col_widths[c] + 2) for c in columns) + '+'
    header = '|' + '|'.join(' {0} '.format(str(c)[:col_widths[c]].ljust(col_widths[c])) for c in columns) + '|'

    print(sep)
    print(header)
    print(sep)

    for r in records:
        parts = []
        for c in columns:
            v = r.get(c, '')
            s = '' if v is None else str(v)
            parts.append(' {0} '.format(s[:col_widths[c]].ljust(col_widths[c])))
        print('|' + '|'.join(parts) + '|')

    print(sep)

def aggregate_values(records: List[Dict], func: str, arg: str):
    vals = []
    for r in records:
        v = r.get(arg)
        if v is None or str(v).strip() == '':
            continue
        try:
            if '.' in str(v):
                nv = float(v)
            else:
                nv = int(v)
            vals.append(nv)
        except:
            try:
                nv = float(v)
                vals.append(nv)
            except:
                continue

    if func == 'COUNT': return len(vals)
    if func == 'SUM': return sum(vals) if vals else 0
    if func == 'AVG': return (sum(vals) / len(vals)) if vals else None
    if func == 'MIN': return min(vals) if vals else None
    if func == 'MAX': return max(vals) if vals else None

    raise ValueError('Unknown aggregate')