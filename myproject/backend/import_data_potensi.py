import os
import django
import pandas as pd

# 1. Set path dan setting
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# 2. Import model
from api.models import DataPotensi

# 3. Lokasi file Excel
excel_path = '../backend/data/04 data rincian PDRD.xlsx'

# 4. Baca file Excel
try:
    df = pd.read_excel(excel_path, sheet_name='data')
except Exception as e:
    print(f"❌ Gagal membaca Excel: {e}")
    exit()

print("📊 Kolom Excel:", df.columns.tolist())

# 5. Simpan ke database
sukses = 0
gagal = 0

for _, row in df.iterrows():
    try:
        DataPotensi.objects.create(
            rincian=row.get('4_Rincian') or '',
            objek=row.get('3_Objek') or '',
            jenis=row.get('2_Jenis') or '',
            provinsi=row.get('Provinsi') or '',
            daerah=row.get('Daerah') or '',
            kategori_apbd=row.get('APBD') or '',
            tahun=int(row.get('Tahun')) if not pd.isna(row.get('Tahun')) else 0,
            nilai=int(row.get('Nilai')) if not pd.isna(row.get('Nilai')) else 0
        )
        sukses += 1
    except Exception as e:
        print(f"❌ Gagal insert baris: {row.to_dict()}")
        print(f"   Error: {e}")
        gagal += 1

print(f"✅ Selesai! {sukses} baris berhasil, {gagal} gagal.")
