# PLAN.md — Sıfırdan Üretime 10 Adımlık Uygulama Planı

Bu plan, AI destekli ATS uyumlu CV optimizasyon uygulamasını boş depodan güvenli bir ilk üretim sürümüne taşımak için izlenecek sırayı tanımlar. Adımlar birbirine bağımlıdır; bir adımın çıkış kriterleri sağlanmadan sonraki adım tamamlanmış sayılmaz.

> **Uygulama durumu (19 Temmuz 2026):** Adım 1–9 çalışan MVP kapsamında tamamlandı. Adım 10 için dağıtım paketi ve işletim prosedürleri hazırlandı; canlı barındırma ve kontrollü beta depo dışındaki ortamda yürütülecektir. Ayrıntılı kanıt: [`docs/implementation-status.md`](./docs/implementation-status.md).

Ana referanslar:

- Ürün kapsamı ve değişmez ilkeler: [`intent.md`](./intent.md)
- Geliştirme çalışma kuralları: [`AGENTS.md`](./AGENTS.md)
- Görsel tasarım sistemi: [`design.md`](./design.md)
- Hafıza ve veri saklama yaklaşımı: [`memory.md`](./memory.md)

Planın tüm aşamalarında şu kurallar geçerlidir:

- Kaynak CV'de bulunmayan hiçbir kariyer bilgisi üretilemez.
- Gerçeklik, ATS skorunu yükseltmekten daha önemlidir.
- Analiz ve optimize edilmiş CV İngilizce olmalıdır.
- Optimize edilmiş CV yalnızca analiz sonrasında alınan açık “Evet” onayıyla üretilebilir.
- İlk sürüm oturumluk bağlam kullanır; kalıcı kullanıcı hafızası kapsam dışıdır.
- Kişisel veriler loglara, test fixture'larına veya analitik olaylara yazılamaz.
- Her adım test, güvenlik ve gözlemlenebilirlik gereksinimleriyle birlikte tamamlanır.

## 1. Ürün Kararlarını ve Teknik Temeli Netleştir

**Amaç:** Kod yazmaya başlamadan önce ilk sürümün kesin sınırlarını, teknik mimarisini ve başarı ölçütlerini karar kayıtlarına dönüştürmek.

**Yapılacak işler:**

- [ ] `intent.md` içindeki fonksiyonel gereksinimleri MVP, sonraki sürüm ve kapsam dışı olarak etiketle.
- [ ] Desteklenecek ilk CV dosya türlerini belirle. Başlangıç için metin çıkarımı güvenilir tek veya iki formatla sınırlandır.
- [ ] Optimize edilmiş CV'nin ilk dışa aktarma formatını belirle.
- [ ] Web istemcisi, sunucu uygulaması, arka plan işleri ve veri katmanının sorumluluklarını ayıran üst düzey mimariyi tanımla.
- [ ] Uygulama dili, web çatısı, veritabanı, dosya işleme yaklaşımı, test araçları ve dağıtım hedefi için kısa teknik karar kayıtları oluştur.
- [ ] Model sağlayıcısından bağımsız bir AI adaptör sınırı tanımla; alan mantığını tek sağlayıcıya bağlama.
- [ ] Dosya boyutu, metin uzunluğu, istek süresi ve model bağlamı için başlangıç sınırları belirle.
- [ ] Ham CV, iş ilanı ve türetilmiş çıktıların saklama/silme politikasını yazılı hâle getir.
- [ ] İlk sürüm için kullanıcı hesabı gerekip gerekmediğini karara bağla. Hesap yoksa oturum izolasyonunu güvenli, kısa ömürlü kimlikle tasarla.
- [ ] Tehdit modeli çıkar: kişisel veri sızıntısı, kötü amaçlı dosya, prompt injection, kullanıcılar arası veri karışması, desteklenmeyen iddia üretimi ve yetkisiz çıktı erişimi.
- [ ] İngilizce sentetik CV ve iş ilanlarından oluşan küçük bir değerlendirme veri seti tasarla.

