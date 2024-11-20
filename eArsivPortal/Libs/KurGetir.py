from Oturum import legacy_session
import xmltodict

def kurGetir(kur_kodu:str = "USD"):
    """
    TCMB'nin günlük döviz kurları XML dosyasından belirtilen döviz kurunu getirir.

    Args:
        kur_kodu (str): Döviz kuru kodu (örneğin, "USD").

    Returns:
        str: Belirtilen döviz kurunun satış bilgilerini içeren string.
    """
    kurlar  = []
    result  = None

    url     = "https://www.tcmb.gov.tr/kurlar/today.xml"
    oturum  = legacy_session()
    try:
        response = oturum.get(url=url)
        response.raise_for_status()                                     #response hatalarını yakalamak için
        data    = xmltodict.parse(response.text)                        #xml verisini dict'e çevirir
        kurlar  = [ kur for kur in data["Tarih_Date"].get("Currency")]  #tüm kurlar listeye alınır
        
    except Exception as e:
        print(f"Döviz kuru getirilirken bir Hata oluştu: {e}")
        return None

    for kur in kurlar:
        if kur["@Kod"] == kur_kodu:
            result = kur
            break
    
    return result.get("ForexSelling")
