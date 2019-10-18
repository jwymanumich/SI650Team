import app
import unittest

class Test1(unittest.TestCase): 

    def test1(self): 
        print("A Test")
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()