**Teslimatlar:**

- MVP kapsam listesi,
- Üst düzey mimari diyagramı,
- Teknik karar kayıtları,
- Veri saklama ve silme politikası,
- Tehdit modeli,
- İlk değerlendirme veri seti şeması.

**Çıkış kriteri:** Ekip, ilk sürümde hangi girdilerin destekleneceğini, verinin nereden geçeceğini, hangi verinin ne kadar süre tutulacağını ve sistemin hangi sınırlar içinde çalışacağını koddan bağımsız biçimde açıklayabilmelidir.

## 2. Depoyu, Geliştirme Ortamını ve Kalite Kapılarını Kur

**Amaç:** Tek komutlarla kurulabilen, test edilebilen ve güvenli biçimde geliştirilebilen proje iskeleti oluşturmak.

**Yapılacak işler:**

- [ ] Seçilen teknoloji yığınıyla istemci ve sunucu iskeletini oluştur.
- [ ] Kaynak kodu; arayüz, alan mantığı, dış entegrasyonlar ve ortak şemalar arasında anlaşılır biçimde ayır.
- [ ] Ortam değişkenleri için örnek dosya oluştur; gerçek anahtarları depoya ekleme.
- [ ] Biçimlendirme, lint, tip kontrolü, birim testi ve üretim derleme komutlarını tanımla.
- [ ] Kilit dosyasını ve tek paket yöneticisi standardını belirle.
- [ ] Test klasörlerini; birim, entegrasyon, sözleşme ve uçtan uca testler için yapılandır.
- [ ] Sentetik fixture üretme kurallarını tanımla; gerçek CV kullanımını yasakla.
- [ ] Pull request veya ana dal için otomatik kalite akışı kur: kurulum → lint → tip kontrolü → test → derleme.
- [ ] Bağımlılık güvenliği, secret taraması ve lisans kontrolü için temel kontroller ekle.
- [ ] Yerel geliştirme, test ve üretim yapılandırmalarını birbirinden ayır.
- [ ] Sağlık kontrolü ve yapılandırma doğrulaması sunan en küçük sunucu uç noktasını oluştur.

**Teslimatlar:**

- Çalışan proje iskeleti,
- Geliştirme ortamı talimatları,
- Otomatik kalite komutları,
- CI iş akışı,
- Ortam değişkeni şablonu,
- Temel sağlık kontrolü.

**Çıkış kriteri:** Temiz bir ortamda proje belgelenmiş komutlarla kurulmalı; lint, tip kontrolü, testler ve üretim derlemesi başarıyla tamamlanmalıdır.

## 3. Alan Modelini, Oturum Yönetimini ve Veri Güvenliğini Oluştur

**Amaç:** CV, iş ilanı, analiz, kullanıcı kararı ve çıktı arasındaki ilişkileri güvenli ve izlenebilir bir veri modeliyle kurmak.

**Yapılacak işler:**

- [ ] `user/session`, `cv_document`, `cv_version`, `job_target`, `analysis`, `consent_decision`, `optimization` ve `source_reference` varlıklarını tanımla.
- [ ] Her çalışma akışı için benzersiz `session_id`, her yükleme için değişmez `cv_version_id` ve her ilan için `job_target_id` üret.
- [ ] Analiz sonucunu CV sürümü, iş ilanı sürümü, model sürümü, prompt sürümü ve skorlayıcı sürümüne bağla.
- [ ] “Evet” veya “Hayır” kararını yalnızca ilgili oturum, CV sürümü ve iş ilanı için geçerli olacak şekilde modelle.
- [ ] `cv_analysis` ve `cv_optimization` süreçlerini yetki ve durum açısından ayır.
- [ ] İlk sürümde yalnızca oturumluk hafıza uygula; kalıcı profil veya semantik kullanıcı hafızası ekleme.
- [ ] Kayıt durumlarını tanımla: oluşturuldu, doğrulandı, işleniyor, tamamlandı, başarısız, süresi doldu, silindi.
- [ ] Veri erişimini sunucu tarafında oturum sahibine göre sınırla.
- [ ] Aktarım ve depolama şifrelemesini etkinleştir; geçici dosyaları güvenli ve kısa ömürlü alanda tut.
- [ ] Silme işlemini ham belge, çıkarılmış metin, analiz, çıktı, önbellek ve türev kayıtları kapsayacak biçimde tasarla.
- [ ] Loglama için izin verilen teknik alanların beyaz listesini oluştur.
- [ ] Veritabanı şeması ve API veri sözleşmelerini sürümlendir.

