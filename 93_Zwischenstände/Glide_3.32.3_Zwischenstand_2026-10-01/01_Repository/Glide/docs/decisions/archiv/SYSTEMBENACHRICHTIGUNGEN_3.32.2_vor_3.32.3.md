# Systembenachrichtigungen für Erinnerungen – Entscheidung

Stand: 30.09.2026 · Glide 3.32.2, Stufe B als Option umgesetzt (Tk 9, standardmäßig aus) · Ausgangspunkt: Glide 3.8.0, erste lokale Erinnerungsstufe.
Diese Entscheidung ist nach Regel 4 der [Arbeitsregeln](../../AGENTS.md) nötig,
bevor ein Hilfsprozess, ein Autostart oder eine neue Abhängigkeit entsteht.

## Die kurze Antwort

| Betriebszustand | Was Glide leisten kann | Voraussetzung |
|---|---|---|
| App läuft, Fenster sichtbar | Hinweis in der App – **vorhanden seit 3.8.0** | keine |
| App läuft, Fenster verdeckt oder minimiert | Aufmerksamkeit über Taskleiste/Dock und Statuszeile | Stufe A, reiner App-Code |
| App läuft, echte Systembenachrichtigung mit Glide-Namen | Mitteilungszentrale von macOS bzw. Windows | **Stufe B, setzt Paketierung voraus** |
| App beendet, abgemeldet, Ruhezustand, Gerät aus | keine Zustellung; verpasste Termine erscheinen gesammelt nach dem Start | bewusst nicht umgesetzt |

Der entscheidende Befund: **Eine Systembenachrichtigung, die als „Glide"
erscheint, ist kein Feature des Anwendungscodes, sondern eine Folge der
Paketierung.** Beide Zielplattformen verlangen dafür eine installierte,
beim Betriebssystem registrierte Anwendung. Das koppelt Stufe B an das
Installer- und Signierungsthema, das im [QA-Bericht](../07_QA_BERICHT.md)
ohnehin offen steht.

## Warum der naheliegende Weg nicht trägt

Der übliche Kurzweg wäre, aus Python heraus ein Systemwerkzeug aufzurufen.
Beide Varianten sind geprüft worden und scheiden für ein Produkt aus:

**macOS – `osascript -e 'display notification …'`.** Der Aufruf läuft als
nicht gebündelter Prozess. macOS ordnet die Mitteilung deshalb dem Script
Editor zu (`com.apple.ScriptEditor2`), nicht Glide. Das betrifft nicht nur
Symbol und Name, sondern auch den Eintrag in den Systemeinstellungen, die
Vorschau auf dem Sperrbildschirm und das Verhalten im Fokusmodus: Der Nutzer
müsste Benachrichtigungen für „Script Editor" erlauben, um Glide-Erinnerungen
zu sehen. Hinzu kommt, dass der Aufruf unter aktuellen macOS-Versionen ohne
Fehlermeldung und mit Rückgabewert 0 wirkungslos bleiben kann – ein stiller
Fehlschlag ist für eine Erinnerungsfunktion die schlechteste aller Varianten.

**Windows – Toast über PowerShell.** Eine Toast-Benachrichtigung wird vom
Betriebssystem stillschweigend verworfen, wenn die verwendete Anwendungs-ID
nicht als AppUserModelID registriert ist. Der kursierende Ausweg, die
vorinstallierte PowerShell-AUMID zu verwenden, erzeugt sichtbare
PowerShell-Benachrichtigungen – mit fremdem Namen und fremdem Symbol.

Beides verletzt dieselbe Produktregel: Die Oberfläche muss die tatsächlich
unterstützten Betriebszustände erklären. Eine Erinnerung, die unter fremdem
Namen erscheint oder stumm ausbleibt, tut das nicht.

## Was die Plattformen tatsächlich verlangen

