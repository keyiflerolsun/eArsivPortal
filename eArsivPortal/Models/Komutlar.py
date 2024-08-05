# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pydantic.v1 import BaseModel, Field

class Komut(BaseModel):
    cmd:str   = Field(..., description="Komut Adı")
    sayfa:str = Field(..., description="Sayfa Adı")

class Komutlar(BaseModel):
    KULLANICI_BILGILERI_GETIR:Komut      = Komut(
        cmd   = "EARSIV_PORTAL_KULLANICI_BILGILERI_GETIR",
        sayfa = "RG_KULLANICI"
    )
    MERNISTEN_BILGILERI_GETIR:Komut      = Komut(
        cmd   = "SICIL_VEYA_MERNISTEN_BILGILERI_GETIR",
        sayfa = "RG_BASITFATURA"
    )
    FATURA_OLUSTUR:Komut                 = Komut(
        cmd   = "EARSIV_PORTAL_FATURA_OLUSTUR",
        sayfa = "RG_BASITFATURA"
    )
    TASLAKLARI_GETIR:Komut               = Komut(
        cmd   = "EARSIV_PORTAL_TASLAKLARI_GETIR",
        sayfa = "RG_BASITTASLAKLAR"
    )
    FATURA_GOSTER:Komut                  = Komut(
        cmd   = "EARSIV_PORTAL_FATURA_GOSTER",
        sayfa = "RG_BASITTASLAKLAR"
    )
    FATURA_SIL:Komut                     = Komut(
        cmd   = "EARSIV_PORTAL_FATURA_SIL",
        sayfa = "RG_BASITTASLAKLAR"
    )
    TELEFONNO_SORGULA:Komut                = Komut(
        cmd   = "EARSIV_PORTAL_TELEFONNO_SORGULA",
        sayfa = "RG_SMSONAY"
    )
    SMSSIFRE_GONDER:Komut                = Komut(
        cmd   = "EARSIV_PORTAL_SMSSIFRE_GONDER",
        sayfa = "RG_SMSONAY"
    )
    SMSSIFRE_DOGRULA:Komut               = Komut(
        cmd   = "0lhozfib5410mp",
        sayfa = "RG_SMSONAY"
    )
    ADIMA_KESILEN_BELGELERI_GETIR:Komut  = Komut(
        cmd   = "EARSIV_PORTAL_ADIMA_KESILEN_BELGELERI_GETIR",
        sayfa = "RG_ALICI_TASLAKLAR"
    )