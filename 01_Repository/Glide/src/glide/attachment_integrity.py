# SPDX-License-Identifier: MPL-2.0
"""Anhangsintegrität eines Arbeitsbereichs prüfen, ohne Tk und ohne Änderung (DS-08, Teil 05B).

Glide verwaltet Anhänge als Kopien unter `attachments/` im Datenordner; ein
Datensatz verweist über `storage` darauf, mehrere Datensätze dürfen dieselbe
Datei nutzen. Externe Dateiverknüpfungen gibt es im Datenformat nicht: Ein
Anhang ist immer eine verwaltete Kopie. Diese Prüfung liest nur. Sie löscht
nie eine vermeintlich verwaiste Datei – das entscheidet der Mensch, nach
einer Sicherung.

Befunde:
- `invalid`: Verweis mit ungültigem oder unsicherem Ablagepfad.
- `missing`: verwaltete Datei fehlt.
- `empty`: Datei hat 0 Byte (nicht nachweisbar beschädigt, aber verdächtig).
- `unreferenced`: Datei unter `attachments/`, auf die kein Datensatz zeigt
  (auch nicht im Papierkorb).
- `shared`: Datei, die von mehreren Datensätzen genutzt wird – kein Fehler,
  aber beim Entfernen eines einzelnen Verweises darf sie nicht gelöscht werden.
"""
from dataclasses import dataclass, field
import os

PREFIX = "attachments/"


@dataclass
class Report:
    references: int = 0
    files: int = 0
    bytes: int = 0
    invalid: list = field(default_factory=list)
    missing: list = field(default_factory=list)
    empty: list = field(default_factory=list)
    unreferenced: list = field(default_factory=list)
    shared: dict = field(default_factory=dict)

    @property
    def ok(self):
        return not (self.invalid or self.missing or self.empty)

    def as_dict(self):
        return {"references": self.references, "files": self.files, "bytes": self.bytes,
                "invalid": list(self.invalid), "missing": list(self.missing), "empty": list(self.empty),
                "unreferenced": list(self.unreferenced), "shared": dict(self.shared), "ok": self.ok}


def check(references, data_dir, validate):
    """`references`: iterierbar über (Besitzerbeschreibung, Anhangsdatensatz).

    `validate(storage)` ist Glides Pfadprüfung; sie wirft ValueError bei
    unsicheren Pfaden. Reine Lesefunktion.
    """
    report = Report()
    nutzer = {}
    for besitzer, anhang in references:
        report.references += 1
        storage = anhang.get("storage") if isinstance(anhang, dict) else None
        try:
            storage = validate(storage)
        except (ValueError, TypeError):
            report.invalid.append({"owner": besitzer, "storage": storage})
            continue
        nutzer.setdefault(storage, []).append(besitzer)
    for storage, besitzer in sorted(nutzer.items()):
        pfad = os.path.join(data_dir, *storage.split("/"))
        if not os.path.isfile(pfad):
            report.missing.append({"storage": storage, "owners": besitzer})
            continue
        groesse = os.path.getsize(pfad)
        if groesse == 0:
            report.empty.append({"storage": storage, "owners": besitzer})
        if len(besitzer) > 1:
            report.shared[storage] = len(besitzer)
    ordner = os.path.join(data_dir, "attachments")
    if os.path.isdir(ordner):
        for wurzel, _dirs, dateien in os.walk(ordner):
            for name in dateien:
                pfad = os.path.join(wurzel, name)
                rel = PREFIX + os.path.relpath(pfad, ordner).replace(os.sep, "/")
                report.files += 1
                try:
                    report.bytes += os.path.getsize(pfad)
                except OSError:
                    pass
                if rel not in nutzer:
                    report.unreferenced.append(rel)
    report.unreferenced.sort()
    return report