**Teslimatlar:**

- Alan modeli,
- Veritabanı şeması ve migration altyapısı,
- Oturum ve kaynak izolasyonu,
- Silme iş akışı,
- Sürüm bilgisi taşıyan API şemaları,
- Kişisel veri içermeyen olay/log şeması.

**Çıkış kriteri:** İki farklı kullanıcı veya oturumun verileri birbirine erişememeli; bir analiz ve onay kaydı yalnızca kendi CV ve iş ilanı sürümleriyle kullanılabilmelidir.

## 4. Güvenli CV Yükleme ve Metin Çıkarma Hattını Geliştir

**Amaç:** Desteklenen İngilizce CV dosyalarını güvenli biçimde kabul etmek, metni ve kaynak konumlarını kaybetmeden yapılandırılmış içeriğe dönüştürmek.

**Yapılacak işler:**

- [ ] Dosya yükleme API'sini boyut ve oran sınırlamasıyla oluştur.
- [ ] Dosya uzantısı, MIME türü ve gerçek dosya imzasını birlikte doğrula.
- [ ] Desteklenmeyen, boş, şifreli, bozuk veya metni çıkarılamayan dosyaları güvenli hata ile reddet.
- [ ] Yüklenen dosyayı yürütme; dosya adını güvenilir yol olarak kullanma.
- [ ] Seçilen formatlar için metin çıkarma adaptörleri oluştur.
- [ ] Sayfa, bölüm, paragraf veya karakter aralığı gibi kaynak konumlarını koru.
- [ ] CV bölümlerini yapılandır: iletişim, özet, deneyim, eğitim, beceriler, projeler ve sertifikalar.
- [ ] Tarih, unvan ve kurum gibi alanları orijinal metinle birlikte sakla; normalleştirme sırasında kaynağı kaybetme.
- [ ] Dil kontrolü uygula. İngilizce olmayan içeriği otomatik çevirmek yerine kullanıcıya açık hata göster.
- [ ] Metin çıkarma kalitesi yetersizse analizi başlatma.
- [ ] Dosya ve çıkarılmış metin için güvenli silme/sona erme işini bağla.
- [ ] Gerçek kullanıcı belgesi içermeyen sentetik ve bozuk dosya fixture'larıyla test et.

**Teslimatlar:**

- Güvenli yükleme bileşeni ve API'si,
- Format bazlı metin çıkarıcılar,
- Kaynak konumlu yapılandırılmış CV şeması,
- Dil ve kalite doğrulaması,
- Hata durumları ve test paketi.

**Çıkış kriteri:** Desteklenen sentetik CV'lerde gerekli içerik ve kaynak konumları güvenilir biçimde çıkarılmalı; tehlikeli veya okunamayan dosyalar analiz yapılmadan reddedilmelidir.

## 5. İş İlanı Girişi ve Normalizasyonunu Tamamla

**Amaç:** İngilizce iş tanımını güvenli, doğrulanmış ve analiz edilebilir bir yapıya dönüştürmek.

**Yapılacak işler:**

