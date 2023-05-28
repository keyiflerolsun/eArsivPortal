# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from ..Libs   import legacy_session, Komut, Komutlar, fatura_ver
from requests import Response
from json     import dumps
from uuid     import uuid4
from parsel   import Selector
from .Hatalar import GirisYapilmadi, OturumSuresiDoldu, eArsivPortalHatasi

from datetime import datetime
from pytz     import timezone

class eArsivPortal:
    def __init__(self, kullanici_kodu:str="33333301", sifre:str="1", test_modu:bool=True):

        self.kullanici_kodu = kullanici_kodu
        self.sifre          = sifre
        self.test_modu      = test_modu

        apiler = {
            "YAYIN" : "https://earsivportal.efatura.gov.tr",     # * https://earsivportal.efatura.gov.tr/intragiris.html
            "TEST"  : "https://earsivportaltest.efatura.gov.tr"  # * https://earsivportaltest.efatura.gov.tr/login.jsp
        }

        self.url      = apiler["TEST" if test_modu else "YAYIN"]
        self.oturum   = legacy_session()
        self.komutlar = Komutlar()

        self.oturum.headers.update({
            "User-Agent" : "https://github.com/keyiflerolsun/eArsivPortal"
        })

        self.__giris_yap(kullanici_kodu, sifre)

    def __istek_ayristir(self, istek:Response, veri:dict) -> dict | Exception:
        if istek.status_code != 200 or veri.get("error"):
            try:
                hata_metni = veri["messages"][0]["text"]
            except TypeError:
                hata_metni = veri["messages"][0]

            if "Oturum zamanaşımına uğradı" in hata_metni:
                raise OturumSuresiDoldu(hata_metni)

            raise eArsivPortalHatasi(hata_metni)

        return veri

    def __giris_yap(self, kullanici_kodu:str, sifre:str) -> bool | eArsivPortalHatasi:
        istek = self.oturum.post(
            url     = f"{self.url}/earsiv-services/assos-login",
            data    = {
                "assoscmd" : "login" if self.test_modu else "anologin",
                "rtype"    : "json",
                "userid"   : kullanici_kodu,
                "sifre"    : sifre,
                "sifre2"   : sifre,
                "parola"   : "1"
            }
        )
        veri = istek.json()
        self.token = self.__istek_ayristir(istek, veri)["token"]
        return self.token is not None

    def __kod_calistir(self, komut:Komut, jp:dict):
        if not self.token:
            raise GirisYapilmadi("Giriş yapmadan fatura oluşturamazsınız!")

        try:
            istek = self.oturum.post(
                url     = f"{self.url}/earsiv-services/dispatch",
                data    = {
                    "cmd"      : komut.cmd,
                    "callid"   : f"{uuid4()}",
                    "pageName" : komut.sayfa,
                    "token"    : self.token,
                    "jp"       : dumps(jp)
                }
            )
            veri = istek.json()

            return self.__istek_ayristir(istek, veri)
        except OturumSuresiDoldu:
            self.__giris_yap(self.kullanici_kodu, self.sifre)
            return self.__kod_calistir(komut, jp)

    def bilgilerim(self) -> dict:
        veri = self.__kod_calistir(
            komut = self.komutlar.KULLANICI_BILGILERI_GETIR,
            jp    = {}
        )

        return veri.get("data")

    def kisi_getir(self, vkn_veya_tckn:str):
        veri = self.__kod_calistir(
            komut = self.komutlar.MERNISTEN_BILGILERI_GETIR,
            jp    = {
                "vknTckn" : vkn_veya_tckn
            }
        )

        return veri.get("data")

    def fatura_olustur(
        self,
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
    ) -> bool:
        kisi_bilgi = self.kisi_getir(vkn_veya_tckn)

        veri = self.__kod_calistir(
            komut = self.komutlar.FATURA_OLUSTUR,
            jp    = fatura_ver(
                tarih         = tarih or datetime.now(timezone("Turkey")).strftime("%d/%m/%Y"),
                saat          = saat,
                vkn_veya_tckn = vkn_veya_tckn,
                ad            = kisi_bilgi.get("adi") or ad,
                soyad         = kisi_bilgi.get("soyadi") or soyad,
                unvan         = kisi_bilgi.get("unvan") or unvan,
                vergi_dairesi = kisi_bilgi.get("vergiDairesi") or vergi_dairesi,
                urun_adi      = urun_adi,
                fiyat         = fiyat,
                fatura_notu   = fatura_notu
            )
        )

        return "Faturanız başarıyla oluşturulmuştur." in veri.get("data")

    def faturalari_getir(self, baslangic_tarihi:str="01/05/2023", bitis_tarihi:str="28/05/2023") -> list[dict]:
        veri = self.__kod_calistir(
            komut = self.komutlar.TASLAKLARI_GETIR,
            jp    =     {
                "baslangic" : baslangic_tarihi,
                "bitis"     : bitis_tarihi or datetime.now(timezone("Turkey")).strftime("%d/%m/%Y"),
                "hangiTip"  :"5000/30000",
                "table"     : []
            }
        )

        return veri.get("data")

    def fatura_html(self, ettn:str, onay_durumu:str) -> str:
        veri = self.__kod_calistir(
            komut = self.komutlar.FATURA_GOSTER,
            jp    = {
                "ettn"       : ettn,
                "onayDurumu" : onay_durumu
            }
        )

        secici = Selector(veri.get("data"))

        for tr in secici.xpath("//tr"):
            bos_tdler = tr.xpath(".//td[normalize-space(.)='\xa0']")

            if len(bos_tdler) == len(tr.xpath(".//td")):
                tr_element = tr.root
                tr_element.getparent().remove(tr_element)

        return secici.extract()


    # TODO: https://github.com/mlevent/fatura 'dan faydalanarak geri kalan fonksiyonlar yazılacaktır..