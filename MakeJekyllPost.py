import sublime, sublime_plugin
import datetime

header = '''---
layout: post
category : blog
tags : []
---
{% include JB/setup %}
'''

def make_post_date():
	now = datetime.datetime.now()
	file_date = now.strftime("%Y-%m-%d")
	return file_date

def make_file_name(title_input):
	jek_date = make_post_date()
	jek_title = title_input.lower().replace(' ','-')
	jek_file_type = '.md'
	jek_post_title = jek_date + '-' + jek_title + jek_file_type
	return jek_post_title

class MakeJekyllPostCommand(sublime_plugin.WindowCommand):
	
	def on_done(self, title):
		new_post = self.window.new_file()
		post_title = make_file_name(title)
		new_post.set_name(post_title)
		edit = new_post.begin_edit()
		new_post.insert(edit, 0, header)
		new_post.end_edit()

	def run(self):
		self.window.show_input_panel("Post Title:", "", self.on_done, None, None)
