import re
from dataclasses import dataclass
from typing import List, Optional, Union, Tuple

class ParseError(Exception): pass

@dataclass
class Condition:
    col: str
    op: str
    val: Union[str,int,float,None]
    raw: str

@dataclass
class SQLQuery:
    select: List[Tuple[str, Optional[str]]]
    aggregates: List[Tuple[str,str]]
    from_table: str
    where: Optional[List]
    order_by: Optional[Tuple[str,str]]
    limit: Optional[int]

OP_RE = r'(>=|<=|!=|=|>|<)'

def _parse_value(token: str):
    token = token.strip()
    if (token.startswith("'") and token.endswith("'")) or (token.startswith('"') and token.endswith('"')):
        return token[1:-1]
    if token.upper() == 'NULL': return None
    try:
        if '.' in token: return float(token)
        return int(token)
    except:
        return token

def parse(sql: str) -> SQLQuery:
    if not sql or not sql.strip(): raise ParseError('Empty query')
    s = sql.strip().rstrip(';').strip()
    order_by = None; limit = None
    m_lim = re.search(r'\bLIMIT\s+(\d+)$', s, re.IGNORECASE)
    if m_lim:
        limit = int(m_lim.group(1)); s = re.sub(r'\bLIMIT\s+\d+$', '', s, flags=re.IGNORECASE).strip()
    m_ob = re.search(r'\bORDER\s+BY\s+([A-Za-z0-9_]+)(?:\s+(ASC|DESC))?$', s, re.IGNORECASE)
    if m_ob:
        order_by = (m_ob.group(1), (m_ob.group(2) or 'ASC').upper())
        s = re.sub(r'\bORDER\s+BY\s+[A-Za-z0-9_]+(?:\s+(ASC|DESC))?$', '', s, flags=re.IGNORECASE).strip()
    m = re.match(r'\s*SELECT\s+(.*?)\s+FROM\s+(\S+)(?:\s+WHERE\s+(.*))?$', s, re.IGNORECASE)
    if not m:
        upper = s.upper()
        if 'SELECT' not in upper: raise ParseError('Missing SELECT clause')
        if 'FROM' not in upper: raise ParseError('Missing FROM clause')
        raise ParseError('Malformed query. Expected: SELECT <cols> FROM <table> [WHERE ...]')
    select_part = m.group(1).strip(); from_part = m.group(2).strip().strip(';')
    where_part = m.group(3).strip() if m.group(3) else None
    aggregates = []; select_items = []
    parts = [p.strip() for p in select_part.split(',') if p.strip()]
    for p in parts:
        alias = None
        p = p.strip().rstrip(";")
        m_as = re.match(r'(.+?)\s+AS\s+([A-Za-z0-9_]+)$', p, re.IGNORECASE)
        if m_as:
            expr = m_as.group(1).strip().rstrip(";")
            alias = m_as.group(2).strip()
        else:
            expr = p.strip().rstrip(";")
        m_agg = re.match(r'(COUNT|SUM|AVG|MIN|MAX)\s*\(\s*([*A-Za-z0-9_]+)\s*\)$', expr, re.IGNORECASE)
        if m_agg:
            func = m_agg.group(1).upper(); arg = m_agg.group(2)
            aggregates.append((func,arg)); select_items.append((f'{func}({arg})', alias))
        else:
            select_items.append((expr, alias))
    where = None
    if where_part:
        tokens = re.split(r'\s+(AND|OR)\s+', where_part, flags=re.IGNORECASE)
        where = []
        for t in tokens:
            if t is None: continue
            t = t.strip()
            if t.upper() in ('AND','OR'): where.append(t.upper())
            else:
                m_op = re.search(OP_RE, t)
                if not m_op: raise ParseError('Unsupported operator in WHERE')
                op = m_op.group(1); left, right = t.split(op,1)
                col = left.strip(); valtok = right.strip(); val = _parse_value(valtok)
                where.append(Condition(col=col, op=op, val=val, raw=valtok))
    return SQLQuery(select=select_items, aggregates=aggregates, from_table=from_part, where=where, order_by=order_by, limit=limit)
