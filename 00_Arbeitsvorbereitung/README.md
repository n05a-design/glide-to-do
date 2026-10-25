# Arbeitsvorbereitung

Stand 25.10.2026 · Glide 3.44.0 · Aufgabenformat 26

Planung, Übergabe und alles, was der Inhaber entscheidet oder von Hand prüft. Seit 03.10.2026 zusammengeführte Übergaben, Planungen, Auswahl- und Entscheidungsvorlagen, Recherchen und Checklisten; seit 08.10.2026 dazu die Analyse. Die Vorfassungen trägt Git. Das UI-/UX-Paket vom 15.10.2026 ist ein zusätzlicher ausführbarer Auftrag mit eigenen Eingangsbelegen, kein paralleles Backlog.

| Dokument | Wozu |
|---|---|
| [Übergabe](Glide_Uebergabe.md) | Einstieg für jede neue Sitzung: Stand, Orte, Regeln, Lehren, nächste Schritte |
| [Entwicklungsplan](Glide_Entwicklungsplan.md) | Alle Aufgaben mit Status (✅ erledigt, ◐ teilweise, ▶ beauftragt, ○ offen, ◇ Zukunft, ✕ bewusst nicht), Stufen, Ziele, offene Inhaberpunkte |
| [Analyse](Glide_Analyse.md) | Funktions-, Oberflächen-, Entscheidungs- und Nutzungsanalyse; Abgleich Dokumentation ↔ Code mit Befundliste |
| [Markt und Vorbilder](Glide_Markt_und_Vorbilder.md) | Vorbilder des Inhabers mit Belegstufe, Vergleichsfeld 2026 mit Stärke, Grenze und Bedeutung, vertiefte Featurematrix, Offline-/Portabilitätsmodelle, Szenarien; Primärquellen sowie fremde Implementierungsansätze mit Lizenzgrenzen |
| [Manuelle Prüfung](Glide_Manuelle_Pruefung.md) | Was nur am echten Gerät geht: Mac, Windows (mit Anleitung), Screenreader, Linux |
| [Feature-Paket UI/UX: Ausführungsprompt](Featurepaket_UI_UX/PROMPT.md) | A01–A03 und B01–B22 zur Beobachtung 3.42.0 vom 15.10.2026, 13:42 Uhr; Originalauftrag, 28 nummerierte lokale Screenshots und Abnahmekriterien; seit D50 vorrangig; B01–B20 als 3.43.0 geliefert; E-U1–E-U3 A seit D55 gewählt und als lokaler Kandidat umgesetzt (Status im Entwicklungsplan §17/§21.11) |

Zentrale Gestaltungsvorgaben: [Design Richtlinien](../01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md). Die Originalbilder im Feature-Paket enthalten teilweise Kontoangaben, bleiben lokal und müssen bei einer Agentenübergabe ausdrücklich mitgegeben werden.

**Gutachten 25.10.2026:** Das eingereichte Sicherheits- und Architekturgutachten ist in der [Analyse §13.12](Glide_Analyse.md#1312-sicherheits--und-architekturgutachten-vom-25102026) gegengeprüft und im [Plan §21.12](Glide_Entwicklungsplan.md#2112-technische-folge-aus-dem-sicherheits--und-architekturgutachten) als technische Folge eingeordnet; kein eigenes Gutachtendokument.

**Phasenabschluss 3.44.0 (22.10.2026):** Die lokal entwickelten Pakete seit 3.43.1 sind versioniert, eingefroren geprüft, nach `07_Python-Versionen` und in den Showcase geliefert und über einen Pull Request in `main` übernommen. Stand und nächste Schritte: [Übergabe](Glide_Uebergabe.md), [Plan §21.10](Glide_Entwicklungsplan.md#2110-phasenabschluss-3440), [Phasennachweis](../01_Repository/Glide/tests/qa-3.44.0/phasenabschluss_2026-10-22/README.md). Mac-Bundle, eigenständige Pakete 3.44.0 und menschliche Abnahmen bleiben offen.

Breite Neuuntersuchung 21.10.2026: [Analyse §13](Glide_Analyse.md#13-neuuntersuchung-vom-21102026), [Markt §12](Glide_Markt_und_Vorbilder.md#12-erweiterte-recherche-vom-21102026), zentrale [Roadmap §21](Glide_Entwicklungsplan.md#21-roadmap-abgleich-vom-21102026). Designgeltung und Pflege sind im Arbeitsablauf verankert; lokale Fakten und Vorschläge werden zusätzlich zweiwöchentlich aktualisiert. Der damalige einmalige Git-Auftrag vom 21.10. blieb nach roter Pflichtprüfung ohne Commit/Push beendet ([Nachweis](../01_Repository/Glide/tests/qa-3.43.1/gitauftrag_2026-10-21/README.md)); der ausdrückliche neue Auftrag vom 22.10. ist davon getrennt.

Die zusammengeführte [Bestandsaufnahme und der Dokumentabgleich](Glide_Analyse.md#137-konsolidierte-bestandsaufnahme-und-dokumentabgleich) vom 21.10. trennten damals den Format-26-Kandidaten, die Format-25-Python-Lieferung und Pakete 3.42.0; mit 3.44.0 tragen Quelle und Python-Lieferung wieder denselben Stand. Die [Übergabe](Glide_Uebergabe.md) ist der kompakte Einstieg mit Quellenhierarchie.

Entscheidungen D01–D55 (D49 als Auslegung mit Korrekturvorbehalt, D50 UI-/UX-Vorrang, D52–D54 Roadmap-/Design-/Pflegeauftrag, D55 Auswahl E-U1 A/E-U2 A/E-U3 A) und frühere gültige Antworten stehen im Quellbaum in der [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md); neue Produktentscheidungen beginnen bei D56. Technische und fachliche Dokumente stehen im [Dokumentationsindex](../01_Repository/Glide/docs/00_INDEX.md).

Analyseabschluss 18.10.2026: [tatsächlicher Stand](Glide_Analyse.md#9-gesamtanalyse-vom-18102026), [vollständiges Inventar](Glide_Entwicklungsplan.md#18-konsolidiertes-funktions--und-aufgabeninventar), [Paketplanung](Glide_Entwicklungsplan.md#19-paketgrenzen-ausbaustufen-und-aufwand), [Entscheidungen](Glide_Entwicklungsplan.md#20-vollständiges-entscheidungsregister). D51 und Kennungen aus dem getrennten Planungszweig sind konsolidiert. Eine erfolgreich geprüfte Python-Fassung ist noch kein signiertes Releasepaket.
