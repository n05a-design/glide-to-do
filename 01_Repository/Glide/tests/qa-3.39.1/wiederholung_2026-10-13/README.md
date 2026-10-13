# Wiederholungen – Nachweisrahmen

Stand 13.10.2026 · Glide 3.39.1 · Aufgabenformat 23

FP-00 behebt drei Befunde aus der [Wettbewerbs- und Codeanalyse](../../qa-3.39.0/wettbewerbsanalyse_2026-10-13/README.md) als Fehlerbehebung ohne Produktentscheidung (Plan §16, E-W7 A, D49):

- **A29 Schnelleingabe:** Ankertag und Wochentage gehören vollständig zur Regel; nicht Abbildbares bleibt vollständig Titel mit einem Hinweis ohne Wirkung.
- **A28 Kalenderaustausch:** Monats- und Jahresreihen ab dem 29. bzw. am 29.02. tragen die Klemmform `BYMONTHDAY=…;BYSETPOS=-1`; der Import lehnt RFC-Reihen mit anderer Terminfolge sichtbar ab.
- **A30 Zeitzonen im Aufgabenimport:** `TZID` über die mitgelieferten IANA-Daten, Windows-Namen über CLDR.

Aufgabenformat 23, Einstellungenformat 2 und alle gespeicherten Regeln bleiben unverändert.

Gezielte Proben vor dem Einfrieren:

- Pflichtsuite `test_wiederholung3391` grün; gegen die unveränderte 3.39.0 (Apphash 7995ecbc) rot am ersten Befund.
- [Getrennte Gegenprobe](gegenprobe.py): [3.39.0](gegenprobe_3390.json) zeigt A28, A29 und A30 einzeln als vorhanden, [3.39.1](gegenprobe_3391.json) alle drei als behoben. A30 ist auch ohne Systemzeitzonen (`PYTHONTZPATH=""`) behoben.
- 451 Unit-Tests grün, mit und ohne Systemzeitzonen; darunter 19 neue für `repeat_ics.py` und die Erfassung. Die Monatsreihen jedes Starttags werden mit `ics_recurrence` gegengerechnet.
- [Auslaufende QA-Nachweise 3.33.21](aufbewahrung33321.json): sechs Dateien bytegleich zum Commit, auf den der QA-Bericht nun verweist.

Die Mac-Vollprüfung auf eingefrorener Kopie, der Lieferabgleich, Bundle und Signaturen sowie die native Linux-/Windows-Matrix folgen.
Tatsächliche menschliche Bedienung bleibt ein gesondertes Abnahmetor.
