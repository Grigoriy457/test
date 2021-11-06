import instaloader
from flask import *
import requests
from PIL import Image
from datetime import datetime
from itertools import dropwhile, takewhile
import sys

users = [['mapen32403', 'dfye56edr572f'], ['kenoji8548', 'aijoi1hdft32'], ['bemeki9259', 'dfye56edr57']]

USERNAME = 'bmw'

user_index = 0

app = Flask(__name__)
s = requests.Session()

def login(data):
	global insta
	user_name, password = data
	print(f'Logging... ({user_name})')
	insta.login(user_name, password)
	print('Successfully logged in')

# class tooManyQueriesError(Exception):
#     def __init__(self, secs):
#         self.secs = str(secs)

#     def __str__(self):
#         if self.secs:
#             return '{0} seconds passed'.format(self.secs)
#         else:
#             return 'tooManyQueriesError has been raised'

# raise tooManyQueriesError('15')

class MyRateController(instaloader.RateController):
    def sleep(self, secs):
        global users, user_index
        # raise tooManyQueriesError(secs)
        user_index += 1
        try:
        	login(users[user_index])
        except:
        	print('<ERROR:> Out of accounts')
        	sys.exit()


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/result')
def result():
	global user_index, insta

	while True:
		print('Выбери тип:')
		print('1) Посты пользователя/группы')
		print('2) Отмеченные у пользователя/группы')
		_type = input('>>> ')
		if _type in ['1', '2']:
			break
		else:
			print('Error, try again!')

	_type = int(_type)
	html_text = ''
	insta = instaloader.Instaloader(rate_controller=lambda ctx: MyRateController(ctx))

	print('Start parsing')

	login(users[user_index])

	profile = instaloader.Profile.from_username(insta.context, USERNAME)

	print()
	print('Business accaunt:', profile.is_business_account)
	print('Subscribers:', profile.followers)
	print()

	SINCE = datetime(2021, 10, 4)
	UNTIL = datetime(2020, 10, 1)

	all_posts = list()
	index = 0
	if _type == 1:
		posts = profile.get_posts()
		for post in posts:#takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
			shortcode = post.shortcode
			caption = post.caption
			if caption != None:
				caption = caption.replace('\n', ' ')
			else:
				caption = ''
			print(f'Post index: {len(all_posts) + 1}')
			print(f'Date: {post.date}')
			print(f'Post url: https://instagram.com/p/{shortcode}/')
			print(f'Post image: {post.mediacount}')
			print(f'Likes: {post.likes}')
			print(f"Description: {caption}")
			print(f'Description hastags: {post.caption_hashtags}')
			print(f'Image url: {post.url}')
			print('=================================')
			print()

			all_posts.append(post)
			index += 1

			img = requests.get(post.url)
			with open(f"static\\images\\{shortcode}.jpg", 'wb') as img_file:
				img_file.write(img.content)
			im = Image.open(f"static\\images\\{shortcode}.jpg")
			im.save(f"static\\images\\{shortcode}.jpg", quality=20)

			html_text += f'<b>Date:</b> {post.date}<br><b><a href="https://instagram.com/p/{shortcode}/" type="_blank">Post url</a></b><br><b>Likes:</b> {post.likes}<br><b>Description:</b> {caption}<br><b>Description hastags:</b> {post.caption_hashtags}<br><b><a href="{post.url}" type="_blank">Image url</a></b><br><b>Image:</b> <img src="/static/images/{shortcode}.jpg" style="width: 200px; height: 200px;"><br><br>'

			# if index >= 500:
			# 	index = 0
			# 	user_index += 1
			# 	login(users[user_index])

			if len(all_posts) >= 1000:
				break
	else:
		tagged_posts = profile.get_tagged_posts()
		for post in tagged_posts:
			shortcode = post.shortcode
			caption = post.caption.replace('\n', ' ')
			print(f'Date: {post.date}')
			print(f'Post url: https://instagram.com/p/{shortcode}/')
			print(f'Post image: {post.mediacount}')
			print(f'Likes: {post.likes}')
			print(f"Description: {caption}")
			print(f'Description hastags: {post.caption_hashtags}')
			print(f'Image url: {post.url}')
			print('=================================')
			print()

			all_posts.append(post)

			img = requests.get(post.url)
			with open(f"static\\images\\{shortcode}.jpg", 'wb') as img_file:
				img_file.write(img.content)

	print('POSTS:', len(all_posts))
	print()

	print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
	print('\t\tThe')
	print('\t\tend')
	print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

	return render_template('result.html')

if __name__ == '__main__':
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(host='0.0.0.0')