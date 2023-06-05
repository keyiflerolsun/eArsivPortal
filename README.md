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

Bilgilerim(
    vknTckn='3333333315',
    unvan='XYZ Yaz',
    ad='',
    soyad='',
    cadde='Sahil yolu',
    apartmanAdi='Dali çıtır pide',
    apartmanNo='12',
    kapiNo='3',
    kasaba='adana',
    ilce='GEMLİK',
    il='Antalya',
    postaKodu='16000',
    ulke='Türkiye',
    telNo='053982456665',
    faksNo='',
    ePostaAdresi='info@vekamp.com',
    webSitesiAdresi='',
    vergiDairesi='orhangazi vergi dairesi',
    sicilNo='00000000000000',
    isMerkezi='',
    mersisNo=''
)
```

```python
portal.kisi_getir(vkn_veya_tckn="3333333301")

#--------------------------------------------------------------#

Kisi(
    unvan='XYZ Yaz',
    adi='',
    soyadi='',
    vergiDairesi='orhangazi vergi dairesi'
)
```

```python
portal.fatura_olustur(
    tarih         = "07/10/1995",
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

#--------------------------------------------------------------#

FaturaOlustur(ettn='8cb401e3-ca6d-442a-8389-894459372134')
```

```python
faturalar = portal.faturalari_getir(
    baslangic_tarihi = "01/05/2023",
    bitis_tarihi     = "28/05/2023"
)

#--------------------------------------------------------------#

[
    Fatura(
        belgeNumarasi='GIB2023000002672',
        aliciVknTckn='16045751784',
        aliciUnvanAdSoyad='Sercan AYDIN',
        belgeTarihi='29-05-2023',
        belgeTuru='FATURA',
        onayDurumu='Silinmiş',
        ettn='7386c1dc-8a23-4d46-9c8d-de3512b630b4'
    ),
    Fatura(
        belgeNumarasi='GIB2023000001918',
        aliciVknTckn='16045751784',
        aliciUnvanAdSoyad='Sercan AYDIN',
        belgeTarihi='29-05-2023',
        belgeTuru='FATURA',
        onayDurumu='Onaylanmadı',
        ettn='2ef98bfa-8787-4429-a1fa-a0514560e7eb'
    ),
    Fatura(
        belgeNumarasi='GIB2023000001919',
        aliciVknTckn='16045751784',
        aliciUnvanAdSoyad='Sercan AYDIN',
        belgeTarihi='29-05-2023',
        belgeTuru='FATURA',
        onayDurumu='Onaylandı',
        ettn='8cb401e3-ca6d-442a-8389-c4d87c9eb67c'
    )
]
```

```python
html_fatura = portal.fatura_html(
    ettn        = faturalar[0].ettn
    onay_durumu = faturalar[0].onayDurumu
)

with open(f"{faturalar[0].aliciUnvanAdSoyad}.html", "w", encoding="utf-8") as dosya:
    dosya.write(html_fatura)
```

```python
portal.fatura_sil(
    faturalar = [faturalar[0], faturalar[1]]
    aciklama  = "Fatura silindi."
)

#--------------------------------------------------------------#

FaturaSil(mesaj='2 fatura başarıyla silindi.')
```

```python
imza = portal.gib_imza()
portal.gib_sms_onay(
    faturalar = faturalar[3],
    oid       = imza.oid,
    sifre     = input("SMS Doğrulama Kodu: ")
)

#--------------------------------------------------------------#

GibSMSOnay(mesaj='SMS şifreniz doğrulandı, işlem başarılı.')
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