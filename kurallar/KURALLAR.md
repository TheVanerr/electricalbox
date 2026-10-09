# Elektrik Panosu Malzeme Listesi — Kurallar

Kaynak: `.cursor/rules/elektrik-malzeme.mdc` (2026-10-07 aktarıldı). Bu dosya tek doğru kaynaktır. Değiştirdikten sonra `python kurallar/build_html.py` ile `kurallar/kurallar.html` yeniden üretilir.

Kural numaraları (R1.2 gibi) üzerinden konuşulur. Stok kodu biçimi her zaman `10 xxxxx`.

## 0. Genel ilke

- **R0.1** Kullanıcı «elektrik panosu malzeme listesi hazırla», «elektrik kutusu yap», «elektrik kutusu hazırlayalım» veya benzerini dediğinde bu dosyadaki kuralların tamamına uyulur.
- **R0.2** Kontaktör, termik, MKŞ, sigorta, pako şalter ve röle yalnız bu dosyadaki stoktan seçilir. Başka marka veya listede olmayan kod yazılmaz.
- **R0.3** Çıktıda malzeme adı (stok adı, tam haliyle) ve stok kodu birlikte yazılır.
- **R0.4** Seri yetmiyorsa uydurulmaz; yetmediği açıkça yazılır.
- **R0.5** Kod verilmemiş bir malzemeye kod uydurulmaz.
- **R0.5a** Stok kodu henüz olmayan malzeme (ör. TMŞ, 6.14) üretici referansıyla yazılır (ör. LV516332); stok kodu yerine «STOK KODU YOK» yazılır. Kod eklenince bu dosyada güncellenir.
- **R0.6** Panoda (iç, kapak ve etikette) kullanılan **tüm** malzemeler depo listesine yazılır. Paftada veya etikette olup depo listesinde olmayan kalem bırakılmaz (R10.6).

## 1. Başlamadan önce sor

> [!SOR]
> Pafta veya depo listesi yazılmadan önce aşağıdakiler eksikse sorulur. Cevap gelmeden HTML'e yazılmaz.

- **R1.0 Makine modeli** — Model (KBN 1B, KBN 2B, LYM …) belirtilmediyse **önce bunu sor**; güç kaynağı, kaçak akım, IOF, bara, röle seti ve motor düzeni modele göre değişir (R5.0). Modele bağlı opsiyonları da sor: yağ sıyırıcı (R4.7), interlock kilit (R9.3a), Safety PLC (R8.7), LYM'de sepet invertörü (R4.1), KBN 1B'de döner nozzle (R7.4a).
- **R1.1 Pano ölçüsü** — Kullanıcı vermediyse **mutlaka sor**. Bilinen proje olsa bile ölçü mesajda yoksa sorulmadan HTML'e yazılmaz.
- **R1.2 Ana kesme: TMŞ mi Pako mu?** — Modele göre: **KBN 2B**'de ana kesme **TMŞ** (Schneider EasyPact CVS, R5.11). **KBN 1B ve LYM**'de TMŞ kullanılmaz, ana kesme **Pako** (R5.6). Tasarımda yalnız biri vardır; seçilmeyen paftaya eklenmez. Kullanıcıya açıkça söylenir: «Panoda Pako şalter yok, ana kesme TMŞ» veya «Panoda TMŞ yok, ana kesme Pako».
- **R1.3 Kaçak akım yardımcı kontağı (IOF)** — Modele göre, sorulmaz: **KBN 2B (PLC'li)** her grup kaçak akımına 1 adet YARDIMCI KONTAK 1NA/1NK A9A26924 IOF `10 10820` kesin konur. **KBN 1B ve LYM**'de IOF konmaz.
- **R1.4** Ölçü alındıktan sonra HTML üst satırı: `380 V · 50 Hz · Pano 1000x1200 mm · Tablo gücü …` Aynı ölçü notlarda da yazılır: «Pano ölçüsü 1000x1200 mm».
- **R1.5 Opsiyon listesi** — Kullanıcı opsiyon listesi verdiğinde her opsiyon tek tek kurallarla eşlenir: eklenen/çıkan malzeme (R4.7, R8.7, R4.1 …), etiket değişikliği (R14) ve **kontak blok sayısı** (R9) opsiyonlara göre yeniden hesaplanır. Listede olup kuralı olmayan opsiyon kullanıcıya sorulur; listede olmayan opsiyon eklenmez.
- **R1.6 Emniyet rölesi** — Her panoda sor: «Panoya emniyet rölesi ekleyelim mi?» Evet ise EMNİYET RÖLESİ G9SPN20S OMRON G9SX `10 04538` 1 adet (R4.6). Cevapsız ekleme veya atlama.

## 2. Elektriksel hesap

- **R2.1** Akım/gerilim verilmezse 380 V, 3 faz, 50 Hz kabul edilir. Çizimde «380 V · 50 Hz» ibaresi üstte durur.
- **R2.2** Termik/MKŞ ayarı = In.
- **R2.3** Tablo gücü = yüklerin kW toplamı.
- **R2.4** Tablo akımı = yükler aynı anda çalışırken hat akımlarının toplamı.
- **R2.5** Isıtıcı akımı I = P / (√3 × U). 8 kW → 12,15 A. 6 kW → 9,12 A.

### Motor anma akımı (380 V, yaklaşık)

| Güç (kW) | In (A) |
|---|---|
| 0,37 | 1,1 |
| 0,55 | 1,5 |
| 0,75 | 1,9 |
| 1,1 | 2,6 |
| 1,5 | 3,7 |
| 2,2 | 5,2 |
| 3 | 6,6 |
| 4 | 8,9 |
| 5,5 | 12 |
| 7,5 | 16 |
| 11 | 23 |

### Seçim kuralları

- **R2.6 Kontaktör** — Hem AC-3 akımı hem katalog kW değeri motoru karşılayan en küçük model.
- **R2.7 Termik** — In, ayar aralığının içinde olan LR2K. Aralık In'i içermiyorsa o model yok sayılır. In iki model arasındaki boşluğa düşerse (ör. 5,5–5,8 A) **bir üst termik** seçilir: LR2K0314 5,80–8,0 A `10 00249`.
- **R2.7a Termik serisi yetmezse** — In 16 A'i aşarsa (LR2K en çok 16 A) motor **MKŞ düzenine** geçer. Ör. 11 kW, 23 A → GV2ME22 20–25 A `10 18165` (R2.8: GV2ME21'de 23 A üst durakta) + LC1D25M7 `10 01329` + GVAE11 `10 01365`.
- **R2.8 MKŞ** — In, ayar aralığının içinde olan GV2ME. In yalnız üst durakta kalıyorsa ve bir üst model de In'i alıyorsa üst model seçilir.
- **R2.9 Sigorta / kaçak akım / aşırı akım / pako** — Akımı karşılayan en küçük model.

