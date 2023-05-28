# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pydantic import BaseModel, Field

class Komut(BaseModel):
    cmd:str   = Field(..., description="Komut Adı")
    sayfa:str = Field(..., description="Sayfa Adı")

class Komutlar(BaseModel):
    FATURA_OLUSTUR:Komut                 = Komut(
        cmd   = "EARSIV_PORTAL_FATURA_OLUSTUR",
        sayfa = "RG_BASITFATURA"
    )
    TASLAKLARI_GETIR:Komut               = Komut(
        cmd   = "EARSIV_PORTAL_TASLAKLARI_GETIR",
        sayfa = "RG_BASITTASLAKLAR"
    )
    ADIMA_KESILEN_BELGELERI_GETIR:Komut  = Komut(
        cmd   = "EARSIV_PORTAL_ADIMA_KESILEN_BELGELERI_GETIR",
        sayfa = "RG_ALICI_TASLAKLAR"
    )
    FATURA_HSM_CIHAZI_ILE_IMZALA:Komut   = Komut(
        cmd   = "EARSIV_PORTAL_FATURA_HSM_CIHAZI_ILE_IMZALA",
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
    MERNISTEN_BILGILERI_GETIR:Komut      = Komut(
        cmd   = "SICIL_VEYA_MERNISTEN_BILGILERI_GETIR",
        sayfa = "RG_BASITFATURA"
    )
    SMSSIFRE_GONDER:Komut                = Komut(
        cmd   = "EARSIV_PORTAL_SMSSIFRE_GONDER",
        sayfa = "RG_SMSONAY"
    )
    SMSSIFRE_DOGRULA:Komut               = Komut(
        cmd   = "EARSIV_PORTAL_SMSSIFRE_DOGRULA",
        sayfa = "RG_SMSONAY"
    )
    KULLANICI_BILGILERI_GETIR:Komut      = Komut(
        cmd   = "EARSIV_PORTAL_KULLANICI_BILGILERI_GETIR",
        sayfa = "RG_KULLANICI"
    )
    KULLANICI_BILGILERI_KAYDET:Komut     = Komut(
        cmd   = "EARSIV_PORTAL_KULLANICI_BILGILERI_KAYDET",
        sayfa = "RG_KULLANICI"
    )
    MUSTAHSIL_OLUSTUR:Komut              = Komut(
        cmd   = "EARSIV_PORTAL_MUSTAHSIL_OLUSTUR",
        sayfa = "RG_MUSTAHSIL"
    )
    SERBEST_MESLEK_MAKBUZU_OLUSTUR:Komut = Komut(
        cmd   = "EARSIV_PORTAL_SERBEST_MESLEK_MAKBUZU_OLUSTUR",
        sayfa = "RG_SERBEST"
    )