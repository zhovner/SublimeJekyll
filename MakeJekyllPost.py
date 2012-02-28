import sublime, sublime_plugin
import datetime

header = '''---
layout: post
category : blog
tags : []
---
{% include JB/setup %}

'''

code_template = "{%% highlight %s %%} %s {%% endhighlight %%}"

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


def get_syntax(active_view):
	raw_syntax = active_view.settings().get('syntax')
	split_syntax = raw_syntax.split('/') #is this portable across oses?
	view_syntax = split_syntax[1].lower()
	return view_syntax


def create_code_blocks(active_view):
	active_syntax = get_syntax(active_view)
	selections = active_view.sel()

	code_blocks = []

	for selection in selections:
		selected_text = active_view.substr(selection)
		code_chunk = code_template % (active_syntax, selected_text)
		code_blocks.append(code_chunk)

	return code_blocks


def check_for_code_selection(active_view):
	
	check_sels = active_view.sel()

	if len(check_sels) > 1: #there are multiple text selections, assume the use has done this on purpose
		a_syn = get_syntax(active_view)
		code_lines_list = create_code_blocks(active_view)
		return code_lines_list # need to write after end of header
	elif len(check_sels) == 1:
		if check_sels[0].begin() != check_sels[0].end(): #if nothing is selected being==end
			a_syn = get_syntax(active_view)
			code_lines_list = create_code_blocks(active_view)
			return code_lines_list # need to write after end of header


class MakeJekyllPostCommand(sublime_plugin.WindowCommand):
	
	def on_done(self, title):

		a_view = self.window.active_view()

		code_lines = check_for_code_selection(a_view)

		new_post = self.window.new_file()
		post_title = make_file_name(title)
		new_post.set_name(post_title)
		edit = new_post.begin_edit()
		new_post.insert(edit, 0, header)

		offset = 70 # how to get the end of each block inserted and add newline?
		for code_line in code_lines: # if there are no code lines?
			new_post.insert(edit, 70 + offset, header)
			offset = offset + 70

		new_post.end_edit(edit)

	def run(self):
		self.window.show_input_panel("Post Title:", "", self.on_done, None, None)
