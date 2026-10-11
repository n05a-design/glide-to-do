# Prüfstandnachlauf zur Aufgabenoberfläche

Stand 11.10.2026 · Glide 3.38.0 · Aufgabenformat 23

Die zweite [native Matrix](../aufgaben_2026-10-11/native-wiederholung.json)
am Kandidatcommit `e5eff6a` hat einen grünen Linux-Volllauf und einen roten
Windows-Volllauf. Zwei Prüfstandbefunde werden bei unverändertem Apphash
`49ca48aa…` behoben; die Mac-Vollprüfung bleibt der Nachweis ihres damaligen
eingefrorenen Werkzeugstands.

- Die Werkzeugleistenmutation erreichte zuvor ihre Layoutassertion nicht,
  weil eine frühere Auswahlprüfung scheiterte. Der unveränderte gemeinsame
  Ansichtswechsel mit seinen Layoutassertionen hat jetzt zusätzlich einen
  gezielten Einstieg `--werkzeugzeile`; der vollständige bisherige Ablauf
  bleibt erhalten. Vollständige und gezielte positive Mac-Probe grün,
  passende Werkzeugleistenmutation rot.
- Die Pinnwand-Klickprobe übersprang außerhalb des Ausschnitts liegende
  Felder und zählte unter Windows bei Spalten/75 Prozent keine Treffer.
  Sie navigiert jetzt mit dem bestehenden Kartenfokus, weist alle vier
  Feldtreffer vorab nach und scrollt jeden Treffer vor dem echten Klick
  erreichbar. Kein stilles Überspringen. Alle drei Pinnwandlayouts bei
  75/150 Prozent in der positiven Mac-Probe grün; entfernte Feldtreffer
  werden passend rot erkannt.

Der [Nachweis](ergebnis.json) enthält Werkzeughashes, positive Kontrollen,
beide Defektproben und die Grundstufe. App, 07 und Entwicklungsbundle sind
bytegleich zum Mac-geprüften Lieferkandidaten. Die erneute vollständige
native Matrix einschließlich 17 Linux-Defektfällen bleibt vor dem
Lieferabschluss Pflicht. Menschliche Sicht-/DPI-Abnahme bleibt getrennt.
