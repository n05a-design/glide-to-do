# Arbeitsvorbereitung

Stand 29.10.2026 · Glide 3.49.0 · Aufgabenformat 26

**Fortsetzung 29.10.2026:** Mutationsreste einschließlich „Liste leeren“ gezielt geschlossen (40 Appfälle grün); PC-01 AMD, PC-02 Intel und MacBook M2 mit getrennten Quell-/Prüfständen vergleichen. Erster M2-Lauf ausgewertet, drei gemeinsame Fehlerursachen korrigiert, WA-41A nur auf PC-02 ([Gerätevergleich](../01_Repository/Glide/tests/qa-3.49.0/geraetevergleich_2026-10-29/README.md)); native Mac-Abnahme offen. Letzte breite Intel-CI rot; Gesamtauftrag und Liefer-/Abnahmetore bleiben offen. [Aktueller Nachweis](../01_Repository/Glide/tests/qa-3.49.0/abschlussreste_2026-10-29/README.md).

Planung, Übergabe und alles, was der Inhaber entscheidet oder von Hand prüft. Seit 03.10.2026 zusammengeführte Übergaben, Planungen, Auswahl- und Entscheidungsvorlagen, Recherchen und Checklisten; seit 08.10.2026 dazu die Analyse. Die Vorfassungen trägt Git. Das UI-/UX-Paket vom 15.10.2026 ist ein zusätzlicher ausführbarer Auftrag mit eigenen Eingangsbelegen, kein paralleles Backlog.

