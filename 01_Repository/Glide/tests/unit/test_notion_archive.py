"""Künstliche Notion-Archive: keine echten Exportinhalte und kein Dateiextrahieren."""
import io
import stat
import struct
import unittest
from unittest.mock import patch
import warnings
import zipfile

import notion_archive as notion

A, B = "a" * 32, "b" * 32
ROOT = f"Projekt {A}.md"
CHILD = f"Projekt {A}/Unterseite {B}.md"
IMAGE = f"Projekt {A}/Bild eins.png"


def archive(files):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as output:
        for name, value in files.items():
            # ZipInfo normalisiert unter Windows sonst schon den ungültigen
            # Testpfad. Das Archiv muss die tatsächlich geprüften Bytes tragen.
            entry = zipfile.ZipInfo(name)
            entry.filename = name
            entry.compress_type = zipfile.ZIP_DEFLATED
            output.writestr(entry, value)
    stream.seek(0)
    return stream


def example(text=None, image=b"fake-png"):
    return {ROOT: text or f"# Projekt\n\n**Text**\n\n- [x] Erledigt\n\n![Motiv](Projekt%20{A}/Bild%20eins.png)\n\n[Seite](Projekt%20{A}/Unterseite%20{B}.md)\n",
            CHILD: f"# Unterseite\n\n[Zurück](../Projekt%20{A}.md)\n", IMAGE: image}


