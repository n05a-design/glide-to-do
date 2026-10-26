#!/bin/sh
# Nativer, isolierter Entwicklungsbau. Keine vorhandene Lieferung wird ersetzt.
set -eu
umask 077

usage() {
    cat <<'USAGE'
Aufruf: sh packaging/paket/baue_und_pruefe_macos.sh [--python /Pfad/python3] [--ziel /neuer/Bauordner]

Benötigt einen macOS-arm64-Pythonprozess passend zu den vorhandenen
Original-Lizenzbelegen (derzeit Python 3.14.5 / Tcl 9.0.3 / Tk 9.0).
Der neue Bauordner muss außerhalb des Repositorys und von OneDrive liegen.
Ohne --ziel entsteht ein neuer Ordner im nativen Temporärverzeichnis.
Python, Tcl/Tk und Apple-Bauwerkzeuge werden nicht installiert oder verändert.
Bauabhängigkeiten werden ausschließlich in einer neuen lokalen venv installiert.
Alte Pakete bleiben erhalten; auch bei Fehlern bleibt der Diagnoseordner bestehen.
USAGE
}

PYTHON_GLIDE=python3
DESTINATION_GLIDE=
while [ "$#" -gt 0 ]; do
    case "$1" in
        --help|-h) usage; exit 0 ;;
        --python|--ziel)
            option=$1
            if [ "$#" -lt 2 ] || [ -z "$2" ]; then
                printf '%s benötigt einen Wert.\n' "$option" >&2
                exit 2
            fi
            case "$2" in --*) printf '%s benötigt einen Wert.\n' "$option" >&2; exit 2 ;; esac
            if [ "$option" = --python ]; then PYTHON_GLIDE=$2; else DESTINATION_GLIDE=$2; fi
            shift 2 ;;
        *) printf 'Unbekanntes Argument: %s\n' "$1" >&2; usage >&2; exit 2 ;;
    esac
done

SCRIPT_GLIDE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
REPO_GLIDE=$(CDPATH= cd -- "$SCRIPT_GLIDE/../.." && pwd -P)
PYTHON_GLIDE=$(command -v "$PYTHON_GLIDE") || {
    printf 'Gewähltes Python wurde nicht gefunden.\n' >&2
    exit 1
}
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PIP_DISABLE_PIP_VERSION_CHECK=1

if [ -n "$DESTINATION_GLIDE" ]; then
    BAU_GLIDE=$("$PYTHON_GLIDE" -B "$SCRIPT_GLIDE/macos_build_run.py" prepare \
        --repo "$REPO_GLIDE" --ziel "$DESTINATION_GLIDE")
else
    BAU_GLIDE=$("$PYTHON_GLIDE" -B "$SCRIPT_GLIDE/macos_build_run.py" prepare --repo "$REPO_GLIDE")
fi
printf 'Nativer Bauordner: %s\n' "$BAU_GLIDE"
trap 'status=$?; if [ "$status" -ne 0 ]; then printf "Bau abgebrochen; Diagnoseordner bleibt erhalten: %s\n" "$BAU_GLIDE" >&2; fi' EXIT

run_step() {
    step=$1
    shift
    if "$@" >"$BAU_GLIDE/$step.log" 2>&1; then
        cat "$BAU_GLIDE/$step.log"
    else
        status=$?
        cat "$BAU_GLIDE/$step.log" >&2
        return "$status"
    fi
}

run_step 01-venv "$PYTHON_GLIDE" -B -m venv "$BAU_GLIDE/venv"
VENV_GLIDE="$BAU_GLIDE/venv/bin/python3"
run_step 02-bauabhaengigkeiten "$VENV_GLIDE" -B -m pip install \
    -r "$REPO_GLIDE/requirements/build-macos.txt"
run_step 03-lizenzen "$VENV_GLIDE" -B "$SCRIPT_GLIDE/lizenzen_vorbereiten_macos.py" \
    --quelle "$REPO_GLIDE/src/glide" --repo "$REPO_GLIDE" --ziel "$BAU_GLIDE/lizenzen"
VERSION_GLIDE=$("$VENV_GLIDE" -B -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$BAU_GLIDE/eingang.json")
run_step 04-paketbau "$VENV_GLIDE" -B "$SCRIPT_GLIDE/baue_paket.py" \
    --quelle "$REPO_GLIDE/src/glide" --version "$VERSION_GLIDE" --ziel "$BAU_GLIDE/bau" \
    --plattform macos-arm64 --lizenzen "$BAU_GLIDE/lizenzen"

# Bestehender Schutz gilt nur im Prüf-Kindprozess. Keine Installation wird
# umbenannt, verschoben, umberechtigt oder vorübergehend verändert.
PYTHON_BASE_GLIDE=$("$VENV_GLIDE" -B -c 'import sys; print(sys.base_prefix)')
run_step 05-isolierter-start "$VENV_GLIDE" -B "$SCRIPT_GLIDE/pruefe_start_macos.py" \
    --paket "$BAU_GLIDE/bau/dist/Glide.app" --bericht "$BAU_GLIDE/startprobe.json" \
    --sperren "$PYTHON_BASE_GLIDE" --sperren "$BAU_GLIDE/venv" \
    --sperren "$BAU_GLIDE/bau/quelle" --sperren "$REPO_GLIDE"

ARCHIV_GLIDE="$BAU_GLIDE/Glide-$VERSION_GLIDE-macos-arm64.tar.gz"
# bsdtar erzeugt sonst AppleDouble-Dateien für copyfile-/xattr-Metadaten.
# Nur diese Metadatenbeigaben abschalten; Inhalte, Dateimodi und Links erhalten.
run_step 06-archiv env COPYFILE_DISABLE=1 /usr/bin/tar --no-mac-metadata --no-xattrs \
    -czf "$ARCHIV_GLIDE" -C "$BAU_GLIDE/bau/dist" Glide.app
run_step 07-abschluss "$VENV_GLIDE" -B "$SCRIPT_GLIDE/macos_build_run.py" finish \
    --repo "$REPO_GLIDE" --ziel "$BAU_GLIDE" --archiv "$ARCHIV_GLIDE"
printf 'Geprüftes Entwicklungsartefakt: %s\nSHA-256: %s.sha256\nBericht: %s/abschluss.json\n' \
    "$ARCHIV_GLIDE" "$ARCHIV_GLIDE" "$BAU_GLIDE"
