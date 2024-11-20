# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from ..Libs      import legacy_session, Komut, Komutlar, fatura_ver
from requests    import Response
from json        import dumps
from uuid        import uuid4
from parsel      import Selector
from .Hatalar    import GirisYapilmadi, OturumSuresiDoldu, eArsivPortalHatasi

from datetime    import datetime
from pytz        import timezone

from pydantic.v1 import create_model, BaseModel

class eArsivPortal:
    def __init__(self, kullanici_kodu:str="33333315", sifre:str="1", test_modu:bool=True):

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

        self.token = None
        self.giris_yap()

    def __nesne_ver(self, isim, veri) -> BaseModel:
        __nesne = create_model(isim, **veri)

        return __nesne(**veri)

    def __istek_ayristir(self, istek:Response, veri:dict) -> dict | str | Exception:
        if istek.status_code != 200 or veri.get("error"):
            veri_mesaj = veri["messages"][0]
            hata_metni = veri_mesaj["text"] if isinstance(veri_mesaj, dict) else veri_mesaj

            if "Oturum zamanaşımına uğradı" in hata_metni:
                raise OturumSuresiDoldu(hata_metni)

            raise eArsivPortalHatasi(hata_metni)

        return veri

    def giris_yap(self) -> bool | eArsivPortalHatasi:
        istek = self.oturum.post(
            url  = f"{self.url}/earsiv-services/assos-login",
            data = {
                "assoscmd" : "login" if self.test_modu else "anologin",
                "rtype"    : "json",
                "userid"   : self.kullanici_kodu,
                "sifre"    : self.sifre,
                "sifre2"   : self.sifre,
                "parola"   : "1"
            }
        )
        veri = istek.json()
        self.token = self.__istek_ayristir(istek, veri)["token"]
        return self.token is not None

    def cikis_yap(self) -> bool | eArsivPortalHatasi:
        if not self.token:
            raise GirisYapilmadi("Giriş yapmadan çıkış yapamazsınız!")

        istek = self.oturum.post(
            url  = f"{self.url}/earsiv-services/assos-login",
            data = {
                "assoscmd" : "logout",
                "rtype"    : "json",
                "token"    : self.token
            }
        )
        if istek.status_code != 200:
            return False

        self.token = None
        return True

    def __kod_calistir(self, komut:Komut, jp:dict):
        if not self.token:
            raise GirisYapilmadi("Giriş yapmadan işlem yapamazsınız!")

        try:
            istek = self.oturum.post(
                url  = f"{self.url}/earsiv-services/dispatch",
                data = {
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

    def bilgilerim(self) -> BaseModel:
        istek = self.__kod_calistir(
            komut = self.komutlar.KULLANICI_BILGILERI_GETIR,
            jp    = {}
        )
        veri  = istek.get("data")

        return self.__nesne_ver("Bilgilerim", veri)

    def kisi_getir(self, vkn_veya_tckn:str) -> BaseModel:
        try:
            istek = self.__kod_calistir(
                komut = self.komutlar.MERNISTEN_BILGILERI_GETIR,
                jp    = {
                    "vknTcknn" : vkn_veya_tckn
                }
            )
            veri  = istek.get("data")
        except Exception:
            veri  = {"unvan": None, "adi": None, "soyadi": None, "vergiDairesi": None}

        return self.__nesne_ver("Kisi", veri)

    def fatura_olustur(
        self,
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
        fatura_notu:str   = "— QNB Finansbank —\nTR70 0011 1000 0000 0118 5102 59\nÖmer Faruk Sancak"
    ) -> BaseModel:
        kisi_bilgi = self.kisi_getir(vkn_veya_tckn)

        fatura = fatura_ver(
            tarih         = tarih or datetime.now(timezone("Turkey")).strftime("%d/%m/%Y"),
            saat          = saat,
            para_birimi   = para_birimi,
            vkn_veya_tckn = vkn_veya_tckn,
            ad            = kisi_bilgi.adi or ad,
            soyad         = kisi_bilgi.soyadi or soyad,
            unvan         = kisi_bilgi.unvan or unvan,
            vergi_dairesi = kisi_bilgi.vergiDairesi or vergi_dairesi,
            urun_adi      = urun_adi,
            fiyat         = fiyat,
            fatura_notu   = fatura_notu
        )

        while True:
            istek = self.__kod_calistir(
                komut = self.komutlar.FATURA_OLUSTUR,
                jp    = fatura
            )

            ettn = None
            if "Faturanız başarıyla oluşturulmuştur." in istek.get("data"):
                ettn = fatura.get("faturaUuid")
                break

            print(f"{fatura.get('aliciAdi')} {fatura.get('aliciSoyadi')} | {istek.get('data')} | Yeniden Deneniyor..")

        return self.__nesne_ver("FaturaOlustur", {"ettn": ettn})

    def faturalari_getir(self, baslangic_tarihi:str="01/05/2023", bitis_tarihi:str="28/05/2023") -> list[BaseModel]:
        istek = self.__kod_calistir(
            komut = self.komutlar.TASLAKLARI_GETIR,
            jp    = {
                "baslangic" : baslangic_tarihi or datetime.now(timezone("Turkey")).strftime("%d/%m/%Y"),
                "bitis"     : bitis_tarihi or datetime.now(timezone("Turkey")).strftime("%d/%m/%Y"),
                "hangiTip"  :"5000/30000",
                "table"     : []
            }
        )
        veri  = istek.get("data")

        return [self.__nesne_ver("Fatura", fatura) for fatura in veri]

    def fatura_html(self, ettn:str, onay_durumu:str) -> str:
        istek = self.__kod_calistir(
            komut = self.komutlar.FATURA_GOSTER,
            jp    = {
                "ettn"       : ettn,
                "onayDurumu" : onay_durumu
            }
        )
        veri  = istek.get("data")

        secici = Selector(veri)

        for tr in secici.xpath("//tr"):
            bos_tdler = tr.xpath(".//td[normalize-space(.)='\xa0']")

            if len(bos_tdler) == len(tr.xpath(".//td")):
                tr_element = tr.root
                tr_element.getparent().remove(tr_element)

        for td in secici.xpath("//td[@align='right' and @class='lineTableTd']"):
            if td.xpath("string(.)").get().strip() in ["%0,00", "0,00 TL", "İskonto -"]:
                td_element = td.root
                td_element.text = ""

        return secici.extract()

    def __fatura_ver(self, faturalar) -> list[dict] | Exception:
        if not isinstance(faturalar, list):
            faturalar = [faturalar]

        payload = []
        for fatura in faturalar:
            if isinstance(fatura, dict):
                payload.append(fatura)
            elif isinstance(fatura, list):
                payload.extend(fatura)
            else:
                payload.append(fatura.dict())

        return payload

    def fatura_sil(self, faturalar:list[dict] | dict, aciklama:str) -> BaseModel:
        istek = self.__kod_calistir(
            komut = self.komutlar.FATURA_SIL,
            jp    = {
                "silinecekler" : self.__fatura_ver(faturalar),
                "aciklama"     : aciklama
            }
        )

        return self.__nesne_ver("FaturaSil", {"mesaj": istek.get("data")})

    def gib_imza(self) -> BaseModel:
        telefon_istek = self.__kod_calistir(
            komut = self.komutlar.TELEFONNO_SORGULA,
            jp    = {}
        )
        telefon_veri = telefon_istek.get("data")
        telefon_no   = telefon_veri.get("telefon")
        if not telefon_no:
            return self.__nesne_ver("GibImza", {"oid": None})

        sms_gonder = self.__kod_calistir(
            komut = self.komutlar.SMSSIFRE_GONDER,
            jp    = {
                "CEPTEL"  : telefon_no,
                "KCEPTEL" : False,
                "TIP"     : ""
            }
        )
        print(f"\n[~] {telefon_no} numarasına SMS gönderildi.\n")

        return self.__nesne_ver("GibImza", sms_gonder.get("data"))

    def gib_sms_onay(self, faturalar:list[dict] | dict, oid:str, sifre:str) -> BaseModel:
        istek = self.__kod_calistir(
            komut = self.komutlar.SMSSIFRE_DOGRULA,
            jp    = {
                "SIFRE" : sifre,
                "OID"   : oid,
                "OPR"   : 1,
                "DATA"  : self.__fatura_ver(faturalar),
            }
        )
        veri  = istek.get("data")

        return self.__nesne_ver("GibSMSOnay", {"mesaj": veri.get("msg")})

    def satınalma_faturalari_getir(self, baslangic_tarihi:str="01/05/2023", bitis_tarihi:str="28/05/2023", hourlySearch:str="NONE") -> list[BaseModel]:
        istek = self.__kod_calistir(
            komut = self.komutlar.ADIMA_KESILEN_BELGELERI_GETIR,
            jp    = {
                "baslangic"            : baslangic_tarihi or datetime.now(timezone("Turkey")).strftime("%d/%m/%Y"),
                "bitis"                : bitis_tarihi or datetime.now(timezone("Turkey")).strftime("%d/%m/%Y"),
                "hourlySearchInterval" : hourlySearch,
                "table"                : []
            }
        )
        veri  = istek.get("data")

        return [self.__nesne_ver("Fatura", fatura) for fatura in veri]

    # TODO: https://github.com/mlevent/fatura 'dan faydalanarak geri kalan fonksiyonlar yazılacaktır..