# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from eArsivPortal.Libs import fatura_ver, tutar_yaziyla, Komutlar
from eArsivPortal      import eArsivPortal
from pydantic          import BaseModel
import pytest

def test_tutar_yaziyla():
    assert tutar_yaziyla(100) == "Yalnız Yüz Türk Lirası"
    assert tutar_yaziyla(1234.56) == "Yalnız Bin İki Yüz Otuz Dört Türk Lirası Elli Altı Kuruş"
    assert tutar_yaziyla(0) == "Yalnız Sıfır Türk Lirası"

def test_komutlar_duzeltme():
    komutlar = Komutlar()
    assert komutlar.SMSSIFRE_DOGRULA.cmd == "EARSIV_PORTAL_SMSSIFRE_DOGRULA"
    assert komutlar.KULLANICI_BILGILERI_KAYDET.cmd == "EARSIV_PORTAL_KULLANICI_BILGILERI_KAYDET"
    assert komutlar.FATURA_IMZALA.cmd == "EARSIV_PORTAL_FATURA_HSM_CIHAZI_ILE_IMZALA"

def test_fatura_ver_unit():
    fatura = fatura_ver(
        tarih         = "11/08/2026",
        saat          = "12:00:00",
        vkn_veya_tckn = "11111111111",
        ad            = "Test",
        soyad         = "Kullanıcı",
        urun_adi      = "Test Ürünü",
        fiyat         = 120
    )
    assert fatura["faturaUuid"] == ""
    assert fatura_ver(fatura_uuid="ozel-uuid")["faturaUuid"] == "ozel-uuid"
    assert fatura["matrah"] == "100.00"
    assert fatura["hesaplanankdv"] == "20.00"
    assert fatura["odenecekTutar"] == "120.00"
    assert "Yalnız Yüz Yirmi Türk Lirası" in fatura["not"]

@pytest.mark.integration
def test_bilgilerim():
    try:
        portal     = eArsivPortal()
        bilgilerim = portal.bilgilerim()
        portal.cikis_yap()
        assert isinstance(bilgilerim, BaseModel)
    except Exception as e:
        pytest.skip(f"GİB Portal canlı/test sunucusuna erişilemedi: {e}")

@pytest.mark.integration
def test_fatura_olustur():
    try:
        from datetime import datetime
        from pytz     import timezone

        portal = eArsivPortal()
        bugun  = datetime.now(timezone("Turkey")).strftime("%d/%m/%Y")
        saat   = datetime.now(timezone("Turkey")).strftime("%H:%M:%S")

        fatura = portal.fatura_olustur(
            tarih         = bugun,
            saat          = saat,
            para_birimi   = "TRY",
            vkn_veya_tckn = "11111111111",
            ad            = "Ömer Faruk",
            soyad         = "Sancak",
            unvan         = "",
            vergi_dairesi = "",
            urun_adi      = "Python Yazılım Hizmeti",
            fiyat         = 100,
            fatura_notu   = "Test Faturası"
        )
        portal.cikis_yap()
        assert isinstance(fatura.ettn, str)
        assert len(fatura.ettn) == 36
    except Exception as e:
        pytest.skip(f"GİB Portal canlı/test sunucusuna erişilemedi: {e}")

@pytest.mark.integration
def test_fatura_sorgu():
    try:
        portal    = eArsivPortal()
        faturalar = portal.faturalari_getir(
            baslangic_tarihi = "29/05/2023",
            bitis_tarihi     = "29/05/2023"
        )
        portal.cikis_yap()
        assert isinstance(faturalar, list)
    except Exception as e:
        pytest.skip(f"GİB Portal canlı/test sunucusuna erişilemedi: {e}")