**Aktuell 29.10.2026:** Quelle 3.49.0 als lokal committeter, nicht gepushter Prüfkandidat (`27a2b27`), Python/Showcase 3.47.0, native Pakete 3.45.0. [Abnahmeaudit](../01_Repository/Glide/tests/qa-3.49.0/abnahme_2026-10-28/README.md) und [lokaler Dokumentabgleich](../01_Repository/Glide/tests/qa-3.49.0/dokumentabgleich_2026-10-29/README.md): historischer Abnahmestand. [Fortsetzung](../01_Repository/Glide/tests/qa-3.49.0/abschlussreste_2026-10-29/README.md): A01-Pflichtfolge in 13 Bereichssuiten/136 Fällen grün; WA-09 lokal umgesetzt, fünf Appfälle und 21 Regressionen grün. Gesamtauftrag weiterhin offen. Einstieg [Übergabe](Glide_Uebergabe.md), aktueller Rest [Plan §21.30](Glide_Entwicklungsplan.md#2130-gesamtabschluss-begonnener-arbeiten). Die folgenden datierten Abschlüsse sind historisch.

| Dokument | Wozu |
|---|---|
| [Übergabe](Glide_Uebergabe.md) | Einstieg für jede neue Sitzung: Stand, Orte, Regeln, Lehren, nächste Schritte |
| [Entwicklungsplan](Glide_Entwicklungsplan.md) | Alle Aufgaben mit Status (✅ erledigt, ◐ teilweise, ▶ beauftragt, ○ offen, ◇ Zukunft, ✕ bewusst nicht), Stufen, Ziele, offene Inhaberpunkte |
| [Analyse](Glide_Analyse.md) | Funktions-, Oberflächen-, Entscheidungs- und Nutzungsanalyse; Abgleich Dokumentation ↔ Code mit Befundliste |
| [Markt und Vorbilder](Glide_Markt_und_Vorbilder.md) | Vorbilder des Inhabers mit Belegstufe, Vergleichsfeld 2026 mit Stärke, Grenze und Bedeutung, vertiefte Featurematrix, Offline-/Portabilitätsmodelle, Szenarien; Primärquellen sowie fremde Implementierungsansätze mit Lizenzgrenzen |
| [Manuelle Prüfung](Glide_Manuelle_Pruefung.md) | Was nur am echten Gerät geht: Mac, Windows (mit Anleitung), Screenreader, Linux |
| [Feature-Paket UI/UX: Ausführungsprompt](Featurepaket_UI_UX/PROMPT.md) | A01–A03 und B01–B22 zur Beobachtung 3.42.0 vom 15.10.2026, 13:42 Uhr; Originalauftrag, 28 nummerierte lokale Screenshots und Abnahmekriterien; seit D50 vorrangig; B01–B20 seit 3.43.0, E-U1–E-U3 A seit 3.45.0 geliefert; offene Abnahmen im Entwicklungsplan §17/§21.11 |

Zentrale Gestaltungsvorgaben: [Design Richtlinien](../01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md). Die Originalbilder im Feature-Paket enthalten teilweise Kontoangaben, bleiben lokal und müssen bei einer Agentenübergabe ausdrücklich mitgegeben werden.

**Gutachten 25.10.2026:** Das eingereichte Sicherheits- und Architekturgutachten ist in der [Analyse §13.12](Glide_Analyse.md#1312-sicherheits--und-architekturgutachten-vom-25102026) gegengeprüft und im [Plan §21.12](Glide_Entwicklungsplan.md#2112-technische-folge-aus-dem-sicherheits--und-architekturgutachten) als technische Folge eingeordnet; kein eigenes Gutachtendokument.

**Weitere lokale Fortsetzung 26.10.2026:** Verweisvorschau der gewählten Nebenansicht ergänzt; 29 Fachfälle und zwei neue Bedienfälle grün, breite native Restprüfung offen. [Plan §21.17](Glide_Entwicklungsplan.md#2117-verweise-in-der-nebenansicht-nachschlagen-wa-11).

**Lokale Fortsetzung 26.10.2026:** WA-12 „gibt andere frei“ im Tagesvorschlag umgesetzt, 14 Fachfälle und die erweiterte Tagespaketsuite grün. Quellkandidat auf 3.45.0, vorheriger Lieferabschluss unverändert; [Plan §21.16](Glide_Entwicklungsplan.md#2116-tagesvorschlag-aufgaben-die-andere-freigeben-wa-12).

**Lieferabschluss 3.45.0 (25.–26.10.2026):** Sicherungsübersicht, Vergleich, Anhangsrückfrage und Windows-Pfadkorrektur ergänzen D55 und Speicherstatus. Die Python-Fassung ist bytegleich geliefert; gezielter Nachlauf, Lieferprobe, Showcase und strenge CI-Grundstufe 19/19 sind grün. Eingefrorene Vollprüfung, nachfolgende Korrekturen und offene native Abnahmen sind getrennt dokumentiert. [Plan §21.15](Glide_Entwicklungsplan.md#2115-weiterentwicklung-zu-3450-sicherungen-und-anhänge), [Nachweis](../01_Repository/Glide/tests/qa-3.45.0/weiterentwicklung_2026-10-25/README.md). Historischer Abschluss 3.44.0 und seine offenen nativen Tore bleiben im Plan §21.10 und QA-Bericht dokumentiert.

Breite Neuuntersuchung 21.10.2026: [Analyse §13](Glide_Analyse.md#13-neuuntersuchung-vom-21102026), [Markt §12](Glide_Markt_und_Vorbilder.md#12-erweiterte-recherche-vom-21102026), zentrale [Roadmap §21](Glide_Entwicklungsplan.md#21-roadmap-abgleich-vom-21102026). Designgeltung und Pflege sind im Arbeitsablauf verankert; lokale Fakten und Vorschläge werden zusätzlich zweiwöchentlich aktualisiert. Der damalige einmalige Git-Auftrag vom 21.10. blieb nach roter Pflichtprüfung ohne Commit/Push beendet ([Nachweis](../01_Repository/Glide/tests/qa-3.43.1/gitauftrag_2026-10-21/README.md)); der ausdrückliche neue Auftrag vom 22.10. ist davon getrennt.

Die zusammengeführte [Bestandsaufnahme und der Dokumentabgleich](Glide_Analyse.md#137-konsolidierte-bestandsaufnahme-und-dokumentabgleich) vom 21.10. trennten damals den Format-26-Kandidaten, die Format-25-Python-Lieferung und Pakete 3.42.0; beim Abschluss 3.44.0 wurden Quelle und Python-Lieferung wieder angeglichen. Der heutige Abstand Quelle 3.49.0 / Python 3.47.0 / native Pakete 3.45.0 ist wegen WA-41 ausdrücklich offen. Die [Übergabe](Glide_Uebergabe.md) ist der kompakte Einstieg mit Quellenhierarchie.

Entscheidungen D01–D57 (D49 als Auslegung mit Korrekturvorbehalt, D50 UI-/UX-Vorrang, D52–D54 Roadmap-/Design-/Pflegeauftrag, D55 Auswahl E-U1 A/E-U2 A/E-U3 A, D56 Weiterentwicklung zu 3.45.0, D57 Tagessteuerung und Nebenansicht) und frühere gültige Antworten stehen im Quellbaum in der [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md); neue Produktentscheidungen beginnen bei D58. Technische und fachliche Dokumente stehen im [Dokumentationsindex](../01_Repository/Glide/docs/00_INDEX.md).

Analyseabschluss 18.10.2026: [tatsächlicher Stand](Glide_Analyse.md#9-gesamtanalyse-vom-18102026), [vollständiges Inventar](Glide_Entwicklungsplan.md#18-konsolidiertes-funktions--und-aufgabeninventar), [Paketplanung](Glide_Entwicklungsplan.md#19-paketgrenzen-ausbaustufen-und-aufwand), [Entscheidungen](Glide_Entwicklungsplan.md#20-vollständiges-entscheidungsregister). D51 und Kennungen aus dem getrennten Planungszweig sind konsolidiert. Eine erfolgreich geprüfte Python-Fassung ist noch kein signiertes Releasepaket.
