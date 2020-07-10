from ua_parser import user_agent_parser

def os(parseString):
    os = parseString['os']['family']
    return os

def os_version(parseString):
    # os version
    os_version = parseString['os']['major']
    if parseString['os']['minor'] != None:
        os_version += ".{}".format(parseString['os']['minor'])
    if parseString['os']['patch'] != None:
        os_version += ".{}".format(parseString['os']['patch'])
    return os_version

def browser(parseString):
    browser = parseString['user_agent']['family']
    return browser

def browser_version(parseString):
    browser_version = parseString['user_agent']['major']
    if parseString['user_agent']['minor'] != None:
        browser_version += ".{}".format(parseString['user_agent']['minor'])
    if parseString['user_agent']['patch'] != None:
        browser_version += ".{}".format(parseString['user_agent']['patch'])
    return browser_version