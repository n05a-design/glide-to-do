# SPDX-License-Identifier: MPL-2.0
"""KI-Arbeitsbereich: Prompts, Projekt- und Agentenprofile, Kontexte, Berichte, Dokumente (Teil 06).

Tk-frei. Ein Prompt ist eine gewöhnliche Glide-Seite (Titel, Freitext, Labels,
Ordner als Projekt, Archiv, Verweise und Suche kommen aus dem Aufgabenformat).
Diese Datei hält nur, was das Aufgabenformat nicht kennt, in der eigenen
Begleitdatei `ai_workspace.json` (Format `glide-ai-workspace` 1):

- `prompts[<Seiten-ID>]`: Modus, strukturierte Felder, eigene Felder,
  Gruppenreihenfolge, ausgeblendete Gruppen, Status, Agent, Vorlage,
  Kontextauswahl, Platzhalterwerte, Versionen (eingefrorene Fassungen),
  Beziehungen (Folge-, Korrektur-, Prüfauftrag, Bericht, Dokument).
- `projects[<Ordner-ID>]`: KI-Projektprofil mit versionierten Projektanweisungen.
- `agents`, `blocks` (Kontextbausteine), `packs` (Kontextpakete), `reports`.
- `documents`: Dokumentobjekte mit Versionen; jede Version zeigt auf eine
  verwaltete Datei unter `attachments/` (SHA-256, Größe, Originalname).

Grundsätze: keine Netzwerkzugriffe, keine Geheimnisse (Agentenprofile haben
kein Feld für Schlüssel), importierte Berichte sind Daten und werden nie als
Anweisung ausgeführt, eine Statusangabe behauptet keine externe Bearbeitung.
"""
from __future__ import annotations

import copy
import datetime as _dt
import difflib
import hashlib
import html
import io
import json
import math
import os
import re
import shutil
import uuid
import zipfile
import xml.etree.ElementTree as ET

import local_json_store

FORMAT = "glide-ai-workspace"
VERSION = 1
FILE_NAME = "ai_workspace.json"
JOURNAL_NAME = "ai_workspace.journal.json"
MAX_TEXT = 200_000
MAX_INDEX_TEXT = 200_000
MAX_VERSIONS = 100
MAX_FILE_BYTES = 64 * 1024 * 1024  # Versionen mit eingefrorenem Kontext; Komfortdateien bleiben bei 2 MB

# (Gruppe, deutscher Titel, englischer Titel, [(Feld, de, en)]). Reihenfolge = Ausgabereihenfolge.
FIELD_GROUPS = (
    ("basics", "Kurzfassung", "Essentials", (
        ("goal", "Ziel", "Goal"), ("task", "Aufgabe", "Task"), ("context", "Kontext", "Context"),
        ("result", "Gewünschtes Ergebnis", "Expected result"), ("output_format", "Ausgabeformat", "Output format"))),
    ("organisation", "Identifikation und Organisation", "Identification and organisation", (
        ("summary", "Kurzbeschreibung", "Summary"), ("category", "Kategorie", "Category"),
        ("version", "Version", "Version"), ("priority", "Priorität", "Priority"), ("date", "Datum", "Date"))),
    ("role", "Rolle und Verantwortung", "Role and responsibility", (
        ("agent_role", "Agentenrolle", "Agent role"), ("domain", "Fachgebiet", "Domain"),
        ("seniority", "Erfahrungsniveau", "Seniority"), ("responsibility", "Verantwortungsbereich", "Responsibility"),
        ("working_style", "Erwartete Arbeitsweise", "Working style"))),
    ("situation", "Ziel und Ausgangslage", "Goal and situation", (
        ("overall_goal", "Übergeordnetes Ziel", "Overall goal"), ("current_state", "Bisheriger Arbeitsstand", "Current state"),
        ("problem", "Problemstellung", "Problem"), ("motivation", "Motivation", "Motivation"),
        ("benefit", "Erwarteter Nutzen", "Expected benefit"), ("history", "Relevante Vorgeschichte", "History"))),
    ("technical", "Technischer Kontext", "Technical context", (
        ("repository", "Repository", "Repository"), ("branch", "Branch", "Branch"), ("commit", "Commit", "Commit"),
        ("directories", "Relevante Verzeichnisse", "Relevant directories"), ("files", "Betroffene Dateien", "Affected files"),
        ("language", "Programmiersprache", "Language"), ("frameworks", "Frameworks", "Frameworks"),
        ("architecture", "Architektur", "Architecture"), ("interfaces", "Schnittstellen", "Interfaces"),
        ("dependencies", "Abhängigkeiten", "Dependencies"), ("os", "Betriebssystem", "Operating system"),
        ("environment", "Entwicklungsumgebung", "Environment"), ("versions", "Versionsstände", "Versions"))),
    ("knowledge", "Wissens- und Dokumentenkontext", "Knowledge and documents", (
        ("sources", "Quellen und Referenzen", "Sources and references"), ("design_rules", "Designrichtlinien", "Design rules"),
        ("project_rules", "Projektanweisungen", "Project instructions"), ("decisions", "Entscheidungsregister", "Decisions"),
        ("previous", "Vorherige Aufträge und Berichte", "Previous briefs and reports"))),
    ("requirements", "Anforderungen", "Requirements", (
        ("functional", "Funktional", "Functional"), ("non_functional", "Nicht funktional", "Non-functional"),
        ("design", "Design", "Design"), ("architecture_req", "Architekturvorgaben", "Architecture"),
        ("data", "Daten", "Data"), ("security", "Sicherheit", "Security"), ("performance", "Performance", "Performance"),
        ("accessibility", "Barrierefreiheit", "Accessibility"), ("platform", "Plattformen", "Platforms"))),
    ("scope", "Umfang und Grenzen", "Scope and limits", (
        ("in_scope", "Im Umfang", "In scope"), ("out_of_scope", "Nicht im Umfang", "Out of scope"),
        ("allowed", "Erlaubte Änderungen", "Allowed changes"), ("forbidden", "Nicht erlaubte Änderungen", "Forbidden changes"),
        ("protected", "Zu schützende Funktionen", "Protected functions"), ("approvals", "Freigabepflichtige Entscheidungen", "Decisions needing approval"))),
    ("method", "Arbeitsweise", "Way of working", (
        ("approach", "Vorgehensweise", "Approach"), ("steps", "Arbeitsschritte", "Steps"),
        ("uncertainty", "Umgang mit Unsicherheit und Blockaden", "Uncertainty and blockers"),
        ("git", "Git-Regeln", "Git rules"), ("documentation", "Dokumentationsanforderungen", "Documentation"))),
    ("quality", "Qualitätssicherung", "Quality assurance", (
        ("tests", "Tests", "Tests"), ("regression", "Regressionstests", "Regression tests"),
        ("security_checks", "Sicherheitsprüfungen", "Security checks"), ("platform_checks", "Plattformprüfungen", "Platform checks"),
        ("acceptance", "Abnahmekriterien", "Acceptance criteria"), ("dod", "Definition of Done", "Definition of Done"))),
    ("handover", "Ergebnis und Übergabe", "Result and handover", (
        ("report_structure", "Berichtsstruktur", "Report structure"), ("artifacts", "Erwartete Artefakte", "Expected artefacts"),
        ("open_items", "Offene Aufgaben", "Open items"), ("next_agent", "Übergabe an weiteren Agenten", "Handover to next agent"),
        ("follow_up", "Nachfolgeauftrag", "Follow-up brief"))),
)
GROUP_KEYS = tuple(g[0] for g in FIELD_GROUPS)
SIMPLE_GROUPS = ("basics",)
STATUSES = ("draft", "prepared", "handed_over", "in_progress", "result_received", "in_review", "done", "blocked", "archived")
RELATION_KINDS = ("follow_up", "correction", "review", "report", "document", "agent", "task")
PLACEHOLDER = re.compile(r"\{\{\s*([A-Za-z0-9_.-]{1,40})\s*\}\}")
TEXT_SUFFIXES = (".txt", ".md", ".markdown", ".csv", ".json", ".py", ".js", ".ts", ".css", ".xml", ".yml", ".yaml",
                 ".toml", ".ini", ".log", ".svg", ".html", ".htm", ".rtf", ".docx")
