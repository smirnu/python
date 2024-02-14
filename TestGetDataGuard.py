import unittest
import getDataGuardian
import os

class TestGetDataGuard(unittest.TestCase):
    
    def setUp(self):
        self.apiAddress = 'https://content.guardianapis.com/search?page='
        self.apiKey = '&api-key=deleted to keep privacy'
        self.bytes = getDataGuardian.connectToApi(self.apiAddress, 1, '', self.apiKey)

    def tearDown(self):
        if os.path.exists('success_load.txt'):
            os.remove('success_load.txt')
        if os.path.exists('error_load.txt'):
            os.remove('error_load.txt')
        if os.path.exists('result.csv'):
            os.remove('result.csv')

    # test_connectToApi
    def test_connectToApi_withInvalidPage(self):
        noneResult = getDataGuardian.connectToApi(self.apiAddress, 3801, '', self.apiKey)
        self.assertEqual(noneResult, None)

    def test_connectToApi_withValidPage(self):
        json = getDataGuardian.connectToApi(self.apiAddress, 1, '', self.apiKey)
        self.assertEqual(type(json), bytes)

    def test_connectToApi_withWrongCredential(self):
        booleanResult = getDataGuardian.connectToApi(self.apiAddress, 1, '', '&api-key=eec9a-63d8-bbd8-ea415d78')
        self.assertFalse(booleanResult)

    # test_analyseTheResponse
    def test_analyseTheResponse_true(self):
        trueResponse = getDataGuardian.analyseTheResponse(self.bytes, 0, 1, [])
        self.assertTrue(trueResponse)

    def test_analyseTheResponse_false(self):
        falseResponse = getDataGuardian.analyseTheResponse(False, 0, 1, [])
        self.assertFalse(falseResponse)

    # getPageNumber(currPage, maxPage, pageMemory)
    def test_getPageNumber_inTheMiddle(self):
        pageMemory = [True, True, True, True, False, True]
        pageToLoad = getDataGuardian.getPageNumber(1, 5, pageMemory)
        self.assertEqual(pageToLoad, 4)

    def test_getPageNumber_atTheEnd(self):
        pageMemory = [True, True, True, True, True, False]
        pageToLoad = getDataGuardian.getPageNumber(1, 5, pageMemory)
        self.assertEqual(pageToLoad, 5)

    def test_getPageNumber_atTheBeg(self):
        pageMemory = [True, False, True, True, False, True]
        pageToLoad = getDataGuardian.getPageNumber(1, 5, pageMemory)
        self.assertEqual(pageToLoad, 1)

    def test_getPageNumber_allPgesProc(self):
        pageMemory = [True, True, True, True, True, True]
        pageToLoad = getDataGuardian.getPageNumber(1, 5, pageMemory)
        self.assertEqual(pageToLoad, -1)

    # checkPrevSessionInterrupted
    def test_checkPrevSessionInterrupted_succExists(self):
        pageMemory = []
        with open('success_load.txt', 'a') as file:
            for i in range(1, 5):
                file.write(str(i) + '\n')
        getDataGuardian.checkPrevSessionInterrupted(pageMemory)
        self.assertEqual(len(pageMemory), 5)

    def test_checkPrevSessionInterrupted_errExists(self):
        pageMemory = []
        with open('error_load.txt', 'a') as file:
            for i in range(1, 5):
                file.write(str(i) + '\n')
        getDataGuardian.checkPrevSessionInterrupted(pageMemory)
        self.assertEqual(len(pageMemory), 5)

    def test_checkPrevSessionInterrupted_errSuccExist(self):
        pageMemory = []
        with open('error_load.txt', 'a') as file:
            for i in range(1, 5):
                file.write(str(i) + '\n')
        with open('success_load.txt', 'a') as file:
            for i in range(5, 10): 
                file.write(str(i) + '\n')
        getDataGuardian.checkPrevSessionInterrupted(pageMemory)
        self.assertEqual(len(pageMemory), 10)

    def test_checkPrevSessionInterrupted_onePageNoProcc(self):
        pageMemory = []
        with open('error_load.txt', 'a') as file:
            for i in range(1, 5):
                file.write(str(i) + '\n')
        with open('success_load.txt', 'a') as file:
            for i in range(6, 10): # skippin page 5, it has to be False in pageMemory
                file.write(str(i) + '\n')
        getDataGuardian.checkPrevSessionInterrupted(pageMemory)
        self.assertFalse(pageMemory[5])

    def test_checkPrevSessionInterrupted_notInterruption(self):
        pageMemory = []
        getDataGuardian.checkPrevSessionInterrupted(pageMemory)
        self.assertEqual(len(pageMemory), 0)  
    
    # fillState
    def test_fillState_err(self): # check that an error file created 
        pageMemory = [False, False]
        getDataGuardian.fillState(False, 1, pageMemory)
        self.assertTrue(os.path.exists('error_load.txt'))

    def test_fillState_succ(self): # check that success file created
        pageMemory = [False, False]
        getDataGuardian.fillState(True, 1, pageMemory)
        self.assertTrue(os.path.exists('success_load.txt'))

    def test_fillState_errNotCreated(self): # check that an error file not created 
        pageMemory = [False, False]
        getDataGuardian.fillState(True, 1, pageMemory)
        self.assertFalse(os.path.exists('error_load.txt'))

    def test_fillState_succNotCreated(self): # check that success file not created
        pageMemory = [False, False]
        getDataGuardian.fillState(False, 1, pageMemory)
        self.assertFalse(os.path.exists('success_load.txt'))

    def test_fillState_pmFilled(self): # changed status in pageMemory for page 1
        pageMemory = [False, False]
        getDataGuardian.fillState(False, 1, pageMemory)
        self.assertTrue(pageMemory[1])

    # runThroughErrors
    def test_runThroughErrors_lenErrZero(self):
        pageMemory = [True, True, True, True, True]
        with open('error_load.txt', 'a') as file:
            pass
        getDataGuardian.runThroughErrors(pageMemory)
        self.assertFalse(os.path.exists('result.csv'))

    def test_runThroughErrors_errWithRecords(self):
        pageMemory = [True, True, True, True, True]
        with open('error_load.txt', 'a') as file:
            for i in range(1, 5):
                file.write(str(i) + '\n')
        getDataGuardian.runThroughErrors(pageMemory)
        self.assertTrue(os.path.exists('result.csv'))

    def test_runThroughErrors_creatNotEmptyRes(self):
        pageMemory = [True, True, True, True, True]
        with open('error_load.txt', 'a') as file:
            for i in range(1, 5):
                file.write(str(i) + '\n')
        getDataGuardian.runThroughErrors(pageMemory)
        self.assertTrue(os.path.getsize('result.csv') > 0)

if __name__ == '__main__':
    unittest.main()
