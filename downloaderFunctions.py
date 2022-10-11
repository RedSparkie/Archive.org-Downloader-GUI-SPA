import requests
import random, string
from concurrent import futures
from tqdm import tqdm
import img2pdf
import time
import argparse
import os
import sys
import shutil


def get_book_infos(session, url):
	r = session.get(url).text
	infos_url = "https:" + r.split('bookManifestUrl="')[1].split('"\n')[0]
	response = session.get(infos_url)
	data = response.json()['data']
	title = data['brOptions']['bookTitle'].strip().replace(" ", "_")
	title = ''.join( c for c in title if c not in '<>:"/\\|?*' ) # Filter forbidden chars in directory names (Windows & Linux)
	title = title[:150] # Trim the title to avoid long file names
	links = []
	for item in data['brOptions']['data']:
		for page in item:
			links.append(page['uri'])

	if len(links) > 1:
		print(f"[+] Found {len(links)} pages")
		return title, links, len(links)
	else:
		print("[-] Error while getting image links")
		return 1, 1

def format_data(content_type, fields):
	data = ""
	for name, value in fields.items():
		data += f"--{content_type}\x0d\x0aContent-Disposition: form-data; name=\"{name}\"\x0d\x0a\x0d\x0a{value}\x0d\x0a"
	data += content_type+"--"
	return data

def login(email, password):
	session = requests.Session()
	session.get("https://archive.org/account/login")
	content_type = "----WebKitFormBoundary"+"".join(random.sample(string.ascii_letters + string.digits, 16))

	headers = {'Content-Type': 'multipart/form-data; boundary='+content_type}
	data = format_data(content_type, {"username":email, "password":password, "submit_by_js":"true"})

	response = session.post("https://archive.org/account/login", data=data, headers=headers)
	if "bad_login" in response.text:
		print("[-] Invalid credentials!")
		return 1
	elif "Successful login" in response.text:
		print("[+] Successful login")
		return session
	else:
		print("[-] Error while login:")
		print(response)
		print(response.text)
		return 2

def loan(session, book_id, verbose=True):
	data = {
		"action": "grant_access",
		"identifier": book_id
	}
	response = session.post("https://archive.org/services/loans/loan/searchInside.php", data=data)
	data['action'] = "browse_book"
	response = session.post("https://archive.org/services/loans/loan/", data=data)
	data['action'] = "create_token"
	response = session.post("https://archive.org/services/loans/loan/", data=data)

	if "token" in response.text:
		if verbose:
			print("[+] Successful loan")
		return session
	else:
		print("Something went wrong when trying to borrow the book, maybe you can't borrow this book")
		print(response)
		print(response.text)
		exit()

def return_loan(session, book_id):
	data = {
		"action": "return_loan",
		"identifier": book_id
	}
	r = session.post("https://archive.org/services/loans/loan/", data=data)
	if r.status_code == 200 and r.json()["success"]:
		print("[+] Book returned")
	else:
		print("Something went wrong when trying to return the book")
		print(r)
		print(r.text)
		exit()

def download_one_image(session, link, i, directory, book_id):
	headers = {
		"Referer": "https://archive.org/",
		"Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
		"Sec-Fetch-Site": "same-site",
		"Sec-Fetch-Mode": "no-cors",
		"Sec-Fetch-Dest": "image",
	}
	retry = True
	while retry:
		try:
			response = session.get(link, headers=headers)
			if response.status_code == 403:
				session = loan(session, book_id, verbose=False)
				raise Exception("Borrow again")
			elif response.status_code == 200:
				retry = False
		except:
			time.sleep(1)	# Wait 1 second before retrying

	image = f"{directory}/{i}.jpg"
	with open(image,"wb") as f:
		f.write(response.content)

def make_pdf(pdf, title):
	file = title+".pdf"
	# Handle the case where multiple books with the same name are downloaded
	i = 1
	while os.path.isfile(file):
		file = f"{title}({i}).pdf"
		i += 1

	with open(file,"wb") as f:
		f.write(pdf)
	print(f"[+] PDF saved as \"{title}.pdf\"")

def parse_urls(urls):
	url_list = []
	url_list = urls.split("\n")
	# remove excessive newlines in list
	for url in url_list:
		if len(url) == 0:
			url_list.remove(url)
	return url_list
