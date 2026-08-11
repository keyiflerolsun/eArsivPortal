# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

BIRLER = ["", "Bir", "İki", "Üç", "Dört", "Beş", "Altı", "Yedi", "Sekiz", "Dokuz"]
ONLAR  = ["", "On", "Yirmi", "Otuz", "Kırk", "Elli", "Altmış", "Yetmiş", "Seksen", "Doksan"]
BINLER = ["", "Bin", "Milyon", "Milyar", "Trilyon"]

def _ucbasamak_metin(sayi: int) -> str:
    yuzler_basamagi = sayi // 100
    onlar_basamagi  = (sayi % 100) // 10
    birler_basamagi = sayi % 10

    parcalar = []
    if yuzler_basamagi > 1:
        parcalar.append(f"{BIRLER[yuzler_basamagi]} Yüz")
    elif yuzler_basamagi == 1:
        parcalar.append("Yüz")

    if onlar_basamagi > 0:
        parcalar.append(ONLAR[onlar_basamagi])

    if birler_basamagi > 0:
        parcalar.append(BIRLER[birler_basamagi])

    return " ".join(parcalar).strip()

def tutar_yaziyla(tutar: float | int | str) -> str:
    """
    Sayısal tutarı GİB fatura formatına uygun Türkçe metne çevirir.
    Örnek: 1234.56 -> "Yalnız Bin İki Yüz Otuz Dört Türk Lirası Elli Altı Kuruş"
    """
    try:
        tutar_float = float(tutar)
    except (ValueError, TypeError):
        return str(tutar)

    lira  = int(abs(tutar_float))
    kurus = int(round((abs(tutar_float) - lira) * 100))

    if lira == 0 and kurus == 0:
        return "Yalnız Sıfır Türk Lirası"

    lira_parcalari = []
    grup_index     = 0
    gecici_lira    = lira

    while gecici_lira > 0:
        üçlü = gecici_lira % 1000
        if üçlü > 0:
            metin = _ucbasamak_metin(üçlü)
            if grup_index == 1 and üçlü == 1:
                # "Bir Bin" yerine "Bin" yazılır
                lira_parcalari.append("Bin")
            else:
                ek = f" {BINLER[grup_index]}" if BINLER[grup_index] else ""
                lira_parcalari.append(f"{metin}{ek}".strip())
        gecici_lira //= 1000
        grup_index += 1

    lira_parcalari.reverse()
    lira_metin = " ".join(lira_parcalari).strip() if lira_parcalari else "Sıfır"

    metin_sonuc = f"Yalnız {lira_metin} Türk Lirası"

    if kurus > 0:
        kurus_metin = _ucbasamak_metin(kurus)
        metin_sonuc += f" {kurus_metin} Kuruş"

    return metin_sonuc
