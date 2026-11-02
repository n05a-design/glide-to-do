# Startseitenlayout – Glide 3.50.0, 02.11.2026

Bei der Gesamtvalidierung reproduzierter Linux-Hänger: Arbeitsmodifall `home_tagesnavigation`, schreibgeschützter Tageswechsel. Der normale Gesamtlauf erreicht 22 grüne Fälle und läuft in das unveränderte 900-s-Limit. Die gezielte native Diagnose reproduziert den Fehler auch im frischen Einzelprozess: [10.000 Geometrieereignisse](linux_layout_vorher.json), Karte/Rasterspalte zwischen 322 und 323 px.

Ursache: Die Umbruchbreite eines Labels verändert dessen natürliche Breitenanforderung. Das Raster verschiebt daraufhin die Spaltenbreite, das Configure-Ereignis ändert den Umbruch erneut. `update_idletasks` kommt nicht zum Ende. Kein reines Timeout-/Prüfplatzproblem.

Korrektur im lokalen `label`-Baustein von `ListApp._render_home`: Umbruchlabels fordern eine feste kleine Breite an und füllen ihre zugeteilte Fläche weiter horizontal. Der Umbruch beeinflusst damit nur die natürliche Höhe, nicht die erneut zu verteilende Breite. Nicht umbrechende Texte behalten ihre natürliche Breite; bestehende Aktionen, Retention und Responsivität bleiben erhalten.

[Stand und Ergebnisse](ergebnis.json); [gezielter nativer Mac-Fall](mac_tagesnavigation.json). Linux-Gegenprobe, neuer eingefrorener Gesamtstand und native Lieferung werden anhand tatsächlicher Ergebnisse ergänzt. Quellhash ist gegenüber den älteren UI-Paketbelegen geändert; diese werden nicht als neuer Liefernachweis ausgegeben. Keine Veränderung echter Nutzdaten, des Wiederanlaufschutzes, der Datenformate oder der Version.
