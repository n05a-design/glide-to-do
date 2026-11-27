# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 20: spell-checking contract for host text fields (Shell 0.8.0).

Tk-free. The host talks to one small interface and never to a concrete engine:

- `SpellChecker`: `languages()`, `check(word, language)`, `suggest(word, language, limit)`.
- `WordListChecker`: words per language from the host (tests, demos, a user dictionary).
- `LayeredChecker`: wraps an engine with an ignore list for the session and a
  personal word list that the host stores where it likes (`on_add` callback).
- `words(text)`: (start, end, word) for checkable words; URLs, e-mail addresses,
  paths, code-like identifiers (digits, `_`, inner capitals, all capitals) and
  single letters are skipped, because a dictionary cannot judge them.
- `misspelled(checker, text, language, ranges=None)`: unknown words, optionally
  only inside the given (start, end) ranges, so a host checks just what changed.
- `probe_backends()`: which optional engines are installed, found by
  `pkgutil.iter_modules` without importing them. The shell ships no engine
  and no dictionary; choosing one is the host owner's decision (licence, size).

No network access, no background threads: the host schedules checks after an
input pause on its own timer (for example `window_lifetime.AfterScope`).
"""
from __future__ import annotations

import pkgutil
import re

_TOKEN = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*", re.UNICODE)
_SKIP = re.compile(r"(?:https?://|www\.|mailto:)\S+|\S+@\S+\.\S+|(?:[A-Za-z]:)?[\\/][\w.\\/-]+|`[^`]*`", re.UNICODE)


class SpellChecker:
    """Interface of a spell-checking engine; subclasses override the three methods."""

    def languages(self):
        return ()

    def check(self, word, language):
        raise NotImplementedError

    def suggest(self, word, language, limit=5):
        return []


class WordListChecker(SpellChecker):
    def __init__(self, words_by_language):
        self._words = {lang: {w.casefold(): w for w in words} for lang, words in words_by_language.items()}

    def languages(self):
        return tuple(sorted(self._words))

    def check(self, word, language):
        return word.casefold() in self._words.get(language, ())

    def suggest(self, word, language, limit=5):
        """Candidates with edit distance 1, then 2, in alphabetical order."""
        ziel = word.casefold()
        woerter = self._words.get(language, {})
        treffer = sorted((_distance(ziel, k), w) for k, w in woerter.items() if abs(len(k) - len(ziel)) <= 2)
        return [w for d, w in treffer if d <= 2][:limit]


class LayeredChecker(SpellChecker):
    def __init__(self, engine, personal=(), on_add=None):
        self.engine = engine
        self.personal = {w.casefold() for w in personal}
        self.ignored = set()
        self.on_add = on_add

    def languages(self):
        return self.engine.languages()

    def check(self, word, language):
        key = word.casefold()
        return key in self.ignored or key in self.personal or self.engine.check(word, language)

    def suggest(self, word, language, limit=5):
        return self.engine.suggest(word, language, limit)

    def ignore(self, word):
        self.ignored.add(word.casefold())

    def add(self, word):
        self.personal.add(word.casefold())
        if self.on_add is not None:
            self.on_add(sorted(self.personal))


def _distance(a, b):
    vorher = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        aktuell = [i]
        for j, y in enumerate(b, 1):
            aktuell.append(min(vorher[j] + 1, aktuell[j - 1] + 1, vorher[j - 1] + (x != y)))
        vorher = aktuell
    return vorher[-1]


def _code_like(word):
    return (len(word) < 2 or word.isupper() and len(word) > 1
            or any(c.isupper() for c in word[1:]) and not word.isupper())


def words(text):
    """(start, end, word) of checkable words; see the module docstring for what is skipped."""
    gesperrt = [(m.start(), m.end()) for m in _SKIP.finditer(text)]
    ergebnis = []
    for treffer in _TOKEN.finditer(text):
        a, b = treffer.span()
        if any(s <= a < e for s, e in gesperrt):
            continue
        davor, danach = text[a - 1:a], text[b:b + 1]
        if davor in ("_",) or danach in ("_",) or (danach.isdigit() if danach else False):
            continue
        if _code_like(treffer.group()):
            continue
        ergebnis.append((a, b, treffer.group()))
    return ergebnis


def misspelled(checker, text, language, ranges=None):
    """(start, end, word) not known to `checker`; only within `ranges` when given."""
    befund = []
    for a, b, wort in words(text):
        if ranges is not None and not any(s <= a and b <= e for s, e in ranges):
            continue
        if not checker.check(wort, language):
            befund.append((a, b, wort))
    return befund


OPTIONAL_BACKENDS = {"spylls": "spylls", "pyenchant": "enchant", "pyobjc-appkit": "AppKit", "comtypes": "comtypes"}


def probe_backends():
    """{backend name: importable} without importing anything."""
    vorhanden = {modul.name for modul in pkgutil.iter_modules()}
    return {name: modul in vorhanden for name, modul in OPTIONAL_BACKENDS.items()}
