# AI Destekli ATS Uyumlu CV Optimizasyon Uygulaması — Proje Niyet Dokümanı

Bu doküman, projenin temel amacını, kapsamını, kullanıcı problemini, çalışma prensiplerini ve başarı ölçütlerini tanımlar. Ürün, tasarım, yazılım geliştirme, yapay zekâ davranışı ve kalite güvence kararlarında ana referans olarak kullanılmalıdır.

## Proje Amacı

Projenin amacı, kullanıcının mevcut İngilizce CV'si ile başvurmak istediği pozisyona ait İngilizce iş ilanını birlikte analiz ederek CV'nin pozisyona tahmini uyumunu değerlendirmek ve kullanıcının açık onayı hâlinde CV'yi ATS (Aday Takip Sistemi) uyumluluğu açısından iyileştirmektir.

Uygulama iki temel değer sunar:

1. Kullanıcıya CV'sinin hedef pozisyonla ne ölçüde örtüştüğünü anlaşılır ve gerekçeli bir analizle göstermek.
2. Yalnızca kullanıcının mevcut CV'sindeki doğrulanabilir bilgileri kullanarak içeriği daha profesyonel, ilgili ve ATS tarafından daha kolay işlenebilir bir yapıya dönüştürmek.

Ürün, yüksek bir uyum yüzdesi üretmeyi tek başına amaçlamaz. Gerçekliğin korunması, önerilerin izlenebilir olması ve kullanıcının deneyimlerinin doğru temsil edilmesi her zaman ATS uyumunu artırma hedefinden önce gelir.

## Problem Tanımı

İş başvurularında kullanılan ATS sistemleri CV'leri biçim, bölüm yapısı, anahtar kelimeler ve iş ilanıyla içerik benzerliği gibi ölçütlere göre değerlendirebilir. Nitelikli adaylar dahi aşağıdaki nedenlerle hedef pozisyon açısından yeterince görünür olmayabilir:

- CV ile iş ilanındaki terminolojinin farklı olması,
- İlgili deneyim ve yetkinliklerin yeterince öne çıkarılmaması,
- CV yapısının otomatik sistemler tarafından kolay işlenememesi,
- Kullanıcının hangi beceri veya deneyimlerinin pozisyonla örtüştüğünü görememesi,
- Eksik anahtar kelimeler ile gerçekten eksik niteliklerin birbirinden ayırt edilememesi,
- CV ifadelerinin belirsiz, zayıf veya gereğinden uzun olması.

Mevcut üretken yapay zekâ çözümleri ise CV'yi güçlendirmeye çalışırken kullanıcının sağlamadığı deneyim, beceri veya başarıları ekleme riski taşıyabilir. Bu proje, CV optimizasyonunu doğruluk ve kaynak izlenebilirliği sınırları içinde gerçekleştirerek bu iki problemi birlikte çözmeyi hedefler.

Gösterilen uyum oranı bir tahmindir; belirli bir ATS sağlayıcısının gerçek skoru, işe alım kararı veya başvuru sonucuna ilişkin garanti değildir.

## Hedef Kullanıcılar

- İngilizce hazırlanmış mevcut bir CV ile İngilizce yayımlanmış pozisyonlara başvuran adaylar,
- CV'sini belirli bir iş ilanına göre uyarlamak isteyen iş arayanlar,
- ATS uyumluluğu konusunda sınırlı bilgiye sahip kullanıcılar,
- Kariyer değişikliği yapan ve mevcut aktarılabilir yetkinliklerini doğru biçimde öne çıkarmak isteyen kişiler,
- CV'sindeki bilgileri değiştirmeden anlatımını ve yapısını geliştirmek isteyen profesyoneller.

Kullanıcının işe alım, insan kaynakları veya teknik CV hazırlama konusunda uzman olması beklenmez.

## Kullanıcı Yolculuğu

