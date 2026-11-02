# Arbeitsmodi-Timeout: Diagnose erhalten – 02.11.2026

Der Linux-Volllauf am Code-/Belegstand `c81a769` stoppte nach 900 Sekunden in `test_arbeitsmodi`. Die bisherigen 108-Suiten-Folgen wurden korrekt gestoppt. Der Wächter hielt Teil-stdout/stderr lokal, der Adapter `pruefen.py` übernahm sie beim Timeout aber nicht in die hochgeladene Logablage; der Arbeitsmodi-Bericht entstand erst am Ende aller Fälle. Damit fehlte der zuletzt laufende Fall. Die Ursache des Linux-Hängers ist noch offen, keine Appreparatur behauptet.

`Prueflauf.prozess` sichert bei Zeitüberschreitung jetzt Teil-stdout/stderr auch im üblichen Suite-Log und zeigt dessen Ende in der Konsole. Die Arbeitsmodi-Suite schreibt atomar vor/nach jedem Fall und bei Setup/Test/Abbau, nennt START und Dauer und hält nach 120 Sekunden pro Fall wiederholte Python-Stacktraces fest. Das 900-Sekunden-Limit, Assertions und Folgestopp bleiben erhalten. Appquelle/Format/Version unverändert.

Zwei neue echte Prozess-/Adapterprüfungen: kontrolliert hängender Fakefall ohne Tk bewahrt START, Stacktrace, laufenden Fall und Folgestopp; zusätzlich Byteausgabe im ungeguardeten Adapter. Vor Korrektur beide rot wegen fehlendem Log, danach alle 18 Wächtertests grün. Echter Tk-Fall `werkzeugzeile` grün, Fortschritt endet mit `laufender_fall: null` und einer Dauer.

Eine zusätzliche, ausschließlich an den Diagnosebranch gebundene Linux-Workflowdatei reproduziert die gesamte Arbeitsmodi-Suite isoliert mit derselben Python-/Tk-Laufzeit; der normale vollständige Workflow bleibt unverändert. Das ist Diagnose, keine Gesamtabnahme. Die temporäre Workflowdatei gehört nicht in den späteren Produktbranch. [Gesamtauftrag](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2151-gesamtvalidierung-nach-claudes-ui-runde).
