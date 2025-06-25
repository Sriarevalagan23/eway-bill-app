from flask import Flask, render_template, request, send_file, redirect, url_for, session
from weasyprint import HTML
import tempfile
from num2words import num2words
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form.to_dict()
        data['qty'] = float(data['qty'])
        data['price'] = float(data['price'])
        data['subtotal'] = round(data['qty'] * data['price'], 2)
        data['gst'] = round(data['subtotal'] * 0.18, 2)
        data['total'] = round(data['subtotal'] + data['gst'], 2)
        data['total_words'] = num2words(data['total'], to='currency', lang='en_IN').replace('euro', 'Rupees').title()
        data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').strftime('%d %b %Y').upper()

        session['bill_data'] = data
        return redirect(url_for('preview'))
    return render_template('form.html')

@app.route('/preview')
def preview():
    data = session.get('bill_data')
    if not data:
        return redirect(url_for('index'))
    return render_template('bill.html', data=data)

@app.route('/download')
def download():
    data = session.get('bill_data')
    if not data:
        return redirect(url_for('index'))
    html = render_template('bill.html', data=data)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        HTML(string=html).write_pdf(f.name)
        return send_file(f.name, as_attachment=True, download_name="eway_bill.pdf")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)


