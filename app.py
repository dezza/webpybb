import web
from web import form
import model

import markdown

urls = (
	'/', 'test',
	'/bb', 'index',				# Index
	'/bb/topic/(\d+)-([a-z0-9-]+)', 'view',	# View Topic
	'/bb/topic/new', 'new',			# New Topic
	'/bb/reply/(\d+)-([a-z0-9-]+)', 'add', 	# Reply
	'/bb/search/results', 'search'		# Search
)

### Templates
render = web.template.render('templates/',base='base',globals={'mark':markdown.markdown})
formSearch = form.Form(form.Textbox('q', description=''),form.Button('search'))
#formNewPost = form.Form(
#			form.Textarea('reply',description='Reply:'),
#			form.Button('Reply'),
                        
#)
class test:
    def GET(self):
        return render.test('titel-og-kage')

class index:
    def GET(self):	# form (search)
        topics = model.getTopics(0)
        return render.forum('index',formSearch,topics)
    def POST(self):
        form = search()
	if form.validates():
		return 'searching ..'
	# search query

# Index
class view:
    def GET(self, tid, slug):
	# +1 VIEW
	# TODO FUTURE
	posts = model.getPosts(tid)
	topic = model.getTopic(slug, tid)
	if(posts and topic):
            return render.view(topic[0].title,formSearch, posts, tid, slug)
        else:
            return 'wrong topic'
# Add Reply (Post)
class add:
    def POST(self, id, slug):
	i = web.input()
	q = model.addReply(id, i.reply, 1)
	# TODO
	# +1 reply paa id
	# TODO
	
	#return "done"
	raise web.seeother('/bb/topic/'+id+'-'+slug)	

# New Topic
class new:
    def GET(self):
        return render.new('New Topic',formSearch)
    def POST(self):
	i = web.input()
	q = model.addTopic(i.title, i.b)
	raise web.redirect('/bb')

# Search
class search:
    def POST(self):
	i = web.input()
	q = i.q
	results = model.search(q)
	return render.search('Search',formSearch,results)
 
app = web.application(urls, globals())
if __name__ == '__main__': app.run()
