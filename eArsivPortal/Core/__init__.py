# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from ..Libs       import legacy_session, Komut, Komutlar, fatura_ver
from requests     import Response
from json         import dumps
from uuid         import uuid4
from parsel       import Selector
from urllib.parse import quote
from .Hatalar     import GirisYapilmadi, OturumSuresiDoldu, eArsivPortalHatasi

from datetime import datetime
from pytz     import timezone

from typing   import Any
from pydantic import create_model, BaseModel

class eArsivPortal:
    def __init__(self, kullanici_kodu:str="33333315", sifre:str="1", test_modu:bool=True):

        self.kullanici_kodu = kullanici_kodu
        self.sifre          = sifre
        self.test_modu      = test_modu

        apiler = {
            "YAYIN" : "https://earsivportal.efatura.gov.tr",  # * https://earsivportal.efatura.gov.tr/intragiris.html
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
        if isinstance(veri, str):
            veri = {"mesaj": veri}
        elif not isinstance(veri, dict):
            veri = {"veri": veri}
        fields  = {k: (type(v) if v is not None else Any, v) for k, v in veri.items()}
        __nesne = create_model(isim, **fields)

        return __nesne()

    def __istek_ayristir(self, istek:Response, veri:dict) -> dict | str | Exception:
        if istek.status_code != 200 or (isinstance(veri, dict) and veri.get("error")):
            messages = veri.get("messages", []) if isinstance(veri, dict) else []
            if messages:
                veri_mesaj = messages[0]
                hata_metni = veri_mesaj.get("text") if isinstance(veri_mesaj, dict) else str(veri_mesaj)
            else:
                hata_metni = "GİB API hatası oluştu."

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
        veri       = istek.json()
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
            self.giris_yap()
            return self.__kod_calistir(komut, jp)

    def bilgilerim(self) -> BaseModel:
        istek = self.__kod_calistir(
            komut = self.komutlar.KULLANICI_BILGILERI_GETIR,
            jp    = {}
        )
        veri  = istek.get("data")

        return self.__nesne_ver("Bilgilerim", veri)

    def bilgileri_guncelle(self, bilgiler: dict | BaseModel) -> BaseModel:
        if isinstance(bilgiler, BaseModel):
            bilgiler_dict = bilgiler.model_dump() if hasattr(bilgiler, "model_dump") else bilgiler.dict()
        else:
            bilgiler_dict = bilgiler

        istek = self.__kod_calistir(
            komut = self.komutlar.KULLANICI_BILGILERI_KAYDET,
            jp    = bilgiler_dict
        )
        veri  = istek.get("data")

        return self.__nesne_ver("BilgileriGuncelle", {"mesaj": veri})

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
        fatura_notu:str   = "— QNB Finansbank —\nTR70 0011 1000 0000 0118 5102 59\nÖmer Faruk Sancak",
        max_tekrar:int    = 3,
        **kwargs
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
            fatura_notu   = fatura_notu,
            **kwargs
        )

        ettn      = ""
        son_mesaj = None
        basarili  = False
        for _ in range(max_tekrar):
            istek = self.__kod_calistir(
                komut = self.komutlar.FATURA_OLUSTUR,
                jp    = fatura
            )
            son_mesaj = istek.get("data")
            if son_mesaj and "Faturanız başarıyla oluşturulmuştur." in str(son_mesaj):
                basarili = True
                try:
                    taslaklar = self.faturalari_getir(
                        baslangic_tarihi = fatura.get("faturaTarihi"),
                        bitis_tarihi     = fatura.get("faturaTarihi")
                    )
                    for t in reversed(taslaklar):
                        if t.aliciVknTckn == fatura.get("vknTckn"):
                            ettn = t.ettn
                            break
                except Exception:
                    ettn = fatura.get("faturaUuid") or ""
                break
            print(f"{fatura.get('aliciAdi')} {fatura.get('aliciSoyadi')} | {son_mesaj} | Yeniden Deneniyor..")

        if not basarili:
            raise eArsivPortalHatasi(f"Fatura oluşturulamadı: {son_mesaj}")

        return self.__nesne_ver("FaturaOlustur", {"ettn": ettn or ""})

    def faturalari_getir(self, baslangic_tarihi:str="01/05/2023", bitis_tarihi:str="28/05/2023") -> list[BaseModel]:
        istek = self.__kod_calistir(
            komut = self.komutlar.TASLAKLARI_GETIR,
            jp    = {
                "baslangic" : baslangic_tarihi or datetime.now(timezone("Turkey")).strftime("%d/%m/%Y"),
                "bitis"     : bitis_tarihi or datetime.now(timezone("Turkey")).strftime("%d/%m/%Y"),
                "hangiTip"  : "5000/30000",
                "table"     : []
            }
        )
        veri  = istek.get("data")

        return [self.__nesne_ver("Fatura", fatura) for fatura in veri]

    def fatura_html(self, ettn:str, onay_durumu:str="Onaylandı") -> str:
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
                td_element      = td.root
                td_element.text = ""

        return secici.extract()

    def fatura_indirme_linki(self, ettn:str, onay_durumu:str="Onaylandı") -> str:
        onay_q = quote(onay_durumu)
        return (
            f"{self.url}/earsiv-services/download"
            f"?token={self.token}&ettn={ettn}&belgeTip=FATURA"
            f"&onayDurumu={onay_q}&cmd=downloadResource&"
        )

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
                payload.append(fatura.model_dump() if hasattr(fatura, "model_dump") else fatura.dict())

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

    def fatura_imzala(self, faturalar:list[dict] | dict) -> BaseModel:
        istek = self.__kod_calistir(
            komut = self.komutlar.FATURA_IMZALA,
            jp    = {
                "imzalanacaklar" : self.__fatura_ver(faturalar)
            }
        )
        veri  = istek.get("data")

        return self.__nesne_ver("FaturaImzala", {"mesaj": veri})

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

    def satinalma_faturalari_getir(self, baslangic_tarihi:str="01/05/2023", bitis_tarihi:str="28/05/2023", hourlySearch:str="NONE") -> list[BaseModel]:
        """satınalma_faturalari_getir fonksiyonu için ASCII takma ad."""
        return self.satınalma_faturalari_getir(baslangic_tarihi=baslangic_tarihi, bitis_tarihi=bitis_tarihi, hourlySearch=hourlySearch)
