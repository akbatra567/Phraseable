from flask import Flask, render_template, request, send_file
import PyPDF2
import os.path
import zipfile36 as zipfile

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', isFileSubmitted=False)


@app.route('/multi', methods=['GET', 'POST'])
def multi_file():
    if request.method == 'POST':
        file = request.files['file']
        start = int(request.form['start'])
        end = int(request.form['end'])

        filename = os.path.splitext(file.filename)[0]
        extension = os.path.splitext(file.filename)[1]

        if extension == ".pdf":
            # pdf writer object
            pdf_writer = PyPDF2.PdfFileWriter()
            # pdf reader object
            pdf_reader = PyPDF2.PdfFileReader(file)
            start = start - 1
            end = end
            for i in range(start, end):
                pdf_writer.addPage(pdf_reader.getPage(i))

            newFile = "static/data/" + filename + '_extracted' + extension
            with open(newFile, 'wb') as fh:
                pdf_writer.write(fh)
            return render_template('index.html', isFileSubmitted=True, fileName=newFile)

        return render_template('index.html', isFileSubmitted=False, error='File not pdf')


@app.route('/single', methods=['GET', 'POST'])
def single_file():
    if request.method == 'POST':
        pdf = request.files['pdf']
        name = os.path.splitext(pdf.filename)[0]
        extension_file = os.path.splitext(pdf.filename)[1]

        if extension_file == ".pdf":
            zipp = name + ".zip"
            zipobj = zipfile.ZipFile(zipp, 'w')
            # pdf reader object
            pdfreader = PyPDF2.PdfFileReader(pdf)
            last = pdfreader.getNumPages()
            for count in range(0, last):
                # pdf writer object
                pdfwriter = PyPDF2.PdfFileWriter()
                pdfwriter.addPage(pdfreader.getPage(count))
                newfiles = "static/data/" + name + str(count) + ".pdf"
                with open(newfiles, 'wb') as filehead:
                    pdfwriter.write(filehead)
                zipobj.write(newfiles)

            zipobj.close()

            return render_template('index.html', isFileSubmitted=True, fileName=zipp)

        return render_template('index.html', isFileSubmitted=False, error='File not pdf')


@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'GET':
        files_ = request.args.get("file")
    try:
        return send_file(files_)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
