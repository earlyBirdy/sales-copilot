from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
import logging,os,time
from app.api import routes_health,routes_intake,routes_sources,routes_drafts,routes_revisions,routes_guardrail,routes_safety,routes_templates,routes_sessions,routes_export
app=FastAPI(title='Sales Copilot',version='0.51.0')
origins=[x.strip() for x in os.getenv('SALES_COPILOT_CORS_ORIGINS','http://localhost:3000').split(',') if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_methods=['GET','POST'],allow_headers=['Content-Type','X-Request-ID'])
logger=logging.getLogger('sales_copilot');logging.basicConfig(level=logging.INFO)
@app.middleware('http')
async def trace(request:Request,call_next):
    rid=(request.headers.get('X-Request-ID') or uuid4().hex)[:100];start=time.monotonic()
    try:response=await call_next(request)
    except Exception:
        logger.exception('request_error id=%s path=%s',rid,request.url.path)
        raise
    response.headers['X-Request-ID']=rid
    logger.info('request_id=%s method=%s path=%s status=%s ms=%.1f',rid,request.method,request.url.path,response.status_code,(time.monotonic()-start)*1000)
    return response
for prefix,module in [('',routes_health),('/intake',routes_intake),('/sources',routes_sources),('/drafts',routes_drafts),('/drafts',routes_revisions),('/drafts',routes_guardrail),('/safety',routes_safety),('/templates',routes_templates),('/sessions',routes_sessions),('/export',routes_export)]:
    app.include_router(module.router,prefix=prefix)
