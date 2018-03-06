# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import sqlite3
import random
import time
try:
	import schedule
except:
	print "[x] Need schedule"

web_dir = "F:\\phpStudy\\WWW\\"
words_per_day = 30
db = "database.db"
total = 19752	

def gen_html():
	# Get words
	result = []
	conn = sqlite3.connect(db)
	c = conn.cursor()

	while(len(result) < words_per_day):
		word_id = random.randint(1,total)
		cursor = c.execute("SELECT FREQUENCY, WORD, EXPLANATION, FLAG FROM words WHERE ID =" + str(word_id))
		value = cursor.fetchall()
		# print value[0][0]
		if value[0][3] == 0:
			result.append(value[0])
			c.execute("UPDATE words SET FLAG = 1 WHERE ID = " + str(word_id))

	# Write into HTML
	file_name = time.strftime('%Y-%m-%d',time.localtime(time.time())) + ".html"
	f = open(web_dir + file_name,"w+")
	data = "<h2>" + time.strftime('%Y-%m-%d',time.localtime(time.time())) + "</h1>"

	for r in result:
		data += "<h3>" + str(r[1]) + "\t|\t" + str(r[0]) +"</h3>"
		data += "</br>"
		data += str(r[2])
		data += "</br>"
	f.write(data)
	f.close()

	i = open(web_dir + "index.html", "a+")
	i.write('<a href="./' + file_name + '">' + time.strftime('%Y-%m-%d',time.localtime(time.time())) +'</a> &nbsp;')

	print "[*] File Generated: " + file_name

# schedule.every(1).seconds.do(gen_html)
schedule.every().day.at("8:00").do(gen_html)

index_file = open(web_dir + "index.html","a+")
index_file.write("<h2>Contents</h2>")
index_file.close()


while True:
	schedule.run_pending()
	time.sleep(1)


# <a href="./2018-03-05.html">2018-03-06</a>