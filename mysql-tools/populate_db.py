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
	"""
	Generate a random string of <length>
	"""
	lst = [random.choice(string.ascii_letters) for n in xrange(length)]
	return "".join(lst)

def generate_id():
	"""
	Get a very long int based on tiem since epoch
	"""
	# This will take time in nanoseconds, and present it as a large int
	return int(time.time()*1000000)

def main():
	"""
	This is the schema used for the test table in test database
	CREATE TABLE test (
	                   id BIGINT NOT NULL AUTO_INCREMENT,
	                   data INT,
	                   data2 VARCHAR(20)
	                   PRIMARY KEY (id)
	                   ) CHARSET=utf8;
	"""

	# Creating the database connection
	connection = MySQLdb.connect (host = "127.0.0.1", user = "test", passwd = "army01", db = "test")

	num = 100 #number of rows to add

	information = "Populating database with %d rows: " % (num) # some info on the conole
	sys.stdout.write(information)
	sys.stdout.flush()

	for i in range(1, num):
		if i % (num/10) == 0: # Will write a progress bar each 1/10th of the progress
			progress = "%d.." % (i)
			sys.stdout.write(progress)
			sys.stdout.flush() # Flushing on each iteration, to make sure it goes to console

		cursor = connection.cursor()

		random_data2 = phrase(1) # Getting a word

		for attempt_number in range(3): # Doing x attempts before throwing error
			try:

				cursor.execute("INSERT INTO test(data, data2) VALUES (%s, %s)",  (random.randint(1,9), random_data2))
				connection.commit()
				break
			except MySQLdb.Error, e:
				print "MySQL Error %d: %s" % (e.args[0], e.args[1])

		time.sleep(.5) # Sleeping for half a second before each insert, this is not a benchmark

	cursor.close()
	connection.close()
	sys.exit()


if __name__ == '__main__':
	main()