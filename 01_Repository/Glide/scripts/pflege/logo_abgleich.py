"""Neue Logo-Master unverändert verteilen und alle Raster-/Paketsymbole erzeugen.

Aufruf aus 01_Repository/Glide mit Tk 9: python -B scripts/pflege/logo_abgleich.py
--pruefen erzeugt Vergleichsdateien nur temporär und meldet jede Abweichung.
"""
import argparse
import importlib.util
from pathlib import Path
import tempfile

REPO = Path(__file__).resolve().parents[2]
ROOT = REPO.parents[1]
MASTER = ROOT / "20_Grafik_Master/01_Logo"
MAPPING = {
    "2026-Glide-Logo-in-App.svg": ("glide-logo.svg", "glide-logo-klein.svg"),
    "2026-Glide-Logo-App-und-Fav-Icon.svg": ("glide-app-icon.svg", "glide-app-icon-klein.svg"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pruefen", action="store_true")
    args = parser.parse_args()
    resources = REPO / "src/glide/resources/logo"
    changes = []

    def compare_or_write(data, target):
        if target.exists() and target.read_bytes() == data:
            return
        changes.append(target.relative_to(ROOT).as_posix())
        if not args.pruefen:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)

    for name, copies in MAPPING.items():
        for copy in copies:
            compare_or_write((MASTER / name).read_bytes(), resources / copy)
    if args.pruefen and changes:
        raise SystemExit("SVG-Abweichungen: " + ", ".join(changes))

    spec = importlib.util.spec_from_file_location("glide_icon_build", REPO / "packaging/baue_symbole.py")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    with tempfile.TemporaryDirectory(prefix="glide-logo-") as folder:
        temp = Path(folder)
        builder.erzeugen(temp / "icons", temp / "resources")
        for generated in (temp / "icons").iterdir():
            compare_or_write(generated.read_bytes(), REPO / "assets/icons" / generated.name)
        for generated in (temp / "resources").iterdir():
            compare_or_write(generated.read_bytes(), resources / generated.name)
        compare_or_write((temp / "resources/glide-logo.png").read_bytes(),
                         MASTER / "Exporte/2026-Glide-Logo-in-App.png")
        compare_or_write((temp / "resources/glide-app-icon.png").read_bytes(),
                         MASTER / "Exporte/2026-Glide-Logo-App-und-Fav-Icon.png")
        fav = ROOT / "20_Grafik_Master/03_Fav-Icon"
        compare_or_write((MASTER / "2026-Glide-Logo-App-und-Fav-Icon.svg").read_bytes(), fav / "favicon.svg")
        compare_or_write((temp / "icons/glide.ico").read_bytes(), fav / "favicon.ico")
        for size in (16, 32, 64, 256):
            compare_or_write((temp / f"resources/glide-app-icon-{size}.png").read_bytes(),
                             fav / f"favicon-{size}.png")
        compare_or_write((temp / "icons/glide_512.png").read_bytes(), fav / "favicon-512.png")
    print(("Abweichungen" if args.pruefen else "Aktualisiert") + ": " + str(len(changes)))
    if args.pruefen and changes:
        raise SystemExit("\n".join(changes))


if __name__ == "__main__":
    main()
