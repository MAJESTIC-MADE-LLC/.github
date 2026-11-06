from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import datetime,hashlib,json,os,subprocess,time
root=Path('/Users/bespin-starter/Documents/Majestic'); repo=root/'Majestic-Made-Hub'; out=root/'.archives/validation/native-hosting-deletion-2026-11-06/hub-final'
node=Path('/Users/bespin-starter/.nvm/versions/node/v26.13.0/bin'); env=os.environ.copy(); env['PATH']=str(node)+os.pathsep+env['PATH']
results=[]
def check(name,argv):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat(); t=time.monotonic(); log=out/(name+'.log')
 with log.open('wb') as f:r=subprocess.run(argv,cwd=repo,env=env,stdout=f,stderr=subprocess.STDOUT)
 item={'name':name,'argv':argv,'cwd':str(repo),'node':str(node/'node'),'startedUtc':start,'endedUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':round(time.monotonic()-t,3),'exitCode':r.returncode,'log':str(log),'logSha256':hashlib.sha256(log.read_bytes()).hexdigest()}
 print(json.dumps(item),flush=True);return item
with ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(lambda x:check(x,['/Users/bespin-starter/.nvm/versions/node/v26.13.0/bin/npm','run',x]),['lint','typecheck','test']))
if all(r['exitCode']==0 for r in results):results.append(check('build',[str(node/'npm'),'run','build']))
else:print('Build not run because prerequisite checks failed.',flush=True)
(out/'results.json').write_text(json.dumps({'nodeVersion':subprocess.check_output([str(node/'node'),'--version'],text=True).strip(),'baseCommit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),'checks':results},indent=2)+'\n')
raise SystemExit(0 if len(results)==4 and all(r['exitCode']==0 for r in results) else 1)
