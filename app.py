from flask import Flask, render_template, request
from downloader_functions import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    email = request.form['email']
    password = request.form['password']
    book_id = request.form['book_id']
    directory = request.form['directory']
    
    session = login(email, password)
    session = loan(session, book_id)
    title, links, num_pages = get_book_infos(session, url)
    
    os.makedirs(directory, exist_ok=True)
    
    with futures.ThreadPoolExecutor() as executor:
        to_do = []
        for i, link in enumerate(links):
            future = executor.submit(download_one_image, session, link, i, directory, book_id)
            to_do.append(future)
            if (i+1)%10==0 or (i+1)==len(links):
                for future in tqdm(to_do, desc=f"Downloading {title} ({i-len(to_do)+1}-{i+1})", total=len(to_do), unit="img"):
                    pass
                to_do = []

    images = [f"{directory}/{i}.jpg" for i in range(num_pages)]
    pdf_bytes = img2pdf.convert(images)
    make_pdf(pdf_bytes, title)
    
    return f"El archivo PDF de {title} se ha descargado exitosamente en {directory}"

if __name__ == '__main__':
    app.run(debug=True)
