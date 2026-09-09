# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from .KurGetir   import kurGetir
from .TutarMetin import tutar_yaziyla

def fatura_ver(
    tarih:str         = "07/10/1995",
    saat:str          = "14:28:37",
    para_birimi:str   = "TRY",
    vkn_veya_tckn:str = "11111111111",
    ad:str            = "Ömer Faruk",
    soyad:str         = "Sancak",
    unvan:str         = "",
    vergi_dairesi:str = "",
    urun_adi:str      = "Python Yazılım Hizmeti",
    fiyat:int | float = 100,
    fatura_notu:str   = "— QNB Finansbank —\nTR70 0011 1000 0000 0118 5102 59\nÖmer Faruk Sancak",
    fatura_uuid:str   = "",
    fatura_tipi:str   = "SATIS",
    kdv_orani:int     = 20,
    kalemler:list[dict] = None
):
    fatura_uuid = fatura_uuid or ""
    doviz       = "0" if para_birimi == "TRY" else str(kurGetir(para_birimi) or "0")

    if kalemler:
        mal_hizmet_table = kalemler
        toplam_matrah    = sum(float(k.get("malHizmetTutari", 0)) for k in kalemler)
        toplam_kdv       = sum(float(k.get("kdvTutari", 0)) for k in kalemler)
        toplam_iskonto   = sum(float(k.get("iskontoTutari", 0)) for k in kalemler)
        odenecek_tutar   = toplam_matrah + toplam_kdv - toplam_iskonto
    else:
        kdv_bolen      = 1 + (kdv_orani / 100)
        matrah         = fiyat / kdv_bolen
        kdv            = fiyat - matrah
        toplam_matrah  = matrah
        toplam_kdv     = kdv
        toplam_iskonto = 0.0
        odenecek_tutar = matrah + kdv

        mal_hizmet_table = [
            {
                "malHizmet"                     : urun_adi,
                "miktar"                        : 1,
                "birim"                         : "C62",
                "birimFiyat"                    : f"{round(matrah, 2):.2f}",
                "fiyat"                         : f"{round(matrah, 2):.2f}",
                "iskontoOrani"                  : 0,
                "iskontoTutari"                 : "0.00",
                "iskontoNedeni"                 : "",
                "malHizmetTutari"               : f"{round(matrah, 2):.2f}",
                "kdvOrani"                      : str(kdv_orani),
                "vergiOrani"                    : 0,
                "kdvTutari"                     : f"{round(kdv, 2):.2f}",
                "vergininKdvTutari"             : "0.00",
                "ozelMatrahTutari"              : "0.00",
                "hesaplananotvtevkifatakatkisi" : "0.00",
            }
        ]

    not_metni = fatura_notu
    yaziyla   = tutar_yaziyla(odenecek_tutar)
    if yaziyla not in not_metni:
        not_metni = f"{not_metni}\n{yaziyla}" if not_metni else yaziyla

    return {
        "faturaUuid"               : fatura_uuid,
        "belgeNumarasi"            : "",
        "faturaTarihi"             : tarih,
        "saat"                     : saat,
        "paraBirimi"               : para_birimi,
        "dovzTLkur"                : doviz,
        "faturaTipi"               : fatura_tipi,
        "hangiTip"                 : "5000/30000",
        "vknTckn"                  : vkn_veya_tckn,
        "aliciUnvan"               : unvan,
        "aliciAdi"                 : ad,
        "aliciSoyadi"              : soyad,
        "binaAdi"                  : "",
        "binaNo"                   : "",
        "kapiNo"                   : "",
        "kasabaKoy"                : "",
        "vergiDairesi"             : vergi_dairesi,
        "ulke"                     : "Türkiye",
        "bulvarcaddesokak"         : "",
        "irsaliyeNumarasi"         : "",
        "irsaliyeTarihi"           : "",
        "mahalleSemtIlce"          : "",
        "sehir"                    : " ",
        "postaKodu"                : "",
        "tel"                      : "",
        "fax"                      : "",
        "eposta"                   : "",
        "websitesi"                : "",
        "iadeTable"                : [],
        "vergiCesidi"              : " ",
        "malHizmetTable"           : mal_hizmet_table,
        "tip"                      : "İskonto",
        "matrah"                   : f"{round(toplam_matrah, 2):.2f}",
        "malhizmetToplamTutari"    : f"{round(toplam_matrah, 2):.2f}",
        "toplamIskonto"            : f"{round(toplam_iskonto, 2):.2f}",
        "hesaplanankdv"            : f"{round(toplam_kdv, 2):.2f}",
        "vergilerToplami"          : f"{round(toplam_kdv, 2):.2f}",
        "vergilerDahilToplamTutar" : f"{round(odenecek_tutar, 2):.2f}",
        "odenecekTutar"            : f"{round(odenecek_tutar, 2):.2f}",
        "not"                      : not_metni,
        "siparisNumarasi"          : "",
        "siparisTarihi"            : "",
        "fisNo"                    : "",
        "fisTarihi"                : "",
        "fisSaati"                 : " ",
        "fisTipi"                  : " ",
        "zRaporNo"                 : "",
        "okcSeriNo"                : "",
    }