- [ ] İş ilanı metin alanını kalıcı etiket, yardımcı metin ve açık doğrulama mesajlarıyla geliştir.
- [ ] Boş, aşırı kısa, aşırı uzun veya analiz edilemeyen girdiler için sınırlar uygula.
- [ ] İngilizce dil kontrolü yap; otomatik çeviri ekleme.
- [ ] Prompt injection niteliğindeki metni güvenilmeyen veri olarak işaretle; sistem talimatı gibi yorumlama.
- [ ] İş ilanını başlık, sorumluluklar, zorunlu gereklilikler, tercih edilen gereklilikler, beceriler ve anahtar kelimeler olarak yapılandır.
- [ ] Kaynak ilan metnini ve yapılandırılmış alanları birbirine bağla.
- [ ] Aynı ilanın tekrar gönderilmesini algılamak için güvenli içerik özeti üret.
- [ ] İş ilanındaki gerekliliklerin kullanıcı becerisi olarak kaydedilemeyeceğini şema ve testlerle garanti et.
- [ ] CV ve iş ilanı tamamlanmadan analiz eylemini etkinleştirme.
- [ ] CV ve iş ilanı özetini analiz öncesinde kullanıcıya kontrol ettirilecek biçimde sun.

**Teslimatlar:**

- İş ilanı giriş bileşeni ve API sözleşmesi,
- Yapılandırılmış iş ilanı şeması,
- Dil, uzunluk ve güvenlik doğrulamaları,
- Sentetik ilan test paketi.

**Çıkış kriteri:** Sistem, İngilizce ve yeterli bir iş ilanını yapılandırabilmeli; eksik veya güvenilmeyen içeriği kullanıcı kariyer gerçeğine dönüştürmeden güvenli biçimde ele almalıdır.

## 6. Açıklanabilir Analiz ve Tahmini Skorlama Motorunu Kur

**Amaç:** CV ile iş ilanını tutarlı, sürümlenebilir ve açıklanabilir biçimde karşılaştırarak 0–100 aralığında tahmini uyum sonucu üretmek.

**Yapılacak işler:**

- [ ] Skoru tek bir model yargısına bırakmayan değerlendirme boyutları tanımla.
- [ ] Başlangıç boyutlarını belirle: zorunlu gereklilik uyumu, ilgili deneyim, doğrulanmış beceriler, sorumluluk benzerliği, eğitim/sertifika gereklilikleri ve ATS okunabilirliği.
- [ ] Her boyutun ağırlığını, puanlama mantığını ve nedenini sürümlendir.
- [ ] Zorunlu ile tercih edilen gereklilikleri farklı ağırlıklandır.
- [ ] Tam eşleşme, anlamca desteklenen eşleşme, CV'de görünmeyen alan ve doğrulanamayan alan durumlarını ayır.
- [ ] Anahtar kelime eşleşmesinde yalnızca yazım benzerliğine güvenme; anlam eşleşmesini kaynak kanıtıyla doğrula.
- [ ] AI çıktısını zorunlu şemaya bağla ve tür, aralık, liste boyutu ve zorunlu alan kontrolü uygula.
- [ ] 0–100 dışındaki veya gerekçesiyle çelişen skorları reddet.
- [ ] Çıktıda tahmini skor, güçlü yönler, eksik görünen alanlar, önemli anahtar kelimeler ve geliştirme noktalarını zorunlu kıl.
- [ ] Her olumlu eşleşmeyi kaynak CV konumuna, her ilan gerekliliğini kaynak ilan konumuna bağla.
- [ ] “CV'de görünmüyor” ifadesini “kullanıcı bu beceriye sahip değil” sonucuna dönüştürme.
- [ ] Model ve deterministik hesaplama sonuçlarını birleştiren, test edilebilir alan servisi oluştur.
- [ ] Temsili değerlendirme veri setinde skor kararlılığı ve gerekçe kalitesini ölç.

**Teslimatlar:**

- Sürümlü skorlama spesifikasyonu,
- Yapılandırılmış analiz servisi,
- Kaynak bağlantılı analiz çıktısı,
- Model adaptörü ve şema doğrulayıcı,
- Değerlendirme testleri ve başlangıç kalite raporu.

**Çıkış kriteri:** Aynı sürümlü girdilerde sonuç makul ölçüde tutarlı olmalı; skor gerekçelerle çelişmemeli ve analizdeki her kariyer iddiası kaynak CV kanıtına bağlanmalıdır.