PREVIEW_IMAGE_SUFFIXES = (".png", ".gif", ".jpg", ".jpeg", ".webp", ".bmp", ".svg")


# Mitgelieferte Prompt-Vorlagen: tatsächlich ausfüllbare Feldgruppen, Platzhalter in {{…}}.
# Der fachliche Ausbau der Vorlagenbibliothek folgt in Teil 10.
def _t(goal, task, result, extra=None, mode="advanced"):
    felder = {"basics": {"goal": goal, "task": task, "result": result, "output_format": "Markdown-Bericht"}}
    for gruppe, werte in (extra or {}).items():
        felder.setdefault(gruppe, {}).update(werte)
    return {"mode": mode, "fields": felder}


BUILTIN_TEMPLATES = {
    "software_task": ("Softwareentwicklungsauftrag", _t("{{ziel}} umsetzen", "Implementiere {{funktion}} im Repository {{repo}}.", "Umgesetzte Änderung mit Tests und Bericht",
                      {"technical": {"repository": "{{repo}}", "branch": "{{branch}}"}, "scope": {"in_scope": "", "out_of_scope": ""},
                       "quality": {"tests": "Unit- und Integrationstests", "dod": "Tests grün, Doku aktualisiert"}, "method": {"git": "Kein Push ohne Freigabe"}})),
    "bug_analysis": ("Fehleranalyse", _t("Ursache von {{fehler}} finden", "Reproduziere und analysiere {{fehler}}.", "Ursache, Belege, Korrekturvorschlag",
                     {"situation": {"problem": "{{fehlerbild}}"}, "quality": {"regression": "Regressionstest für den Fehler"}})),
    "regression_test": ("Regressionstest", _t("Bestehendes Verhalten absichern", "Prüfe {{bereich}} auf Regressionen.", "Prüfprotokoll mit Ergebnissen",
                        {"quality": {"regression": "{{suiten}}", "acceptance": "Alle Suiten grün"}})),
    "architecture_plan": ("Architekturplanung", _t("Architektur für {{vorhaben}} entwerfen", "Erarbeite Varianten mit Bewertung.", "Architekturentscheidung mit Begründung",
                          {"technical": {"architecture": "{{ist_architektur}}"}, "scope": {"approvals": "Grundsatzentscheidungen"}})),
    "refactoring": ("Architekturrefactoring", _t("Struktur von {{modul}} verbessern", "Refaktoriere ohne Verhaltensänderung.", "Refactoring mit unveränderten Tests",
                    {"scope": {"protected": "Bestehendes Verhalten"}, "quality": {"regression": "Vollständige Regression"}})),
    "uiux_revision": ("UI/UX-Überarbeitung", _t("{{ansicht}} verbessern", "Überarbeite Layout und Bedienung.", "Umgesetzte Gestaltung mit Sichtbelegen",
                      {"requirements": {"design": "Designrichtlinien einhalten", "accessibility": "Tastatur und Kontrast"}})),
    "design_brief": ("Designbrief", _t("Gestaltung für {{produkt}} festlegen", "Beschreibe Zielgruppe, Ton und Gestaltungsregeln.", "Designbrief", {}, "simple")),
    "design_system": ("Designsystem", _t("Designsystem für {{produkt}}", "Lege Tokens, Komponenten und Regeln fest.", "Designsystem-Dokument",
                      {"requirements": {"design": "{{marke}}"}})),
    "security_review": ("Sicherheitsprüfung", _t("Sicherheitsrisiken in {{bereich}} finden", "Prüfe Eingaben, Dateizugriffe, Abhängigkeiten.", "Befundliste nach Schweregrad",
                        {"requirements": {"security": "Keine Geheimnisse, keine Netzwerkzugriffe ohne Freigabe"}})),
    "data_migration": ("Datenmigration", _t("Daten von {{alt}} nach {{neu}} migrieren", "Plane und teste die Migration mit Vorsicherung.", "Migration mit Rückweg",
                       {"requirements": {"data": "Bytegenaue Vorsicherung, Rückweg"}, "quality": {"tests": "Rundlauf und Altfassung"}})),
    "code_review": ("Code-Review", _t("Änderung {{pr}} prüfen", "Prüfe Korrektheit, Lesbarkeit, Tests.", "Review mit Befunden", {})),
    "repo_audit": ("Repository-Audit", _t("Zustand von {{repo}} bewerten", "Prüfe Struktur, Tests, Doku, Abhängigkeiten.", "Auditbericht", {"technical": {"repository": "{{repo}}"}})),
    "docs_review": ("Dokumentationsprüfung", _t("Dokumentation von {{projekt}} prüfen", "Prüfe Vollständigkeit und Aktualität.", "Liste der Abweichungen", {})),
    "performance": ("Performance-Optimierung", _t("{{bereich}} beschleunigen", "Miss, finde Engpässe, optimiere.", "Messwerte vorher/nachher",
                    {"requirements": {"performance": "{{zielwert}}"}})),
    "release_prep": ("Release-Vorbereitung", _t("Release {{version}} vorbereiten", "Prüfe Versionen, Changelog, Pakete.", "Release-Checkliste", {"method": {"git": "Kein Tag ohne Freigabe"}})),
    "project_handover": ("Projektübergabe", _t("Projekt {{projekt}} übergeben", "Fasse Stand, Entscheidungen, Risiken zusammen.", "Übergabedokument",
                         {"handover": {"report_structure": "Stand · Entscheidungen · Offen · Risiken"}})),
    "agent_handover": ("Agentenübergabe", _t("Arbeit an {{agent}} übergeben", "Übergib Kontext und nächste Schritte.", "Übergabe-Prompt",
                       {"handover": {"next_agent": "{{agent}}"}})),
    "research": ("Recherche", _t("{{frage}} beantworten", "Recherchiere Quellen und fasse zusammen.", "Bericht mit Quellen", {}, "simple")),
    "knowledge": ("Wissensaufbereitung", _t("Wissen zu {{thema}} aufbereiten", "Strukturiere vorhandene Notizen.", "Gegliederte Wissensseite", {}, "simple")),
    "master_brief": ("Master-Arbeitsauftrag", _t("{{ziel}}", "Bearbeite Teil {{teil}} von {{gesamt}} vollständig.", "Abschlussbericht nach Gliederung",
                     {"organisation": {"version": "{{teil}}/{{gesamt}}"}, "scope": {"approvals": "Formate, Abhängigkeiten, Git"},
                      "method": {"git": "Keine Branches, Commits, Pushes ohne Freigabe"}, "quality": {"dod": "Alle Anforderungen belegt"},
                      "handover": {"follow_up": "Teil {{naechster}}"}})),
}


