from jobScraper import find_all_job_offers, get_all_job_offers_await, get_all_job_offers
import unittest
import time
import sys
sys.path.append('../JOBOT')


class TestJobSearch(unittest.TestCase):
    def test_find_all_job_offers(self):
        job_titles = ['Cyber']
        job_locations = ['Alabama']
        job_type = 'fulltime'
        find_all_job_offers(job_titles, job_locations, job_type)
        # Add an appropriate delay here to allow the async job searches to complete
        time.sleep(10)

    def test_get_all_job_offers_await(self):
        job_offers = get_all_job_offers_await()
        self.assertGreater(len(job_offers), 0, "No job offers retrieved")

    def test_get_all_job_offers(self):
        job_offers = get_all_job_offers()
        self.assertGreater(len(job_offers), 0, "No job offers retrieved")

    @classmethod
    def tearDownClass(cls):
        job_offers_await = get_all_job_offers_await()
        job_offers = get_all_job_offers()

        # Grade calculation
        grade = 0
        if len(job_offers_await) > 0:
            grade += 1
        if len(job_offers) > 0:
            grade += 1

        total_grade = grade / 2 * 100
        print(f"Grade: {total_grade}%")


if __name__ == '__main__':
    unittest.main()