## 7. Uçtan Uca Analiz Deneyimini Tasarım Sistemine Göre Uygula

**Amaç:** Kullanıcının CV yüklemeden analiz sonucuna kadar olan akışı erişilebilir, anlaşılır ve güven veren bir arayüzle tamamlamasını sağlamak.

**Yapılacak işler:**

- [ ] `design.md` tokenlarını uygulamanın tema veya stil değişkenlerine aktar.
- [ ] Mürekkep `#0B051D`, marka pembesi `#FFA8CD` ve tanımlı semantik renkleri sabit renkler yerine tokenlarla kullan.
- [ ] Mobil tek sütun ve masaüstü kontrollü iki sütun yerleşimini uygula.
- [ ] Adım göstergesini oluştur: CV yükleme → iş ilanı → analiz → karar → sonuç.
- [ ] Yükleme, iş ilanı ve analiz durumları için boş, yükleniyor, başarılı ve hata görünümlerini tamamla.
- [ ] Tahmini skoru yüzde, “tahmini” etiketi, kısa açıklama ve gerekçeyle birlikte göster.
- [ ] Güçlü yönler, eksik görünen alanlar, önemli anahtar kelimeler ve geliştirme noktaları için ayrı, taranabilir kartlar oluştur.
- [ ] Desteklenen ve CV'de görünmeyen anahtar kelimeleri yalnızca renkle değil metin ve ikonla ayır.
- [ ] Klavye dolaşımı, görünür odak, ekran okuyucu etiketleri, hata ilişkilendirmeleri ve en az 44×44px hedefleri uygula.
- [ ] Hareket azaltma tercihini destekle; sonucu dramatize eden veya kesinlik hissi veren animasyon kullanma.
- [ ] Analiz tamamlandıktan sonra bağımsız onay alanında “CV'nizi bu pozisyona göre yeniden düzenlemek ister misiniz?” sorusunu göster.
- [ ] “Evet” ve “Hayır” seçeneklerini eşit derecede açık, varsayılan seçim olmadan sun.

**Teslimatlar:**

- Responsive ana kullanıcı akışı,
- Tasarım tokenlarının uygulama karşılıkları,
- Analiz sonuç ekranı,
- Onay bileşeni,
- Erişilebilirlik kontrolleri ve görsel regresyon testleri.

**Çıkış kriteri:** Kullanıcı geçerli girdilerle ana akışı yardımsız tamamlayabilmeli; analiz bölümlerini ayırt edebilmeli ve CV üretmeden önce bilinçli “Evet” veya “Hayır” kararı verebilmelidir.

## 8. Onay Kontrollü CV Optimizasyonu, Doğrulama ve Dışa Aktarmayı Geliştir

**Amaç:** Yalnızca açık kullanıcı onayından sonra, kaynak CV'deki bilgileri koruyarak İngilizce ve ATS dostu CV üretmek.

**Yapılacak işler:**

- [ ] Optimizasyon API'sinde geçerli analiz ve ilgili “Evet” onayını sunucu tarafında zorunlu kıl.
- [ ] “Hayır” kararı sonrası optimizasyon işi oluşturulmasını şema, servis ve entegrasyon testleriyle engelle.
- [ ] CV üretim şemasını tanımla: iletişim, özet, deneyim, eğitim, beceriler, projeler ve sertifikalar.
- [ ] Yalnızca kaynak CV tarafından desteklenen bölümleri oluştur; boş bölümler veya tahmini içerik ekleme.
- [ ] İlgili mevcut deneyimleri yeniden sırala ve ifadeleri anlamı değiştirmeden profesyonelleştir.
- [ ] İş ilanı anahtar kelimelerini yalnızca kaynak CV'deki kanıtla destekleniyorsa kullan.
- [ ] Her üretilen maddeye kaynak CV'deki `source_reference` kayıtlarını bağla.
- [ ] Üretim sonrası doğrulama kapısı oluştur: kaynaksız iddia, değişmiş tarih, yeni sayı, yeni beceri, genişletilmiş sorumluluk ve dil ihlalini tespit et.
- [ ] Doğrulama başarısızsa kısmi veya şüpheli CV göstermeden üretimi güvenli biçimde durdur.
- [ ] Kaynak ve optimize edilmiş CV arasında değişiklik özeti sun.
- [ ] ATS dostu sade başlıklar, tek anlamlı okuma sırası ve karmaşık olmayan düzen kullan.
- [ ] İlk sürüm için belirlenen dosya formatında dışa aktarma oluştur.
- [ ] Dışa aktarılan dosyayı tekrar okuyarak içerik, sıra ve metin bütünlüğü kontrolü yap.