class NotionArchiveTests(unittest.TestCase):
    def test_pages_folders_utf8_and_source_ids(self):
        result = notion.inspect_export(archive(example()))
        pages = {page.key: page for page in result.pages}
        self.assertEqual(set(pages), {"notion:" + A, "notion:" + B})
        self.assertEqual(pages["notion:" + A].title, "Projekt")
        self.assertEqual(pages["notion:" + B].folders, (("notion:" + A, "Projekt"),))
        self.assertEqual(pages["notion:" + A].asset_paths, (IMAGE,))
        self.assertEqual(result.losses, ())

    def test_folder_with_dot_and_uuid_retains_stable_identity(self):
        path = f"Projekt.v1 {A}/Kind {B}.md"
        result = notion.inspect_export(archive({path: "# Kind"}))
        self.assertEqual(result.pages[0].folders, (("notion:" + A, "Projekt.v1"),))

    def test_md_bom_crlf_and_missing_heading_are_supported(self):
        path = f"Anderer Titel {A}.md"
        result = notion.inspect_export(archive({path: b"\xef\xbb\xbfText\r\n- Punkt\r\n"}))
        self.assertEqual(result.pages[0].title, "Anderer Titel")
        self.assertEqual(result.pages[0].markdown, "Text\n- Punkt\n")

    def test_export_wrapper_changes_do_not_create_changed_sources(self):
        first = notion.inspect_export(archive({"Export-123/" + path: data for path, data in example().items()}))
        second = notion.inspect_export(archive({"Export-456/" + path: data for path, data in example().items()}))
        self.assertEqual([(p.key, p.source_hash, p.folders) for p in first.pages],
                         [(p.key, p.source_hash, p.folders) for p in second.pages])

    def test_path_identity_without_uuid_is_explicit_and_wrapper_independent(self):
        first = notion.inspect_export(archive({"Export-1/Ordner/Seite.md": "# Seite"}))
        second = notion.inspect_export(archive({"Export-2/Ordner/Seite.md": "# Seite"}))
        self.assertTrue(first.pages[0].key.startswith("path:"))
        self.assertEqual(first.pages[0].key, second.pages[0].key)
        self.assertEqual(first.pages[0].folders, second.pages[0].folders)
        self.assertIn("path-identity", {loss.code for loss in first.losses})

    def test_changed_image_is_changed_source_even_when_markdown_is_unchanged(self):
        first = notion.inspect_export(archive(example()))
        second = notion.inspect_export(archive(example(image=b"different-image")))
        by_key = {p.key: p.source_hash for p in first.pages}
        self.assertNotEqual(by_key["notion:" + A], next(p.source_hash for p in second.pages if p.key == "notion:" + A))
        self.assertEqual(by_key["notion:" + B], next(p.source_hash for p in second.pages if p.key == "notion:" + B))

    def test_renamed_page_keeps_id_but_reports_changed_location(self):
        first = notion.inspect_export(archive({ROOT: "# Titel"})).pages[0]
        second = notion.inspect_export(archive({f"Neuer Name {A}.md": "# Titel"})).pages[0]
        self.assertEqual(first.key, second.key)
        self.assertNotEqual(first.source_hash, second.source_hash)

    def test_render_preserves_heading_bold_tasks_image_and_internal_link(self):
        export = notion.inspect_export(archive(example()))
        page = next(p for p in export.pages if p.key == "notion:" + A)
        document = notion.page_document(export, page, {"notion:" + A: "glide-a", "notion:" + B: "glide-b"}, {IMAGE: {"id": "attachment-1"}})
        self.assertIn("Projekt", document["text"])
        self.assertIn("Text", document["text"])
        self.assertEqual(document["tasks"], [{"ref": 0, "text": "Erledigt", "done": True}])
        self.assertTrue({"h1", "bold", "task", "taskref:0"}.issubset({s["tag"] for s in document["spans"]}))
        self.assertIn("glide://list/glide-b", document["links"].values())
        self.assertEqual(next(iter(document["images"].values())), {"attachment": "attachment-1", "mode": "left", "width": 360})

    def test_parent_relative_page_reference_is_resolved(self):
        export = notion.inspect_export(archive(example()))
        page = next(p for p in export.pages if p.key == "notion:" + B)
        doc = notion.page_document(export, page, {"notion:" + A: "local-a"}, {})
        self.assertEqual(list(doc["links"].values()), ["glide://list/local-a"])

    def test_inline_images_become_blocks_without_losing_surrounding_text(self):
        text = f"Vorher ![Motiv](Projekt%20{A}/Bild%20eins.png) nachher"
        export = notion.inspect_export(archive(example(text)))
        page = next(p for p in export.pages if p.key == "notion:" + A)
        doc = notion.page_document(export, page, {}, {IMAGE: {"id": "pic"}})
        self.assertEqual(doc["text"], "Vorher\n\ufffc\nnachher")
        self.assertEqual(len(doc["images"]), 1)
        self.assertIn("inline-image-block", {loss.code for loss in export.losses})

    def test_same_image_twice_has_distinct_image_anchors(self):
        text = f"![a](Projekt%20{A}/Bild%20eins.png)\n\n![b](Projekt%20{A}/Bild%20eins.png)"
        export = notion.inspect_export(archive(example(text)))
        page = next(p for p in export.pages if p.key == "notion:" + A)
        doc = notion.page_document(export, page, {}, {IMAGE: {"id": "pic"}})
        self.assertEqual(len(doc["images"]), 2)
        self.assertEqual({info["attachment"] for info in doc["images"].values()}, {"pic"})

    def test_code_links_are_not_rewritten_or_counted_as_assets(self):
        literal = f"[wörtlich](Projekt%20{A}/Unterseite%20{B}.md)"
        missing = "[Datei](fehlt.png)"
        text = f"# Code\n\n```md\n{literal}\n{missing}\n```\n\n`{missing}`\n"
        export = notion.inspect_export(archive(example(text)))
        page = next(p for p in export.pages if p.key == "notion:" + A)
        doc = notion.page_document(export, page, {"notion:" + B: "local-b"}, {})
        self.assertIn(literal, doc["text"])
        self.assertIn(missing, doc["text"])
        self.assertEqual(page.asset_paths, ())
        self.assertEqual(export.losses, ())

    def test_unselected_targets_are_reported_before_render(self):
        export = notion.inspect_export(archive(example()))
        losses = notion.unresolved_links(export, {"notion:" + A: "local-a"})
        self.assertEqual([loss.code for loss in losses], ["unselected-page"])
        self.assertEqual(notion.unresolved_links(export, {"notion:" + A: "local-a", "notion:" + B: "local-b"}), ())

    def test_csv_html_and_unsupported_features_are_visible_and_sources_preserved(self):
        files = example("# Titel\n\n<aside>Wichtiger Text</aside>\n\n###### Tief\n\n[fehlt](missing.md#abschnitt)")
        files.update({"Datenbank.csv": "Name,Datum\nBeispiel,2026-10-10", "Ansicht.html": "<b>Quelle</b>"})
        export = notion.inspect_export(archive(files))
        self.assertTrue({"csv-database", "html-file", "html-block", "heading-depth", "missing-local-target", "link-anchor"}.issubset({l.code for l in export.losses}))
        self.assertEqual(export.members["Datenbank.csv"], files["Datenbank.csv"].encode())
        self.assertEqual(export.members["Ansicht.html"], files["Ansicht.html"].encode())

    def test_file_links_become_available_attachments(self):
        files = example(f"[Dokument](Projekt%20{A}/Text.pdf)")
        files[f"Projekt {A}/Text.pdf"] = b"%PDF-fake"
        export = notion.inspect_export(archive(files))
        page = next(p for p in export.pages if p.key == "notion:" + A)
        self.assertEqual(page.asset_paths, (f"Projekt {A}/Text.pdf",))
        self.assertIn("attachment-link", {loss.code for loss in export.losses})

    def test_external_links_survive_and_external_images_are_never_loaded(self):
        export = notion.inspect_export(archive({ROOT: "[Web](https://example.test/path)\n\n![Bild](https://example.test/image.png)"}))
        page = export.pages[0]
        doc = notion.page_document(export, page, {}, {})
        self.assertEqual(page.asset_paths, ())
        self.assertIn("https://example.test/path", doc["links"].values())
        self.assertIn("https://example.test/image.png", doc["links"].values())

    def test_outside_paths_and_local_file_uris_are_not_resolved(self):
        members = {"inside.png": b"x", "folder/file.png": b"y"}
        for target in ("../../inside.png", "/inside.png", "file:///inside.png", "C:/inside.png", "../..%2Finside.png", "\\inside.png", "data:image/png,123"):
            self.assertIsNone(notion.local_target("folder/page.md", target, members), target)
        self.assertEqual(notion.local_target("folder/page.md", "../inside.png", members), "inside.png")

    def test_traversal_absolute_windows_and_control_paths_are_rejected(self):
        for separator in ('/', '\\'):
            with patch.object(zipfile.os, 'sep', separator):
                for path in ("../bad.md", "/bad.md", "C:/bad.md", "a\\bad.md", "a/./bad.md", "a//bad.md", "a/../bad.md", "a/\x01bad.md", "a/bad.md\x00hidden"):
                    with self.subTest(separator=separator, path=path), self.assertRaises(notion.NotionFormatError):
                        notion.inspect_export(archive({path: "# Bad"}))

    def test_duplicate_case_and_unicode_paths_are_rejected(self):
        for paths in (("A.md", "a.md"), ("ä.md", "a\u0308.md")):
            with self.subTest(paths=paths), self.assertRaises(notion.NotionFormatError):
                notion.inspect_export(archive({paths[0]: "a", paths[1]: "b"}))
        stream = io.BytesIO()
        with warnings.catch_warnings(), zipfile.ZipFile(stream, "w") as output:
            warnings.simplefilter("ignore", UserWarning)
            output.writestr("same.md", "a"); output.writestr("same.md", "b")
        stream.seek(0)
        with self.assertRaises(notion.NotionFormatError):
            notion.inspect_export(stream)

    def test_duplicate_notion_ids_are_rejected(self):
        with self.assertRaises(notion.NotionFormatError):
            notion.inspect_export(archive({ROOT: "a", f"Andere {A}.md": "b"}))

    def test_symlink_and_special_members_are_rejected(self):
        for mode in (stat.S_IFLNK, stat.S_IFIFO):
            info = zipfile.ZipInfo("link.md"); info.create_system = 3; info.external_attr = (mode | 0o777) << 16
            stream = io.BytesIO()
            with zipfile.ZipFile(stream, "w") as output:
                output.writestr(info, "target.md")
            stream.seek(0)
            with self.assertRaises(notion.NotionFormatError):
                notion.inspect_export(stream)

    def test_declared_size_count_and_archive_limits_are_enforced(self):
        for name, limit, files in (("MAX_MARKDOWN_BYTES", 3, {ROOT: "four"}),
                                   ("MAX_MEMBER_BYTES", 3, {ROOT: "a", "big.bin": "four"}),
                                   ("MAX_EXPANDED_BYTES", 3, {ROOT: "abc", "x.bin": "x"}),
                                   ("MAX_MEMBERS", 1, {ROOT: "a", "x.bin": "x"}),
                                   ("MAX_ARCHIVE_BYTES", 1, {ROOT: "a"})):
            with self.subTest(limit=name), patch.object(notion, name, limit), self.assertRaises(notion.NotionFormatError):
                notion.inspect_export(archive(files))

    def test_empty_invalid_non_markdown_and_invalid_utf8_archives_are_rejected(self):
        for source in (io.BytesIO(b"not zip"), archive({}), archive({"table.csv": "a,b"}), archive({ROOT: b"\xff"}), archive({ROOT: b"a\x00b"})):
            with self.assertRaises(notion.NotionFormatError):
                notion.inspect_export(source)

    def test_crc_error_is_visible(self):
        stream = archive({ROOT: "# Inhalt"})
        raw = bytearray(stream.getvalue())
        name_len, extra_len = struct.unpack_from("<HH", raw, 26)
        raw[30 + name_len + extra_len] ^= 0xFF
        with self.assertRaises(notion.NotionFormatError):
            notion.inspect_export(io.BytesIO(raw))


if __name__ == "__main__":
    unittest.main()
