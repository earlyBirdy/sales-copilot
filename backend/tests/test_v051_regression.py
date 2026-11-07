import json, sqlite3
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core import session_store as store_module
from app.core.session_store import SessionStore
from app.core.intake_pipeline import parse_uploaded, normalize_unified_intake
from app.api import routes_intake, routes_templates, routes_revisions, routes_guardrail

@pytest.fixture
def client(tmp_path, monkeypatch):
    store=SessionStore(str(tmp_path/'db.sqlite'))
    for mod in [store_module, routes_intake, routes_templates, routes_revisions, routes_guardrail]:
        monkeypatch.setattr(mod,'session_store',store,raising=False)
    from app.api import routes_sessions, routes_export, routes_drafts
    for mod in [routes_sessions,routes_export,routes_drafts]:monkeypatch.setattr(mod,'session_store',store)
    monkeypatch.setattr(routes_intake.intake_agent if hasattr(routes_intake,'intake_agent') else routes_intake.IntakeAgent,'run',
        lambda self,src: {'source_type':src['source_type'],'title':src['title'],'company':src.get('sender_company',''),
             'product_or_solution':'Edge AI','summary_bullets':['one','two','three'],
             'claims':['rugged Edge AI'],'explicit_cta':[]})
    monkeypatch.setattr(routes_intake.ExtractorAgent,'run',lambda self,n: {'company':n['company'],'product_or_solution':'Edge AI',
       'announcement_type':'update','target_industries':[],'target_buyers':[],'selling_points':['rugged Edge AI'],
       'proof_points':[],'customer_pain_points':[],'business_value':[],'risks_or_unclear_claims':[],
       'cta_options':['Happy to discuss.']})
    monkeypatch.setattr(routes_templates.DraftAgent,'run',lambda self, signals, req: {'draft_set_id':'set1',
       'audience':req['audience'],'tone':req['tone'],'drafts':[{'draft_id':'d1','length':'short','text':'Rugged Edge AI is suitable for review.'}]})
    monkeypatch.setattr(routes_revisions.RevisionAgent,'run',lambda self, text,instruction,context:{'revision_id':'rev1','text':'Revised: '+text})
    monkeypatch.setattr(routes_guardrail.GuardrailAgent,'run',lambda self,text,ctx:{'review_notes':[],'risk_level':'low'})
    return TestClient(app)

def test_safety_approval_edit_and_reopen(client):
    s=client.post('/intake/unified',json={'intake_mode':'paste','source_type':'email','title':'Demo',
      'raw_text':'An announcement about rugged Edge AI.','sender_company':'Vendor'}).json()
    sid=s['session_id'];assert s['source_evidence'][0]['verified_in_source']
    assert client.post('/sessions/'+sid+'/approval',json={'approval_state':'approved','checklist':{}}).status_code==409
    d=client.post('/templates/generate-template',json={'session_id':sid,'template_key':'customer_update'});assert d.status_code==200,d.text
    assert client.post('/drafts/'+sid+'/select-draft',json={'draft_id':'missing'}).status_code==404
    assert client.post('/drafts/'+sid+'/select-draft',json={'draft_id':'d1'}).status_code==200
    assert client.post('/export/markdown',json={'session_id':sid}).status_code==409
    assert client.post('/export/final-pack',json={'session_id':sid}).status_code==200
    assert client.post('/drafts/guardrail',json={'session_id':sid,'draft_id':'d1'}).status_code==200
    check={c:True for c in ('source_verified','claims_verified','audience_checked','recipients_checked')}
    assert client.post('/sessions/'+sid+'/approval',json={'approval_state':'approved','checklist':check}).status_code==200
    assert client.get('/sessions/'+sid).json()['approval_state']=='approved'
    assert client.post('/export/markdown',json={'session_id':sid}).status_code==200
    block=client.get('/sessions/'+sid).json()['final_pack']['final_editable_blocks'][0]
    assert client.post('/export/'+sid+'/editable-block',json={'label':block['label'],'text':'New wording'}).status_code==200
    assert client.post('/export/email-ready',json={'session_id':sid}).status_code==409
    assert client.get('/sessions/'+sid).json()['approval_state']=='revised'
    assert client.get('/sessions',params={'company':'Vendor'}).json()['sessions'][0]['session_id']==sid

