"""SVG export compatibility and compound path invariants, without Tk."""
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
import svg_geometry as svg


class SVGGeometryTests(unittest.TestCase):
    def test_css_tint_is_inline(self):
        original = '<svg xmlns="http://www.w3.org/2000/svg"><style>.a {fill: #9e4ac8; fill-rule: evenodd;}</style><path class="a" d="M0 0H10V10H0Z"/></svg>'
        result = svg.tinted(original, "#123456")
        node = ET.fromstring(result).find('{http://www.w3.org/2000/svg}path')
        self.assertIn('fill: #123456', node.get('style'))
        self.assertIn('fill-rule: evenodd', node.get('style'))
        self.assertNotIn('#9e4ac8', result)

    def test_rgb_tint_and_bad_color(self):
        self.assertIn('#ABCDEF', svg.tinted('<svg fill="rgb(158,74,200)"/>', '#ABCDEF'))
        for value in ('red', '#12345', None):
            with self.assertRaises(ValueError):
                svg.tinted('<svg fill="#9e4ac8"/>', value)

    def test_nonpainted_css_path_is_excluded(self):
        source = '<svg xmlns="http://www.w3.org/2000/svg"><style>.empty {fill: none;}</style><path class="empty" d="M0 0H100V100H0Z"/><path d="M10 10H20V20H10Z"/></svg>'
        self.assertEqual(len(svg.outline(source)), 1)
        self.assertEqual(min(x for ring in svg.outline(source) for x, _y in ring), 10)

    def test_compound_hole_is_cut_out(self):
        outer = ((0, 0), (10, 0), (10, 10), (0, 10))
        hole = ((3, 3), (7, 3), (7, 7), (3, 7))
        result = svg.canvas_polygons((outer, hole))
        self.assertEqual(len(result), 1)
        self.assertEqual(abs(svg.signed_area(result[0])), 84)
        self.assertTrue(svg.contains(result[0], (1, 1)))
        self.assertFalse(svg.contains(result[0], (5, 5)))

    def test_disjoint_and_nested_island(self):
        rings = svg.subpaths('M0 0H20V20H0Z M2 2H18V18H2Z M8 8H12V12H8Z M30 0H40V10H30Z')
        result = svg.canvas_polygons(rings)
        self.assertEqual(len(result), 3)
        self.assertEqual(sum(abs(svg.signed_area(r)) for r in result), 260)

    def test_smooth_curves_and_control_reset(self):
        explicit = svg.subpaths("M0 0C1 2 3 4 5 6C7 8 9 10 11 12")
        self.assertEqual(explicit, svg.subpaths("M0 0C1 2 3 4 5 6S9 10 11 12"))
        self.assertEqual(explicit, svg.subpaths("M0 0c1 2 3 4 5 6s4 4 6 6"))
        self.assertEqual(svg.subpaths("M0 0L5 6C5 6 9 10 11 12"),
                         svg.subpaths("M0 0L5 6S9 10 11 12"))
        with self.assertRaises(ValueError):
            svg.subpaths("M0 0Q5 5 10 10")

    def test_attribute_nonpainted_path_is_excluded(self):
        source = '<svg xmlns="http://www.w3.org/2000/svg"><path fill="none" d="M0 0H100V100H0Z"/><path d="M10 10H20V20H10Z"/></svg>'
        self.assertEqual(len(svg.outline(source)), 1)

    def test_entities_rejected(self):
        source = '<!DOCTYPE svg [<!ENTITY a "x">]><svg/>'
        for method in (svg.outline, svg.inline_styles, svg.document_box):
            with self.assertRaises(ValueError):
                method(source)

    def test_icon_uses_full_document_box_including_background(self):
        source = '<svg viewBox="0 0 841.89 841.89"><rect width="841.89" height="841.89"/><path d="M200 100H600V700H200Z"/></svg>'
        self.assertEqual(svg.document_box(source), (0., 0., 841.89, 841.89))
        for box in ("", "0 0 0 100", "0 0 100 -1", "0 0 nan 100", "0 0 100", "0 0 inf 100"):
            with self.subTest(box=box), self.assertRaises(ValueError):
                svg.document_box(f'<svg viewBox="{box}"/>')


if __name__ == '__main__':
    unittest.main()