**Teslimatlar:**

- Yetki kontrollü optimizasyon servisi,
- Kaynak bağlantılı CV üretim şeması,
- Halüsinasyon ve anlam değişikliği doğrulayıcısı,
- Değişiklik özeti ve CV önizlemesi,
- ATS dostu dışa aktarma.

**Çıkış kriteri:** Optimize edilmiş CV'deki her bilgi kaynak CV ile ilişkilendirilebilmeli; kaynaksız bilgi oranı %0 olmalı ve “Hayır” akışında hiçbir CV çıktısı üretilememelidir.

## 9. Güvenlik, Kalite, Performans ve Uçtan Uca Doğrulamayı Tamamla

**Amaç:** Sistemin yalnızca mutlu yolda değil, kötü niyetli, hatalı ve sınır durumlarında da güvenli çalıştığını kanıtlamak.

**Yapılacak işler:**

- [ ] Alan servisleri için kapsamlı birim testleri yaz.
- [ ] Dosya çıkarma, veritabanı, model adaptörü ve dışa aktarma için entegrasyon testleri oluştur.
- [ ] CV yükleme → iş ilanı → analiz → karar → optimizasyon → indirme akışını uçtan uca test et.
- [ ] “Hayır” yolu, onaysız API çağrısı ve başka oturumun onayını kullanma girişimi için negatif testler ekle.
- [ ] Kaynakta olmayan deneyim, sayı, sertifika, tarih, beceri ve başarı ekleme girişimlerini değerlendirme setinde test et.
- [ ] CV ve iş ilanındaki prompt injection örneklerini test et.
- [ ] Kullanıcılar arası veri erişimi, tahmin edilebilir kimlikler ve yetki atlama senaryoları için güvenlik testleri yap.
- [ ] Dosya bombası, hatalı MIME, bozuk dosya, aşırı uzun metin, model zaman aşımı ve geçersiz model çıktısını test et.
- [ ] Log, hata, izleme ve analitik kayıtlarında kişisel veri taraması yap.
- [ ] Silme işleminin ham veri, türev, çıktı ve önbellekleri kapsadığını doğrula.
- [ ] Erişilebilirlik taraması ve klavyeyle manuel ana akış testi gerçekleştir.
- [ ] Temel performans bütçeleri belirle: yükleme, ayrıştırma, analiz, üretim ve sayfa etkileşimi.
- [ ] Model maliyeti, token kullanımı, başarısızlık oranı ve yeniden denemeleri kişisel veri toplamadan ölç.
- [ ] Model ve prompt sürümleri için regresyon değerlendirme kapısı oluştur.
- [ ] Kritik riskler için hata bütçesi, alarm ve güvenli geri dönüş davranışı tanımla.

**Teslimatlar:**

- Birim, entegrasyon ve uçtan uca test paketi,
- AI kalite ve halüsinasyon değerlendirme raporu,
- Güvenlik ve gizlilik kontrol raporu,
- Erişilebilirlik raporu,
- Performans ve maliyet başlangıç ölçümleri,
- Operasyon alarm ve geri dönüş planı.

**Çıkış kriteri:** Kritik ve yüksek riskli açık kalmamalı; kaynaksız bilgi üretimi, kullanıcılar arası sızıntı ve onaysız CV üretimi testlerde %0 olmalı; ana akış belirlenen performans ve erişilebilirlik kapılarını geçmelidir.

