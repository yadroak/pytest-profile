from cProfile import Profile
from pstats import Stats
import pytest
import py
import os
import time

SHOULD_PROFILE = None
SHOULD_PRINT = None
SHOULD_STORE = None
BASEDIR = 'stats'

def pytest_addoption(parser):
    general_group = parser.getgroup("general")
    general_group.addoption("--profile-tests",
                            action="store_true",
                            dest="profile_tests",
                            default=False,
                            help="profile test results")
    general_group.addoption("--profile-tests-print",
                            action="store_true",
                            default=True,
                            dest="profile_tests_print",
                            help="print top 50 profiling results as part of the report")
    general_group.addoption("--profile-tests-store",
                            action="store_true",
                            default=False,
                            dest="profile_tests_store",
                            help="create a pickle file under ./stats/")

def pytest_configure(config):
    global SHOULD_PROFILE, SHOULD_PRINT, SHOULD_STORE, TIMEOUT
    SHOULD_PROFILE = config.option.profile_tests
    SHOULD_PRINT = config.option.profile_tests_print
    SHOULD_STORE = config.option.profile_tests_store


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    if SHOULD_PROFILE:
        p = Profile()
        p.enable()
        yield
        p.disable()
        stats = Stats(p)
        if SHOULD_PRINT:
            stats.sort_stats('cumulative').print_stats(50)
        if SHOULD_STORE:
             if not os.path.exists(BASEDIR):
                os.mkdir(BASEDIR)
             p.dump_stats(os.path.join(BASEDIR, '%s.pkl' % item.name))
    else:
        yield

