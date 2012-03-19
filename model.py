import re
import web

#db = web.database(dbn='mysql', db='bb', user='root', pw='pass')
import config # ^ this is

def getTopics(fid):
	return db.select('topics', order='id', where='fid='+str(fid))

def getTopic(s, tid):
	return db.where('topics', slug=s, id=tid) 

def getPosts(tid):
	return db.where('posts', order='id', tid=str(tid))

def addTopic(t, b):
	tt = t
        t = t.lower()
	t = re.sub('[\s]+', '-', t)
	t = re.sub(r'[^a-z0-9-]', '', t)
        result = db.insert('topics', uid=1, title=tt, date=1, fid=0, slug=t, replies=0)
        if(result):
		db.update('topics', where='id=%s' % result, last_poster='%s' % 'johndoe')
	        return db.insert('posts', uid=1, body=b, date=1, tid=result)
        else:
                return 'error'
# SLUG TODO
#import re
#topic = topic.lower()
#topic = re.sub('[\s]+', '-', topic)
#topic = re.sub(r'[^a-z0-9-]', '', topic)
#	return 'slug'
#	db.insert(topics, uid=1,title=t, body=b, date=1, fid=0, slug=#TODO)

def addReply(id, reply, userid):
	# TODO LASTPOST
	# db.query('UPDATE LASTPOST ?
	# db.update ?
	replies_update = db.query('UPDATE topics SET replies=replies+1 WHERE id=%s' % id)
        post = db.insert('posts', uid=userid, body=reply, tid=id)
	last_poster = db.update('topics', where='id=%s' % id, last_poster='%s' % 'johndoe')
	return db.update('topics', where='id=%s' % id, last_post='%s' % post)
	#last_post_update = db.update('topics', where='id=%s' % id, last_post='%s' % reply)
#	last_post_update = db.query('UPDATE topics SET last_post=%s WHERE id=%s') % reply, id
#        return db.query('UPDATE topics SET last_post=%s' % reply)
	
#        return db.insert('posts', uid=userid, body=reply, tid=id)

# pid = postid, tid = topic-id
def delPost(pid, tid):
	replies_update = db.query('UPDATE topics SET replies=replies-1 WHERE id=%s' % tid)
	return db.delete('posts', where='id=%s' % pid)

def search(query):
	# match against
	a = db.query('SELECT title FROM topics WHERE MATCH(title) AGAINST (\'*%s*\' IN BOOLEAN MODE)' % query)
	#b = db.query('SELECT body FROM posts WHERE MATCH(body) AGAINST (\'*%s*\' IN BOOLEAN MODE)' % query)
	return a
