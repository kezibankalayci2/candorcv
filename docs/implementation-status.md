# Uygulama Durumu

Bu belge, `plan.md` içindeki on adımın mevcut depo karşılığını kaydeder. İlk dokuz adım çalışan MVP kapsamında tamamlanmıştır. Onuncu adım için üretim paketi, CI ve operasyon prosedürleri hazırdır; gerçek bir alan adına canlı dağıtım ve kontrollü beta, depo dışında bir barındırma hedefi ve kullanıcı grubu gerektirir.

## 1. Ürün ve teknik temel — Tamamlandı

- PDF ve DOCX girdi, düz metin (`.txt`) çıktı sınırı belirlendi.
- Tek süreçli web uygulaması, SQLite veri katmanı ve sağlayıcıdan bağımsız AI adaptörü kuruldu.
- Mimari ve AI sağlayıcı kararları ADR olarak kaydedildi.

## 2. Depo ve kalite altyapısı — Tamamlandı

- Python paket yapısı, statik istemci, test dizini, kalite betiği ve GitHub Actions iş akışı oluşturuldu.
- Örnek ortam yapılandırması ve sırları dışlayan `.gitignore` eklendi.

## 3. Alan modeli ve oturum güvenliği — Tamamlandı

- Oturum, CV, iş hedefi, analiz, karar ve optimizasyon kayıtları SQLite şemasında ilişkilendirildi.
- HttpOnly/SameSite oturum çerezi, CSRF kontrolü, rastgele kimlikler, TTL temizliği, cascade silme ve oturum izolasyonu uygulandı.

## 4. CV yükleme ve çıkarma — Tamamlandı

- Dosya boyutu, uzantı ve gerçek imza doğrulaması eklendi.
- PDF ve DOCX çıkarıcıları; bölüm, blok ve kaynak konumu üretir.
- Bozuk, boş, şifreli, desteklenmeyen ve İngilizce olmayan belgeler analizden önce reddedilir.

## 5. İş ilanı normalizasyonu — Tamamlandı

- İngilizce, uzunluk ve kalite kontrolleri uygulanır.
- Sorumluluklar, gereklilikler, beceriler ve anahtar kelimeler yapılandırılır.
- İlan metni güvenilmeyen veri olarak işlenir; kullanıcı deneyimine dönüştürülmez.

## 6. Açıklanabilir analiz — Tamamlandı

- Sürümlü ve ağırlıklı 0–100 tahmini skor hesaplanır.
- Güçlü yönler, CV'de görünmeyen alanlar, desteklenen/eksik anahtar kelimeler ve geliştirme önerileri kaynak referanslarıyla döndürülür.
- AI kullanılamazsa doğrulanabilir yerel analiz güvenli geri dönüş olarak çalışır.

## 7. Kullanıcı deneyimi — Tamamlandı

- `design.md` renk ve düzen tokenları responsive, klavye erişilebilir arayüze aktarıldı.
- Yükleme, ilan, analiz, bağımsız Evet/Hayır kararı, sonuç önizleme, indirme ve oturum silme akışları uygulandı.
- Masaüstü ve 390 px mobil görünümde konsol hatası ve yatay taşma olmadan doğrulandı.

## 8. Onay kontrollü optimizasyon — Tamamlandı

- Sunucu ilgili analiz için açık “Evet” kararı olmadan optimizasyon üretmez.
- Çıktı İngilizce kalır; kaynak bloklarla bire bir ilişkilendirilir.
- Yeni sayı, iletişim bilgisi, URL veya yalnızca iş ilanında bulunan beceri eklenmesi doğrulama kapısında engellenir.

## 9. Güvenlik ve kalite — Tamamlandı

- Birim, entegrasyon ve HTTP uçtan uca testleri bulunur.
- Olumsuz yol; CSRF, oturum izolasyonu, “Hayır” kararı, zararlı AI çıktısı, dil, dosya imzası ve veri silme senaryolarını kapsar.
- CSP, güvenlik başlıkları, istek zaman aşımı, oran sınırlama ve kişisel veri içermeyen yapılandırılmış loglama etkinleştirildi.

## 10. Dağıtım ve işletim — Dağıtıma hazır

- Root olmayan, salt okunur dosya sistemiyle çalışabilen Docker imajı ve Compose tanımı oluşturuldu.
- Sağlık/hazır olma uç noktaları, CI, gizlilik, tehdit modeli, olay müdahale ve geri alma dokümanları eklendi.
- `ANALYSIS_ENABLED` ve `OPTIMIZATION_ENABLED` acil durdurma bayrakları sağlandı.
- Canlı alan adı/TLS, harici sır yönetimi, üretim metriği ve kontrollü beta çalışması barındırma ortamında etkinleştirilmelidir.

## Doğrulama özeti

- Python derleme kontrolü: başarılı.
- JavaScript sözdizimi kontrolü: başarılı.
- Otomatik test paketi: başarılı.
- Chromium masaüstü ve mobil görsel kontrol: başarılı; konsol hatası ve mobil yatay taşma yok.
