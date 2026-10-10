import unittest
import svg_geometry as svg

class SamplingTests(unittest.TestCase):
    def test_sampling_changes_curves_but_preserves_endpoints_and_holes(self):
        source='<svg xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M0 0C0 5 5 10 10 10L10 0Z M3 3L4 3L4 4L3 4Z"/></svg>'
        coarse=svg.outline(source,schritte=4);fine=svg.outline(source,schritte=32)
        self.assertEqual(len(coarse),2)
        self.assertEqual(coarse[1],fine[1])
        self.assertEqual(coarse[0][0],fine[0][0])
        self.assertEqual(coarse[0][-2:],fine[0][-2:])
        self.assertEqual(len(fine[0])-len(coarse[0]),28)
        for steps in (0,-1,257,1.5):
            with self.assertRaises(ValueError):svg.subpaths('M0 0L1 1Z',schritte=steps)

if __name__=='__main__':unittest.main()
