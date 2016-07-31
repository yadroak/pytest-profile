import pytest
import py

SHOULD_PROFILE_TESTS = False
SHOULD_PRINT_RESULTS = True
SHOULD_STORE_RESULTS = False
BASEDIR = 'stats'

def pytest_addoption(parser):
    general_group = parser.getgroup("general")
    general_group.addoption("--profile-tests",
                            default=False,
                            action="store_true",
                            dest="profile_tests",
                            help="profile test results")
    general_group.addoption("--profile-tests-print",
                            action="store_true",
                            default=True,
                            dest="profile_tests_print",
                            help="print top 50 profiling results as part of the report")
    general_group.addoption("--profile-tests-store",
                            action="store_true",
                            default=False,
                            dest="profile_tests_print",
                            help="create a pickle file under ./stats/")
    parser.addini('profile_test', SHOULD_PROFILE_TESTS)
    parser.addini('profile_tests_print', SHOULD_PRINT_RESULTS)
    parser.addini('profile_tests_store', SHOULD_STORE_RESULTS)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item):
    if SHOULD_PROFILE_TESTS:
        p = Profile()
        p.enable()
        yield
        p.disable()
        stats = Stats(p)
        if SHOULD_PRINT_RESULTS:
            stats.sort_stats('cumulative').print_stats(50)
        if SHOULD_STORE_RESULTS:
            if not os.path.exists(BASEDIR):
                os.mkdir(BASEDIR)
            p.dump_stats(os.path.join(BASEDIR, '%s.pkl' % item.name))
    else:
        yield