1. Kullanıcı İngilizce CV dosyasını sisteme yükler.
2. Sistem dosyanın desteklenen bir formatta ve okunabilir olduğunu doğrular. İçerik çıkarılamazsa kullanıcıya anlaşılır bir hata mesajı gösterilir.
3. Kullanıcı başvurmak istediği pozisyonun İngilizce iş tanımını ve gerekliliklerini sisteme girer.
4. Sistem gerekli iki girdinin mevcut olduğunu doğrular ve CV ile iş ilanını analiz eder.
5. Sistem kullanıcıya CV'nin hedef pozisyonla tahmini uyum oranını yüzde olarak sunar. Bu oranın tahmini olduğu açıkça belirtilir.
6. Sistem uyum oranıyla birlikte şu analizleri sunar:
   - CV'nin pozisyon açısından güçlü yönleri,
   - Eksik veya yeterince görünür olmayan alanlar,
   - Pozisyon açısından önemli anahtar kelimeler,
   - CV'de geliştirilmesi gereken noktalar.
7. Sistem kullanıcıya **“CV'nizi bu pozisyona göre yeniden düzenlemek ister misiniz?”** sorusunu yöneltir.
8. Kullanıcı **“Evet”** seçerse sistem:
   - Mevcut CV'yi hedef pozisyona göre yeniden yapılandırır,
   - ATS tarafından kolay işlenebilen bir düzen kullanır,
   - CV içeriğini İngilizce olarak korur,
   - Mevcut bilgileri daha açık ve profesyonel ifadelerle sunar,
   - Pozisyonla ilgili mevcut deneyim ve yetkinlikleri öne çıkarır,
   - Yeni CV'deki her bilginin orijinal CV'deki dayanağını korur,
   - Kullanıcıya oluşturulan CV'yi inceleme ve uygun bir biçimde edinme olanağı sağlar.
9. Kullanıcı **“Hayır”** seçerse CV oluşturulmaz; analiz sonuçları gösterildikten sonra süreç sonlandırılır.

## Temel Özellikler

### CV yükleme ve içerik çıkarma

- İngilizce CV dosyasının sisteme yüklenmesi,
- Metin, bölüm ve temel CV yapısının analiz için çıkarılması,
- Okunamayan, boş veya desteklenmeyen dosyalar için hata yönetimi.

### İş ilanı girişi

- İngilizce iş tanımı ve gerekliliklerinin kullanıcı tarafından girilmesi,
- Boş, yetersiz veya analiz edilemeyen girişlerin doğrulanması.

### CV–pozisyon uyum analizi

- CV'deki deneyim, eğitim, beceri ve diğer doğrulanabilir bilgilerin iş ilanındaki beklentilerle karşılaştırılması,
- Tahmini uyum oranının yüzde olarak hesaplanması,
- Uyum oranını oluşturan temel gerekçelerin kullanıcıya açıklanması,
- Güçlü yönlerin, eksik görünen alanların, önemli anahtar kelimelerin ve iyileştirme fırsatlarının ayrı olarak sunulması.

### Kullanıcı onayı

- Analiz tamamlanmadan CV oluşturma aşamasına geçilmemesi,
- Yeniden düzenleme işlemi öncesinde kullanıcıdan açık bir **“Evet”** yanıtı alınması,
- **“Hayır”** yanıtında yeni CV üretmeden sürecin sonlandırılması.

### ATS uyumlu CV optimizasyonu

- Mevcut içeriğin ATS dostu bölüm yapısı ve sıralamayla yeniden düzenlenmesi,
- İş ilanıyla ilgili mevcut deneyim ve yetkinliklerin önceliklendirilmesi,
- Anlam ve gerçeklik korunarak ifadelerin profesyonelleştirilmesi,
- Uygun anahtar kelimelerin yalnızca orijinal CV'deki bilgilerle desteklendiğinde kullanılması,
- Oluşturulan içeriğin İngilizce tutulması.

### Kaynak izlenebilirliği ve doğruluk kontrolü

