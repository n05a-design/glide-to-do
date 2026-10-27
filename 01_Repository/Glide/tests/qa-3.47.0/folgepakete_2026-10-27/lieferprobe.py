"""Bestehende echte Paketfälle gegen 07, mit expliziter Modul-/Versionsprüfung."""
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
DELIVERY=REPO.parents[1]/'07_Python-Versionen'
sys.path.insert(0,str(REPO/'tests/integration'))
import test_arbeitsmodi as suite


class DeliveryLauf(suite.Lauf):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        assert self.mod.APP_VERSION=='3.47.0'
        assert self.mod.ListApp.DATA_SCHEMA_VERSION==26
        for module in (self.mod.glide_task_tiles,self.mod.glide_side_view):
            assert Path(module.__file__).resolve().parent==DELIVERY.resolve(),module.__file__


suite.Lauf=DeliveryLauf
suite.FAELLE=('home_mehrfachplanung','side_history')
sys.argv=[str(REPO/'tests/integration/test_arbeitsmodi.py'),'--app',
          str(DELIVERY/'Glide-Aufgaben-und-Listen_v3.47.0.pyw'),'--report',str(HERE/'python_lieferprobe.json')]
raise SystemExit(suite.main())
