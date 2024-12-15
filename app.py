from flask import Flask, render_template, request
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Konfigurasi Google Sheets
def init_gspread():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Path ke file JSON kredensial
    creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Hoki Apps/credentials/credentials.json', scope)
    client = gspread.authorize(creds)
    return client

def hitung_hoki(nama):
    huruf = nama[:3].upper()
    hoki = sum(ord(char) - ord('A') + 1 for char in huruf if 'A' <= char <= 'Z')
    
    tanggal = datetime.now().day
    bulan = datetime.now().month
    
    total_hoki = hoki + tanggal + bulan
    return min(total_hoki, 99)

def pesan_hoki(hoki):
    if hoki < 50:
        return "Waduh bre, mungkin lu hari ini kurang hoki. Coba lain kali ya!"
    elif hoki < 80:
        return "Lumayan juga hoki lu, semoga beruntung ya hari ini"
    else:
        return "Gede banget woi hoki lu, gaslah jalan-jalan"

@app.route('/', methods=['GET', 'POST'])
def index():
    hasil_hoki = None
    warna = None
    pesan = None
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1QkwAa5UCy0Q1hyZE-ohBUy7GLSK7ulFU0pghIbG8On4/edit"  # Link spreadsheet Anda
    if request.method == 'POST':
        nama = request.form['nama']
        hoki_akhir = hitung_hoki(nama)
        hasil_hoki = hoki_akhir
        
        if hoki_akhir < 50:
            warna = "oramge"
        elif hoki_akhir < 80:
            warna = "blue"
        else:
            warna = "green"
        
        pesan = pesan_hoki(hoki_akhir)

        # Simpan data ke Google Sheets
        client = init_gspread()
        sheet = client.open_by_key('1QkwAa5UCy0Q1hyZE-ohBUy7GLSK7ulFU0pghIbG8On4').sheet1  # ID spreadsheet Anda
        sheet.append_row([nama, hoki_akhir, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    return render_template('index.html', hasil_hoki=hasil_hoki, warna=warna, pesan=pesan, spreadsheet_url=spreadsheet_url)

if __name__ == '__main__':
    app.run(debug=True)