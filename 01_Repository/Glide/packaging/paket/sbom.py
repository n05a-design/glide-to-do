# SPDX-License-Identifier: MPL-2.0
"""CycloneDX-1.6-Inventar aus dem geprüften Lizenz-/Baubestand, ohne Zusatzpaket.

Scope: pre-build, Komponenten und Original-Lizenzbelege einschließlich Bauhilfen.
Kein behaupteter vollständiger Laufzeit-Abhängigkeitsgraph; aggregate=incomplete.
Dateihashes beziehen sich ausdrücklich auf Lizenzbelege, nicht auf Bibliotheken.
Spezifikation: https://cyclonedx.org/docs/1.6/json/
"""
import copy
import json
import re
from urllib.parse import quote


def make_bom(records, runtime):
    if not isinstance(records, list) or not records:
        raise ValueError("Leeres Komponentenverzeichnis")
    components, names = [], set()
    for record in records:
        name, version = record.get('name'), record.get('version')
        if not isinstance(name, str) or not name.strip() or name in names:
            raise ValueError("Fehlender oder doppelter Komponentenname")
        if not isinstance(version, str) or not version.strip():
            raise ValueError("Fehlende Komponentenversion: " + name)
        names.add(name)
        files = record.get('files')
        if not isinstance(files, dict) or not files:
            raise ValueError("Fehlende Lizenzbelege: " + name)
        for path, digest in files.items():
            if (not isinstance(path, str) or not path or path.startswith('/') or '\\' in path
                    or ':' in path or '..' in path.split('/')
                    or not isinstance(digest, str) or not re.fullmatch('[0-9a-f]{64}', digest)):
                raise ValueError("Ungültiger Lizenzbeleg: " + name)
        source = record.get('source')
        if not isinstance(source, str) or not source.strip():
            raise ValueError("Fehlende Komponentenherkunft: " + name)
        # Nur explizit bekannte IDs verwenden; fremde Bedingungen nicht erraten.
        license_id = record.get('license')
        if license_id is not None and license_id != 'MPL-2.0':
            raise ValueError("Nicht belegte SPDX-Lizenz-ID: " + name)
        licensing = {'id': license_id} if license_id else {'name': 'Originalbedingungen: ' + ', '.join(sorted(files))}
        components.append(dict(type='application' if name == 'Glide' else 'library',
            **{'bom-ref': 'component:' + quote(name, safe='')}, name=name, version=version,
            licenses=[{'license': licensing}], properties=[
                {'name': 'glide:source-evidence', 'value': source},
                {'name': 'glide:license-evidence-sha256', 'value': json.dumps(files, sort_keys=True, ensure_ascii=False)}]))
    main = [component for component in components if component['name'] == 'Glide']
    if len(main) != 1:
        raise ValueError("Genau ein Glide-Hauptbestand erforderlich")
    if not isinstance(runtime, dict) or not runtime:
        raise ValueError("Tatsächliche Baulaufzeit fehlt")
    return dict(bomFormat='CycloneDX', specVersion='1.6', version=1,
        metadata=dict(lifecycles=[{'phase': 'pre-build'}], component=main[0], properties=[
            {'name': 'glide:build-runtime', 'value': json.dumps(runtime, sort_keys=True, ensure_ascii=False)},
            {'name': 'glide:inventory-scope', 'value': 'Geprüfter Lizenz-/Baubestand; kein vollständiger transitiver Laufzeitgraph'}]),
        components=sorted([component for component in components if component['name'] != 'Glide'], key=lambda c: c['name']),
        compositions=[{'aggregate': 'incomplete'}])


def validate_bom(document, records, runtime):
    """BOM und eingefrorenen Ursprungsbestand vollständig abgleichen.

    Das ist eine Bestands-/Konsistenzprüfung, kein allgemeiner JSON-Schemavalidator.
    Die vollständige Schemaprobe wird zusätzlich im datierten QA-Beleg geführt.
    """
    if document != make_bom(records, runtime):
        raise ValueError("CycloneDX-Inventar stimmt nicht mit Lizenz-/Baubestand überein")
    return copy.deepcopy(document)