def now():
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def new_id():
    return uuid.uuid4().hex


def group_title(key, lang="de"):
    for g in FIELD_GROUPS:
        if g[0] == key:
            return g[1] if lang == "de" else g[2]
    return key


def field_label(group, key, lang="de"):
    for g in FIELD_GROUPS:
        if g[0] == group:
            for f in g[3]:
                if f[0] == key:
                    return f[1] if lang == "de" else f[2]
    return key


def _text(value, limit=MAX_TEXT):
    return value[:limit] if isinstance(value, str) else ""


def _id(value):
    return value if isinstance(value, str) and 0 < len(value) <= 100 else None


class Workspace:
    """Datenbestand des KI-Arbeitsbereichs; reine Datenoperationen, Speichern über `to_payload`."""

    def __init__(self, payload=None):
        p = payload if isinstance(payload, dict) else {}
        p = {k: (v if isinstance(v, dict) else {}) for k, v in p.items()}
        self.prompts = {k: self._prompt(v) for k, v in (p.get("prompts") or {}).items() if _id(k) and isinstance(v, dict)}
        self.projects = {k: self._project(v) for k, v in (p.get("projects") or {}).items() if _id(k) and isinstance(v, dict)}
        self.agents = {k: self._plain(v, ("name", "provider", "model", "areas", "output_format", "rules", "context_structure", "handover", "url"))
                       for k, v in (p.get("agents") or {}).items() if _id(k) and isinstance(v, dict)}
        self.blocks = {k: self._block(v) for k, v in (p.get("blocks") or {}).items() if _id(k) and isinstance(v, dict)}
        self.packs = {k: self._pack(v) for k, v in (p.get("packs") or {}).items() if _id(k) and isinstance(v, dict)}
        self.reports = {k: self._report(v) for k, v in (p.get("reports") or {}).items() if _id(k) and isinstance(v, dict)}
        self.documents = {k: self._document(v) for k, v in (p.get("documents") or {}).items() if _id(k) and isinstance(v, dict)}
        # Strukturierte Felder zu Glide-Vorlagen (Vorlagen-ID aus vorlagen.json); keine zweite Vorlagenverwaltung.
        self.prompt_templates = {k: {"fields": self._prompt(v).get("fields", {}), "custom": self._prompt(v).get("custom", []),
                                     "mode": self._prompt(v).get("mode")}
                                 for k, v in (p.get("prompt_templates") or {}).items() if _id(k) and isinstance(v, dict)}

    # --- Normalisierung -----------------------------------------------------
    @staticmethod
    def _plain(v, keys):
        out = {k: _text(v.get(k), 20_000) for k in keys}
        out["created"] = _text(v.get("created"), 40) or now()
        out["updated"] = _text(v.get("updated"), 40) or out["created"]
        return out

    def _prompt(self, v):
        felder = {}
        for g, werte in (v.get("fields") or {}).items():
            if g in GROUP_KEYS and isinstance(werte, dict):
                felder[g] = {k: _text(t) for k, t in werte.items() if isinstance(k, str) and isinstance(t, str) and t}
        eigene = [{"id": _id(c.get("id")) or new_id(), "group": _text(c.get("group"), 80) or "custom",
                   "label": _text(c.get("label"), 120), "value": _text(c.get("value"))}
                  for c in (v.get("custom") or []) if isinstance(c, dict) and _text(c.get("label"), 120)]
        reihenfolge = [g for g in (v.get("group_order") or []) if isinstance(g, str)]
        status = v.get("status") if v.get("status") in STATUSES else "draft"
        return {
            "mode": "advanced" if v.get("mode") == "advanced" else "simple",
            "fields": felder, "custom": eigene,
            "group_order": list(dict.fromkeys(reihenfolge + [g for g in GROUP_KEYS if g not in reihenfolge])),
            "hidden": [g for g in (v.get("hidden") or []) if isinstance(g, str)],
            "status": status, "agent": _id(v.get("agent")), "template": _text(v.get("template"), 120) or None,
            "context": [c for c in (v.get("context") or []) if isinstance(c, dict) and c.get("kind") in ("block", "pack", "doc", "ref", "instruction")
                        and _text(c.get("id"), 300)][:200],
            "placeholders": {k: _text(t, 2000) for k, t in (v.get("placeholders") or {}).items() if isinstance(k, str) and isinstance(t, str)},
            "versions": [x for x in (v.get("versions") or []) if isinstance(x, dict) and isinstance(x.get("markdown"), str)][-MAX_VERSIONS:],
            "relations": [r for r in (v.get("relations") or []) if isinstance(r, dict) and r.get("kind") in RELATION_KINDS and _text(r.get("target"), 300)],
            "created": _text(v.get("created"), 40) or now(), "updated": _text(v.get("updated"), 40) or now(),
        }

    def _project(self, v):
        anweisungen = []
        for a in v.get("instructions") or []:
            if isinstance(a, dict) and _text(a.get("title"), 200):
                anweisungen.append({"id": _id(a.get("id")) or new_id(), "title": _text(a.get("title"), 200),
                                    "text": _text(a.get("text")), "version": int(a.get("version") or 1),
                                    "history": [h for h in (a.get("history") or []) if isinstance(h, dict)][-MAX_VERSIONS:],
                                    "updated": _text(a.get("updated"), 40) or now()})
        out = self._plain(v, ("description", "goal", "repository", "local_path", "language", "stack", "architecture", "state",
                              "versions", "formats", "design_system", "docs_structure", "work_rules", "security_rules",
                              "git_rules", "test_procedure", "open_decisions", "risks"))
        out["instructions"] = anweisungen
        return out

    def _block(self, v):
        out = self._plain(v, ("title", "kind", "text", "project", "ref"))
        return out

    def _pack(self, v):
        out = self._plain(v, ("title", "description", "project"))
        out["items"] = [c for c in (v.get("items") or []) if isinstance(c, dict) and c.get("kind") in ("block", "doc", "ref", "instruction")][:200]
        out["revision"] = int(v.get("revision") or 1)
        return out

    def _report(self, v):
        out = self._plain(v, ("prompt", "title", "kind", "text", "source_name"))
        out["untrusted"] = True  # Importierte Berichte sind Daten, keine Anweisungen.
        return out

    def _document(self, v):
        out = self._plain(v, ("title", "description", "project", "category", "source"))
        out["labels"] = [x for x in (v.get("labels") or []) if isinstance(x, str)][:50]
        out["archived"] = bool(v.get("archived"))
        out["favorite"] = bool(v.get("favorite"))
        out["external_path"] = None  # externe Verknüpfungen sind kein verwalteter Anhang
        versionen = []
        for x in v.get("versions") or []:
            if isinstance(x, dict) and isinstance(x.get("storage"), str) and isinstance(x.get("sha256"), str):
                versionen.append({"id": _id(x.get("id")) or new_id(), "storage": x["storage"], "sha256": x["sha256"],
                                  "size": int(x.get("size") or 0), "name": _text(x.get("name"), 255),
                                  "created": _text(x.get("created"), 40) or now(), "note": _text(x.get("note"), 1000)})
        out["versions"] = versionen
        return out

    def to_payload(self):
        return {"format": FORMAT, "version": VERSION, "prompts": self.prompts, "projects": self.projects,
                "agents": self.agents, "blocks": self.blocks, "packs": self.packs, "reports": self.reports,
                "documents": self.documents, "prompt_templates": self.prompt_templates}

    # --- Prompts ------------------------------------------------------------
    def prompt(self, list_id, create=True):
        if list_id not in self.prompts and create:
            self.prompts[list_id] = self._prompt({})
        return self.prompts.get(list_id)

    def set_field(self, list_id, group, key, value):
        p = self.prompt(list_id)
        if group not in GROUP_KEYS:
            raise ValueError("unbekannte Feldgruppe")
        werte = p["fields"].setdefault(group, {})
        if value:
            werte[key] = _text(value)
        else:
            werte.pop(key, None)
        p["updated"] = now()

    def add_custom_field(self, list_id, label, group="custom", value=""):
        p = self.prompt(list_id)
        feld = {"id": new_id(), "group": group, "label": _text(label, 120), "value": _text(value)}
        if not feld["label"]:
            raise ValueError("Feldname fehlt")
        p["custom"].append(feld)
        if group not in p["group_order"]:
            p["group_order"].append(group)
        p["updated"] = now()
        return feld["id"]

    def set_status(self, list_id, status):
        if status not in STATUSES:
            raise ValueError("unbekannter Status")
        self.prompt(list_id)["status"] = status

    def relate(self, list_id, kind, target):
        if kind not in RELATION_KINDS:
            raise ValueError("unbekannte Beziehung")
        p = self.prompt(list_id)
        eintrag = {"kind": kind, "target": target, "created": now()}
        if not any(r["kind"] == kind and r["target"] == target for r in p["relations"]):
            p["relations"].append(eintrag)

    def predecessors(self, list_id):
        return [pid for pid, p in self.prompts.items()
                if any(r["kind"] in ("follow_up", "correction", "review") and r["target"] == list_id for r in p["relations"])]

    def chain(self, list_id, limit=50):
        """Vorgänger-/Nachfolgerkette (z. B. eine 13-teilige Serie), vom Anfang her."""
        anfang, gesehen = list_id, {list_id}
        while True:
            vor = [x for x in self.predecessors(anfang) if x not in gesehen]
            if not vor or len(gesehen) > limit:
                break
            anfang = vor[0]
            gesehen.add(anfang)
        kette, aktuell, gesehen = [anfang], anfang, {anfang}
        while len(kette) < limit:
            nach = [r["target"] for r in self.prompt(aktuell, create=False)["relations"]
                    if r["kind"] == "follow_up" and r["target"] not in gesehen] if aktuell in self.prompts else []
            if not nach:
                break
            aktuell = nach[0]
            gesehen.add(aktuell)
            kette.append(aktuell)
        return kette

    # --- Projekte, Anweisungen, Kontext -------------------------------------
    def project(self, folder_id, create=True):
        if folder_id not in self.projects and create:
            self.projects[folder_id] = self._project({})
        return self.projects.get(folder_id)

    def set_instruction(self, folder_id, title, text, instruction_id=None):
        """Neue oder geänderte Projektanweisung; der vorige Stand bleibt in `history`."""
        pr = self.project(folder_id)
        a = next((x for x in pr["instructions"] if x["id"] == instruction_id), None) if instruction_id else None
        if a is None:
            a = {"id": new_id(), "title": _text(title, 200), "text": _text(text), "version": 1, "history": [], "updated": now()}
            pr["instructions"].append(a)
        elif a["text"] != text or a["title"] != title:
            a["history"].append({"version": a["version"], "title": a["title"], "text": a["text"], "updated": a["updated"]})
            a.update(title=_text(title, 200), text=_text(text), version=a["version"] + 1, updated=now())
        return a["id"]

    def instruction(self, instruction_id, version=None):
        for folder_id, pr in self.projects.items():
            for a in pr["instructions"]:
                if a["id"] == instruction_id:
                    if version is None or version == a["version"]:
                        return a
                    return next((dict(h, id=a["id"]) for h in a["history"] if h.get("version") == version), None)
        return None

    def add_block(self, title, text="", kind="text", project=None, ref=None):
        bid = new_id()
        self.blocks[bid] = self._block({"title": title, "text": text, "kind": kind, "project": project or "", "ref": ref or ""})
        return bid

    def add_pack(self, title, items, project=None, description=""):
        pid = new_id()
        self.packs[pid] = self._pack({"title": title, "items": items, "project": project or "", "description": description})
        return pid

    def add_agent(self, name, **felder):
        aid = new_id()
        self.agents[aid] = self._plain(dict(felder, name=name), ("name", "provider", "model", "areas", "output_format", "rules",
                                                                  "context_structure", "handover", "url"))
        return aid

    def add_report(self, list_id, title, text, kind="report", source_name=""):
        rid = new_id()
        self.reports[rid] = self._report({"prompt": list_id, "title": title, "text": text, "kind": kind, "source_name": source_name})
        self.relate(list_id, "report", rid)
        return rid

    # --- Dokumente ------------------------------------------------------------
    def add_document(self, title, version, project=None, category="", source="import", description=""):
        did = new_id()
        d = self._document({"title": title, "project": project or "", "category": category, "source": source,
                            "description": description, "versions": [version]})
        self.documents[did] = d
        return did

    def add_document_version(self, doc_id, version):
        d = self.documents[doc_id]
        d["versions"].append(self._document({"versions": [version]})["versions"][0])
        d["updated"] = now()
        return d["versions"][-1]["id"]

    def find_by_sha(self, sha256):
        return [(did, v["id"]) for did, d in self.documents.items() for v in d["versions"] if v["sha256"] == sha256]

    def document_storages(self):
        return sorted({v["storage"] for d in self.documents.values() for v in d["versions"]})

    def document_usages(self, doc_id):
        """Wo ein Dokument verwendet wird: Prompts (Kontext, Beziehungen) und Pakete."""
        orte = []
        for pid, p in self.prompts.items():
            if any(c.get("kind") == "doc" and str(c.get("id")).split("@")[0] == doc_id for c in p["context"]) or \
                    any(r["kind"] == "document" and r["target"] == doc_id for r in p["relations"]):
                orte.append(("prompt", pid))
        for kid, k in self.packs.items():
            if any(c.get("kind") == "doc" and str(c.get("id")).split("@")[0] == doc_id for c in k["items"]):
                orte.append(("pack", kid))
        return orte

    # --- Zusammensetzen -------------------------------------------------------
    def context_items(self, list_id):
        p = self.prompt(list_id)
        items = []
        for c in p["context"]:
            if c["kind"] == "pack" and c["id"] in self.packs:
                items.extend(self.packs[c["id"]]["items"])
            else:
                items.append(c)
        return items

    def render(self, list_id, title, body, resolve=lambda item: (None, None), lang="de", frozen=None, exclude=()):
        """Prompt als Markdown. `resolve(item)` liefert (Überschrift, Text) für Seiten-/Dokumentverweise.

        Rückgabe (markdown, info) mit verwendeten Quellen, fehlenden Quellen und
        unaufgelösten Platzhaltern. `frozen` ersetzt Kontexttexte durch einen
        eingefrorenen Stand (historische Fassung).
        """
        p = self.prompt(list_id)
        teile = [f"# {title}".rstrip()]
        info = {"sources": [], "missing": [], "placeholders": [], "sections": []}
        sichtbar = [g for g in p["group_order"] if g not in p["hidden"] and (p["mode"] == "advanced" or g in SIMPLE_GROUPS)]
        if body.strip():
            teile.append(body.strip())
            info["sections"].append("body")
        for g in sichtbar:
            werte = p["fields"].get(g, {})
            eigene = [c for c in p["custom"] if c["group"] == g and c["value"].strip()]
            zeilen = []
            if g in GROUP_KEYS:
                for gruppe in FIELD_GROUPS:
                    if gruppe[0] == g:
                        for key, de, en in gruppe[3]:
                            if werte.get(key, "").strip():
                                zeilen.append(f"**{de if lang == 'de' else en}:** {werte[key].strip()}")
            zeilen += [f"**{c['label']}:** {c['value'].strip()}" for c in eigene]
            if zeilen:
                titel = group_title(g, lang) if g in GROUP_KEYS else g
                teile.append(f"## {titel}\n\n" + "\n\n".join(zeilen))
                info["sections"].append(g)
        kontext = []
        for item in self.context_items(list_id):
            schluessel = f"{item['kind']}:{item['id']}"
            if schluessel in exclude:
                info.setdefault("excluded", []).append(schluessel)
                continue
            if frozen is not None and schluessel in frozen:
                kopf, text = frozen[schluessel]
            elif item["kind"] == "block" and item["id"] in self.blocks:
                b = self.blocks[item["id"]]
                kopf, text = b["title"], b["text"]
            elif item["kind"] == "instruction":
                iid, _, ver = str(item["id"]).partition("@")
                a = self.instruction(iid, int(ver) if ver.isdigit() else None)
                kopf, text = (a["title"] + (f" (Stand {a['version']})" if a else ""), a["text"]) if a else (None, None)
            else:
                kopf, text = resolve(item)
            if text is None:
                info["missing"].append(schluessel)
                continue
            info["sources"].append((schluessel, kopf, text))
            kontext.append(f"### {kopf}\n\n> Übernommener Kontext ({item['kind']})\n\n{text.strip()}")
        if kontext:
            teile.append("## " + ("Kontext" if lang == "de" else "Context") + "\n\n" + "\n\n".join(kontext))
        md = "\n\n".join(teile) + "\n"

        def ersetzen(m):
            wert = p["placeholders"].get(m.group(1))
            if wert:
                return wert
            info["placeholders"].append(m.group(1))
            return m.group(0)
        md = PLACEHOLDER.sub(ersetzen, md)
        info["placeholders"] = sorted(set(info["placeholders"]))
        return md, info

    def freeze_sources(self, info):
        """Eingefrorene Kontexttexte für eine Version: spätere Änderungen wirken nicht zurück."""
        return {k: [kopf, text] for k, kopf, text in info["sources"]}

    def create_version(self, list_id, markdown, body, info, note=""):
        p = self.prompt(list_id)
        nummer = (p["versions"][-1]["number"] + 1) if p["versions"] else 1
        p["versions"].append({"number": nummer, "created": now(), "note": _text(note, 1000), "markdown": markdown,
                              "body": body, "fields": copy.deepcopy(p["fields"]), "custom": copy.deepcopy(p["custom"]),
                              "mode": p["mode"], "frozen": self.freeze_sources(info), "status": p["status"]})
        p["versions"] = p["versions"][-MAX_VERSIONS:]
        return nummer

    def version(self, list_id, number):
        return next((v for v in self.prompt(list_id)["versions"] if v["number"] == number), None)

    def restore_version(self, list_id, number):
        """Felder einer früheren Version zurückholen; die aktuelle Fassung wird vorher selbst Version."""
        v = self.version(list_id, number)
        if v is None:
            raise KeyError(number)
        p = self.prompt(list_id)
        p["fields"], p["custom"], p["mode"] = copy.deepcopy(v["fields"]), copy.deepcopy(v["custom"]), v["mode"]
        p["updated"] = now()
        return v["body"]

    @staticmethod
    def diff(a, b):
        return "\n".join(difflib.unified_diff(a.splitlines(), b.splitlines(), "älter", "neuer", lineterm=""))


