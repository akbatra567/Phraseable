from flask import Flask, render_template, request, send_file
import PyPDF2
import os.path

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', isFileSubmitted=False)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
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
            pdfReader = PyPDF2.PdfFileReader(file)
            start = start - 1
            end = end
            for i in range(start, end):
                # pdfReader.getPage(i)
                pdf_writer.addPage(pdfReader.getPage(i))

            newFile = filename + '_extracted' + extension

            with open(newFile, 'wb') as fh:
                pdf_writer.write(fh)

            return render_template('index.html', isFileSubmitted=True, fileName=newFile)

        return render_template('index.html', isFileSubmitted=False, error='File not pdf')


@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'GET':
        filename2 = request.args.get("file")
    try:
        return send_file(filename2)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
