# Glide user guide (English)

Status as of 24.11.2026 · Glide 1.0.3 · Task format 27

<p align="right"><a href="../20_FUNKTIONEN.md">Deutsch</a></p>

This guide explains how to use Glide 1.0.2 in English. It is a **controlled translation** of the German function reference [`20_FUNKTIONEN.md`](../20_FUNKTIONEN.md). It is not a second source of truth. The German text sets the product behavior. If the two ever differ, the German text applies, and the English page is corrected to match. The guide describes only features that exist in the 1.0.2 source baseline. It leaves out internal test, delivery and audit details, which stay in the German source and the [QA report](../07_QA_BERICHT.md).

## Contents

| # | Page | German source |
|---|---|---|
| 1 | [Getting started](01-getting-started.md) | [§1 Grundbegriffe](../20_FUNKTIONEN.md#1-grundbegriffe), [§2 Seitenleiste](../20_FUNKTIONEN.md#2-seitenleiste-und-navigation), [§7 Startseite](../20_FUNKTIONEN.md#7-startseite) |
| 2 | [Installation](02-installation.md) | [Eigenständiger Start](../20_FUNKTIONEN.md#eigenständiger-start-3450), [§13 Bekannte Grenzen](../20_FUNKTIONEN.md#13-bekannte-grenzen) |
| 3 | [Tasks and lists](03-tasks-and-lists.md) | [§3 Erfassen](../20_FUNKTIONEN.md#3-erfassen), [§5 Liste, Tabelle, Gruppierung](../20_FUNKTIONEN.md#5-liste-tabelle-gruppierung) |
| 4 | [Day planning](04-day-planning.md) | [§4 Heute, Demnächst und Planung](../20_FUNKTIONEN.md#4-heute-demnächst-und-planung) |
| 5 | [Calendar](05-calendar.md) | [§4 Tagespaket und Kalender](../20_FUNKTIONEN.md#tagespaket-33314-au01-au03-g05au05-h-02), [Tagesplanung 3.39.0](../20_FUNKTIONEN.md#tagesplanung-3390) |
| 6 | [Pages and notes](06-pages-and-notes.md) | [§8 Seiten, Notizen, Notizbuch, Galerie](../20_FUNKTIONEN.md#8-seiten-notizen-notizbuch-galerie) |
| 7 | [Pinboards](07-pinboards.md) | [§6 Pinnwand](../20_FUNKTIONEN.md#6-pinnwand) |
| 8 | [Pixel workshop](08-pixel-workshop.md) | [§9 Pixel-Werkstatt](../20_FUNKTIONEN.md#9-pixel-werkstatt) |
| 9 | [Import and export](09-import-and-export.md) | [§11 Import, Ausgabe und Austausch](../20_FUNKTIONEN.md#11-import-ausgabe-und-austausch) |
| 10 | [Backups](10-backups.md) | [Sicherungsübersicht](../20_FUNKTIONEN.md#sicherungsübersicht-und-anhangsrückfrage-3450), [Daten und Migration](../06_DATA_BACKUP_MIGRATION.md) |
| 11 | [Keyboard shortcuts](11-keyboard-shortcuts.md) | Shortcuts named across [`20_FUNKTIONEN.md`](../20_FUNKTIONEN.md) |
| 12 | [Troubleshooting](12-troubleshooting.md) | [Speicherstatus](../20_FUNKTIONEN.md#speicherstatus-und-sicherungsreserve-wa-40wa-47-seit-3450-geliefert), [§13 Bekannte Grenzen](../20_FUNKTIONEN.md#13-bekannte-grenzen) |

## Interface language

Glide 1.0.2 offers German and English. Choose **Settings › Appearance & Controls › Language** (*Einstellungen › Darstellung und Bedienung › Sprache*): *Automatic (System)*, *Deutsch* or *English*. The automatic setting uses English when the operating system reports an English locale and German otherwise. Your saved settings and data do not change when you switch the language.

**The whole interface is available in English** (D93, since Glide 1.0.0): menus, views, dialogs, messages, the built-in manual and the keyboard shortcut overview, the AI format description, the built-in templates and the default titles of new lists, pages and drawings. TXT and CSV exports use the chosen language, and Glide reads exports in either language. Quick capture understands English and German date and repeat words (for example `tomorrow`, `every week`, `morgen`, `jede Woche`). Only the names you gave your own content stay as you wrote them. Date formats and system dialogs follow your operating system. After switching the language in Settings, some fixed bars of the main window change after the next start; Glide says so when you switch. Please report missing or wrong translations with the [localization issue form](https://github.com/n05a-design/glide-to-do/issues/new?template=lokalisierung.yml).

**How this guide names controls:** labels in **bold** are what the English interface shows. Quick-capture words are given in `code` style.

## Keeping the guide in sync

- The German [function reference](../20_FUNKTIONEN.md) is changed first. Every user-visible change there is checked against the matching English page in the same change; see the [maintenance matrix](../DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge).
- Each English page links to its German source section. The tool test `test_standpruefung.py` checks that these links and their section anchors resolve, that the German reference links back here and that all twelve pages are listed.
- This guide is not published as a GitHub wiki (owner decision I11 B).
