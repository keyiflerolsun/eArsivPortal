# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from eArsivPortal import eArsivPortal
from pydantic.v1  import BaseModel

def test_bilgilerim():
    portal     = eArsivPortal()
    bilgilerim = portal.bilgilerim()

    portal.cikis_yap()

    assert isinstance(bilgilerim, BaseModel)

def test_fatura_olustur():
    portal = eArsivPortal()
    fatura = portal.fatura_olustur(
        tarih         = "29/05/2023",
        saat          = "14:28:37",
        vkn_veya_tckn = "11111111111",
        ad            = "Ömer Faruk",
        soyad         = "Sancak",
        unvan         = "",
        vergi_dairesi = "",
        urun_adi      = "Python Yazılım Hizmeti",
        fiyat         = 100,
        fatura_notu   = "— QNB Finansbank —\nTR70 0011 1000 0000 0118 5102 59\nÖmer Faruk Sancak"
    )

    portal.cikis_yap()

    assert isinstance(fatura.ettn, str)

def test_fatura_sorgu():
    portal     = eArsivPortal()

    faturalar = portal.faturalari_getir(
        baslangic_tarihi = "29/05/2023",
        bitis_tarihi     = "29/05/2023"
    )

    portal.cikis_yap()

    assert isinstance(faturalar[0], BaseModel)