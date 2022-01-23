#!/usr/bin/env python3

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

if __name__ == "__main__":

	my_parser = argparse.ArgumentParser()
	my_parser.add_argument('-e', '--email', help='Your archive.org email', type=str, required=True)
	my_parser.add_argument('-p', '--password', help='Your archive.org password', type=str, required=True)
	my_parser.add_argument('-u', '--url', help='Link to the book (https://archive.org/details/XXXX). You can use this argument several times to download multiple books', action='append', type=str)
	my_parser.add_argument('-f', '--file', help='File where are stored the URLs of the books to download', type=str)
	my_parser.add_argument('-r', '--resolution', help='Image resolution (10 to 0, 0 is the highest), [default 3]', type=int, default=3)
	my_parser.add_argument('-t', '--threads', help="Maximum number of threads, [default 50]", type=int, default=50)
	my_parser.add_argument('-j', '--jpg', help="Output to individual JPG's rather then a PDF", action='store_true')
	if len(sys.argv) == 1:
		my_parser.print_help(sys.stderr)
		sys.exit(1)
	args = my_parser.parse_args()

	if args.url is None and args.file is None:
		my_parser.error("At least one of --url and --file required")

	email = args.email
	password = args.password
	scale = args.resolution
	n_threads = args.threads

	if args.url is not None:
		urls = args.url
	else:
		if os.path.exists(args.file):
			with open(args.file) as f:
				urls = f.read().strip().split("\n")
		else:
			print(f"{args.file} does not exist!")
			exit()

	# Check the urls format
	for url in urls:
		if not url.startswith("https://archive.org/details/"):
			print(f"{url} --> Invalid url. URL must starts with \"https://archive.org/details/\"")
			exit()

	print(f"{len(urls)} Book(s) to download")
	session = login(email, password)

	for url in urls:
		book_id = list(filter(None, url.split("/")))[-1]
		print("="*40)
		print(f"Current book: {url}")
		session = loan(session, book_id)
		title, links = get_book_infos(session, url)

		directory = os.path.join(os.getcwd(), title)
		if not os.path.isdir(directory):
			os.makedirs(directory)

		images = download(session, n_threads, directory, links, scale, book_id)

		if not args.jpg: # Create pdf with images and remove the images folder
			pdf = img2pdf.convert(images)
			make_pdf(pdf, title)
			try:
				shutil.rmtree(directory)
			except OSError as e:
				print ("Error: %s - %s." % (e.filename, e.strerror))

		return_loan(session, book_id)
