from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Sum, Avg, Q
from django.conf import settings
from django.db.models.functions import Coalesce
import json
from .models import ProdukHukum, LogUpdate, DataPotensi
from .serializers import ProdukHukumSerializer, LogUpdateSerializer, DataPotensiSerializer

import pandas as pd
import traceback
from collections import Counter

# Mapping kolom Excel ke model
COLUMN_MAPPING = {
    'LEVEL.1': 'level1', 'LEVEL.2': 'level2', 'LEVEL.3': 'level3', 'LEVEL.4': 'level4',
    **{f'ATURAN.{i}': f'aturan{i}' for i in range(1, 10)},
    **{f'REMARK.{i}': f'remark{i}' for i in range(1, 10)},
    **{f'LINK.{i}': f'link{i}' for i in range(1, 10)},
    **{f'STATUS.{i}': f'status{i}' for i in range(1, 10)}
}

@method_decorator(csrf_exempt, name='dispatch')
class ProdukHukumViewSet(viewsets.ModelViewSet):
    queryset = ProdukHukum.objects.all()
    serializer_class = ProdukHukumSerializer
    parser_classes = (MultiPartParser, FormParser)

    @action(detail=False, methods=['post'], url_path='upload-excel', permission_classes=[AllowAny])
    def upload_excel(self, request):
        try:
            file = request.FILES.get('file')
            if not file:
                return Response({'error': 'File tidak ditemukan'}, status=status.HTTP_400_BAD_REQUEST)

            # Validasi kolom Excel
            required_columns = set(COLUMN_MAPPING.keys())
            uploaded_columns = set(pd.read_excel(file, nrows=0).columns)
            missing_columns = required_columns - uploaded_columns
            if missing_columns:
                return Response({
                    'error': f"Format kolom tidak sesuai. Kolom berikut wajib ada: {', '.join(missing_columns)}"
                }, status=status.HTTP_400_BAD_REQUEST)

            df = pd.read_excel(file).fillna("")
            df.rename(columns=COLUMN_MAPPING, inplace=True)

            uploaded_data = {}
            for _, row in df.iterrows():
                key = tuple(str(row.get(k, '')).strip().lower() for k in ['level1', 'level2', 'level3', 'level4'])
                uploaded_data[key] = row

            old_objects = ProdukHukum.objects.all()
            old_data = {}
            for obj in old_objects:
                key = tuple(str(getattr(obj, k, '')).strip().lower() for k in ['level1', 'level2', 'level3', 'level4'])
                old_data[key] = obj

            for key, row in uploaded_data.items():
                if key in old_data:
                    obj = old_data[key]
                    changed = False
                    for i in range(1, 10):
                        field = f'aturan{i}'
                        old_val = str(getattr(obj, field, '') or '').strip()
                        new_val = str(row.get(field, '') or '').strip()
                        if old_val != new_val:
                            if old_val and not new_val:
                                LogUpdate.objects.create(aksi='Hapus', detail_aksi=f"Menghapus peraturan: '{old_val}' dengan topik {row.get('remark'+str(i), '')}")
                            elif not old_val and new_val:
                                LogUpdate.objects.create(aksi='Tambah', detail_aksi=f"Menambahkan {field}: '{new_val}' dengan topik {row.get('remark'+str(i), '')}")
                            else:
                                LogUpdate.objects.create(aksi='Update', detail_aksi=f"Mengubah peraturan: '{old_val}' menjadi '{new_val}' dengan topik {row.get('remark'+str(i), '')}")
                            setattr(obj, field, new_val)
                            changed = True

                    for suffix in ['remark', 'link', 'status']:
                        for i in range(1, 10):
                            f = f'{suffix}{i}'
                            setattr(obj, f, row.get(f, ''))

                    if changed:
                        obj.save()
                else:
                    new_data = {col: row.get(col, '') for col in COLUMN_MAPPING.values()}
                    ProdukHukum.objects.create(**new_data)
                    for i in range(1, 10):
                        val = str(row.get(f'aturan{i}', '') or '').strip()
                        if val:
                            LogUpdate.objects.create(aksi='Tambah', detail_aksi=f"Menambahkan aturan{i}: '{val}' dengan topik {row.get('remark'+str(i), '')}")

            deleted_keys = set(old_data.keys()) - set(uploaded_data.keys())
            for key in deleted_keys:
                obj = old_data[key]
                for i in range(1, 10):
                    old_val = str(getattr(obj, f'aturan{i}', '') or '').strip()
                    if old_val:
                        LogUpdate.objects.create(aksi='Hapus', detail_aksi=f"Menghapus peraturan: '{old_val}' dengan topik {getattr(obj, f'remark{i}', '')}")
                obj.delete()

            return Response({'message': 'Upload berhasil'}, status=200)

        except Exception as e:
            print("Terjadi error saat upload Excel:", e)
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)

class LogUpdateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogUpdate.objects.all().order_by('-waktu')
    serializer_class = LogUpdateSerializer

