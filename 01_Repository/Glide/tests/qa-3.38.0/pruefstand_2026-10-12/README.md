# Windows-Layoutdiagnose 3.38.0

Stand 12.10.2026 · Glide 3.38.0 · Prüfwerkzeugnachlauf, keine Lieferfreigabe

Die native Matrix [38176254912](https://github.com/n05a-design/glide-to-do/actions/runs/38176254912)
prüfte Kandidat `2576e4e` mit App-SHA-256
`49ca48aad93d0be0ba9fce8dd0bd82e980e3eaa673ff549bdb3ba04614ebcf28`.
Linux scheiterte ausschließlich an der Auswahlzählung, Windows ausschließlich
an der Aufgaben-Pflichtsuite: erste Inhaltskante Liste 147 px statt höchstens
120 px bei 1280 × 800. Die übrigen 84 Windows-Suiten sind grün. Die zuvor
fehlerhafte Pinnwand-Feldklickprobe besteht jetzt; die anschließende
Flächenprobe erreicht erstmals ihren eigenen Befund.

Die Flächenprobe schreibt ihre unveränderten Messungen einschließlich
Widget-Wunschgrößen und tatsächlicher Tk-Skalierung nun vor der Assertion
in das lokale Protokoll. Keine Grenze oder Auswahlbedingung wird gelockert.
Der manuelle Workflow-Modus `aufgaben-layout` führt genau diese Pflichtprobe
auf dem nativen Windows-Prüfstand aus. Die Standardwahl `voll` und sämtliche
Push-/PR-Läufe behalten die vollständige native Matrix. Der Diagnosemodus
ersetzt keinen Volllauf und keine menschliche Abnahme.

Gezielter Windows-Diagnoselauf und vollständige Neuabnahme nach den
Produktionskorrekturen stehen noch aus. Rohprotokolle bleiben außerhalb
OneDrive und Git; die endgültigen Ergebnisse erhalten ihren eigenen Hashbeleg.

Die isolierte [CI-Grundstufe](ci-grundstufe.json) ist grün (bekannter lokaler
SSL-Hinweis beim Fremdcodeabruf); App und 07 sind dort bytegleich am
unveränderten Hash 49ca48aa. Der [Werkzeugbeleg](ergebnis.json) enthält die
SHA-256 der beiden geänderten Werkzeuge.

Erster [Diagnoselauf 38180748925](https://github.com/n05a-design/glide-to-do/actions/runs/38180748925)
scheiterte bereits beim Checkout am langen Grafikdateinamen. Keine
Layoutmessung und kein Artefakt entstanden. Der im Volljob vorhandene
Schritt `core.longpaths` ist jetzt auch im Diagnosejob vor dem Checkout
gesetzt; Kopfzeilen-Unterrahmen werden zusätzlich berichtet. Die
[erneute isolierte Grundstufe](ci_folge.json) ist grün;
[separater Nachlaufbeleg](nachlauf.json).
