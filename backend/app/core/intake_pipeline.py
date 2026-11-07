"""Source-backed text intake; never synthesize article or attachment text."""
from __future__ import annotations
import email, ipaddress, re, socket, subprocess
from email import policy
from html.parser import HTMLParser
from urllib.parse import urlsplit
import httpx
from fastapi import HTTPException

MAX_BYTES=2_000_000
class ExtractHTML(HTMLParser):
    def __init__(self): super().__init__();self.parts=[];self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','noscript'): self.skip+=1
        if tag in ('p','article','h1','h2','h3','li','br'): self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in ('script','style','noscript'):self.skip=max(0,self.skip-1)
        if tag in ('p','article','h1','h2','h3','li'):self.parts.append('\n')
    def handle_data(self,data):
        if not self.skip:self.parts.append(data)

def fetch_article(url):
    p=urlsplit(url)
    if p.scheme!='https' or not p.hostname or p.username or p.password or p.port not in (None,443):
        raise HTTPException(400,'Only public HTTPS URLs on port 443 are supported')
    try: addresses=socket.getaddrinfo(p.hostname,443,type=socket.SOCK_STREAM)
    except OSError: raise HTTPException(422,'URL hostname could not be resolved')
    if not addresses:raise HTTPException(422,'URL hostname could not be resolved')
    for item in addresses:
        ip=ipaddress.ip_address(item[4][0])
        if not ip.is_global:raise HTTPException(400,'Private or non-public destinations are blocked')
    ip=addresses[0][4][0]
    try:
        result=subprocess.run(['curl','-q','--fail','--silent','--show-error','--noproxy','*',
            '--proto','=https','--max-redirs','0','--max-time','12','--max-filesize',str(MAX_BYTES),
            '--resolve',f'{p.hostname}:443:{ip}',url],capture_output=True,timeout=15,check=False)
    except (OSError,subprocess.TimeoutExpired):
        raise HTTPException(502,'Article fetch failed')
    if result.returncode or not result.stdout or len(result.stdout)>MAX_BYTES:
        raise HTTPException(422,'Unable to fetch article text (redirects and oversized responses are blocked)')
    raw=result.stdout.decode('utf-8',errors='replace')
    if '<html' in raw[:2000].lower() or '<body' in raw[:2000].lower():
        parser=ExtractHTML();parser.feed(raw);raw=' '.join(''.join(parser.parts).split())
    if len(raw)<40:raise HTTPException(422,'Article has insufficient extractable content')
    return raw[:200000]

def parse_email(raw):
    if raw.lstrip().startswith(('From:','Subject:','MIME-Version:')):
        msg=email.message_from_string(raw,policy=policy.default)
        texts=[]
        for part in msg.walk():
            if part.get_content_type()=='text/plain' and part.get_content_disposition()!='attachment':
                try:texts.append(part.get_content())
                except Exception:pass
        body='\n'.join(texts).strip()
        if not body:
            html_parts=[]
            for part in msg.walk():
                if part.get_content_type()=='text/html' and part.get_content_disposition()!='attachment':
                    try:
                        parser=ExtractHTML();parser.feed(part.get_content())
                        html_parts.append(' '.join(''.join(parser.parts).split()))
                    except Exception: pass
            body='\n'.join(html_parts).strip() or raw
        return {'raw_text':body,'title':str(msg.get('subject') or ''),'sender_person':str(msg.get('from') or '')}
    return {'raw_text':raw}

def parse_uploaded(filename,data):
    if not data or len(data)>MAX_BYTES:raise HTTPException(413,'Upload must be nonempty and at most 2 MB')
    name=filename.lower()
    if name.endswith(('.txt','.md','.eml')):
        raw=data.decode('utf-8-sig',errors='replace')
        return parse_email(raw) if name.endswith('.eml') else {'raw_text':raw}
    if name.endswith('.pdf'):
        from io import BytesIO
        from pypdf import PdfReader
        try: raw='\n'.join(p.extract_text() or '' for p in PdfReader(BytesIO(data)).pages[:30])
        except Exception: raise HTTPException(422,'Could not extract text from PDF')
        if not raw.strip():raise HTTPException(422,'PDF has no extractable text; scanned PDFs require manual text')
        return {'raw_text':raw}
    raise HTTPException(415,'Only .txt, .md, .eml, and text-based .pdf files are supported')

def normalize_unified_intake(payload):
    mode=payload.get('intake_mode','paste')
    if mode=='paste':
        raw=(payload.get('raw_text') or '').strip()
        if not raw:raise HTTPException(422,'Source text required')
        cleaned=parse_email(raw) if payload.get('source_type')=='email' else {'raw_text':raw}
    elif mode=='url_fetch':
        cleaned={'raw_text':fetch_article(payload.get('url',''))}
    else:raise HTTPException(422,'Use the multipart upload endpoint to ingest a file')
    return {'source_type':payload.get('source_type','email'), 'title':payload.get('title') or cleaned.get('title') or 'Untitled source',
            'raw_text':cleaned['raw_text'],'sender_company':payload.get('sender_company',''),
            'sender_person':cleaned.get('sender_person',''), 'url':payload.get('url',''),
            'user_goal':payload.get('user_goal',''),'intake_mode':mode}

def gmail_placeholder(payload):
    return {'status':'not_connected','message':'Gmail ingestion is not connected. Paste or upload an email.'}