- Üretilen her bilgi parçasının orijinal CV'deki bir bilgiyle ilişkilendirilebilir olması,
- Kaynağı bulunmayan ifadelerin çıktıya eklenmemesi,
- Belirsiz bilgilerin kesin bir gerçek gibi genişletilmemesi,
- Eksik niteliklerin kullanıcıda varmış gibi CV'ye yazılmaması.

## Fonksiyonel Gereksinimler

### Girdi gereksinimleri

- **FR-01:** Sistem, kullanıcının İngilizce CV dosyasını yüklemesine izin vermelidir.
- **FR-02:** Sistem, yüklenen dosyanın desteklenen formatta, boş olmayan ve metni çıkarılabilir durumda olup olmadığını kontrol etmelidir.
- **FR-03:** Sistem, kullanıcının İngilizce iş ilanı metnini girmesine izin vermelidir.
- **FR-04:** Sistem, CV ve iş ilanı sağlanmadan analizi başlatmamalıdır.
- **FR-05:** Sistem, girdinin İngilizce olmadığı tespit edildiğinde kullanıcıyı bilgilendirmeli; içeriği kendiliğinden başka bir dile çevirmemelidir.

### Analiz gereksinimleri

- **FR-06:** Sistem, CV'deki doğrulanabilir içerik ile iş ilanındaki sorumlulukları, gereklilikleri ve anahtar kavramları karşılaştırmalıdır.
- **FR-07:** Sistem, CV'nin pozisyonla tahmini uyum oranını 0–100 aralığında yüzde olarak göstermelidir.
- **FR-08:** Sistem, uyum oranını bir tahmin olarak etiketlemeli ve gerçek ATS sonucu ya da işe alım garantisi olarak sunmamalıdır.
- **FR-09:** Sistem, uyum değerlendirmesinin temel gerekçelerini kullanıcı tarafından anlaşılabilir biçimde açıklamalıdır.
- **FR-10:** Sistem; güçlü yönleri, eksik görünen alanları, önemli anahtar kelimeleri ve geliştirme önerilerini ayrı bölümler hâlinde sunmalıdır.
- **FR-11:** Sistem, CV'de bulunmayan bir niteliği “eksik” veya “doğrulanamıyor” olarak işaretleyebilmeli ancak bu niteliği kullanıcıya aitmiş gibi ifade etmemelidir.
- **FR-12:** Analiz çıktısı İngilizce olmalıdır.

### Karar ve optimizasyon gereksinimleri

- **FR-13:** Sistem, analiz sonrasında kullanıcıya “CV'nizi bu pozisyona göre yeniden düzenlemek ister misiniz?” sorusunu sormalıdır.
- **FR-14:** Sistem, yalnızca kullanıcının açık “Evet” onayından sonra optimize edilmiş CV üretmelidir.
- **FR-15:** Kullanıcı “Hayır” seçtiğinde sistem yeni CV üretmemeli ve oluşturma sürecini sonlandırmalıdır.
- **FR-16:** Optimize edilmiş CV İngilizce olmalı ve kaynak CV'nin dilini değiştirmemelidir.
- **FR-17:** Sistem, kaynak CV'deki mevcut bilgileri ATS uyumlu başlıklar, bölümler ve sıralamayla yeniden yapılandırmalıdır.
- **FR-18:** Sistem, pozisyonla ilgili mevcut deneyim ve yetkinlikleri görünür ve öncelikli hâle getirmelidir.
- **FR-19:** Sistem, doğruluk korunmak şartıyla zayıf veya belirsiz ifadeleri daha açık, öz ve profesyonel biçimde yeniden yazabilmelidir.
- **FR-20:** Sistem; kaynak CV'de bulunmayan deneyim, eğitim, sertifika, proje, teknik yetkinlik, sorumluluk, tarih, ölçüm veya başarı eklememelidir.
- **FR-21:** Sistem, iş ilanındaki bir anahtar kelimeyi ancak kaynak CV'deki bilgiyle anlam bakımından destekleniyorsa optimize edilmiş CV'de kullanmalıdır.
- **FR-22:** Optimize edilmiş CV'deki her iddia, kaynak CV'deki dayanak bilgiyle ilişkilendirilebilir olmalıdır.
- **FR-23:** Sistem, kullanıcıya optimize edilmiş CV'yi inceleyebileceği açık bir çıktı sunmalıdır.