## 10. Üretim Dağıtımı, Kontrollü Beta ve Sürdürülebilir İşletimi Başlat

**Amaç:** Uygulamayı gözlemlenebilir, geri alınabilir ve kullanıcı geri bildirimiyle güvenli biçimde geliştirilebilir bir üretim ortamında çalıştırmak.

**Yapılacak işler:**

- [ ] Geliştirme, ön izleme ve üretim ortamlarını ayrı veri ve anahtarlarla kur.
- [ ] Veritabanı migration, dosya depolama, kuyruk/arka plan işi ve model yapılandırmasını üretime hazırla.
- [ ] Secret yönetimi, en az yetki erişimi, ağ kuralları, yedekleme ve geri yükleme prosedürlerini uygula.
- [ ] Alan adı, TLS, güvenlik başlıkları, oran sınırlama ve kötüye kullanım korumalarını etkinleştir.
- [ ] Sağlık, hazır olma ve bağımlılık kontrollerini dağıtım sistemine bağla.
- [ ] Kişisel veri içermeyen metrik, iz ve hata takibini etkinleştir.
- [ ] Model veya skorlayıcı arızasında analizi güvenli biçimde durduracak özellik bayrağı ya da kapatma mekanizması oluştur.
- [ ] Geri alma prosedürünü ve veritabanı migration geri dönüş stratejisini test et.
- [ ] Gizlilik bildirimi, veri saklama açıklaması, tahmini skor uyarısı ve kullanıcı silme yolunu yayımla.
- [ ] Sentetik kontrollerle üretim ana akışını düzenli izle.
- [ ] Sınırlı kullanıcı grubuyla kontrollü beta başlat; gerçek CV'leri inceleme veya eğitim verisi olarak toplama.
- [ ] Kullanıcı geri bildirimini doğruluk, açıklanabilirlik, kullanılabilirlik ve güven başlıklarında ölç.
- [ ] Beta sonuçlarına göre skor ağırlıklarını, promptları veya arayüzü yalnızca sürümlü değerlendirme sonrasında değiştir.
- [ ] Olay müdahale, veri ihlali, model bozulması ve sağlayıcı kesintisi prosedürlerini belgele.
- [ ] Üretim sonrası düzenli kalite değerlendirmesi ve bağımlılık güncelleme takvimi oluştur.

**Teslimatlar:**

- Çalışan üretim ortamı,
- Otomatik ve geri alınabilir dağıtım süreci,
- Gözlemlenebilirlik panelleri ve alarmlar,
- Gizlilik ve kullanıcı bilgilendirme metinleri,
- Kontrollü beta raporu,
- Olay müdahale ve bakım prosedürleri.

**Çıkış kriteri:** Uygulama üretimde güvenli biçimde erişilebilir olmalı; temel kullanıcı akışı sentetik ve gerçek beta senaryolarında çalışmalı; hata durumları gözlemlenebilmeli, dağıtım geri alınabilmeli ve kullanıcı verisi tanımlanan politika uyarınca silinebilmelidir.

---

Plan tamamlandığında ortaya çıkması gereken ilk üretim sürümü şunları yapar:

1. İngilizce CV'yi güvenli biçimde yükler ve okur.
2. İngilizce iş ilanını doğrular ve yapılandırır.
3. Kaynak bağlantılı, açıklanabilir ve tahmini uyum analizi üretir.
4. Güçlü yönleri, eksik görünen alanları, anahtar kelimeleri ve geliştirme önerilerini gösterir.
5. Kullanıcıdan açık optimizasyon kararı alır.
6. “Hayır” yanıtında süreci CV üretmeden bitirir.
7. “Evet” yanıtında yalnızca mevcut bilgileri kullanarak İngilizce, ATS dostu CV oluşturur.
8. Üretilen her iddiayı kaynak CV ile doğrular.
9. Sonucu kullanıcıya inceleme ve dışa aktarma olanağı verir.
10. Tüm akışı kişisel veri güvenliği, oturum izolasyonu ve gözlemlenebilirlik sınırları içinde çalıştırır.
