import sys
sys.path.append('../JOBOT')
import unittest
from flask import Flask
from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_home_route(self):
        response = self.app.get('/get?msg=hi')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello! I'm here to assist you with your job search. Would you like to start?", response.data)
    
    def test_get_bot_response_route(self):
        response = self.app.get('/get?msg=Yes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"What is your preferred job title or role?", response.data)

    def test_reset_conversation_route(self):
        response = self.app.get('/reset')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Conversation has been reset. You can now start a new conversation.", response.data)



if __name__ == '__main__':
    # Create a TestSuite and add the test cases
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AppTestCase))

    # Create a TextTestRunner and run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Calculate the grade
    total_tests = result.testsRun
    total_failures = len(result.failures)
    total_errors = len(result.errors)
    total_passed = total_tests - total_failures - total_errors
    grade = (total_passed / total_tests) * 100

    print("\n========== TEST REPORT ==========")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failures: {total_failures}")
    print(f"Errors: {total_errors}")
    print(f"Grade: {grade:.2f}%")
