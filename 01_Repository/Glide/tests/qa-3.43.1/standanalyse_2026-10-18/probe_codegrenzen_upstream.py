"""Variante von probe_codegrenzen.py fuer einen anderen Quellstand (Gegenpruefung 18.10.2026).
Unterschiede zur Vorlage, sonst unveraendert: (1) --label benennt den untersuchten Stand im Ergebnis;
(2) im Undo-Fall ersetzt ein Platzhalter sync_current_list_reference, weil FP-01 (9ec474b) den Undo-Weg
ueber undo_state fuehrt. Keine Produktionsaenderung und keine Behauptung einer vollstaendigen UI-Pruefung.
Aufruf: python -B probe_codegrenzen_upstream.py --source <app.pyw> --label <Commit:Pfad> --output <json>
"""
import argparse,contextlib,copy,hashlib,importlib.machinery,importlib.util,json,os
from pathlib import Path
import tempfile,types

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--source',required=True);parser.add_argument('--output',required=True);parser.add_argument('--label',default='01_Repository/Glide/src/glide/app.pyw');args=parser.parse_args()
 source=Path(args.source).resolve()
 with tempfile.TemporaryDirectory(prefix='glide-codeanalyse-probe-') as directory:
  os.environ['GLIDE_DATA_DIR']=str(Path(directory)/'data')
  loader=importlib.machinery.SourceFileLoader('glide_analysis_probe',str(source));spec=importlib.util.spec_from_loader(loader.name,loader);m=importlib.util.module_from_spec(spec);loader.exec_module(m)
  result={'date':'2026-10-18','source':args.label,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'tests':[],'limits':'Keine Tk-Instanz; kuenstlicher Bestand; gezielte Fehlerinjektionen. Kein Beleg fuer natuerliche Haeufigkeit oder vollstaendige UI-Abnahme.'}
  def fake_app(depth):
   a=m.ListApp.__new__(m.ListApp);a.settings={};a.lists=[{'id':'l','items':[{'id':'a','text':'A','children':[]},{'id':'b','text':'B','children':[]}]}];a.folders=[];a.labels=[];a.trash=[];a.active_list_id=None;a.active_folder_id=None;a.view_mode='list';a.undo_stack=[{'old':i}for i in range(depth)];a.flush_drawing_editor=lambda:None;a.dirty=False
   def restore(snapshot):
    a.lists=m.unpack_state(snapshot['lists'])
   a.apply_snapshot=restore
   return a
  for depth in (0,19,20):
   for wrapper in (False,True):
    a=fake_app(depth);reports=[];a.report_integrity_stop=lambda *args,**kwargs:reports.append([args,kwargs])
    a.settings_write_batch=contextlib.nullcontext;a.done_item_ids=lambda x:set();a.record_completions=lambda *args:None;a.feedback_for_changes=lambda *args:None;a.refresh_tree=lambda **kw:None;a._restore_item_selection=lambda *args:None;a.save_items=lambda **kw:True
    with a.guarded_structural_change('injizierter Verlust'):
     if wrapper:
      with a.item_change(())as change:
       a.lists[0]['items'].pop();change.mark()
     else:
      a.snapshot_undo();a.lists[0]['items'].pop()
    ids=a.data_item_ids();result['tests'].append({'name':'guard_stack_boundary','initial_depth':depth,'item_change_wrapper':wrapper,'remaining_ids':sorted(ids),'restored':ids=={'a','b'},'reports':reports,'final_depth':len(a.undo_stack)})
  a=m.ListApp.__new__(m.ListApp);a.settings={};a.lists=[{'id':'l','title':'Nachher','items':[]}];a.folders=[];a.labels=[];a.trash=[];a.dirty=False;a.active_list_id='l';a.active_folder_id=None;a.view_mode='list'
  snapshot={'sidebar_locations':{},'lists':m.PackedState([{'id':'l','title':'Vorher','items':[]}]),'folders':m.PackedState([]),'labels':m.PackedState([]),'trash':m.PackedState([]),'active_list_id':'l','active_folder_id':None,'view_mode':'list'}
  a.undo_stack=[snapshot];a.sync_current_list_reference=lambda:None;a.current_drawing_editor=lambda:None;a.flush_drawing_editor=lambda:None;a.snapshot_keeping_drawings=lambda x:x;a.settings_write_batch=contextlib.nullcontext;a.save_settings=lambda **kw:True;a.ensure_inbox_list=lambda:None;a.set_active_list=lambda identity,refresh=False:setattr(a,'active_list_id',identity);a.save_items=lambda **kw:False;a.update_sidebar_list=lambda:None;a.refresh_tree=lambda:None
  feedback=[];a.feedback=lambda *args:feedback.append(args)
  a.undo_last_change();result['tests'].append({'name':'undo_write_failure','remaining_undo_steps':len(a.undo_stack),'save_items_result':False,'in_memory_title':a.lists[0]['title'],'feedback':feedback,'production_apply_snapshot_used':True})
  a=m.ListApp.__new__(m.ListApp);a.settings={};a.lists=[];a.folders=[];a.labels=[];a.trash=[];a.view_mode='list';a.active_list_id=None;a.active_folder_id=None;a.remove_stale_temp_files=lambda:None;a.back_up_before_title_clipping=lambda:None;a.ensure_inbox_list=lambda:None;a.update_sidebar_list=lambda:None
  payload={'version':25,'folders':[],'lists':[{'id':'l','title':'Gueltige Daten','items':[{'id':'a','text':'A','children':[]}]}],'labels':[],'trash':[]}
  Path(m.SAVE_FILE).write_text(json.dumps(payload),encoding='utf8');original=Path(m.SAVE_FILE).read_bytes()
  a.set_active_list=lambda identity,refresh=False:setattr(a,'active_list_id',identity)
  a.refresh_tree=lambda:(_ for _ in ()).throw(m.tk.TclError('injizierter Darstellungsfehler'))
  a.start_with_empty_dataset=lambda:setattr(a,'lists',[])
  errors=[];a.show_error=lambda title,message:errors.append({'title':title,'misclassified_as_corrupt':'beschädigt oder ungültig' in message})
  a.load_items();result['tests'].append({'name':'load_ui_error','file_still_identical':Path(m.SAVE_FILE).read_bytes()==original,'in_memory_lists':a.lists,'read_only':getattr(a,'_data_read_only',False),'errors':errors,'backup_count':len(list(Path(m.BACKUP_DIR).glob('liste_unlesbar_*.json')))})
  for note,drawing in ((False,True),(True,False),(True,True)):
   a=m.ListApp.__new__(m.ListApp);a.rich_note_editor=types.SimpleNamespace(winfo_exists=lambda:True,flush=lambda:note);a.flush_drawing_editor=lambda:drawing
   value=a.flush_rich_note();result['tests'].append({'name':'flush_status','rich_note_ok':note,'drawing_ok':drawing,'returned':value,'caller_would_stop':value is False})
  raw={'settings_version':999,'future_top':{'keep':True},'saved_filters':[{'id':'future-filter','name':'Zukunft','future_condition':{'field':'x'}}]}
  normalized=m.ListApp.normalize_personal_settings(raw)
  result['tests'].append({'name':'settings_forward_gate','input_version':999,'output_version':normalized['settings_version'],'future_top_retained':normalized.get('future_top')==raw['future_top'],'future_filter_field_retained':'future_condition'in normalized['saved_filters'][0]})
  Path(args.output).write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
  print(json.dumps(result,indent=2,ensure_ascii=True))
if __name__=='__main__':main()
