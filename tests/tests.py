'''
	Run with:
		python example_tests.py TARGET_NAME TESTER_TOKEN
'''

import sys
import dismock

# The tests themselves

testcollector = dismock.TestCollector()

@testcollector()
async def test_ping(interface):
	await interface.assert_reply_equals('.ping', 'pong!')

# Make it easy to run the tests

if __name__ == '__main__':
	target_name = "InfiniBot Unit Tests"
	with open('testbot.token.txt', 'r') as f:
         token = f.read()
	dismock.run_interactive_bot(target_name, token, testcollector)