> [!ORNEK]
> **Termik düzeni:** 3 kW, In 6,6 A → LC1K0910M7 `10 01331` + LR2K0314 ayar 6,6 A `10 00249`. LC1K06 yetmez (6 A / 2,2 kW).
> **MKŞ düzeni:** aynı motor → GV2ME14 ayar 6,6 A `10 01363` + LC1K0910M7 `10 01331` + GVAE11 `10 01365`. Termik bu düzene girmez.

## 3. Motor sürme düzenleri

- **R3.1** Bir motoru süren düzenlerden yalnız biri seçilir. Üçü bir arada olmaz. MKŞ ile termik aynı motorda durmaz.
- **R3.2 Düzen A — MKŞ + kontaktör + yardımcı kontak.** Her MKŞ için bir YARDIMCI KONTAK GVAE11 MKŞ `10 01365`.
- **R3.3 Düzen B — Termik + kontaktör.**
- **R3.4 Düzen C — İnvertör + sigorta.**

## 4. Yük eşlemeleri

- **R4.1 Sepet redüktörü (0,37 kW)** — invertörle sürüldüğünde depo listesine aşağıdakiler yazılır. KBN 1B'de sepet her zaman invertörlüdür. LYM'de invertör istenirse aynısı eklenir (unutma). KBN 2B'de R4.1c/d eklenmez.
- **R4.1a** İNVERTÖR VFD004EL21W-1 0,4KW `10 16319` — 1 adet.
- **R4.1b** SCHNEIDER SİGORTA A9F74106 1*6 `10 01421` — 1 adet.
- **R4.1c** MİNYATÜR RÖLE RXM4AB1P7 220V `10 00294` — 1 adet, R7.4'teki röle setine **ek**. Yalnız KBN 1B ve invertörlü LYM.
- **R4.1d** RÖLE SOKETİ RXZE2M114M `10 00295` — 1 adet, R7.4'teki soketlere **ek**. Yalnız KBN 1B ve invertörlü LYM.
- **R4.2 Pompa 7,5 kW** — İNVERTÖR VFD75E43A 7,5KW `10 05803`. Giriş 380 V üç faz; ön sigorta 3 kutup: SİGORTA A9F74340 SCHNEİDER 40A `10 16119`.
- **R4.2a Pompa 2,2 kW invertörlü (KBN 2B)** — KBN 2B'de yıkama ve durulama pompaları invertörle sürülür (pompa basıncı invertör kontrolü). İnvertör sepet invertörüyle aynı seriden: İNVERTÖR VFD022EL43A 2,2KW (Delta VFD-EL, 380 V üç faz) — STOK KODU YOK (R0.5a). Ön sigorta 3 kutup: SİGORTA A9F74316 SCHNEİDER 16A `10 04000`. MKŞ ve termik eklenmez.
- **R4.3 Isıtıcı — KBN 1B** — yalnız kontaktör: KONTAKTÖR LC1K1610M7 220V `10 01332` (8 kW için 16 A). Termik, MKŞ ve ayrı sigorta eklenmez; ısıtıcı hattının koruması girişteki tek büyük sigortadan (aşırı akım koruma, R5.5) gelir.
- **R4.4 Isıtıcı — KBN 2B** — kontaktör + 3P sigorta. Termik ve MKŞ eklenmez. 8 kW (12,15 A) ve 6 kW (9,12 A) için: KONTAKTÖR LC1K1610M7 220V `10 01332` + SİGORTA A9F74316 SCHNEİDER 16A `10 04000`. LC1K09 (9 A) 6 kW ısıtıcının 9,12 A'ini karşılamaz. A9F74306 (6 A) ikisini de karşılamaz.
- **R4.5 Sensörler** — sensör, termokupl ve el koruma sensörüne kontaktör, termik, MKŞ eklenmez.
- **R4.6 Kapak kapalı sensörü** — kuru kontaktır, 24 V veya 220 V beslemesi yoktur. Emniyet rölesi istenirse (R1.6; KSYSTEM siparişlerinde istendi) 1 adet EMNİYET RÖLESİ G9SPN20S OMRON G9SX `10 04538`; kapak kapalı switchleri ve acil stop bu röleye bağlanır. G9SB2002 bu düzende kullanılmaz.
- **R4.7 Yağ sıyırıcı (opsiyon)** — Opsiyon varsa depo listesine yazılır. Etiket kısmı R14.5.
- **R4.7a KBN 1B ve LYM: termik + kontaktör** — TERMIK RÖLESİ LR2K0305 0,54-0,8A `10 00243` + KONTAKTÖR LC1K0610M7 220V `10 02314`.
- **R4.7b KBN 2B: MKŞ + kontaktör** — MOTOR KORUMA ŞALTERİ GV2ME04 0,40-0,63A `10 01368` + KONTAKTÖR LC1K0610M7 220V `10 02314` + YARDIMCI KONTAK GVAE11 MKŞ `10 01365`. (KBN 1B/LYM termiği LR2K0305 aynı kalır.) Etikete buton/lamba konmaz; yağ sıyırıcı **ekrandan** kumanda edilir.
- **R4.7c Etiket kalemleri (yalnız KBN 1B ve LYM)** — BUTON MANDAL B100S20 `10 00262` 1 adet + SİNYAL LAMBASI S14B BEYAZ 220V `10 00279` 1 adet + KONTAK BLOK NO B1 `10 00267` 1 adet.
- **R4.8 Saha satırı üç bölüm (KBN 2B)** — Saha kalemleri paftada üç satırda yazılır: **Sensörler**, **Valfler**, **Switchboxlar**. Hiçbirine kontaktör, termik, MKŞ eklenmez; stok kodu verilmedi.
- **R4.9 Tahliye pistonu (KBN 2B)** — Her tank için 1 adet tahliye pistonu valfi 5/3 (yıkama tankı, durulama tankı …) yazılır. Her pistonun açık ve kapalı sensörü vardır (+24VDC, 2 giriş); PLC çıkışı pistonu aç / kapa (2 çıkış).
- **R4.10 Otomatik dolum (EX108)** — Opsiyon varsa tank sayısı kaç olursa olsun **tank başına**: 1 adet 3/2 valf (aktüatörlü dolum vanası), 1 adet switchbox (vana açık / kapalı bilgisi, 2 giriş) ve 1 adet üst seviye sensörü. PLC çıkışı vana başına 1. Opsiyon yoksa tank başına yalnız alt seviye sensörü vardır.

