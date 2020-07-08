

import unittest
from HW2_2018204 import binary_covertor
from HW2_2018204 import dict_append
from HW2_2018204 import PIchecker
from HW2_2018204 import _forcommon
from HW2_2018204 import binary_to_equation
from HW2_2018204 import minFunc
class testpoint(unittest.TestCase):
	def test_minFunc(self):
		self.assertAlmostEqual(minFunc(4,'(0,1,2,5,6,7)'),"w'x'y'+w'xz+w'yz'")
		self.assertAlmostEqual(minFunc(4,'(0,1,2,5,6,7) d(11,14)'),"w'x'y'+w'xz+w'yz'")
		self.assertAlmostEqual(minFunc(4,'(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)'),"1")
		self.assertAlmostEqual(minFunc(4,'(0,1,2,3,13) d(5,7,9)'),"w'x'+y'z")
		self.assertAlmostEqual(minFunc(3,'(0,1,2,3) d(7)'),"w'")
		self.assertAlmostEqual(minFunc(2,'(0,1,2)'),"w'+x'")
		self.assertAlmostEqual(minFunc(4,'(0,1,2,3,4,5,8,9,10,11,12,13)'),"x'+y'")
		self.assertAlmostEqual(minFunc(3,'(0,7) d(5,6)'),"w'x'y'+wy")


		
                
if __name__=='__main__':
	unittest.main()