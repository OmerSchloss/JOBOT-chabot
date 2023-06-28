import time
from jobScraper_Google import find_job_offers_thread_in_Google, get_job_offers_in_Google
from jobScraper_Indeed import find_job_offers_thread_in_Indeed, get_job_offers_in_Indeed
from jobScraper_JobIsJob import find_job_offers_thread_in_JobIsJob, get_job_offers_in_JobIsJob
from jobScraper_LinkUp import find_job_offers_thread_in_LinkUp, get_job_offers_in_LinkUp
from jobscraper_Monster import find_job_offers_thread_in_Monster, get_job_offers_in_Monster
from jobScraper_SimplyHired import find_job_offers_thread_in_SimplyHired, get_job_offers_in_SimplyHired
from jobScraper_SnagaJob import find_job_offers_thread_in_SnagaJob, get_job_offers_in_SnagaJob


def find_all_job_offers(job_titles, job_locations, job_type):
    # Call each find_job_offers_thread function with the provided parameters
    find_job_offers_thread_in_Google(job_titles, job_locations, job_type)
    time.sleep(1)
    find_job_offers_thread_in_Indeed(job_titles, job_locations, job_type)
    time.sleep(1)
    find_job_offers_thread_in_JobIsJob(job_titles, job_locations, job_type)
    time.sleep(1)
    find_job_offers_thread_in_LinkUp(job_titles, job_locations, job_type)
    time.sleep(1)
    find_job_offers_thread_in_Monster(job_titles, job_locations, job_type)
    time.sleep(1)
    find_job_offers_thread_in_SimplyHired(job_titles, job_locations, job_type)
    time.sleep(1)
    find_job_offers_thread_in_SnagaJob(job_titles, job_locations, job_type)


def get_all_job_offers_await():
    job_offers = []

    job_offers.extend(get_job_offers_in_Google())
    job_offers.extend(get_job_offers_in_Indeed())
    job_offers.extend(get_job_offers_in_JobIsJob())
    job_offers.extend(get_job_offers_in_LinkUp())
    job_offers.extend(get_job_offers_in_Monster())
    job_offers.extend(get_job_offers_in_SimplyHired())
    job_offers.extend(get_job_offers_in_SnagaJob())

    return job_offers


def get_all_job_offers():
    job_offers = []

    job_offers.extend(get_job_offers_in_Google(True))
    job_offers.extend(get_job_offers_in_Indeed(True))
    job_offers.extend(get_job_offers_in_JobIsJob(True))
    job_offers.extend(get_job_offers_in_LinkUp(True))
    job_offers.extend(get_job_offers_in_Monster(True))
    job_offers.extend(get_job_offers_in_SimplyHired(True))
    job_offers.extend(get_job_offers_in_SnagaJob(True))

    return job_offers