## 5. Pano beslemesi — her panoda

> [!NOT]
> Bu kalemler elektrik kutusu malzemesi istendiğinde her zaman eklenir. Modele göre değişenler R5.0 tablosundadır.

- **R5.0 Modele göre seçim** — aşağıdaki tabloya göre.

| Kalem | KBN 1B | KBN 2B (PLC'li) | LYM |
|---|---|---|---|
| Ana kesme | Pako | TMŞ + döner kol | Pako |
| Aşırı akım koruma 4P | 1 | Yok | 1 |
| Röle seti (RXM + soket) | 4 soket (döner nozzle: 6) | Yok — yaprak röle | 3 soket (invertör: 4) |
| Güç kaynağı | MDR 100/24 `10 02772` | LRS 350/24 `10 04903` | MDR 20/24 `10 02491` |
| Kaçak akım | 1 adet (tüm pano) | Grup başına | 1 adet (tüm pano) |
| Kaçak akım IOF `10 10820` | Yok | Her kaçak akıma 1 | Yok |
| BARA 4×7 `10 03578` (motor grubu) | 1 | 1 | Yok |
| BARA GWEST 2X7 `10 15962` | Yok | 1 (ek) | Yok |
| Sepet 220V röle + soket (R4.1c/d) | Var | Yok | İnvertör varsa |
| Yağ sıyırıcı düzeni (R4.7) | Termik + kontaktör | MKŞ + kontaktör | Termik + kontaktör |

- **R5.1 Güç kaynağı** — 1 adet, R5.0'a göre: KBN 1B GÜÇ KAYNAĞI MDR 100/24 `10 02772`; KBN 2B GÜÇ KAYNAĞI LRS 350/24 24VDC 14,6AMP `10 04903`; LYM GÜÇ KAYNAĞI MDR 20/24 `10 02491`.
- **R5.2** FAZ KORUMA RÖLESİ MKS-03 `10 00258` — 1 adet. KBN 1B, KBN 2B ve LYM'de zorunlu.
- **R5.3** Kumanda sigortası SİGORTA A9F74103 1*3 `10 00302` — 1 adet.
- **R5.4 Kaçak akım** — KBN 1B ve LYM: tüm pano için 1 adet, tablo akımını karşılayan en küçük model (tablo 6.5). KBN 2B (PLC'li): **grup başına** 1 adet (ör. yıkama, durulama, ısıtıcı grupları), her biri o grubun akımını karşılayan en küçük model; gruplar paftadan net değilse sor. 100 A üstü → yetmediğini yaz.
- **R5.5 Aşırı akım koruma** — KBN 1B ve LYM: tüm pano için 1 adet, aynı seçim (tablo 6.6). 63 A üstü → yetmediğini yaz. **KBN 2B'de yok**; koruma TMŞ + grup kaçak akımlarıdır.
- **R5.6 Pako şalter** — KBN 1B ve LYM: tüm pano için 1 adet, tablo akımına göre en küçük model (tablo 6.7). 63 A üstü → yetmediğini yaz. KBN 2B'de pako yok (R1.2).
- **R5.7 Pano lambası** — PANO LAMBASI CT-2467 `10 03253` 1 adet. Sigortası SCHNEIDER SİGORTA A9F74106 1*6 `10 01421`. Anahtarı SWITCH BS1022 ANI HARK.1NA+1NK `10 16235`.
- **R5.8 Priz** — PRİZ RAYA MONTAJ TOPRAKLI EPREU2G `10 03313`, 1 adet.
- **R5.9 LRS 350/24 sigortaları** — LRS `10 04903` kullanıldığında: giriş SCHNEIDER SİGORTA A9F74106 1*6 `10 01421`, çıkış SIGORTA A9F74110 1*10 `10 01422`.
- **R5.10 Bara** — KBN 1B ve KBN 2B: motor grubu için 1 adet BARA GWEST 4×7 mm `10 03578`. KBN 2B ayrıca 1 adet BARA GWEST 2X7 MM `10 15962`. LYM'de bara yok.
- **R5.11 TMŞ (yalnız KBN 2B)** — Schneider EasyPact CVS F (36 kA), 3P3D, TM-D termik-manyetik. Tablo akımını karşılayan en küçük In seçilir (tablo 6.14). Termik ayarı Ir = 0,7–1 × In; Ir tablo akımına ayarlanır. 250 A üstü → uydurma, yetmediğini yaz.
- **R5.12 TMŞ döner kolu** — Her TMŞ'ye 1 adet LV429338 uzatılmış döner kol (siyah, IP55): kesici pano içinde, kol kapakta. CVS 100/160/250'nin hepsine aynı kol uyar.
- **R5.13 LYM röle seti** — MİNYATÜR RÖLE RXM4AB1BD 24V `10 01398` 1 adet, MİNYATÜR RÖLE RXM4AB1P7 220V `10 00294` 2 adet, RÖLE SOKETİ RXZE2M114M `10 00295` 3 adet. Sepet invertörü varsa +1 RXM4AB1P7 ve +1 soket (R4.1c/d) → en çok 4 soket. Sensör sayısı röle sayısını artırmaz.

## 6. Stok katalogu

### 6.1 Kontaktör (bobin 220 V)

| Malzeme | Değer | Kod |
|---|---|---|
| KONTAKTÖR LC1K0610M7 220V | 6 A · 2,2 kW | 10 02314 |
| KONTAKTÖR LC1K0910M7 220V | 9 A · 4 kW | 10 01331 |
| KONTAKTÖR LC1K1610M7 220V | 16 A · 7,5 kW | 10 01332 |
| KONTAKTÖR LC1D25M7 | 25 A · 11 kW | 10 01329 |

### 6.2 Termik röle

| Malzeme | Ayar aralığı | Kod |
|---|---|---|
| TERMIK RÖLESİ LR2K0305 | 0,54–0,8 A | 10 00243 |
| TERMIK RÖLESİ LR2K0306 | 0,80–1,2 A | 10 00244 |
| TERMIK RÖLESİ LR2K0307 | 1,20–1,8 A | 10 00245 |
| TERMIK RÖLESİ LR2K0308 | 1,80–2,6 A | 10 00246 |
| TERMIK RÖLESİ LR2K0310 | 2,60–3,7 A | 10 00247 |
| TERMIK RÖLESİ LR2K0312 | 3,70–5,5 A | 10 00248 |
| TERMIK RÖLESİ LR2K0314 | 5,80–8,0 A | 10 00249 |
| TERMIK RÖLESİ LR2K0316 | 8–11,5 A | 10 01359 |
| TERMIK RÖLESİ LR2K0321 | 10,0–14 A | 10 00250 |
| TERMIK RÖLESİ LR2K0322 | 12–16 A | 10 09431 |

### 6.3 Motor koruma şalteri (MKŞ)

Ayar aralığı Schneider GV2ME katalog değeridir. GV2ME32 bu stokta yok.

| Malzeme | Ayar aralığı | Kod |
|---|---|---|
| MOTOR KORUMA ŞALTERİ GV2ME01 | 0,10–0,16 A | 10 18250 |
| MOTOR KORUMA ŞALTERİ GV2ME02 | 0,16–0,25 A | 10 16799 |
| MOTOR KORUMA ŞALTERİ GV2ME03 | 0,25–0,40 A | 10 05619 |
| MOTOR KORUMA ŞALTERİ GV2ME04 | 0,40–0,63 A | 10 01368 |
| MOTOR KORUMA ŞALTERİ GV2ME05 | 0,63–1 A | 10 01370 |
| MOTOR KORUMA ŞALTERİ GV2ME06 | 1–1,6 A | 10 01367 |
| MOTOR KORUMA ŞALTERİ GV2ME07 | 1,6–2,5 A | 10 01371 |
| MOTOR KORUMA ŞALTERİ GV2ME08 | 2,5–4 A | 10 01369 |
| MOTOR KORUMA ŞALTERİ GV2ME10 | 4–6,3 A | 10 01362 |
| MOTOR KORUMA ŞALTERİ GV2ME14 | 6–10 A | 10 01363 |
| MOTOR KORUMA ŞALTERİ GV2ME16 | 9–14 A | 10 01364 |
| MOTOR KORUMA ŞALTERİ GV2ME20 | 13–18 A | 10 01366 |
| MOTOR KORUMA ŞALTERİ GV2ME21 | 17–23 A | 10 01372 |
| MOTOR KORUMA ŞALTERİ GV2ME22 | 20–25 A | 10 18165 |
| YARDIMCI KONTAK GVAE11 MKŞ | her MKŞ'ye 1 | 10 01365 |

### 6.4 Sigorta 3 kutup (C eğrisi)

63 A üstü → uydurma, yetmediğini yaz.

| Malzeme | Akım | Kod |
|---|---|---|
| SİGORTA A9F74306 SCHNEIDER DEVRE KESİCİ İC60N,6KA,6A,3P,C EĞRİSİ | 6 A | 10 06646 |
| SİGORTA A9F74316 SCHNEİDER 16A | 16 A | 10 04000 |
| SİGORTA A9K24325 SCHNEİDER İK60N,6KA,25A,3P,C | 25 A | 10 02822 |
| SİGORTA A9F74332 SCHNEİDER 32A | 32 A | 10 02774 |
| SİGORTA A9F74340 SCHNEİDER 40A | 40 A | 10 16119 |
| SİGORTA A9F74350 SCHNEİDER 50A | 50 A | 10 11474 |
| SİGORTA A9F74363 SCHNEİDER 63A | 63 A | 10 02933 |

### 6.5 Kaçak akım (4 kutup)

100 A üstü → uydurma, yetmediğini yaz.

| Malzeme | Akım | Kod |
|---|---|---|
| SİGORTA KAÇAK AKIMLI A9R41425 4'LÜ 25 A | 25 A | 10 00303 |
| A9R41440 4'LÜ 40 A | 40 A | 10 00304 |
| A9R41463 4'LÜ 63 A | 63 A | 10 00305 |
| SİGORTA KAÇAK AKIMLI A9R11480 4'LÜ 80 A | 80 A | 10 16117 |
| SİGORTA KAÇAK AKIMLI A9R11491 4'LÜ 100 A | 100 A | 10 01416 |
| YARDIMCI KONTAK 1NA/1NK A9A26924 IOF | KBN 2B, her kaçak akıma 1 | 10 10820 |

### 6.6 Aşırı akım koruma (4 kutup)

63 A üstü → uydurma, yetmediğini yaz.

| Malzeme | Akım | Kod |
|---|---|---|
| SİGORTA A9F74425 SCHNEIDER iC60N 6KA 25A | 25 A | 10 02663 |
| SİGORTA A9F74440 SCHNEIDER 40A | 40 A | 10 02664 |
| SİGORTA A9F74463 SCHNEIDER iC60N 6KA 63A 4P 63A | 63 A | 10 04732 |

### 6.7 Pako şalter

63 A üstü → uydurma, yetmediğini yaz.

| Malzeme | Akım | Kod |
|---|---|---|
| PAKO ŞALTER YKL301025 3*25 BÜYÜK KASALI OPAŞ | 25 A | 10 00285 |
| PAKO ŞALTER YKL301M40 3*40 KÜÇÜK KASALI OPAŞ | 40 A | 10 00286 |
| PAKO ŞALTER YKL301M63 3*63 OPAŞ | 63 A | 10 00287 |

### 6.8 Sigorta 1 kutup

| Malzeme | Kullanım | Kod |
|---|---|---|
| SİGORTA A9F74103 1*3 | Kumanda | 10 00302 |
| SCHNEIDER SİGORTA A9F74106 1*6 | Sepet invertörü, pano lambası, LRS girişi | 10 01421 |
| SIGORTA A9F74110 1*10 | LRS çıkışı | 10 01422 |

### 6.9 İnvertör ve güç kaynağı

| Malzeme | Kullanım | Kod |
|---|---|---|
| İNVERTÖR VFD004EL21W-1 0,4KW | Sepet redüktörü 0,37 kW | 10 16319 |
| İNVERTÖR VFD75E43A 7,5KW | Pompa 7,5 kW | 10 05803 |
| İNVERTÖR VFD022EL43A 2,2KW | Pompa 2,2 kW (KBN 2B, R4.2a) | STOK KODU YOK |
| GÜÇ KAYNAĞI MDR 20/24 | LYM | 10 02491 |
| GÜÇ KAYNAĞI MDR 100/24 | KBN 1B | 10 02772 |
| GÜÇ KAYNAĞI LRS 350/24 24VDC 14,6AMP | KBN 2B (PLC'li) | 10 04903 |

### 6.10 Röle ve koruma

| Malzeme | Kullanım | Kod |
|---|---|---|
| FAZ KORUMA RÖLESİ MKS-03 | Her pano, 1 adet | 10 00258 |
| EMNİYET RÖLESİ G9SPN20S OMRON G9SX | KSYSTEM, 1 adet | 10 04538 |
| MİNYATÜR RÖLE RXM4AB1BD 24V 16 PİNLİ | Manuel KBN, 1 adet | 10 01398 |
| MİNYATÜR RÖLE RXM4AB1P7 220V | Manuel KBN, 2 adet | 10 00294 |
| RÖLE SOKETİ RXZE2M114M | Manuel KBN, 3 adet | 10 00295 |
| YAPRAK ROLE KONTAĞI WEİDMÜLLER TRS 24VDC 1CO | Çıkış rölesi | 10 02146 |
| RÖLE KÖPRÜSÜ WEIDMÜLLER TCC 6.4/51 OR (24 diş) (3 ADET) | Her 24 röleye 1 | 10 13016 |

### 6.11 Ön yüz: buton, lamba, kontak blok

| Malzeme | Kullanım | Kod |
|---|---|---|
| BUTON START B100DY | Yeşil: kapak aç / START / konveyör ileri | 10 00273 |
| BUTON START B100DK | Kırmızı: kapak kapat / STOP / konveyör geri | 10 00271 |
| BUTON START B100DM | Mavi: RESET / SIFIRLA | 10 00272 |
| BUTON START B100DB | SEPET TEST (yalnız KBN 1B) | 10 00270 |
| BUTON MANDAL B100S20 | Yağ sıyırıcı (opsiyon) | 10 00262 |
| BUTON MANDAL B100SL20Y | LYM HEATER, yeşil ışıklı | 10 00263 |
| BUTON İKİZ LAMBALI B102K20KY | LYM WASHING start/stop | 10 00266 |
| BUTON ACİL STOP MANTAR B200EE | Acil stop | 10 03445 |
| SİNYAL LAMBASI S14B BEYAZ 220V | YIKAMA, ISITICI, YAĞ SIYIRICI | 10 00279 |
| SİNYAL LAMBASI S14K KIRMIZI 220V | Uyarı lambası | 10 00278 |
| KONTAK BLOK NO B1 | NO kontak | 10 00267 |
| KONTAK BLOK NC B2 | NC kontak | 10 00268 |

### 6.12 Diğer

| Malzeme | Kullanım | Kod |
|---|---|---|
| ORDEL OC990-9/0240 FIR.KON.CİH-DİJ.PAN. | Termokupl cihazı (KBN 1B) | 10 00229 |
| TERMOSTAT DİJİTAL DT 481 GEMO | LYM THERMOSTAT | 10 00237 |
| ZAMAN ROLESİ DZ 482 DİJİTAL GEMO | LYM TIMER | 10 10465 |
| BARA GWEST 2X7 MM | KBN 2B, 1 adet (ek) | 10 15962 |
| BARA GWEST 4*11MM | Bara | 10 14974 |
| BARA GWEST 4×7 mm | KBN 1B / 2B motor grubu, 1 adet | 10 03578 |
| PANO LAMBASI CT-2467 | Pano içi lamba | 10 03253 |
| SWITCH BS1022 ANI HARK.1NA+1NK | Pano lambası anahtarı | 10 16235 |
| PRİZ RAYA MONTAJ TOPRAKLI EPREU2G | Priz | 10 03313 |

### 6.13 PLC (KBN 2B)

Stok adları bu şekilde yazılır. CP1W-40EDT1'in stok kodu henüz yok (R0.5a).

| Malzeme | Kullanım | Kod |
|---|---|---|
| PLC EK MODÜL CPU OMRON CP2EN60DT1 | CPU | 10 17185 |
| PLC EK MODÜL OMRON CP1W20EDT1 | Dijital ek modül 12DI/8DO (1. ve gerekirse 2.) | 10 18528 |
| PLC EK MODÜL OMRON CP1WTS002 | Sıcaklık modülü | 10 17183 |
| PLC EK MODÜL OMRON CP1WADB21 | Analog modül | 10 17184 |
| OMRON NB7W-TW01B | Ekran (HMI) | 10 16496 |
| PLC EK MODÜL OMRON CP1W-40EDT1 | 2. ek modül 24DI/16DO | CP1W-40EDT1 | STOK KODU YOK |

### 6.14 TMŞ — Schneider EasyPact CVS F, 3P3D, TM-D (yalnız KBN 2B)

Stok kodları henüz yok (R0.5a). 36 kA @ 415 V. Gövde 3P: 105 × 161 × 86 mm (100/160/250 aynı).

| Malzeme | In / Ir ayarı | Ref | Kod |
|---|---|---|---|
| EasyPact CVS100F TM16D 3P3D | 16 A / 11,2–16 A | LV510330 | STOK KODU YOK |
| EasyPact CVS100F TM25D 3P3D | 25 A / 17,5–25 A | LV510331 | STOK KODU YOK |
| EasyPact CVS100F TM32D 3P3D | 32 A / 22,4–32 A | LV510332 | STOK KODU YOK |
| EasyPact CVS100F TM40D 3P3D | 40 A / 28–40 A | LV510333 | STOK KODU YOK |
| EasyPact CVS100F TM50D 3P3D | 50 A / 35–50 A | LV510334 | STOK KODU YOK |
| EasyPact CVS100F TM63D 3P3D | 63 A / 44,1–63 A | LV510335 | STOK KODU YOK |
| EasyPact CVS100F TM80D 3P3D | 80 A / 56–80 A | LV510336 | STOK KODU YOK |
| EasyPact CVS100F TM100D 3P3D | 100 A / 70–100 A | LV510337 | STOK KODU YOK |
| EasyPact CVS160F TM125D 3P3D | 125 A / 87,5–125 A | LV516332 | STOK KODU YOK |
| EasyPact CVS160F TM160D 3P3D | 160 A / 112–160 A | LV516333 | STOK KODU YOK |
| EasyPact CVS250F TM200D 3P3D | 200 A / 140–200 A | LV525332 | STOK KODU YOK |
| EasyPact CVS250F TM250D 3P3D | 250 A / 175–250 A | LV525333 | STOK KODU YOK |
| Uzatılmış döner kol, siyah, NSX/CVS 100–250 | Her TMŞ'ye 1 | LV429338 | STOK KODU YOK |

## 7. KBN 1B (manuel pano)

- **R7.1** Standart 710x710 KBN 1B panosu kullanılır.
- **R7.2** Sepet redüktörü invertörle döner (R4.1). Sepet durdurma sensörü +24VDC. İnvertör parametreleri ayarlanır.
- **R7.3** Pano etiketi Almanca ve İngilizce. Doküman koyma kısmı ters olmaz. Pano kapağına ve güç kaynağına topraklama hattı çekilir.
- **R7.4 KBN 1B röle seti** — RXM4AB1BD 24V `10 01398` 1 adet, RXM4AB1P7 220V `10 00294` 2 adet, RXZE2M114M soket `10 00295` 3 adet. Sepet invertörü için +1 RXM4AB1P7 ve +1 soket ayrıca eklenir (R4.1c/d) → KBN 1B toplamı 3 adet RXM4AB1P7, 4 adet soket. Sensör sayısı röle sayısını artırmaz.
- **R7.4a Döner nozzle (KBN 1B opsiyonu)** — varsa röle seti 6 sokete çıkar: +2 RXZE2M114M `10 00295` ve +2 röle (tipi Q17).
- **R7.5 Ön yüz, üstte** ORDEL OC990-9/0240 `10 00229`.
- **R7.6 ORDEL varsa** START ve STOP butonu konulmaz; etikette ve depoda yazılmaz, kontakları da yazılmaz. Yerine beyaz lambalar: YIKAMA ve ISITICI — SİNYAL LAMBASI S14B BEYAZ 220V `10 00279`, 2 adet.
- **R7.7** RESET mavi = B100DM `10 00272`. SEPET TEST = B100DB `10 00270`. ACİL STOP = B200EE `10 03445`, 1 adet.
- **R7.8 Uyarı lambası** 3 adet SİNYAL LAMBASI S14K KIRMIZI 220V `10 00278`. Etiket adları: düşük su seviyesi, pompa arızası, redüktör arızası.
- **R7.9 Çift el butonu** — iki kapak aç (yeşil B100DY `10 00273`) sola, iki kapak kapat (kırmızı B100DK `10 00271`) sağa. Aynı taraftaki iki buton arasında yukarıdan aşağı en az 25–30 cm. Aç ile kapat arası yatay mesafe bu ölçü değildir. Etiket dar kalır, dikey ölçü için uzar.

## 8. KBN 2B (PLC'li pano)

- **R8.1 Etiket** — üstte OMRON NB7W-TW01B `10 16496`. Sepet test butonu yoktur; B100DB `10 00270` etikete ve depoya yazılmaz.
- **R8.2** Ortada SIFIRLA mavi = B100DM `10 00272`. Solunda START, sağında STOP. START ve STOP kapak aç/kapat butonlarından **ayrı** butonlardır, aynı model: START yeşil B100DY `10 00273`, STOP kırmızı B100DK `10 00271`. Etikette toplam 3 yeşil (START + 2 kapak aç) ve 3 kırmızı (STOP + 2 kapak kapat).
- **R8.3 Çift el** KBN 1B ile aynı (R7.9).
- **R8.4 PLC I/O** — CP2E-N60 dijital giriş 0.0–0.11, 1.0–1.11, 2.0–2.11 (36 giriş); çıkış 100.0–100.7, 101.0–101.7, 102.0–102.7 (24 çıkış). Dijital ek modül **yalnız** giriş 36'yı veya çıkış 24'ü aşarsa eklenir (R8.4a); aşmıyorsa PLC listesi CPU + TS002 + ADB21 + NB7W'dir ve gereksiz YEDEK uç bırakılmaz. CP1W-20EDT1 eklenirse giriş 3.0–3.11, çıkış 103.0–103.7. Boş uç YEDEK. TS002 ve ADB21 bu dijital uçları kullanmaz.
- **R8.4a Ek modül seçimi** — CPU kapasitesini (36 giriş / 24 çıkış) aşan I/O'yu karşılayan en küçük ek modül seçilir. Fazla ≤ 12 giriş ve ≤ 8 çıkış → PLC EK MODÜL OMRON CP1W20EDT1 `10 18528` (12DI/8DO; giriş 3.0–3.11, çıkış 103.0–103.7). Fazla ≤ 24 giriş ve ≤ 16 çıkış → CP1W-40EDT1 (24DI/16DO; giriş 3.0–3.11, 4.0–4.11, çıkış 103.0–103.7, 104.0–104.7). Daha fazlası → 20EDT1 + 40EDT1 (en çok 72 giriş / 48 çıkış); aşarsa uydurma, yetmediğini yaz. Çıkışlar son modülün son ucuyla biter (R8.5).
- **R8.5 Çıkış rölesi** — YAPRAK ROLE KONTAĞI WEİDMÜLLER TRS 24VDC 1CO `10 02146`, adet R numarası kadar. Çıkışlar son modülün son ucuyla biter (yalnız CPU'da 102.7, 20EDT1 ile 103.7); boş giriş satırına röle yazılmaz. Safety PLC röle sütunu bir sonraki numaradan devam eder ve SO6 ile biter; çıkışı boş safety satırına röle yazılmaz.
- **R8.6 Röle köprüsü** — WEIDMÜLLER TCC 6.4/51 OR (24 diş) `10 13016`, her 24 röle için 1 adet. Safety röleleri (R8.7) bu sayıma dahildir.
- **R8.7 Safety PLC varsa** — depo listesine ayrıca 6 adet YAPRAK ROLE KONTAĞI WEİDMÜLLER TRS 24VDC 1CO `10 02146` eklenir (SO1–SO6). Safety PLC yoksa bu 6 röle eklenmez.

## 9. Kontak blok sayımı

- **R9.1** Acil stop: 2 NC.
- **R9.2** Reset: 1 NO + 1 NC.
- **R9.3** Start ve stop (ORDEL yoksa veya KBN 2B): her biri 1 NO + 1 NC. ORDEL varsa start/stop ve kontakları yazılmaz.
- **R9.3a LYM WASHING ikiz buton** (B102K20KY `10 00266`): 1 NO + 1 NC. **İnterlock kilit** opsiyonu varsa 2 NO + 2 NC.
- **R9.4** Her kapak aç ve her kapak kapat butonu: 1 NO + 1 NC. KBN 2B'de START ve STOP bunlara ek ayrı butonlardır (R8.2, R9.3).
- **R9.5** Sepet test (KBN 1B) ve LYM TEST: 1 NO.
- **R9.5a LYM HEATER** ışıklı mandal buton (B100SL20Y `10 00263`): 1 NO.
- **R9.6a** Yağ sıyırıcı mandal butonu (B100S20): 1 NO.
- **R9.7** Depo listesine NO (B1 `10 00267`) ve NC (B2 `10 00268`) toplam adedi yazılır. Sayım opsiyon listesine göre yapılır (R1.5). Kontak bloklar butona takılı gelmez; her buton için ayrıca yazılır.

## 10. Depo listesi ve fotoğraf

- **R10.1** Depo listesinde Foto sütunu vardır. Kaynak `photos/`; dosya adı stok kodudur, format JPG.
- **R10.2** Ölçü ve kadraj değiştirilmez. Arka plan temizlenir, saydam yapılır. Tabloda `photos/temiz/` altındaki saydam PNG kullanılır. Kaynak PNG'ye dokunulmaz.
- **R10.3** Fotoğraflar HTML'e gömülür: `img` asla `../photos/temiz/...` gibi bir dosya yoluna bağlanmaz. HTML başka yere kopyalansa da foto durur.
- **R10.4** Hücre 68×68 px; uzun kenar 136 px, oran bozulmaz, saydamlık kalır. WebP kalite 75 ile `data:image/webp;base64,...`.
- **R10.5** Fotoğrafı olmayan satır boş kalır. Kökte veya başka klasördeki kopya da aynı şekilde gömülür.
- **R10.6 Eksiksiz liste** — pano içi (DIN ray), kapak/etiket (buton, lamba, kontak blok, ekran, ORDEL), bara, klemens, röle, soket, köprü ve opsiyon malzemelerinin tamamı depo listesindedir. Liste bitince pafta ve etiketle karşılaştırılır; eksik kalem varsa eklenir.

## 11. Pano iç layout (DIN 35)

- **R11.1** Pano içi 2D dizilim istendiğinde ayrı HTML açılmaz; proje HTML'inin en altına `<section class="pano-layout">` eklenir/güncellenir. Satır içeriğini kullanıcı söyler; çerçeve ve ölçü kuralları sabittir.

### Tava ve kanallar

- **R11.2** Dış kare = pano ölçüsü. İç kare = tava montaj alanı (tipik 630×630 mm; farklıysa paftada belirtilir).
- **R11.2a** 900×1200 panoda tava 800×1100 mm kabul edilir (kenarlardan 50 mm); TMŞ ve LRS 350/24 montaj plakasına vidalanır, ray dışıdır (R11.13a). Satırlar genişliğe göre otomatik bölünür; bir satıra sığmayan kalem bir sonraki satıra geçer.
- **R11.3** 40 mm kablo kanalları: üstte (tava üst kenarına sıfır), solda ve sağda (tava alt kenarına kadar), her DIN satırı arasında, altta (tava alt kenarına sıfır).
- **R11.4** İç alan genişliği = tava − 2×40 mm. Dikey: üst kanal + satır bantları + ara kanallar + alt kanal = tava yüksekliği.

### DIN ray ve boşluklar

- **R11.5** Her satırda DIN 35 rayı sol kanaldan sağ kanala tam genişlikte çizilir.
- **R11.6** Malzemeler yalnız ray üzerinde; katalog genişlik×yükseklik kutuları ray dışına taşmaz. Sığmazsa yalnız aralık daraltılır, kutu küçültülmez.
- **R11.7** Yan yana kutular arası tipik 2 mm; motor/termik grupları arasında biraz daha geniş olabilir.
- **R11.8** Satır bandı: en üstte ve en altta kalan parça ile komşu 40 mm kanal arasında en az 20 mm boşluk kalır.
- **R11.9 Satır 1** (besleme/koruma): kullanıcının verdiği sıra. İnvertör varsa satırdaki parçaların ve rayın Y merkezi invertör merkezine hizalı.
- **R11.10 Motor satırı** — termik + kontaktör (LC1K 45×58, LR2K 45×58, direkt montaj birleşim 94 mm, 22 mm bindirme). Kontaktör üstte, termik altta. Ray merkezi kontaktör merkezinde. Termik alt hizasından 20 mm sonra kanal başlar.
- **R11.11 Isıtıcı** — KBN 1B: yalnız LC1K1610M7 çizilir. KBN 2B: kontaktör + 3P sigorta. Termik/MKŞ çizilmez.
- **R11.12 Klemens satırı** — solda birkaç geniş güç klemensi, her motor 4, her ısıtıcı 3 (ısıtıcı hatvesi daha geniş), kumanda hatveleri; toplam ray içinde.
- **R11.13 Ray dışı** — ön yüz/kapı elemanları (ORDEL, acil stop, buton, lamba, priz, HMI vb.) DIN rayına zorla sığdırılmaz; aynı SVG'de not veya ayrı gösterim.
- **R11.13a TMŞ** — DIN rayına değil montaj plakasına vidalanır; 3P gövde 105×161 mm. Satır 1'de en solda durur, satır yüksekliği buna göre hesaplanır (R11.8). Döner kol mili kapağa çıkar.

### Çizim

- **R11.14** Ölçek 1 mm = 1,55 px. Kutuda stok adı ve kodu yazılır.
- **R11.15** BARA GWEST 4×7 mm `10 03578`: ray üstü blok genişliği 10 mm.
- **R11.16 Renkler** — koruma mavi, kontaktör mavi, termik kırmızımsı, röle yeşil, invertör koyu zemin, ısıtıcı kontaktörü turuncu, klemens türüne göre yeşil/mavi/turuncu/mor, ray çelik grisi, kanal gri.

## 12. Sembol ve tablo biçimi

- **R12.1** Makine sütununda ve malzeme satırında sembolün altındaki yazılar ortalıdır; sembol yazının üstünde ortada durur.
- **R12.2** Başlık satırındaki bütün yazılar ortalıdır.
- **R12.3** Sayı sütununda ondalık hane sütundaki en uzun değere göre eşitlenir (0,46 varken 1,10; 16 → 16,00). Birim her satırda aynı yerde durur. Eşitlenen sayı sütunu ortalıdır.
- **R12.4** Genişliği değişen sütunlar sola dayalıdır.

## 13. Bilinen projeler

| Proje | Tip | Pano ölçüsü |
|---|---|---|
| 0326069 KSYSTE | KBN 1B 1850 | 710x710 |
| 0326070 RICHAR | KBN 2B 1650 | 1000x1200 |
| 0326071 FİNAN | KBN 1B 1350 | 710x710 |
| 0326072 KÜRSAN | KBN 1B 2050 | 710x710 |
| 1326050 KSYSTE | KBN 2B 1650 | 1200x1000 |

## 14. Etiket standardı

Pano kapağındaki etiketin ortak düzeni. Modele özel ayrıntılar R7 (KBN 1B), R8 (KBN 2B) ve R14.8 (LYM).

- **R14.1 Dil** — KBN 1B / KBN 2B etiketi Almanca ve İngilizce. LYM etiketi İngilizce (R14.8).
- **R14.2 Üst** — KBN 1B'de ORDEL OC990-9/0240 `10 00229`, KBN 2B'de OMRON NB7W-TW01B `10 16496`, LYM'de logo altında ACİL STOP.
- **R14.3 Orta** — RESET/SIFIRLA mavi B100DM `10 00272`. KBN 2B'de solunda START, sağında STOP. KBN 1B'de ORDEL varsa START/STOP yok, yerine YIKAMA ve ISITICI beyaz lamba.
- **R14.4 Çift el** — iki kapak aç (yeşil) sola, iki kapak kapat (kırmızı) sağa; aynı taraftaki iki buton arasında dikey en az 25–30 cm. Etiket dar kalır, dikey uzar.
- **R14.5 Yağ sıyırıcı opsiyonu** — KBN 1B ve LYM'de etikette OIL SEPERATOR / YAĞ SIYIRICI yeri her zaman vardır. **Opsiyon varsa** butonu **sola**, lambası **sağa** konur: BUTON MANDAL B100S20 `10 00262` (1 NO) + SİNYAL LAMBASI S14B BEYAZ 220V `10 00279`; ikisi ve kontak bloğu depo listesine yazılır (R4.7c, R0.6). **Opsiyon yoksa** iki delik **tapa** ile kapatılır (sol büyük buton tapası, sağ küçük lamba tapası). KBN 2B'de yağ sıyırıcı etikette yoktur, ekrandan kumanda edilir.
- **R14.6** Etikette çizilen her buton, lamba ve kontak bloğu depo listesinde vardır; etikette olmayan buton depo listesine yazılmaz. **İstisna — tapa:** buton ve lamba tapaları etiket çiziminde görsel olarak gösterilir, depo listesine yazılmaz.
- **R14.7 TMŞ kolu** — KBN 2B'de TMŞ döner kolu (LV429338) **pano kapağına** takılır; etikette yer almaz, etiket çiziminde gösterilmez.

### LYM etiket düzeni

- **R14.8 LYM etiketi** — dar dikey etiket, yukarıdan aşağı aşağıdaki sırayla. Sol/sağ sütun hizası korunur.

| Sıra | Sol | Orta | Sağ |
|---|---|---|---|
| 1 | — | Logo + «INDUSTRIAL WASHING SYSTEMS» | — |
| 2 | — | EMERGENCY STOP — BUTON ACİL STOP MANTAR B200EE `10 03445` | — |
| 3 | WASHING — BUTON İKİZ LAMBALI B102K20KY `10 00266` | — | TIMER — ZAMAN ROLESİ DZ 482 DİJİTAL GEMO `10 10465` |
| 4 | TEST — beyaz BUTON START B100DB `10 00270` | — | RESET — mavi BUTON START B100DM `10 00272` |
| 5 | HEATER — BUTON MANDAL B100SL20Y (yeşil ışıklı) `10 00263` | — | THERMOSTAT — TERMOSTAT DİJİTAL DT 481 GEMO `10 00237` |
| 6 | OIL SEPERATOR buton B100S20 `10 00262` veya tapa (görsel) | — | OIL SEPERATOR lamba S14B beyaz `10 00279` veya tapa (görsel) |
| 7 | INADEQUATE WATER LEVEL | REDUCTOR FAILURE | PUMP FAILURE |
| 8 | — | POWER — kapak tipi pako (sarı/kırmızı) | — |
| 9 | — | Firma bilgisi, TÜV, CE | — |

- **R14.9 LYM uyarı lambaları** — 3 adet SİNYAL LAMBASI S14K KIRMIZI 220V `10 00278`: INADEQUATE WATER LEVEL, REDUCTOR FAILURE, PUMP FAILURE.
- **R14.10 LYM'de olmayanlar** — ORDEL, ekran, çift el kapak aç/kapat butonları, sepet test adı (buton yalnız «TEST» yazar).

### Model özeti

| Öğe | KBN 1B | KBN 2B | LYM |
|---|---|---|---|
| Ana kesme kolu | Pako | TMŞ döner kolu (kapakta, etikette değil) | Pako (POWER, en altta) |
| Üst | ORDEL | NB7W ekran | Acil stop |
| START / STOP | ORDEL varsa yok | Var | WASHING çift başlı buton |
| RESET (mavi) | Var | Var (SIFIRLA) | Var |
| SEPET TEST | Var | Yok | Var (TEST, beyaz) |
| Acil stop | Var | Var | Var (en üstte) |
| Çift el kapak aç/kapat | Var | Var | Yok |
| Zaman rölesi / termostat | Yok (ORDEL) | Yok (ekran) | DZ 482 `10 10465` / DT 481 `10 00237` |
| Isıtıcı | Beyaz lamba | Ekran | HEATER ışıklı mandal `10 00263` |
| Uyarı lambası (3 kırmızı) | Var | ? | Var |
| Yağ sıyırıcı buton + lamba | Opsiyon (yoksa tapa) | Yok — ekrandan | Opsiyon (yoksa tapa) |

## 15. Açık sorular

> [!UYARI]
> Kurallar aktarılırken görülen çelişki ve boşluklar. Birlikte karara bağlanınca ilgili kurala işlenip buradan silinir.

- **Q15** KBN 2B: TS002 (sıcaklık) ve ADB21 (analog) modülleri her panoda 1'er adet mi, sensör sayısına göre artar mı?
- **Q16** KBN 2B: Her kontaktör ve valf için bir PLC çıkışı ve bir yaprak röle mi sayılıyor? Lambalar da çıkış/röle alıyor mu?
- **Q17** KBN 1B döner nozzle: 6 sokete çıkınca eklenen 2 röle 220V (RXM4AB1P7) mi, 24V (RXM4AB1BD) mi?
- **Q18** KBN 2B etiketinde uyarı lambaları var mı (KBN 1B/LYM'deki 3 kırmızı gibi)?
- **Q19** Klemens: faz/nötr/toprak/kumanda/sensör klemenslerinin stok adı ve kodları; motor 4, ısıtıcı 3 dışında sayım kuralı.
- **Q20** Selenoid valf: kumanda gerilimi, sigortası, KBN 1B/LYM'de rölesi, KBN 2B'de çıkışı ve stok kodları.
- **Q21** Pano kutusu, DIN ray, kablo kanalı, kablo, yüksük depo listesine yazılıyor mu? Yazılıyorsa stok kodları.
- **Q22** Seri sınırları: 11 kW (25 A) üstü motor, tablo dışındaki güçler (0,18 / 0,25 / 15 kW …) için In kaynağı ve 0,4 / 7,5 kW dışındaki invertör boyları.