class ChartDataView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            produk_list = ProdukHukum.objects.all()

            aturan_set = set()
            sektor_counter = Counter()
            pajak_counter = Counter()
            retribusi_counter = Counter()
            topikumum_counter = Counter()

            for produk in produk_list:
                sektor = None
                if produk.level2 == "Pajak Daerah":
                    sektor = "Pajak Daerah"
                elif produk.level2 == "Retribusi Daerah":
                    sektor = "Retribusi Daerah"
                elif produk.level1 == "Topik Umum":
                    sektor = "Topik Umum"

                for i in range(1, 10):
                    aturan = str(getattr(produk, f'aturan{i}', '') or '').strip()

                    if aturan:
                        key = (sektor, aturan)
                        if key not in aturan_set:
                            aturan_set.add(key)
                            if sektor:
                                sektor_counter[sektor] += 1
                                if sektor == "Pajak Daerah":
                                    pajak_counter[produk.level3] += 1
                                elif sektor == "Retribusi Daerah":
                                    retribusi_counter[produk.level4] += 1
                                elif sektor == "Topik Umum":
                                    topikumum_counter[produk.level3] += 1

            data_chart = {
                "chart_all": {
                    "labels": list(sektor_counter.keys()),
                    "values": list(sektor_counter.values()),
                    "title": "Grafik Distribusi Peraturan Berdasarkan Bidang Sektoral"
                },
                "chart_pajak": {
                    "labels": list(pajak_counter.keys()),
                    "values": list(pajak_counter.values()),
                    "title": "Grafik Peraturan Unik Pajak Daerah"
                },
                "chart_retribusi": {
                    "labels": list(retribusi_counter.keys()),
                    "values": list(retribusi_counter.values()),
                    "title": "Grafik Peraturan Unik Retribusi Daerah"
                },
                "chart_topikumum": {
                    "labels": list(topikumum_counter.keys()),
                    "values": list(topikumum_counter.values()),
                    "title": "Grafik Peraturan Unik Topik Umum"
                }
            }

            return JsonResponse(data_chart)

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

class DataPotensiViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def metadata(self, request):
        provinsi = request.GET.get('provinsi')
        daerah = request.GET.get('daerah')
        tahun = request.GET.get('tahun')
        jenis = request.GET.get('jenis')
        kategori_apbd = request.GET.get('kategori_apbd')

        data = DataPotensi.objects.all()
        if provinsi:
            data = data.filter(provinsi=provinsi)
        if daerah:
            data = data.filter(daerah=daerah)
        if tahun:
            data = data.filter(tahun=int(tahun))
        if jenis:
            data = data.filter(jenis=jenis)
        if kategori_apbd:
            data = data.filter(kategori_apbd__iexact=kategori_apbd)

        anggaran = data.filter(kategori_apbd='Anggaran').values('jenis').annotate(total=Sum('nilai'))
        realisasi = data.filter(kategori_apbd='Realisasi').values('jenis').annotate(total=Sum('nilai'))

        jenis_list = sorted(set([i['jenis'] for i in anggaran] + [i['jenis'] for i in realisasi]))
        dict_anggaran = {i['jenis']: i['total'] for i in anggaran}
        dict_realisasi = {i['jenis']: i['total'] for i in realisasi}

        total_anggaran = sum(item['total'] for item in anggaran)
        total_realisasi = sum(item['total'] for item in realisasi)

        rincian_data = (
            data.values('rincian')
            .annotate(
                anggaran=Coalesce(Sum('nilai', filter=Q(kategori_apbd='Anggaran')), 0),
                realisasi=Coalesce(Sum('nilai', filter=Q(kategori_apbd='Realisasi')), 0)
            )
            .order_by('-realisasi')
        )

        return Response({
            "tahun_list": list(DataPotensi.objects.exclude(tahun__isnull=True).values_list('tahun', flat=True).distinct().order_by('tahun')),
            "provinsi_list": list(DataPotensi.objects.exclude(provinsi__isnull=True).exclude(provinsi='').values_list('provinsi', flat=True).distinct().order_by('provinsi')),
            "daerah_list": list(DataPotensi.objects.filter(provinsi=provinsi).exclude(daerah__isnull=True).exclude(daerah='').values_list('daerah', flat=True).distinct().order_by('daerah')) if provinsi else [],
            "chart_labels": jenis_list,
            "chart_anggaran": [dict_anggaran.get(jenis, 0) for jenis in jenis_list],
            "chart_realisasi": [dict_realisasi.get(jenis, 0) for jenis in jenis_list],
            "total_anggaran": total_anggaran,
            "total_realisasi": total_realisasi,
            "table_data_rinci": list(rincian_data),
        })

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def rincian_by_jenis(self, request):
        provinsi = request.GET.get('provinsi')
        daerah = request.GET.get('daerah')
        tahun = request.GET.get('tahun')
        jenis = request.GET.get('jenis')
        kategori_apbd = request.GET.get('kategori_apbd')

        filters = {}
        if provinsi:
            filters['provinsi'] = provinsi
        if daerah:
            filters['daerah'] = daerah
        if tahun:
            try:
                filters['tahun'] = int(tahun)
            except ValueError:
                return Response({"error": "Tahun tidak valid"}, status=400)
        if jenis:
            filters['jenis'] = jenis
        if kategori_apbd:
            filters['kategori_apbd__iexact'] = kategori_apbd

        data = DataPotensi.objects.filter(**filters).values('rincian').annotate(nilai=Avg('nilai')).order_by('rincian')
        return Response(list(data))

@csrf_exempt
def verify_token(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            token = data.get("token")
            if token == settings.CUSTOM_ACCESS_TOKEN:
                return JsonResponse({"status": "success"}, status=200)
            else:
                return JsonResponse({"status": "unauthorized"}, status=401)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "method_not_allowed"}, status=405)