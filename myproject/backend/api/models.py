from django.db import models

class ProdukHukum(models.Model):
    file = models.CharField(max_length=100, null=True, blank=True)
    level1 = models.CharField(max_length=255, null=True, blank=True)
    level2 = models.CharField(max_length=255, null=True, blank=True)
    level3 = models.CharField(max_length=255, null=True, blank=True)
    level4 = models.CharField(max_length=255, null=True, blank=True)

    aturan1 = models.TextField(null=True, blank=True)
    remark1 = models.TextField(null=True, blank=True)
    link1 = models.URLField(null=True, blank=True)
    status1 = models.URLField(null=True, blank=True)

    aturan2 = models.TextField(null=True, blank=True)
    remark2 = models.TextField(null=True, blank=True)
    link2 = models.URLField(null=True, blank=True)
    status2 = models.URLField(null=True, blank=True)

    aturan3 = models.TextField(null=True, blank=True)
    remark3 = models.TextField(null=True, blank=True)
    link3 = models.URLField(null=True, blank=True)
    status3 = models.URLField(null=True, blank=True)

    aturan4 = models.TextField(null=True, blank=True)
    remark4 = models.TextField(null=True, blank=True)
    link4 = models.URLField(null=True, blank=True)
    status4 = models.URLField(null=True, blank=True)

    aturan5 = models.TextField(null=True, blank=True)
    remark5 = models.TextField(null=True, blank=True)
    link5 = models.URLField(null=True, blank=True)
    status5 = models.URLField(null=True, blank=True)

    aturan6 = models.TextField(null=True, blank=True)
    remark6 = models.TextField(null=True, blank=True)
    link6 = models.URLField(null=True, blank=True)
    status6 = models.URLField(null=True, blank=True)

    aturan7 = models.TextField(null=True, blank=True)
    remark7 = models.TextField(null=True, blank=True)
    link7 = models.URLField(null=True, blank=True)
    status7 = models.URLField(null=True, blank=True)

    aturan8 = models.TextField(null=True, blank=True)
    remark8 = models.TextField(null=True, blank=True)
    link8 = models.URLField(null=True, blank=True)
    status8 = models.URLField(null=True, blank=True)

    aturan9 = models.TextField(null=True, blank=True)
    remark9 = models.TextField(null=True, blank=True)
    link9 = models.URLField(null=True, blank=True)
    status9 = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'produk_hukum'


class LogUpdate(models.Model):
    waktu = models.DateTimeField(auto_now_add=True)
    aksi = models.CharField(max_length=100)
    detail_aksi = models.TextField()

    def __str__(self):
        return f"{self.waktu} - {self.aksi} - {self.detail_aksi}"
    
    class Meta:
        db_table = 'log_update'

class DataPotensi(models.Model):
    rincian = models.TextField()
    objek = models.CharField()
    jenis = models.CharField()
    provinsi = models.CharField()
    daerah = models.CharField()
    kategori_apbd = models.CharField()
    tahun = models.IntegerField()
    nilai = models.BigIntegerField()

    class Meta:
        db_table = 'data_potensi'