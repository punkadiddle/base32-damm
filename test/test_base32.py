import unittest
import base32_crockford
import base32_damm

class Test(unittest.TestCase):

    def test_values(self):
        numbers = (0,1,2,31,32,900,9000,20000,500000,69464656,45454395464,4646536346436,436575743624,99892830928492385239582)
        for x in numbers:
            expected = base32_crockford.encode(x, checksum=False)
            calculated = base32_damm.encode(x, checksum=False)
            
            self.assertEqual(expected, calculated, msg="{} -> {}".format(x, expected))           

    def test_invalid(self):
        numbers = (0.7, -1, -42)
        for x in numbers:
            with self.assertRaises(ValueError, msg="{}".format(x)):
                base32_damm.encode(x, checksum=False)
                
    def test_sort(self):
        b = base32_damm.encode(0, checksum=True, width=10)
        for x in range(1,33):
            a = base32_damm.encode(x, checksum=True, width=10)
            self.assertGreater(a, b)
            b = a

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()