### Hata ve güven sınırı gereksinimleri

- **FR-24:** Sistem, CV içeriğini güvenilir biçimde çıkaramadığında analiz veya CV üretimi yapmamalı ve kullanıcıdan uygun bir dosya istemelidir.
- **FR-25:** Sistem, bir ifadenin kaynak CV tarafından desteklenip desteklenmediğinden emin değilse ifadeyi eklememeli veya belirsizliği açıkça belirtmelidir.
- **FR-26:** Sistem, analiz veya üretim işlemi başarısız olduğunda kullanıcıya anlaşılır bir hata mesajı ve güvenli bir yeniden deneme yolu sunmalıdır.

## Fonksiyonel Olmayan Gereksinimler

### Doğruluk ve güvenilirlik

- Sistem, kaynak CV'de bulunmayan bilgilerin üretilmesini engelleyen kontroller içermelidir.
- Aynı CV ve iş ilanı için değerlendirme mantığı makul ölçüde tutarlı olmalıdır.
- Uyum oranı, sunulan gerekçelerle çelişmemelidir.
- Modelin emin olmadığı durumlar kesinlik izlenimi yaratmadan belirtilmelidir.

### Gizlilik ve güvenlik

- CV'lerde bulunan kişisel veriler hassas veri olarak ele alınmalıdır.
- Veri aktarımı ve saklama sırasında sektör standardı güvenlik önlemleri uygulanmalıdır.
- CV ve iş ilanı verileri, kullanıcıya açıkça bildirilen amaçların dışında kullanılmamalıdır.
- Verilerin saklanma süresi, silinme yöntemi ve erişim politikası kullanıcıya açık olmalıdır.
- Yetkisiz erişimi önlemek için uygun kimlik doğrulama, yetkilendirme ve kayıt mekanizmaları kullanılmalıdır.

### Kullanılabilirlik ve erişilebilirlik

- Kullanıcı akışı, teknik veya işe alım uzmanlığı gerektirmeden tamamlanabilmelidir.
- Uyum oranı ve öneriler sade, açıklanabilir ve eyleme dönük biçimde gösterilmelidir.
- Hata ve doğrulama mesajları kullanıcıya sorunun nedenini ve çözümünü anlatmalıdır.
- Arayüz, uygulanabilir erişilebilirlik standartlarını gözetmelidir.

### Performans ve ölçeklenebilirlik

- Analiz ve CV üretimi, kullanıcıya işlem durumunu gösterecek ve makul bekleme süresi sağlayacak şekilde tasarlanmalıdır.
- Dosya boyutu, metin uzunluğu ve eş zamanlı kullanım için açık sistem sınırları belirlenmelidir.
- Sistem, kullanıcı sayısı arttığında analiz kalitesini ve veri izolasyonunu koruyabilecek biçimde ölçeklenebilmelidir.

### Bakım ve gözlemlenebilirlik

- Analiz, skor hesaplama ve CV oluşturma bileşenleri birbirinden ayrıştırılabilir ve test edilebilir olmalıdır.
- Hatalar, gecikmeler ve başarısız analizler kişisel verileri gereksiz yere kaydetmeden izlenebilmelidir.
- Yapay zekâ modeli veya değerlendirme yöntemi değiştiğinde çıktı kalitesi yeniden ölçülmelidir.
- Prompt, model ve değerlendirme ölçütlerindeki önemli değişiklikler sürümlenmelidir.

### Uyumluluk

- Üretilen CV, yaygın ATS sistemlerinin okuyabildiği sade başlık, metin ve bölüm yapılarını hedeflemelidir.
- Sistem, belirli bir ATS sağlayıcısıyla resmî entegrasyon veya kesin uyumluluk garantisi iddiasında bulunmamalıdır.

