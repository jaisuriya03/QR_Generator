import io
from flask import Flask, request, send_file, render_template_string
import segno

app = Flask(__name__)

# Open and load your pure HTML/CSS code into memory
with open("templates/index.html", "r", encoding="utf-8") as f:
    HTML_FORM = f.read()

@app.route('/')
def home():
    return render_template_string(HTML_FORM)

@app.route('/generate', methods=['POST'])
def generate():
    # 1. Capture all possible incoming fields from our HTML form
    url_data = request.form.get('url_data')
    wifi_ssid = request.form.get('wifi_ssid')
    geo_lat = request.form.get('latitude')
    
    payload = ""
    qr_type = "qr"

    # 2. Determine which option was filled out by checking for text presence
    if url_data!="":
        payload = url_data
        qr_type = "url"
        
    elif wifi_ssid!="":
        wifi_pass = request.form.get('wifi_pass')
        payload = f"WIFI:T:WPA;S:{wifi_ssid};P:{wifi_pass};;"
        qr_type = "wifi"
        
    elif geo_lat!="":
        geo_lon = request.form.get('longitude')
        # Standardized global geo URI scheme syntax
        payload = f"geo:{geo_lat.strip()},{geo_lon.strip()}"
        qr_type = "location"

    # Safety gate in case user hits submit on empty input fields
    if not payload:
        return "Error: Please fill out the required information fields before generating.", 400

    # 3. Create the matrix map structure 
    # High error capacity 'H' format ensures extreme scan resilience
    qr = segno.make(payload, error='H')

    # 4. Burn picture file straight into system RAM memory space
    buffer = io.BytesIO()
    qr.save(buffer, kind='png', scale=10, dark='#000000', light='#ffffff')
    buffer.seek(0)

    # 5. Serve the generated graphic directly back down to user desktop
    return send_file(
        buffer,
        mimetype='image/png',
        as_attachment=True,
        download_name=f'qrcode_{qr_type}.png'
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
