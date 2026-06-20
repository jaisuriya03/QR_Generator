import io,base64
from flask import Flask, request, send_file, render_template
import segno

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    url_data = request.form.get('url_data')
    wifi_ssid = request.form.get('wifi_ssid')
    geo_lat = request.form.get('latitude')
    
    payload = ""
    qr_type = "qr"

    if url_data!="":
        payload = url_data
        qr_type = "url"
        
    elif wifi_ssid!="":
        wifi_pass = request.form.get('wifi_pass')
        payload = f"WIFI:T:WPA;S:{wifi_ssid};P:{wifi_pass};;"
        qr_type = "wifi"
        
    elif geo_lat!="":
        geo_lon = request.form.get('longitude')
        payload = f"geo:{geo_lat.strip()},{geo_lon.strip()}"
        qr_type = "location"

    if not payload:
        return "Error: Please fill out the required information fields before generating.", 400

    qr = segno.make(payload, error='H')

    buffer = io.BytesIO()
    qr.save(buffer, kind='png', scale=10, dark='#000000', light='#ffffff')
    buffer.seek(0)

    qr_bytes=buffer.getvalue()
    base64_qr=base64.b64encode(qr_bytes).decode('utf-8')

    return render_template('index.html', qr_image=base64_qr, qr_type=qr_type)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
