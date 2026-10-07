# Elektrik panosu malzeme listesi

Kullanıcı «elektrik panosu malzeme listesi hazırla», «elektrik kutusu yap», «elektrik kutusu hazırlayalım» veya benzerini dediğinde önce [kurallar/KURALLAR.md](kurallar/KURALLAR.md) dosyasını baştan sona oku ve kuralların tamamına uy.

- Bölüm 1'deki soruları (makine modeli ve opsiyonlar, pano ölçüsü, TMŞ/Pako, IOF) cevap gelmeden geçme.
- Malzeme yalnız KURALLAR.md'deki stoktan; ad + stok kodu birlikte. Kod uydurma.
- Çıktıda hangi kurala dayandığın tartışılırsa kural numarasıyla (R5.4 gibi) belirt.
- «Açık sorular» bölümündeki sorulardan biri işe dokunuyorsa kullanıcıya sor.

## Kuralları değiştirme

- Tek kaynak `kurallar/KURALLAR.md`. `.cursor/rules/elektrik-malzeme.mdc` eski kaynaktır, güncellenmez.
- Kural ekleyince/değiştirince numaralandırmayı koru (yeni kural bölümün sonuna, sıradaki numara).
- Her değişiklikten sonra ikisini de çalıştır: `python kurallar/build_html.py` (→ `kurallar.html`, tüm kurallar) ve `python kurallar/build_panolar.py` (→ `panolar.html`, model sayfaları).
- Model yapısı (etiket yerleşimi, olmazsa olmazlar, opsiyonlar, modele ait kural listesi) `kurallar/build_panolar.py` içindeki `MODELS`'tadır. Bir kural modele özel bir şeyi değiştiriyorsa orayı da güncelle. Malzeme adları ve kural metinleri KURALLAR.md'den okunur; kodu/kuralı bulunamazsa betik hata verir.
- Karara bağlanan açık soru (Qn) ilgili kurala işlenir ve «Açık sorular» bölümünden silinir.
