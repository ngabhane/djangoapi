# import json
# with open('/home/nikhil/Downloads/imdb.json') as json_data:
# 	d = json.load(json_data)
# 	print d
# 	print '-------------------------------------------------'

# import json
# import sqlite3

# traffic = json.load(open('/home/nikhil/Downloads/imdb.json'))

# db = sqlite3.connect("db.sqlite3")

# query = "insert into movies_other values (?,?,?,?,?)"
# columns = ['popularity99', 'director', 'genre', 'imdb_score', 'name']
# i = 1
# for data in traffic:
# 	data['genre'] = ','.join(data['genre'])
# 	keys = tuple(data[c] for c in columns)
# 	c = db.cursor()
# 	c.execute(query, keys)
#  	c.close()

import json
import sqlite3

traffic = json.load(open('/home/nikhil/Downloads/imdb.json'))
db = sqlite3.connect("db.sqlite3")

# query = "insert into movies_movie values (?,?,?,?,?,?)"
# columns = ['id', 'popularity99', 'director', 'genre', 'imdb_score', 'name']
# i=1
# for data in traffic:
# 	data['genre']  = ','.join(data['genre'])
# 	data['id'] = i
# 	i += 1
# 	keys = tuple(data[c] for c in columns)
# 	c = db.cursor()
# 	c.execute(query, keys)
# 	c.close()
# db.commit()
# db.close()

query = 'SELECT * FROM movies_movie'
c = db.cursor()
n = c.execute(query)
# print c.fetchone()
for t in n:
	print t
	print "\n"
c.close()