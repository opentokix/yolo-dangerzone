#!/usr/bin/python
import MySQLdb
import sys
import random
import string
import time
import re

# Or "/usr/share/dict/words" if you prefer it
WORDS_FILE = "/usr/share/dict/cracklib-small"

with open(WORDS_FILE, "r") as __fp:
    __all_words = __fp.readlines()
__all_words = [__x.strip() for __x in __all_words]


def phrase(no_words=2):
	"""
	Generate a phrase with no_words randomly chosen words from WORDS_FILE
	"""
	words = " ".join(random.sample(__all_words, no_words))
	return re.sub(r'\W+', '', words)

def uniquePhrases(no_phrases):
    """

    Generate no_phrases unique phrases, 2-5 words long.

    >>> for p in random_words.uniquePhrases(4):  # doctest: +SKIP
    >>>    print p
    rodgers drawings wheeled adumbrating residentially
    lockstep astute
    pianissimo satire's
    roadster workman intoxicated
    """

    phrases = set()
    while len(phrases) < no_phrases:
        this_phrase = phrase(random.randint(2,5))
        if this_phrase not in phrases:
            phrases.add(this_phrase)
            yield this_phrase

def r_string(length):
	lst = [random.choice(string.ascii_letters) for n in xrange(length)]
	return "".join(lst)

def generate_id():
	# This will take time in nanoseconds, and present it as a large int
	return int(time.time()*1000000)

def main():
	connection = MySQLdb.connect (host = "127.0.0.1", user = "test", passwd = "test", db = "test")


	num = 100
	information = "Populating database with %d rows: " % (num)
	sys.stdout.write(information)
	sys.stdout.flush()

	for i in range(1, num):
		if i % (num/10) == 0:
			progress = "%d.." % (i)
			sys.stdout.write(progress)
			sys.stdout.flush()

		cursor = connection.cursor()
		time_id = generate_id()
		random_data = r_string(2)
		random_data2 = phrase(1)
		for attempt_number in range(3):
			try:
				cursor.execute("INSERT INTO test(data, data2) VALUES ('%d', '%s')" % (random.randint(1,9), random_data2))
				connection.commit()
				break
			except MySQLdb.Error, e:
				print "MySQL Error %d: %s" % (e.args[0], e.args[1])

		time.sleep(.5)

	cursor.close()
	connection.close()
	sys.exit()


if __name__ == '__main__':
	main()