**Windows.** Microsoft ist eindeutig: Ohne gültige Verknüpfung im Startmenü
kann eine Desktop-Anwendung keine Toast-Benachrichtigung auslösen. Die
Verknüpfung unter `%APPDATA%\Microsoft\Windows\Start Menu\Programs\` muss die
Eigenschaft `System.AppUserModel.ID` tragen; dieselbe ID verwendet die
Anwendung beim Senden. Eine Codesignierung verlangt Microsoft dafür nicht.
Empfohlen wird, die Verknüpfung im Installer anzulegen.

**macOS.** Nötig ist ein echtes `.app`-Bundle mit `Info.plist`,
Bundle-Identifikator und Symbol, aus dem heraus die Mitteilung gesendet wird
und das bei den Launch Services registriert ist. Für die Weitergabe an andere
kommt Signierung mit einer Developer-ID samt Notarisierung hinzu. Ob ein
lokal erzeugtes, unsigniertes Bundle für den Eigengebrauch zuverlässig
zustellt, ist offen und muss am Gerät geprüft werden.

## Entscheidung

### Stufe A – Aufmerksamkeit ohne Paketierung (umgesetzt am 12.09.2026)

Solange keine registrierte Anwendung existiert, erzeugt Glide keine
Systembenachrichtigung, sondern macht bei laufender App auf sich aufmerksam:

- Windows: `FlashWindowEx` aus `user32` über `ctypes`, mit `FLASHW_ALL |
  FLASHW_TIMERNOFG`. Das Blinken endet von selbst, sobald das Fenster nach
  vorn kommt, und bleibt aus, solange es bereits vorn ist. Das Fensterhandle
  wird über `GetParent` ermittelt – derselbe Weg, den die Rahmenfärbung
  bereits nutzt.
- macOS: `requestUserAttention:` mit `NSInformationalRequest` über
  `objc_msgSend`, geladen per `ctypes`. Das Dock-Symbol hüpft einmal; bei
  aktiver Anwendung passiert nichts. Je Aufrufform wird ein eigener
  typisierter Funktionszeiger erzeugt, statt globale `argtypes` zu ändern;
  ein `nil`-Empfänger ist in Objective-C gefahrlos. **Die tatsächliche
  Wirkung ist am Gerät zu bestätigen** – die Suite prüft nur, dass die
  Ermittlung nicht wirft.
- Beide: die bestehende Statuszeile nennt weiterhin die Zahl offener Hinweise.
- Der Anstoß erfolgt in `reminder_tick` nach `process_reminders`, also erst
  nach dauerhaft gespeichertem Zustellbeleg, und genau einmal je Prüflauf.
  `process_reminders` bleibt eine reine Datenoperation ohne Oberflächenwirkung.
- Abschaltbar über `reminder_attention` in den persönlichen Einstellungen,
  standardmäßig an. Das Fenster reißt sich den Fokus nicht ungefragt, weil das
  mitten in fremder Arbeit stört.

Der Schalter heißt nicht „Benachrichtigungen", sondern benennt, was er tut:
**Bei fälliger Erinnerung Taskleiste bzw. Dock hervorheben**. Die Grenze
bleibt in der Oberfläche sichtbar, wie sie es seit 3.8.0 ist.

### Stufe B – Echte Systembenachrichtigung (an Paketierung gekoppelt)

Wird erst umgesetzt, wenn es ein Windows-Installationspaket mit
Startmenü-Verknüpfung und ein macOS-`.app`-Bundle gibt. Dann gilt:

- eine feste AppUserModelID bzw. ein fester Bundle-Identifikator,
  abgestimmt mit [PRODUCT_IDENTITY](PRODUCT_IDENTITY.md);
- **eine** Sammelbenachrichtigung je Prüflauf, nicht eine je Aufgabe – die
  bestehende Sammelanzeige bleibt das Vorbild, 25 verpasste Hinweise ergeben
  einen Hinweis;
- Auslösung ausschließlich nach dauerhaft gespeichertem Zustellbeleg, also im
  bestehenden Pfad nach `process_reminders`; der Zustellvertrag aus
  [31_ERINNERUNGEN_3.8.0](../archiv/31_ERINNERUNGEN_3.8.0.md) bleibt unverändert;
- fehlende Systemberechtigung wird erkannt und in der Oberfläche benannt,
  statt stumm zu scheitern;
- keine Zustellung ist kein Datenverlust: Der Hinweis bleibt in der Übersicht
  offen, bis er bearbeitet oder bestätigt wird.

**Stand der Voraussetzungen (26.09.2026):**

- Die Kennungen sind festgelegt: `de.shaye.glide` für macOS, `Shaye.Glide`
  für Windows.
- Glide meldet sich unter Windows mit dieser Kennung an.
- `packaging/windows/verknuepfung_anlegen.ps1` legt die passende
  Startmenü-Verknüpfung an; unter Windows noch nicht geprüft.
- `packaging/macos/baue_app.py` baut ein Entwicklungsbundle, das macOS als
  „Glide“ mit dieser Kennung führt.

**Umsetzung am 27.09.2026** (Entscheidung des Nutzers, Vertrag 66,
Abschnitt 2.14):

- Tk 9 bringt `tk sysnotify` und `tk systray` mit – ohne Zusatzpaket, unter
  macOS über die Mitteilungszentrale, unter Windows über den Infobereich,
  unter Linux über libnotify mit Rückfall. Python 3.14 liefert Tk 9 auf
  macOS und Windows mit.
- Einstellung `system_notifications`, standardmäßig aus. Je Prüflauf eine
  Sammelmeldung, erst nach dem gespeicherten Zustellbeleg
  (`send_reminder_notification` nach `process_reminders`).
- Unter Windows verlangt Tk ein Symbol im Infobereich; es entsteht mit der
  ersten Mitteilung, ein Klick holt Glide nach vorn.
- Unter Tk 8.6 fehlt der Befehl; dann bleibt Stufe A, und die Probe
  („Systemmitteilung testen“) nennt den Grund.

Weiterhin offen (am Gerät):

- die Prüfung unter Windows;
- die Frage, ob ein ad-hoc-signiertes Bundle Mitteilungen unter dem Namen
  „Glide“ zustellt; aus Python gestartet erscheinen sie unter „Python“.

### Stufe C – Zustellung bei beendetem Programm (bewusst nicht)

Ein Hilfsprozess mit Autostart (launchd-Agent, Aufgabenplanung) wird **nicht**
eingeführt. Er verlangt einen zweiten Zugriff auf dieselbe Datenablage,
während OneDrive bereits als externe Synchronisation im Spiel ist; die
Fremdbelegungssperre der App ist für einen Nebenläufer nicht ausgelegt.
Der Nutzen – Hinweise bei geschlossener App – wiegt das Risiko für die
Datenintegrität nicht auf, die ausdrücklich Vorrang hat. Ein ausgeschaltetes
Gerät kann ohnehin nichts anzeigen. Diese Entscheidung wird neu bewertet,
wenn Datenablage und Sperre eine getrennte, nur lesende Terminquelle
anbieten – nicht vorher.

## Keine neue Laufzeitabhängigkeit

Weder Stufe A noch Stufe B verlangen ein zusätzliches Python-Paket.
Stufe A nutzt `ctypes` und Tk, beide bereits im Einsatz. Stufe B nutzt die
Paketierung und die dort vorhandenen Systemschnittstellen. Pakete wie
`pyobjc`, `win10toast` oder `plyer` werden nicht aufgenommen: Sie lösen das
eigentliche Problem – die fehlende Registrierung – nicht, und sie würden die
Regel brechen, dass Glide ohne Zusatzinstallation lauffähig bleibt.

## Auswirkung auf die Reihenfolge

Die [historischen Funktionsvorschläge](../../../../00_Arbeitsvorbereitung/Archiv/Glide_Funktionsvorschlaege_2026-09-16.md)
nennen Systembenachrichtigungen als nächsten Ausbauschritt. Nach diesem Befund
zerfällt der Schritt in einen kleinen Teil im Anwendungscode (Stufe A) und
einen, der am Installer hängt (Stufe B). Vorgeschlagen wird deshalb:

1. Stufe A umsetzen und nativ abnehmen – **umgesetzt am 12.09.2026**; die
   Sichtabnahme auf beiden Plattformen steht aus, für macOS insbesondere die
   tatsächliche Dock-Wirkung.
2. Reiteransicht – **umgesetzt in 3.10.0**; sie hing an
   keiner Paketierung.
3. Stufe B gemeinsam mit Installer und Signierung planen, nicht davor.

## Prüfkriterien

1. Eine fällige Erinnerung erzeugt bei verdecktem Fenster genau einen
   sichtbaren Anstoß, kein wiederholtes Blinken bei jedem Prüflauf.
2. Mehrere gleichzeitig fällige Hinweise erzeugen einen Anstoß, keine Kette.
3. Der Anstoß erfolgt erst nach gespeichertem Zustellbeleg; ein Speicherfehler
   erzeugt keinen Anstoß.
4. Abgeschaltet bedeutet abgeschaltet – auch nach Neustart.
5. Ein offener Bearbeitungsdialog wird nicht unterbrochen.
6. Kein Fokusdiebstahl während fremder Eingabe.
7. Die Oberfläche benennt weiterhin, dass bei beendetem Programm nichts
   zugestellt wird.

## Quellen

- [Enable desktop toast notifications through an AppUserModelID](https://learn.microsoft.com/en-us/windows/win32/shell/enable-desktop-toast-with-appusermodelid) – Microsoft Learn
- [Sending a toast notification from the desktop](https://learn.microsoft.com/en-us/windows/win32/shell/quickstart-sending-desktop-toast) – Microsoft Learn
- [Application User Model IDs](https://learn.microsoft.com/en-us/windows/win32/shell/appids) – Microsoft Learn
- [Displaying Notifications](https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/DisplayNotifications.html) – Apple, Mac Automation Scripting Guide
- Berichte zu stillem Fehlschlagen von `osascript`-Benachrichtigungen und zur
  Zuordnung an den Script Editor; Bericht zum stillen Verwerfen von Toasts
  ohne registrierte AUMID. Diese Punkte sind Erfahrungsberichte, keine
  Herstellerzusagen, und am Gerät zu bestätigen.