## Proje Kapsamı

Proje kapsamında aşağıdaki yetenekler yer alır:

- İngilizce CV dosyasının alınması ve metin içeriğinin çıkarılması,
- İngilizce iş ilanı metninin alınması,
- CV ile iş ilanının anlam, beceri, deneyim, sorumluluk ve anahtar kelime açısından karşılaştırılması,
- Tahmini uyum oranının ve gerekçeli analiz sonuçlarının sunulması,
- Güçlü yönlerin, eksik görünen alanların, önemli anahtar kelimelerin ve iyileştirme noktalarının belirlenmesi,
- Kullanıcı onayıyla mevcut CV'nin hedef pozisyona göre İngilizce ve ATS uyumlu biçimde yeniden düzenlenmesi,
- Mevcut deneyim ve yetkinliklerin profesyonel ifadelerle öne çıkarılması,
- Kaynak CV ile optimize edilmiş CV arasında bilgi izlenebilirliğinin korunması,
- Sonucun kullanıcı tarafından incelenebilir ve kullanılabilir bir çıktı olarak sunulması.

Desteklenen dosya türleri, dışa aktarma biçimleri, azami dosya boyutu ve saklama süreleri teknik tasarım aşamasında netleştirilecektir; bu kararlar doğruluk ve gizlilik ilkelerini zayıflatamaz.

## Kapsam Dışı Özellikler

- Kullanıcı adına yeni deneyim, eğitim, sertifika, proje, beceri, sorumluluk veya başarı üretmek,
- Kaynakta olmayan sayısal sonuçlar, başarı ölçümleri, unvanlar ya da çalışma tarihleri eklemek,
- CV veya iş ilanını başka bir dile çevirmek,
- Türkçe ya da İngilizce dışındaki CV ve iş ilanlarını analiz etmek,
- Kullanıcı adına iş başvurusu yapmak veya başvuruyu otomatik göndermek,
- İşe alınma, mülakata çağrılma ya da belirli bir ATS skoruna ulaşma garantisi vermek,
- Belirli bir ATS sağlayıcısının özel veya kapalı değerlendirme algoritmasını taklit ettiğini iddia etmek,
- Kullanıcı adına referans, ön yazı, portföy, sertifika veya destekleyici belge uydurmak,
- İş ilanında yer alan fakat CV'de doğrulanamayan nitelikleri optimize edilmiş CV'ye eklemek,
- Kariyer, hukuk, göçmenlik veya işe alım sonucu hakkında profesyonel garanti niteliğinde danışmanlık sunmak,
- Kullanıcının açık onayı olmadan optimize edilmiş CV oluşturmak.

## Başarı Kriterleri

Projenin başarısı yalnızca üretilen uyum yüzdesinin yüksekliğiyle değil, doğruluk, kullanılabilirlik ve kullanıcı güveniyle ölçülür.

- Analiz tamamlandığında kullanıcı tahmini uyum oranını ve bu oranın temel gerekçelerini görebilmelidir.
- Her analiz; güçlü yönler, eksik görünen alanlar, önemli anahtar kelimeler ve geliştirme önerileri içermelidir.
- Optimize edilmiş CV'deki bilgilerin tamamı kaynak CV'deki bilgilerle ilişkilendirilebilir olmalıdır.
- Kaynakta bulunmayan bilgi eklenme oranı hedef olarak **%0** olmalıdır.
- Kullanıcının “Hayır” seçtiği hiçbir akışta yeni CV oluşturulmamalıdır.
- Optimize edilmiş CV'nin dili İngilizce kalmalı ve içerik başka bir dile çevrilmemelidir.
- İş ilanındaki anahtar kelimeler yalnızca kullanıcının mevcut, doğrulanabilir geçmişiyle uyumlu olduğunda kullanılmalıdır.
- Optimize edilmiş çıktı, ATS tarafından işlenebilir sade ve tutarlı bir bölüm yapısına sahip olmalıdır.
- Kullanıcı, önerilerin hangilerinin güçlü yön, eksik alan ve anlatım iyileştirmesi olduğunu kolayca ayırt edebilmelidir.
- Hatalı veya okunamayan girdiler, gerçek dışı bir analiz üretmek yerine güvenli biçimde reddedilmelidir.
- Kullanıcı testlerinde hedef kullanıcılar ana akışı dışarıdan yardım almadan tamamlayabilmelidir.

