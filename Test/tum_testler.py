# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from eArsivPortal import eArsivPortal

def test_bilgilerim():
    portal     = eArsivPortal()
    bilgilerim = portal.bilgilerim()

    assert isinstance(bilgilerim, dict)