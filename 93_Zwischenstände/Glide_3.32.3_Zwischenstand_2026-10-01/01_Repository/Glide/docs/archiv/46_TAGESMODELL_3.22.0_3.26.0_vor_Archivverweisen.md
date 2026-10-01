# Mein Tag – ein Tagesmodell statt zweier – Glide 3.22.0

Stand 17.09.2026 · Glide 3.22.0 · Aufgabenformat 16 · Einstellungen 2

Bis 3.21 beantworteten zwei Ansichten dieselbe Frage. „Mein Tag“ war eine
bewusste Auswahl von Punktkennungen in `settings.json`, die um Mitternacht
verfiel und in keinem Aufgabenbackup stand. Die „Tagesplanung“ rechnete
dagegen über das Feld `planned_date` am Punkt, ließ sich tageweise blättern
und verglich Aufwände mit der Tageskapazität. Wer beides benutzte, pflegte
zwei Listen für denselben Tag; wer nur eine benutzte, hatte an zwei Stellen
zu suchen.

3.22 führt beide zusammen. Es gibt genau eine Ansicht **Mein Tag**. Sie
arbeitet auf `planned_date`, hat eine Tagesnavigation und übernimmt alles,
was die Tagesplanung konnte.

## Was sich in der Bedienung ändert

- Die Seitenleiste zeigt eine Tageszeile statt zweier. Sie trägt das Symbol
  der früheren Tagesauswahl und zählt den gerade betrachteten Tag.
- „◀“ und „▶“ in der Filterzeile wechseln den Tag; das Ansichtsmenü führt
  dieselben Befehle als „Mein Tag: Tag zurück“ und „Mein Tag: Tag vor“.
- Das Kontextmenü einer Auswahl heißt weiterhin „Für Mein Tag einplanen“ und
  setzt jetzt den Bearbeitungstag auf **heute**. In der Tagesansicht gilt der
  betrachtete Tag.
- Der Titel lautet „Mein Tag · Mittwoch, 17.09.2026 · heute“.
- „Tag leeren“ nimmt allen Aufgaben des betrachteten Tages den
  Bearbeitungstag. Die Aufgaben selbst bleiben unverändert.

## Der Eingangsblock

Neu erfasste Aufgaben landen im Eingang und tragen noch keinen Tag. Damit sie
nicht unbemerkt liegen bleiben, steht am Ende derselben Ansicht ein Block
**„Eingang · n ohne Bearbeitungstag“** mit den offenen Punkten des Eingangs.
Ein Rechtsklick darauf bietet „Auf <Tag> einplanen“; die Statuszeile nennt die
Anzahl. Der Block zeigt höchstens fünfzig Punkte und weist auf weitere hin.
Er erscheint nur, wenn es etwas zu zeigen gibt.

## Daten und Migration

Die Tagesplanung steht am Punkt und damit in `liste_speicher.json`, in jedem
Aufgabenbackup und im Änderungsverlauf. Sie überlebt Mitternacht, einen
Neustart und einen Gerätewechsel.

Beim ersten Start von 3.22 wird eine noch gültige Auswahl aus 3.21 einmalig
übernommen: Jeder Punkt, der an diesem Kalendertag in `today_plan` stand und
noch keinen Bearbeitungstag trägt, bekommt den heutigen. Danach setzt Glide
`today_plan_migrated` und schreibt `today_plan` nicht mehr. Eine Auswahl von
gestern war schon in 3.21 verfallen und wird nicht wiederhergestellt.

Fälligkeit und Bearbeitungstag bleiben zwei verschiedene Angaben: Die
Fälligkeit sagt, bis wann etwas fertig sein muss, der Bearbeitungstag, wann
man es anfassen will. Eine Wiederholung leert beim Vorrücken weiterhin den
Bearbeitungstag, statt einen Folgetag zu erfinden.

## Grenzen

Mehrere Tageslisten nebeneinander, automatische Vorschläge, welche Aufgabe an
welchen Tag gehört, und eine Verschiebung des ganzen Tages per Zug bleiben
außen vor. Die Ansicht zeigt, was eingetragen ist; sie plant nicht selbst.

Die Regression steht in `tests/integration/test_features312.py`.

[Bearbeitungstag und Aufwand](37_PLANUNG_UND_AUFWAND_3.14.0.md) ·
[Tagesplanung und Kapazität 3.15.0](39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md) ·
[Datenvertrag](06_DATA_BACKUP_MIGRATION.md)
