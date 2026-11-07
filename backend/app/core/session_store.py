from __future__ import annotations
import json, os, sqlite3
from pathlib import Path
from uuid import uuid4

COLUMNS={'approval_state':'TEXT', 'company':'TEXT','source_type':'TEXT','title':'TEXT',
         'prompt_version':'TEXT','template_version':'TEXT','updated_at':'TEXT'}

class SessionStore:
    def __init__(self, db_path=None):
        self.db_path=str(db_path or os.getenv('SALES_COPILOT_DB_PATH') or Path(__file__).resolve().parents[2]/'sales_copilot.db')
        Path(self.db_path).parent.mkdir(parents=True,exist_ok=True)
        self._init_db()
    def _connect(self):
        c=sqlite3.connect(self.db_path,timeout=20)
        c.row_factory=sqlite3.Row
        c.execute('PRAGMA busy_timeout=20000')
        return c
    def _init_db(self):
        with self._connect() as c:
            c.execute('CREATE TABLE IF NOT EXISTS sessions (session_id TEXT PRIMARY KEY,status TEXT NOT NULL,payload TEXT NOT NULL)')
            existing={x['name'] for x in c.execute('PRAGMA table_info(sessions)')}
            for name,sqltype in COLUMNS.items():
                if name not in existing: c.execute(f'ALTER TABLE sessions ADD COLUMN {name} {sqltype}')
            # Old stored sessions still work, and indexed filtering uses their source fields.
            for row in c.execute('SELECT session_id,payload FROM sessions'):
                try: s=json.loads(row['payload'])
                except (TypeError,ValueError):continue
                src=s.get('source') or {}
                c.execute('UPDATE sessions SET approval_state=?,company=?,source_type=?,title=?,prompt_version=?,template_version=?,updated_at=COALESCE(updated_at,CURRENT_TIMESTAMP) WHERE session_id=?',
                 (s.get('approval_state','drafted'),src.get('sender_company',''),src.get('source_type',''),src.get('title',''),s.get('prompt_version',''),s.get('template_version',''),row['session_id']))
    def create(self,source,normalized_source,sales_signals):
        s={'session_id':'sess_'+uuid4().hex[:12],'status':'analyzed','approval_state':'drafted',
           'source':source,'normalized_source':normalized_source,'sales_signals':sales_signals,
           'draft_outputs':[],'selected_draft_id':None,'revision_history':[], 'review_notes':[],
           'guardrail_annotations':[],'guardrail_result':None,'approval_record':None,'final_pack':{},
           'source_evidence':[], 'prompt_version':'v1.1.0','template_version':'v1.0.0'}
        return self.save(s)
    def save(self,s):
        src=s.get('source') or {}
        with self._connect() as c:
            c.execute("""INSERT INTO sessions(session_id,status,approval_state,company,source_type,title,prompt_version,template_version,payload,updated_at)
              VALUES(?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP) ON CONFLICT(session_id) DO UPDATE SET
              status=excluded.status,approval_state=excluded.approval_state,company=excluded.company,
              source_type=excluded.source_type,title=excluded.title,prompt_version=excluded.prompt_version,
              template_version=excluded.template_version,payload=excluded.payload,updated_at=CURRENT_TIMESTAMP""",
              (s['session_id'],s.get('status','analyzed'),s.get('approval_state','drafted'),src.get('sender_company',''),
               src.get('source_type',''),src.get('title',''),s.get('prompt_version',''),s.get('template_version',''),json.dumps(s,ensure_ascii=False)))
        return s
    def get(self,sid):
        with self._connect() as c:
            row=c.execute('SELECT payload FROM sessions WHERE session_id=?',(sid,)).fetchone()
        if row is None: raise KeyError(sid)
        return json.loads(row['payload'])
    def list(self,filters=None):
        filters=filters or {}; q='SELECT payload FROM sessions WHERE 1=1'; params=[]
        for k in ('company','source_type','status'):
            if filters.get(k):
                q+=f' AND {k} LIKE ?';params.append('%'+filters[k]+'%')
        if filters.get('date'):
            q+=' AND substr(updated_at,1,10)=?'; params.append(filters['date'])
        with self._connect() as c: rows=c.execute(q+' ORDER BY updated_at DESC,session_id DESC',params).fetchall()
        return [json.loads(row['payload']) for row in rows]

session_store=SessionStore()