def test_revision_and_source_validation(client):
    sid=client.post('/intake/unified',json={'raw_text':'a rugged Edge AI machine','title':'T','intake_mode':'paste','source_type':'email'}).json()['session_id']
    client.post('/templates/generate-template',json={'session_id':sid,'template_key':'customer_update'})
    client.post('/drafts/'+sid+'/select-draft',json={'draft_id':'d1'})
    result=client.post('/drafts/revise',json={'session_id':sid,'draft_id':'d1','instruction':'Shorten'})
    assert result.status_code==200,result.text
    assert client.get('/sessions/'+sid).json()['revision_history'][0]['result_text'].startswith('Revised:')
    assert client.post('/intake/unified',json={'intake_mode':'paste','raw_text':'','source_type':'article'}).status_code==422
    assert client.post('/intake/unified',json={'intake_mode':'url_fetch','url':'http://127.0.0.1','source_type':'article'}).status_code==400
    assert client.post('/intake/unified',json={'intake_mode':'upload','upload_name':'fake.pdf','source_type':'document'}).status_code==422

def test_file_upload_real_email(client):
    files=list(Path('/mnt/data').glob('*.eml'))
    if not files:pytest.skip('sample email not mounted')
    data=files[0].read_bytes()
    parsed=parse_uploaded(files[0].name,data)
    assert 'SINTRONES' in parsed['raw_text']
    res=client.post('/intake/upload',files={'file':(files[0].name,data,'message/rfc822')})
    assert res.status_code==200,res.text
    assert 'SINTRONES' in res.json()['source']['raw_text']

def test_legacy_db_migration(tmp_path):
    db=tmp_path/'legacy.db'
    with sqlite3.connect(db) as c:
        c.execute('CREATE TABLE sessions (session_id TEXT PRIMARY KEY,status TEXT NOT NULL,payload TEXT NOT NULL)')
        payload={'session_id':'old','status':'analyzed','source':{'sender_company':'Legacy','source_type':'email','title':'A'}}
        c.execute('INSERT INTO sessions VALUES(?,?,?)',('old','analyzed',json.dumps(payload)))
    store=SessionStore(str(db))
    assert store.get('old')['source']['sender_company']=='Legacy'
    assert store.list({'company':'Legacy'})[0]['session_id']=='old'
    store.save(store.get('old'))
    assert store.list({'source_type':'email'})

def test_public_url_fetch_pinned(monkeypatch):
    from app.core import intake_pipeline as intake
    monkeypatch.setattr(intake.socket,'getaddrinfo',lambda *a,**k:[(2,1,6,'',('93.184.215.14',443))])
    class R:
        returncode=0
        stdout=b'<html><body><script>fake data</script><article><h1>Public Product News</h1><p>Rugged Edge AI product available for review and deployment planning.</p></article></body></html>'
    calls=[]
    def fake_run(args,**kwargs):calls.append(args);return R()
    monkeypatch.setattr(intake.subprocess,'run',fake_run)
    text=intake.fetch_article('https://example.com/news')
    assert 'Rugged Edge AI' in text and 'fake data' not in text
    assert '--resolve' in calls[0] and '--max-redirs' in calls[0]
    monkeypatch.setattr(intake.socket,'getaddrinfo',lambda *a,**k:[(2,1,6,'',('127.0.0.1',443))])
    with pytest.raises(Exception):intake.fetch_article('https://internal.example')

def test_html_only_email():
    raw='MIME-Version: 1.0\nSubject: Launch\nContent-Type: text/html; charset=utf-8\n\n<html><body><p>Actual announcement text</p><script>junk</script></body></html>'
    from app.core.intake_pipeline import parse_email
    parsed=parse_email(raw)
    assert 'Actual announcement text' in parsed['raw_text']
    assert 'junk' not in parsed['raw_text']
