"""Actual mutation, complete snapshot/write/render, isolated native process."""
import sys,json,time,tempfile,hashlib,math,statistics,platform,resource
from pathlib import Path
repo=Path(sys.argv[1]).resolve();size=int(sys.argv[2]);output=Path(sys.argv[3]);sys.path.insert(0,str(repo/'tests/integration'))
from test_schutzrunde import Lauf

def stats(values):
 ordered=sorted(values)
 return {'median_ms':statistics.median(values),'p95_ms':ordered[math.ceil(.95*len(ordered))-1],'samples_ms':values}

with tempfile.TemporaryDirectory(prefix='glide-bench-') as directory:
 run=Lauf(repo/'src/glide/app.pyw',str(Path(directory)/'daten'))
 try:
  app=run.app;inbox=app.ensure_inbox_list();inbox['id']='perf-inbox';inbox['created_at']='2026-10-31T10:00:00';inbox['updated_at']='2026-10-31T10:00:00';inbox['items']=[]
  app.lists=[inbox];app.active_list_id=inbox['id'];app.items=inbox['items'];app.folders=[];app.labels=[];app.trash=[]
  for k in range(12):
   items=[app.new_item('Aufgabe '+str(i),item_id='point-'+str(i),description='Prüfbeschreibung '*8) for i in range(k,size,12)]
   for item in items:item['created_at']='2026-10-31T10:00:00'
   app.lists.append(app.new_list_object('Messliste '+str(k),items,list_id='list-'+str(k),created_at='2026-10-31T10:00:00'))
  assert app.save_items();app.update_sidebar_list();app.set_active_list('list-0');run.idle()
  output.with_suffix('.fixture.json').write_text(json.dumps(app.lists,sort_keys=True,ensure_ascii=False,indent=2))
  fixture=hashlib.sha256(json.dumps(app.lists,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
  measures={name:[] for name in ('snapshot','save','render')}
  for name,method in [('snapshot','snapshot_undo'),('save','save_items'),('render','refresh_tree')]:
   original=getattr(app,method)
   def timed(*a,_name=name,_original=original,**kw):
    start=time.perf_counter()
    try:return _original(*a,**kw)
    finally:measures[_name].append((time.perf_counter()-start)*1000)
   setattr(app,method,timed)
  samples=[];followups=[];phases={name:[] for name in measures}
  for n in range(11):
   previous={k:len(v) for k,v in measures.items()};value=(n%3)+1
   start=time.perf_counter();app.update_in_progress_item('point-0','importance',value);elapsed=(time.perf_counter()-start)*1000
   start=time.perf_counter();run.idle();after=(time.perf_counter()-start)*1000
   assert app.find_item_in_lists('point-0')[0]['importance']==value
   payload=json.loads(Path(run.mod.SAVE_FILE).read_text())
   stored=next(item for entry in payload['lists'] for item in entry['items'] if item['id']=='point-0')
   assert stored['importance']==value and not app.dirty and not run.errors
   if n>=2:
    samples.append(elapsed);followups.append(after)
    for key in measures:phases[key].append(sum(measures[key][previous[key]:]))
  result={'app_sha256':hashlib.sha256((repo/'src/glide/app.pyw').read_bytes()).hexdigest(),'fixture_sha256':fixture,'count':size,'lists':len(app.lists),'operation':'update_in_progress_item importance','warmups':2,'repetitions':9,'python':sys.version,'platform':platform.platform(),'tk':str(run.root.tk.call('package','provide','Tk')),'total':stats(samples),'tk_followup':stats(followups),'phases':{k:stats(v) for k,v in phases.items()},'max_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'limits':'One native Mac; synthetic flat tasks over 12 lists, no attachments; p95 over nine samples equals max. Phase times nested in total, not additive. No historical WA-41 cause proof.'}
  output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(size,result['total']['median_ms'],result['total']['p95_ms'],flush=True)
 finally:run.ende()
