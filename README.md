# 🧾 eArsivPortal

[![Boyut](https://img.shields.io/github/repo-size/keyiflerolsun/eArsivPortal?logo=git&logoColor=white&label=Boyut)](#)
[![Görüntülenme](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/keyiflerolsun/eArsivPortal&title=Görüntülenme)](#)
<a href="https://KekikAkademi.org/Kahve" target="_blank"><img src="https://img.shields.io/badge/☕️-Kahve Ismarla-ffdd00" title="☕️ Kahve Ismarla" style="padding-left:5px;"></a>

[![PyPI Yükleyici](https://img.shields.io/github/actions/workflow/status/keyiflerolsun/eArsivPortal/PyPI.yml?label=PyPI%20Y%C3%BCkleyici&logo=github)](https://github.com/keyiflerolsun/eArsivPortal/actions/workflows/PyPI.yml)

[![PyPI](https://img.shields.io/pypi/v/eArsivPortal?logo=pypi&logoColor=white&label=PyPI)](https://pypi.org/project/eArsivPortal)
[![PyPI - Yüklenme](https://img.shields.io/pypi/dm/eArsivPortal?logo=pypi&logoColor=white&label=Yüklenme)](https://pypi.org/project/eArsivPortal)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/eArsivPortal?logo=pypi&logoColor=white&label=Wheel)](https://pypi.org/project/eArsivPortal)

[![Python Version](https://img.shields.io/pypi/pyversions/eArsivPortal?logo=python&logoColor=white&label=Python)](#)
[![Lisans](https://img.shields.io/pypi/l/eArsivPortal?logo=gnu&logoColor=white&label=Lisans)](#)
[![Durum](https://img.shields.io/pypi/status/eArsivPortal?logo=windowsterminal&logoColor=white&label=Durum)](#)

*GİB e-Arşiv Portal e-Fatura Oluşturucu*

> Bu paket [Fatih Kadir Akın](https://github.com/f)'ın hazırlamış olduğu [fatura](https://github.com/f/fatura) `(js)` paketinin `Python` dili ile yazılmış versiyonudur.

[![ForTheBadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![ForTheBadge built-with-love](https://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/keyiflerolsun/)

## 🚀 Kurulum

### <a href="#"><img width="16" src="https://raw.githubusercontent.com/keyiflerolsun/eArsivPortal/main/.github/icons/pypi.svg"></a> PyPI

```bash
# Yüklemek
pip install eArsivPortal

# Güncellemek
pip install -U eArsivPortal
```

## 📝 Kullanım

### <a href="#"><img width="16" src="https://raw.githubusercontent.com/keyiflerolsun/eArsivPortal/main/.github/icons/python.svg"></a> Lib

```python
from eArsivPortal import eArsivPortal

portal = eArsivPortal(
    kullanici_kodu = "33333301",
    sifre          = "1",
    test_modu      = True
)
```

```python
portal.bilgilerim()
#--------------------------------------------------------------#
{
    "vknTckn": "3333333301",
    "unvan": "HOSAM ALDEEN ABUSHAWER TİCARİ GİRİŞİMİ",
    "ad": "",
    "soyad": "",
    "cadde": "şehit yusuf bey",
    "apartmanAdi": "yıldız",
    "apartmanNo": "8",
    "kapiNo": "2",
    "kasaba": "ortakapı",
    "ilce": "Merkez",
    "il": "Kars",
    "postaKodu": "36000",
    "ulke": "Türkiye",
    "telNo": "05524775288",
    "faksNo": "",
    "ePostaAdresi": "",
    "webSitesiAdresi": "",
    "vergiDairesi": "kars",
    "sicilNo": "8729",
    "isMerkezi": "",
    "mersisNo": "9962438036000001"
}
```

```python
portal.kisi_getir(vkn_veya_tckn="3333333301")
#--------------------------------------------------------------#
{
    "unvan":"HOSAM ALDEEN ABUSHAWER TİCARİ GİRİŞİMİ",
    "adi":"",
    "soyadi":"",
    "vergiDairesi":"kars"
}
```

```python
portal.fatura_olustur(
    tarih:str         = "07/10/1995",
    saat:str          = "14:28:37",
    vkn_veya_tckn:str = "11111111111",
    ad:str            = "Ömer Faruk",
    soyad:str         = "Sancak",
    unvan:str         = "",
    vergi_dairesi:str = "",
    urun_adi:str      = "Python Yazılım Hizmeti",
    fiyat:int | float = 100,
    fatura_notu:str   = "— QNB Finansbank —\nTR70 0011 1000 0000 0118 5102 59\nÖmer Faruk Sancak"
)
#--------------------------------------------------------------#
{"ettn": "b40c16ae-8509-434e-bd6f-894459372134"}
```

```python
faturalar = portal.faturalari_getir(
    baslangic_tarihi = "01/05/2023",
    bitis_tarihi     = "28/05/2023"
)
#--------------------------------------------------------------#
[
    {
        'belgeNumarasi': 'GIB2023000002672',
        'aliciVknTckn': '16045751784',
        'aliciUnvanAdSoyad': 'Sercan AYDIN',
        'belgeTarihi': '28-05-2023',
        'belgeTuru': 'FATURA',
        'onayDurumu': 'Onaylanmadı',
        'ettn': '0c111c74-fcd4-11ed-8026-3ae56703837b'
    },
    {
        'belgeNumarasi': 'GIB2023000002673',
        'aliciVknTckn': '16045751784',
        'aliciUnvanAdSoyad': 'Sercan AYDIN',
        'belgeTarihi': '28-05-2023',
        'belgeTuru': 'FATURA',
        'onayDurumu': 'Silinmiş',
        'ettn': '234baa8e-fcd5-11ed-827f-3ae56703837b'
    }
]
```

```python
html_fatura = portal.fatura_html(
    ettn        = faturalar[0].get("ettn")
    onay_durumu = faturalar[0].get("onayDurumu")
)

with open(f"{faturalar[0].get("aliciUnvanAdSoyad")}.html", "w", encoding="utf-8") as dosya:
    dosya.write(html_fatura)
```

```python
portal.fatura_sil(
    faturalar = [faturalar[0], faturalar[1]]
    aciklama  = "Fatura silindi."
)
#--------------------------------------------------------------#
2 fatura başarıyla silindi.
```

```python
oid = portal.gib_imza()
portal.gib_sms_onay(faturalar[3], oid, input("SMS Doğrulama Kodu: "))
```

```python
portal.cikis_yap()
```

## 🌐 Telif Hakkı ve Lisans

* *Copyright (C) 2023 by* [keyiflerolsun](https://github.com/keyiflerolsun) ❤️️
* [GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007](https://github.com/keyiflerolsun/eArsivPortal/blob/master/LICENSE) *Koşullarına göre lisanslanmıştır..*

## ♻️ İletişim

*Benimle iletişime geçmek isterseniz, **Telegram**'dan mesaj göndermekten çekinmeyin;* [@keyiflerolsun](https://t.me/KekikKahve)

## 💸 Bağış Yap

**[☕️ Kahve Ismarla](https://KekikAkademi.org/Kahve)**

***

> **[@KekikAkademi](https://t.me/KekikAkademi)** *için yazılmıştır..*