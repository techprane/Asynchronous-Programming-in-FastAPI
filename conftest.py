def pytest_terminal_summary(terminalreporter, exitstatus, config):
    # Get the test results (passed, failed, skipped)
    passed = terminalreporter.stats.get('passed', [])
    failed = terminalreporter.stats.get('failed', [])
    
    # Output each result in a separate line
    for test in passed:
        terminalreporter.write_line(f"{test.nodeid} PASSED")
    for test in failed:
        terminalreporter.write_line(f"{test.nodeid} FAILED")