Nicel performans hedefleri; doğruluk değerlendirme veri seti, desteklenen dosya biçimleri, kullanıcı araştırması ve altyapı kapasitesi belirlendikten sonra ayrıca tanımlanmalıdır.

## Temel Prensipler

1. **Gerçeklik önce gelir.** Gerçeklik ve doğruluk, ATS skorunu yükseltmekten daha önemlidir.
2. **Bilgi uydurulmaz.** Yapay zekâ hiçbir koşulda deneyim, eğitim, sertifika, proje, teknik yetkinlik, sorumluluk veya başarı uyduramaz.
3. **Kaynak CV tek gerçeklik kaynağıdır.** Kullanıcıya ait olduğu ileri sürülen her bilgi, orijinal CV'de bir dayanağa sahip olmalıdır.
4. **Yeniden yapılandırma serbest, icat yasaktır.** Mevcut bilgiler yeniden sıralanabilir, sadeleştirilebilir ve daha güçlü ifade edilebilir; yeni olgular eklenemez.
5. **Anahtar kelime kullanımı kanıta dayanır.** İş ilanındaki bir terim yalnızca kullanıcının mevcut deneyim veya yetkinliğiyle gerçekten örtüşüyorsa CV'ye dâhil edilebilir.
6. **Eksik olan eksik olarak gösterilir.** CV'de bulunmayan bir gereklilik kullanıcıya analiz sonucu olarak bildirilebilir; kullanıcıda varmış gibi yazılamaz.
7. **İzlenebilirlik korunur.** Yeni CV'deki her bilgi, orijinal CV'deki karşılığıyla ilişkilendirilebilir olmalıdır.
8. **Kullanıcı kontrolü esastır.** Optimize edilmiş CV, yalnızca kullanıcının açık onayıyla oluşturulur.
9. **Şeffaflık korunur.** Uyum oranı tahmini olarak sunulur; gerçek bir ATS sonucu veya işe alım garantisi gibi gösterilmez.
10. **Anlam korunur.** Profesyonelleştirme sırasında cümlelerin tonu güçlendirilebilir ancak sorumlulukların kapsamı, kıdem düzeyi, tarihleri veya sonuçları değiştirilemez.
11. **Gizlilik tasarımın parçasıdır.** CV içeriği ve kişisel veriler yalnızca gerekli amaç ve süre kapsamında işlenir.
12. **Belirsizlikte güvenli davranılır.** Bir bilginin doğruluğu veya kaynağı konusunda şüphe varsa bilgi eklenmez; gerekli durumda kullanıcıya belirsizlik bildirilir.

## Dil Politikası

- Proje dokümantasyonu ve ekip içi ürün tanımları Türkçe hazırlanacaktır.
- Kullanıcının yüklediği CV İngilizce olmalıdır.
- Kullanıcının girdiği iş ilanı, iş tanımı ve gereklilikler İngilizce olmalıdır.
- CV–iş ilanı analizinin kullanıcıya sunulan içeriği İngilizce olmalıdır.
- Optimize edilerek oluşturulan yeni CV İngilizce olmalıdır.
- Sistem, İngilizce CV içeriğini optimize eder; içeriği farklı bir dile çevirmez.
- Profesyonelleştirme işlemi dil değişikliği değil, İngilizce içeriğin açıklık, tutarlılık, uygun terminoloji ve ATS okunabilirliği açısından iyileştirilmesidir.
- İngilizce olmayan veya güvenilir biçimde İngilizce olduğu doğrulanamayan girdiler otomatik olarak çevrilmemeli; kullanıcıdan İngilizce içerik sağlaması istenmelidir.
