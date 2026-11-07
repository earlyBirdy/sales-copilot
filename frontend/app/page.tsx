"use client";
import {useEffect,useState} from 'react';
const BASE=process.env.NEXT_PUBLIC_API_BASE_URL||'http://localhost:8000';
type Obj=Record<string,any>;
async function api(path:string,body?:Obj,method='POST'):Promise<Obj>{
 const res=await fetch(BASE+path,{method:body?method:'GET',headers:{'Content-Type':'application/json','X-Request-ID':crypto.randomUUID()},body:body?JSON.stringify(body):undefined});
 const data=await res.json().catch(()=>({}));if(!res.ok)throw Error(typeof data.detail==='string'?data.detail:`HTTP ${res.status}`);return data;
}
const checks=['source_verified','claims_verified','audience_checked','recipients_checked'];
export default function Page(){
 const [session,setSession]=useState<Obj|null>(null),[sessions,setSessions]=useState<Obj[]>([]),[templates,setTemplates]=useState<Obj[]>([]);
 const [busy,setBusy]=useState(''),[error,setError]=useState(''),[success,setSuccess]=useState('');
 const [mode,setMode]=useState('paste'),[title,setTitle]=useState(''),[company,setCompany]=useState(''),[raw,setRaw]=useState(''),[url,setUrl]=useState('');
 const [file,setFile]=useState<File|null>(null),[template,setTemplate]=useState('customer_update'),[cta,setCta]=useState('');
 const [instruction,setInstruction]=useState(''),[edit,setEdit]=useState(''),[checklist,setChecklist]=useState<Record<string,boolean>>({});
 const [filters,setFilters]=useState({company:'',source_type:'',status:'',date:''}),[exportText,setExportText]=useState('');
 async function run(name:string,fn:()=>Promise<any>){setBusy(name);setError('');setSuccess('');try{return await fn()}catch(e){setError(e instanceof Error?e.message:String(e));return null}finally{setBusy('')}}
 async function list(){const qs=new URLSearchParams(Object.entries(filters).filter(([,v])=>Boolean(v)) as [string,string][]);const response=await api('/sessions'+(qs.toString()?'?'+qs:''));setSessions(response.sessions||[])}
 async function reopen(id:string){const s=await api('/sessions/'+id);setSession(s);localStorage.setItem('sales_copilot_current_session',id);setEdit(s.final_pack?.final_editable_blocks?.[0]?.text||'');return s}
 async function refresh(){if(session)await reopen(session.session_id)}
 useEffect(()=>{api('/sessions').then(x=>setSessions(x.sessions||[])).catch(e=>setError(String(e)));api('/templates/library').then(x=>setTemplates(x.templates||[])).catch(()=>{});const id=localStorage.getItem('sales_copilot_current_session');if(id)reopen(id).catch(()=>localStorage.removeItem('sales_copilot_current_session'))},[]);
 const selected=session?.selected_draft_id;const active=session?.draft_outputs?.flatMap((g:Obj)=>g.drafts||[]).find((d:Obj)=>d.draft_id===selected);
 const block=session?.final_pack?.final_editable_blocks?.[0];const review=session?.guardrail_result;
 async function analyze(){await run('Analyzing',async()=>{
 let s:Obj;
 if(mode==='upload'){
  if(!file)throw Error('Choose an actual file');const form=new FormData();form.append('file',file);form.append('title',title);form.append('sender_company',company);
  const res=await fetch(BASE+'/intake/upload',{method:'POST',body:form});s=await res.json();if(!res.ok)throw Error(s.detail||'Upload failed');
 } else s=await api('/intake/unified',{intake_mode:mode,source_type:mode==='url_fetch'?'article':'email',title,raw_text:raw,url,sender_company:company});
 setSession(s);setEdit('');localStorage.setItem('sales_copilot_current_session',s.session_id);await list();
 })}
 async function act(path:string,payload:Obj,notice?:string){return run('Working',async()=>{const result=await api(path,payload);await refresh();if(notice)setSuccess(notice);return result})}
 async function download(format:'markdown'|'email-ready'){
  await run('Exporting',async()=>{const out=await api('/export/'+format,{session_id:session!.session_id});const text=out.markdown||out.email_ready_block;setExportText(text);const blob=new Blob([text],{type:'text/plain'});const link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download=format==='markdown'?'sales-pack.md':'sales-email.txt';link.click();URL.revokeObjectURL(link.href);await refresh()})
 }
 return <main><h1>Sales Copilot <span className="chip">v0.51</span></h1><p className="muted">Source-grounded drafts · edit · guardrail · explicit approval · copy/export only. No automatic sending.</p>
 {busy&&<div className="ok busy">{busy}…</div>}{error&&<div className="error" role="alert">{error}</div>}{success&&<div className="ok">{success}</div>}
 <div className="grid">
 <div>
  <section className="panel"><h2>Sessions</h2>{Object.keys(filters).map(k=><label className="field" key={k}><span className="muted">{k}</span><input type={k==='date'?'date':'text'} value={(filters as Obj)[k]} onChange={e=>setFilters(p=>({...p,[k]:e.target.value}))}/></label>)}<button className="outline" onClick={()=>run('Searching',list)}>Filter</button><div className="history">{sessions.map(s=><button key={s.session_id} className="outline" style={{display:'block',width:'100%',textAlign:'left',marginTop:6}} onClick={()=>run('Opening',()=>reopen(s.session_id))}>{s.source?.title||s.session_id}<div className="muted">{s.source?.sender_company} · {s.approval_state||s.status}</div></button>)}</div></section>
  <section className="panel"><h2>Template library</h2><select value={template} onChange={e=>setTemplate(e.target.value)}>{templates.map(t=><option key={t.key} value={t.key}>{t.label}</option>)}</select></section>
 </div>
 <div>
  <section className="panel"><h2>1 · Source intake</h2><div className="row">{['paste','upload','url_fetch'].map(m=><button className={mode===m?'':'outline'} key={m} onClick={()=>setMode(m)}>{m==='url_fetch'?'URL':m}</button>)}</div>
  <label className="field">Title<input value={title} onChange={e=>setTitle(e.target.value)}/></label><label className="field">Company<input value={company} onChange={e=>setCompany(e.target.value)}/></label>
  {mode==='paste'?<textarea aria-label="Source text" value={raw} onChange={e=>setRaw(e.target.value)} placeholder="Paste original email or announcement"/>:mode==='url_fetch'?<label className="field">Public HTTPS article URL<input value={url} onChange={e=>setUrl(e.target.value)}/></label>:<label className="field">Text / EML / PDF file<input type="file" accept=".txt,.md,.eml,.pdf" onChange={e=>setFile(e.target.files?.[0]||null)}/></label>}
  <div className="row"><button disabled={!!busy||mode==='paste'&&!raw.trim()||mode==='url_fetch'&&!url.trim()||mode==='upload'&&!file} onClick={analyze}>Analyze source</button></div></section>
  {session&&<><section className="panel"><h2>Original source</h2><p className="muted">{session.source?.title} · {session.source?.source_type} · {session.source?.sender_company}</p><div className="source small">{session.source?.raw_text}</div></section><section className="panel"><h2>Evidence trace</h2>{(session.source_evidence||[]).map((x:Obj,i:number)=><div className="draft small" key={i}><b>{x.verified_in_source?'Exact source match':'Needs manual verification'}</b><p>{x.claim}</p><small>{x.source_quote||'No exact passage matched'}</small></div>)}</section></>}
 </div>
 <div>
  <section className="panel"><h2>2 · Sales analysis</h2>{session?<><h3>Summary</h3>{(session.normalized_source?.summary_bullets||[]).map((x:string,i:number)=><p className="small" key={i}>• {x}</p>)}<h3>Sales angles</h3>{(session.sales_signals?.selling_points||[]).map((x:string,i:number)=><p className="small" key={i}>• {x}</p>)}</>:<p className="muted">Analyze a real source first.</p>}</section>
  <section className="panel"><h2>3 · Generate & select</h2><label className="field">CTA<select value={cta} onChange={e=>setCta(e.target.value)}><option value="">Default CTA</option>{(session?.sales_signals?.cta_options||[]).map((x:string)=><option key={x}>{x}</option>)}</select></label><button disabled={!session||!!busy} onClick={()=>act('/templates/generate-template',{session_id:session!.session_id,template_key:template,selected_cta:cta},'Drafts generated')}>Generate drafts</button>
  {session?.draft_outputs?.map((g:Obj)=><div key={g.draft_set_id}>{g.drafts.map((d:Obj)=><div key={d.draft_id} className={'panel '+(selected===d.draft_id?'selected':'')}><div className="chips"><span className="chip">{g.audience}</span><span className="chip">{d.length}</span></div><div className="small" style={{whiteSpace:'pre-wrap'}}>{d.text}</div><button className="outline" disabled={!!busy} onClick={()=>act('/drafts/'+session!.session_id+'/select-draft',{draft_id:d.draft_id},'Selected')}>{selected===d.draft_id?'Selected ✓':'Select draft'}</button></div>)}</div>)}</section>
 </div>
 <div>
  <section className="panel"><h2>4 · Revise & review</h2><p className="muted">Active draft: {selected||'None'} · {session?.approval_state||'drafted'}</p><textarea aria-label="Revision instruction" placeholder="Make shorter, softer, more technical..." value={instruction} onChange={e=>setInstruction(e.target.value)}/><div className="row"><button disabled={!selected||!instruction.trim()||!!busy} onClick={async()=>{const x=await act('/drafts/revise',{session_id:session!.session_id,draft_id:selected,instruction});if(x)setInstruction('')}}>Revise</button><button className="outline" disabled={!selected||!!busy} onClick={()=>act('/drafts/guardrail',{session_id:session!.session_id,draft_id:selected})}>Guardrail</button></div>
  {(session?.revision_history||[]).filter((x:Obj)=>x.draft_id===selected).map((x:Obj)=><div className="draft small" key={x.revision_id}><b>{x.instruction}</b><p>{x.result_text}</p></div>)}
  {review&&<><div className="chips"><span className="chip">Risk: {review.risk_level}</span><span className="chip">Checked version: {review.text_hash?.slice(0,10)}</span></div>{review.review_notes?.map((n:string,i:number)=><p className="small" key={i}>{n}</p>)}{review.annotations?.map((n:Obj,i:number)=><p className="small" key={i}>⚠ {n.term}: {n.note}</p>)}</>}
  </section><section className="panel"><h2>5 · Edit final block</h2><button className="outline" disabled={!selected||!!busy} onClick={()=>act('/export/final-pack',{session_id:session!.session_id})}>Prepare editable block</button>{block&&<><textarea style={{marginTop:9}} aria-label="Final text" value={edit} onChange={e=>setEdit(e.target.value)}/><button disabled={!!busy||edit===block.text||!edit.trim()} onClick={()=>act('/export/'+session!.session_id+'/editable-block',{label:block.label,text:edit},'Edit saved; review again')}>Save text</button></>}</section>
  <section className="panel"><h2>6 · Human approval</h2>{checks.map(k=><label className="check small" key={k}><input type="checkbox" checked={!!checklist[k]} onChange={e=>setChecklist(p=>({...p,[k]:e.target.checked}))}/> {k.replaceAll('_',' ')}</label>)}<button disabled={!selected||!!busy||!checks.every(k=>checklist[k])} onClick={()=>act('/sessions/'+session!.session_id+'/approval',{approval_state:'approved',checklist},'Approved exact draft version')}>Approve current text</button><p className="muted">Approval requires the latest guardrail result and all checks.</p></section>
  <section className="panel"><h2>7 · Export (no send)</h2><div className="row"><button className="outline" disabled={!block||!!busy} onClick={()=>download('markdown')}>Markdown</button><button className="outline" disabled={!block||!!busy} onClick={()=>download('email-ready')}>Email-ready</button><button className="outline" disabled={!block||!!busy} onClick={()=>run('Copying',async()=>{if(session?.approval_state!=='approved'&&session?.approval_state!=='exported')throw Error('Approve first');await navigator.clipboard.writeText(block.text);setSuccess('Copied')})}>Copy</button></div>{exportText&&<textarea readOnly value={exportText} style={{marginTop:10}}/>}</section>
 </div>
 </div></main>
}