# --- Kennzahlen und Hinweise ------------------------------------------------------
def budget(text):
    """Zeichen, Wörter und eine ausdrücklich geschätzte Tokenzahl (≈ Zeichen/4, kein Tokenizer)."""
    return {"chars": len(text), "words": len(text.split()), "tokens_estimate": math.ceil(len(text) / 4)}


SENSITIVE = (
    ("api_key", re.compile(r"\b(sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|xox[bpa]-[A-Za-z0-9-]{10,})")),
    ("secret_assignment", re.compile(r"(?i)\b(pass(word)?|passwort|secret|token|api[_-]?key)\s*[:=]\s*\S{6,}")),
    ("private_key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("private_path", re.compile(r"(?i)([A-Z]:\\Users\\[^\\\s]+|/Users/[^/\s]+|/home/[^/\s]+)")),
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
)


def sensitive_findings(text):
    """Hinweise auf möglicherweise sensible Inhalte – keine vollständige Geheimniserkennung."""
    funde = []
    for art, muster in SENSITIVE:
        for m in muster.finditer(text or ""):
            funde.append((art, m.group(0)[:60]))
            if len(funde) > 50:
                return funde
    return funde


# --- Dokumente: Dateien sicher ablegen, Text erschließen ------------------------------
def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for teil in iter(lambda: f.read(1 << 20), b""):
            h.update(teil)
    return h.hexdigest()


def safe_name(name):
    stamm, endung = os.path.splitext(os.path.basename(str(name or "datei")))
    stamm = re.sub(r"[^\w .()-]+", "_", stamm, flags=re.UNICODE).strip(" .")[:40] or "datei"
    endung = re.sub(r"[^A-Za-z0-9.]", "", endung)[:16]
    return f"{stamm}{endung}"


class Journal:
    """Wiederanlauf für Dateiablage plus Datensatz (keine gemeinsame atomare Transaktion möglich).

    Reihenfolge: (1) Vorgang mit Zielname ins Journal, (2) Datei als `.part`
    kopieren, fsync, Prüfsumme prüfen, (3) atomar auf den Zielnamen umbenennen,
    (4) Datensatz speichern, (5) Vorgang aus dem Journal löschen. Ein Abbruch
    hinterlässt höchstens eine `.part`-Datei (wird beim Wiederanlauf entfernt)
    oder eine fertige Datei ohne Datensatz (wird gemeldet und nie gelöscht).
    """

    def __init__(self, path):
        self.path = os.fspath(path)
        zustand = local_json_store.read(self.path, "glide-ai-journal", 1)
        self.ops = list((zustand.payload or {}).get("ops") or [])

    def _write(self):
        local_json_store.write_atomic(self.path, {"format": "glide-ai-journal", "version": 1, "ops": self.ops})

    def begin(self, op):
        self.ops.append(dict(op, started=now()))
        self._write()

    def finish(self, op_id):
        self.ops = [o for o in self.ops if o.get("id") != op_id]
        self._write()

    def recover(self, data_dir, known_storages):
        """Abgebrochene Vorgänge auflösen; Rückgabe: Liste von Befunden für die Anzeige."""
        befunde = []
        for op in list(self.ops):
            teil = os.path.join(data_dir, *str(op.get("part", "")).split("/")) if op.get("part") else None
            ziel = op.get("storage")
            if teil and os.path.isfile(teil):
                os.remove(teil)
                befunde.append(("removed_partial", op.get("part")))
            if ziel and ziel not in known_storages and os.path.isfile(os.path.join(data_dir, *ziel.split("/"))):
                befunde.append(("orphan_kept", ziel))
            self.ops.remove(op)
        if befunde or not self.ops:
            self._write()
        return befunde


def store_document_file(source, data_dir, journal, max_bytes=512 * 1024 * 1024, fail_after_copy=None):
    """Kopiert eine Datei in die verwaltete Ablage. Rückgabe: Versionsdatensatz (noch nicht aktiviert).

    `fail_after_copy` ist nur für Prüfstände: wird nach dem Kopieren aufgerufen.
    """
    groesse = os.path.getsize(source)
    if groesse > max_bytes:
        raise OSError("Datei zu groß für die verwaltete Ablage")
    frei = shutil.disk_usage(data_dir).free
    if frei < groesse + 64 * 1024 * 1024:
        raise OSError("Zu wenig freier Speicher für den Import")
    vid = new_id()
    name = safe_name(os.path.basename(source))
    storage = f"attachments/{vid}_{name}"
    part = f"attachments/.{vid}.part"
    os.makedirs(os.path.join(data_dir, "attachments"), exist_ok=True)
    journal.begin({"id": vid, "kind": "document_import", "storage": storage, "part": part})
    teil_pfad = os.path.join(data_dir, *part.split("/"))
    ziel_pfad = os.path.join(data_dir, *storage.split("/"))
    soll = sha256_file(source)
    with open(source, "rb") as quelle, open(teil_pfad, "xb") as ziel:
        shutil.copyfileobj(quelle, ziel, 1 << 20)
        ziel.flush()
        os.fsync(ziel.fileno())
    if fail_after_copy:
        fail_after_copy()
    if sha256_file(teil_pfad) != soll:
        os.remove(teil_pfad)
        journal.finish(vid)
        raise OSError("Prüfsumme nach dem Kopieren abweichend")
    if os.path.exists(ziel_pfad):
        os.remove(teil_pfad)
        journal.finish(vid)
        raise OSError("Zielname bereits belegt")
    os.replace(teil_pfad, ziel_pfad)
    return {"id": vid, "storage": storage, "sha256": soll, "size": groesse, "name": os.path.basename(source),
            "created": now(), "note": ""}


def extract_text(path, limit=MAX_INDEX_TEXT):
    """Text für die lokale Suche aus sicher unterstützten Formaten; sonst None.

    Ohne neue Abhängigkeiten: Text-/Quelldateien, Markdown, CSV, JSON, HTML,
    SVG, RTF (grob) und DOCX (ZIP + XML der Standardbibliothek). PDF braucht
    einen Parser und ist nicht unterstützt (Inhaberentscheidung).
    """
    endung = os.path.splitext(path)[1].lower()
    if endung not in TEXT_SUFFIXES:
        return None
    try:
        if endung == ".docx":
            with zipfile.ZipFile(path) as z:
                info = z.getinfo("word/document.xml")
                if info.file_size > 20 * 1024 * 1024:
                    return None
                roh = z.read(info)
                # Keine DTD: schließt Entity-Expansion und externe Entitäten aus,
                # ohne neue Abhängigkeit (defusedxml wäre freigabepflichtig).
                if b"<!DOCTYPE" in roh or b"<!ENTITY" in roh:
                    return None
                wurzel = ET.fromstring(roh)
            teile = [t.text or "" for t in wurzel.iter() if t.tag.endswith("}t")]
            return " ".join(teile)[:limit]
        with open(path, "rb") as f:
            roh = f.read(limit * 4)
        text = roh.decode("utf-8", errors="replace")
        if endung in (".html", ".htm", ".svg", ".xml"):
            text = html.unescape(re.sub(r"<[^>]+>", " ", text))
        elif endung == ".rtf":
            text = re.sub(r"\\[a-z]+-?\d* ?|[{}]", " ", text)
        return text[:limit]
    except (OSError, KeyError, zipfile.BadZipFile, ET.ParseError, ValueError):
        return None


class TextIndex:
    """Abgeleiteter Suchindex für Dokumentversionen; jederzeit neu erzeugbar, nie Primärdaten."""

    def __init__(self):
        self.texts = {}

    def rebuild(self, workspace, data_dir):
        neu = {}
        for did, d in workspace.documents.items():
            if not d["versions"]:
                continue
            v = d["versions"][-1]
            schluessel = (did, v["id"])
            if schluessel in self.texts:
                neu[schluessel] = self.texts[schluessel]
                continue
            neu[schluessel] = extract_text(os.path.join(data_dir, *v["storage"].split("/")))
        self.texts = neu
        return self

    def search(self, workspace, query, limit=50):
        q = (query or "").strip().casefold()
        if not q:
            return []
        treffer = []
        for did, d in workspace.documents.items():
            felder = " ".join([d["title"], d["description"], d["category"], " ".join(d["labels"]),
                               " ".join(v["name"] for v in d["versions"])]).casefold()
            text = next((t for (x, _v), t in self.texts.items() if x == did and t), "") or ""
            if q in felder:
                treffer.append((did, "meta"))
            elif q in text.casefold():
                treffer.append((did, "text"))
            if len(treffer) >= limit:
                break
        return treffer


# --- Export ------------------------------------------------------------------------
def build_package(target, prompt_markdown, files, metadata, not_included=()):
    """ZIP-Kontextpaket mit PROMPT.md, Dateien und Manifest (SHA-256); atomar geschrieben.

    `files`: [(Name im Paket, Quellpfad oder Bytes)]. `not_included` nennt
    referenzierte, aber bewusst nicht mitgelieferte Inhalte.
    """
    target = os.fspath(target)
    verzeichnis = os.path.dirname(os.path.abspath(target)) or "."
    bedarf = len(prompt_markdown.encode("utf-8")) + sum(len(q) if isinstance(q, bytes) else os.path.getsize(q) for _n, q in files)
    if shutil.disk_usage(verzeichnis).free < bedarf + 16 * 1024 * 1024:
        raise OSError("Zu wenig freier Speicher für das Paket")
    eintraege = [("PROMPT.md", prompt_markdown.encode("utf-8"))] + list(files)
    namen = set()
    manifest = {"format": "glide-context-package", "version": 1, "created": now(), **metadata, "files": [],
                "not_included": list(not_included)}
    temp = f"{target}.{os.getpid()}.tmp"
    try:
        with zipfile.ZipFile(temp, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for name, quelle in eintraege:
                name = name.replace("\\", "/").lstrip("/")
                if ".." in name.split("/") or name in namen:
                    raise ValueError(f"unzulässiger Paketname: {name}")
                namen.add(name)
                daten = quelle if isinstance(quelle, bytes) else open(quelle, "rb").read()
                z.writestr(name, daten)
                manifest["files"].append({"path": name, "size": len(daten), "sha256": hashlib.sha256(daten).hexdigest()})
            z.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        with zipfile.ZipFile(temp) as pruef:
            if pruef.testzip() is not None:
                raise OSError("Paket beschädigt")
        os.replace(temp, target)
    finally:
        if os.path.exists(temp):
            os.remove(temp)
    return manifest


def consistency(workspace, page_ids, trash_page_ids=()):
    """Bezüge zwischen Begleitdatei und Aufgabenformat prüfen; ändert nichts.

    Prompt-Daten zu einer Seite im Papierkorb gelten als ruhend (kehren mit der
    Seite zurück); ohne Seite und ohne Papierkorbeintrag als verwaist.
    """
    befunde = {"orphan_prompts": [], "dormant_prompts": [], "missing_documents": [], "missing_relations": []}
    seiten, papierkorb = set(page_ids), set(trash_page_ids)
    for pid, p in workspace.prompts.items():
        if pid in papierkorb:
            befunde["dormant_prompts"].append(pid)
        elif pid not in seiten:
            befunde["orphan_prompts"].append(pid)
        for c in p["context"]:
            if c.get("kind") == "doc" and str(c.get("id")).split("@")[0] not in workspace.documents:
                befunde["missing_documents"].append((pid, c["id"]))
        for r in p["relations"]:
            if r["kind"] == "document" and r["target"] not in workspace.documents:
                befunde["missing_documents"].append((pid, r["target"]))
            if r["kind"] in ("follow_up", "correction", "review") and r["target"] not in seiten | papierkorb:
                befunde["missing_relations"].append((pid, r["target"]))
    return befunde


def load(path):
    """Primärdaten: unlesbare oder neuere Datei bleibt unverändert, Schreiben gesperrt."""
    zustand = local_json_store.read(path, FORMAT, VERSION, max_bytes=MAX_FILE_BYTES, quarantine=False)
    return Workspace(zustand.payload), zustand


def save(path, workspace):
    local_json_store.write_atomic(path, workspace.to_payload())
