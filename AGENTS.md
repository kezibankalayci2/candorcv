# AGENTS.md

Bu dosya, bu depoda çalışan yapay zekâ ajanları ve geliştiriciler için çalışma kurallarını tanımlar. Ürünün kapsamı ve davranışına ilişkin ana kaynak [`intent.md`](./intent.md) dosyasıdır. Bu dosya ile `intent.md` arasında çelişki oluşursa ürün gerçekliği, güvenlik ve kullanıcı verisi açısından daha katı olan kural uygulanmalı; belirsizlik kullanıcıya bildirilmelidir.

Bu kurallar hızdan çok doğruluk, sadelik ve güvenilirliği gözetir. Açıkça basit ve düşük riskli işlerde gereksiz süreç üretmeden sağduyulu hareket edin.

## 1. Kodlamadan Önce Düşün

**Varsayım yapma, belirsizliği gizleme, önemli ödünleşimleri görünür kıl.**

Uygulamaya başlamadan önce:

- İlgili dosyaları, mevcut mimariyi, testleri ve proje talimatlarını inceleyin.
- Görevin başarı ölçütlerini somut ve doğrulanabilir biçimde belirleyin.
- Gerekli varsayımları açıkça belirtin. Güvenli ve geri alınabilir bir varsayımla ilerlenebiliyorsa bunu kaydedip devam edin.
- Birden fazla anlamlı yorum varsa ve sonuçları önemli ölçüde farklıysa seçenekleri kullanıcıya sunun; sessizce seçim yapmayın.
- Daha basit bir çözüm aynı ihtiyacı karşılıyorsa bunu tercih edin.
- Gereksinim, veri güvenliği veya ürün davranışı kritik ölçüde belirsizse uygulamayı durdurup netleştirme isteyin.
- Henüz seçilmemiş teknoloji, servis, dosya formatı veya ürün davranışını olmuş gibi kabul etmeyin.

## 2. Önce Sadelik

**İstenen problemi çözen en küçük ve anlaşılır değişikliği yapın. Spekülatif özellik eklemeyin.**

- Kullanıcının istemediği özellikleri geliştirmeyin.
- Tek kullanımlık kod için gereksiz soyutlama oluşturmayın.
- Talep edilmemiş esneklik, yapılandırma seçeneği veya eklenti sistemi eklemeyin.
- Varsayımsal gelecek ihtiyaçları için karmaşıklık üretmeyin.
- Gerçekte oluşamayacak durumlar için gereksiz hata yönetimi yazmayın; kullanıcı girdisi, dosya işleme, model çıktısı ve dış servis hataları gibi gerçek sınırları mutlaka ele alın.
- Yeni bağımlılık eklemeden önce mevcut araçlarla çözülüp çözülemeyeceğini kontrol edin.
- Çözüm bir kıdemli mühendise gereğinden karmaşık görünecekse sadeleştirin.

## 3. Cerrahi Değişiklikler Yap

**Yalnızca görevin gerektirdiği alanlara dokunun. Sadece kendi değişikliğinizin oluşturduğu dağınıklığı temizleyin.**

Mevcut kodu düzenlerken:

- İlgisiz kodu, yorumu, biçimlendirmeyi veya dosya düzenini “iyileştirmeyin”.
- Bozuk olmayan ve görevle ilişkisi bulunmayan alanları yeniden yapılandırmayın.
- Kişisel tercihiniz farklı olsa bile projenin mevcut stilini ve kalıplarını izleyin.
- İlgisiz ölü kod fark ederseniz kullanıcıya bildirin; açıkça istenmedikçe silmeyin.
- Kullanıcının mevcut değişikliklerini koruyun ve üzerine yazmayın.
- Değişikliğiniz nedeniyle kullanılmaz hâle gelen import, değişken, fonksiyon ve dosyaları temizleyin.
- Önceden var olan kullanılmayan öğeleri yalnızca görev açıkça gerektiriyorsa kaldırın.

Kontrol sorusu: Değişen her satır doğrudan kullanıcı talebine veya değişikliğin zorunlu güvenliğine bağlanabiliyor mu?

## 4. Hedef Odaklı ve Doğrulanabilir İlerle

**Başarı ölçütünü tanımlayın, uygulayın ve kanıtlayana kadar doğrulama döngüsünü sürdürün.**

Görevleri ölçülebilir sonuçlara dönüştürün:

- “Doğrulama ekle” → geçersiz girdileri kapsayan testleri tanımla, ardından testleri geçir.
- “Hatayı düzelt” → mümkünse hatayı yeniden üreten test ekle, düzeltmeyi yap ve testi geçir.
- “Yeniden yapılandır” → davranışı koruyan testleri önce ve sonra çalıştır.
- “AI çıktısını iyileştir” → temsili örnekler ve değişmez ürün kurallarıyla regresyon değerlendirmesi yap.

Çok adımlı işlerde kısa bir plan kullanın:

```text
1. [Adım] → doğrulama: [kontrol]
2. [Adım] → doğrulama: [kontrol]
3. [Adım] → doğrulama: [kontrol]
```

Değişiklik sonrasında:

- En dar ilgili testleri çalıştırın; ardından riskle orantılı daha geniş kontroller uygulayın.
- Projede tanımlı biçimlendirme, lint, tip kontrolü ve test komutlarını kullanın.
- Çalıştırılamayan kontrolleri ve nedenlerini açıkça bildirin.
- Test geçmesini tek başına yeterli saymayın; değişikliğin `intent.md` ilkelerine uygunluğunu da kontrol edin.

## 5. Değişmez Ürün Kuralları

Aşağıdaki kurallar hiçbir özellik, skor artışı veya kullanıcı deneyimi gerekçesiyle gevşetilemez:

1. **Kaynak CV tek gerçeklik kaynağıdır.** Kullanıcıya atfedilen her bilgi orijinal CV'de açık bir dayanağa sahip olmalıdır.
2. **Bilgi uydurulamaz.** Deneyim, eğitim, sertifika, proje, teknik yetkinlik, sorumluluk, tarih, unvan, ölçüm ve başarı üretilemez.
3. **Gerçeklik ATS skorundan önemlidir.** Daha yüksek tahmini uyum uğruna doğruluk feda edilemez.
4. **Yeniden ifade edilebilir, yeni olgu eklenemez.** Dil daha profesyonel ve güçlü yapılabilir; anlam, kapsam, kıdem, tarih ve sonuç değiştirilemez.
5. **Anahtar kelimeler kanıt gerektirir.** İş ilanındaki bir terim yalnızca kaynak CV tarafından anlam bakımından destekleniyorsa optimize edilmiş CV'ye eklenebilir.
6. **Eksik bilgi eksik kalır.** İş ilanında olup CV'de bulunmayan bir nitelik analizde belirtilebilir, CV'ye kullanıcıda varmış gibi yazılamaz.
7. **Her çıktı izlenebilir olmalıdır.** Optimize edilmiş CV'deki her iddia kaynak CV'deki dayanağıyla ilişkilendirilebilir olmalıdır.
8. **CV üretimi açık onay gerektirir.** Kullanıcı analiz sonrasında “Evet” demeden optimize edilmiş CV oluşturulamaz.
9. **“Hayır” kararı kesindir.** Kullanıcı “Hayır” seçerse analiz gösterilebilir ancak CV oluşturma aşamasına geçilemez.
10. **Uyum oranı tahmindir.** Gerçek ATS sonucu, belirli bir sağlayıcının skoru veya işe alım garantisi olarak sunulamaz.
11. **Belirsizlikte güvenli davranılır.** Bir ifadenin kaynağı veya doğruluğu belirsizse ifadeyi eklemeyin; belirsizliği açıkça belirtin.

Bu kurallar promptlarda, model çağrılarında, çıktı doğrulamasında, testlerde ve kullanıcı arayüzünde birlikte uygulanmalıdır. Yalnızca modele verilen talimata güvenmeyin; mümkün olan yerlerde deterministik doğrulamalar ve yapılandırılmış veri akışları kullanın.

## 6. Temel Kullanıcı Akışını Koru

Ana akış aşağıdaki sırayı korumalıdır:

1. İngilizce CV yüklenir ve okunabilirliği doğrulanır.
2. İngilizce iş ilanı girilir ve doğrulanır.
3. CV ile iş ilanı karşılaştırılır.
4. Tahmini uyum yüzdesi gerekçeleriyle sunulur.
5. Güçlü yönler, eksik görünen alanlar, önemli anahtar kelimeler ve geliştirme noktaları gösterilir.
6. Kullanıcıya CV'yi yeniden düzenlemek isteyip istemediği sorulur.
7. Yalnızca açık “Evet” yanıtında ATS uyumlu İngilizce CV oluşturulur.
8. “Hayır” yanıtında süreç yeni CV üretmeden sonlandırılır.

Bu sırayı değiştiren bir geliştirme, açık ürün gereksinimi ve buna uygun test olmadan yapılmamalıdır.

## 7. Dil Politikası

- Proje dokümantasyonu Türkçe hazırlanmalıdır.
- Kullanıcıdan alınan CV İngilizce olmalıdır.
- Kullanıcıdan alınan iş ilanı İngilizce olmalıdır.
- Kullanıcıya sunulan CV analizi İngilizce olmalıdır.
- Optimize edilmiş CV İngilizce olmalıdır.
- Sistem CV veya iş ilanını otomatik olarak başka bir dile çevirmemelidir.
- Kod içindeki adlandırma, mevcut proje standardı yoksa yaygın teknik uygulamaya uygun olarak İngilizce kullanılmalıdır.
- Kullanıcı arayüzü dili ayrıca kararlaştırılmadıkça ürün içeriğinin dil kurallarıyla karıştırılmamalıdır.

## 8. AI ve Skorlama Davranışı

- Skor hesaplama yöntemi açıklanabilir, tutarlı ve sürümlenebilir olmalıdır.
- Uyum yüzdesi ile sunulan gerekçeler birbiriyle çelişmemelidir.
- Model çıktısını güvenilir veri olarak doğrudan kabul etmeyin; şema, tür, aralık ve zorunlu alan kontrolleri uygulayın.
- 0–100 dışındaki skorları reddedin veya güvenli biçimde ele alın.
- “Eksik” ile “CV'de ifade edilmemiş” kavramlarını mümkün olduğunca ayırın; CV'de görünmeyen bir becerinin kullanıcıda kesinlikle olmadığını iddia etmeyin.
- Prompt ve model değişikliklerini davranış değişikliği olarak değerlendirin; temsili CV–iş ilanı örnekleriyle regresyon testi yapın.
- Model hatası, zaman aşımı veya geçersiz çıktı durumunda gerçek dışı bir sonuç üretmek yerine kullanıcıya güvenli hata ve yeniden deneme yolu sunun.
- Model sağlayıcısına özel davranışı alan mantığına yaymayın; entegrasyon sınırlarını belirgin tutun.

## 9. Gizlilik ve Güvenlik

CV'ler kişisel ve hassas bilgiler içerebilir. Bu nedenle:

- Yalnızca işlem için gereken veriyi toplayın ve işleyin.
- CV metnini, kişisel bilgileri, model girdilerini veya model çıktılarını gereksiz yere loglamayın.
- Loglarda mümkün olduğunca kimliksizleştirilmiş teknik metadata kullanın.
- Gizli anahtarları, erişim belirteçlerini ve kişisel verileri kaynak koda, test fixture'larına veya hata mesajlarına yazmayın.
- Gerçek kullanıcı CV'lerini test verisi olarak depoya eklemeyin; sentetik ve açıkça kurgusal fixture'lar kullanın.
- Dosya türü, boyutu ve içerik sınırlarını doğrulayın; dosya adlarına veya istemci tarafından gönderilen MIME türüne tek başına güvenmeyin.
- Yüklenen dosyaları yürütmeyin ve dosya yollarını kullanıcı girdisiyle güvensiz biçimde birleştirmeyin.
- Saklama ve silme davranışı açıkça tanımlanmadan veriyi kalıcı tutmayın.
- Yeni bir dış servis veya model sağlayıcısı eklerken hangi kullanıcı verisinin dışarı gönderildiğini açıkça değerlendirin.

## 10. Test Beklentileri

Değişiklik türüne göre en az aşağıdaki riskleri kapsayın:

- Geçerli İngilizce CV ve iş ilanı ile başarılı analiz,
- Eksik, boş, desteklenmeyen veya okunamayan CV,
- Eksik veya İngilizce olmayan iş ilanı,
- 0–100 aralığı ve skor–gerekçe tutarlılığı,
- Güçlü yönler, eksik alanlar, anahtar kelimeler ve önerilerin varlığı,
- “Evet” yanıtında CV üretimi,
- “Hayır” yanıtında kesinlikle CV üretilmemesi,
- Kaynak CV'de olmayan bilginin optimize edilmiş CV'ye eklenmemesi,
- Desteklenmeyen anahtar kelimenin CV'ye taşınmaması,
- Üretilen her iddianın kaynak CV ile ilişkilendirilebilmesi,
- Model hatası, zaman aşımı ve geçersiz yapılandırılmış çıktı,
- Kişisel verinin loglara veya hata mesajlarına sızmaması.

Bir AI davranışı yalnızca mutlu yol örneğiyle doğrulanmış sayılmaz. Olumsuz örnekler ve bilgi uydurma girişimleri özellikle test edilmelidir.

## 11. Depoyla Çalışma Kuralları

- İşe başlamadan önce depo kökündeki ve çalışılan alt dizinlerdeki ilgili `AGENTS.md` dosyalarını okuyun.
- Ürün kararı vermeden önce `intent.md` dosyasını kontrol edin.
- Mevcut teknoloji yığınını depo dosyalarından belirleyin; paket yöneticisi, framework veya test aracı varsaymayın.
- Projede tanımlı komutları kullanın. Sırf alışkanlık nedeniyle ikinci bir araç veya yapılandırma eklemeyin.
- Bağımlılık kilit dosyalarını yalnızca bağımlılık değişikliği gerçekten gerekiyorsa güncelleyin.
- Üretilmiş dosyaları, derleme çıktılarını, gizli anahtarları ve gerçek kullanıcı verilerini commit etmeyin.
- Destrüktif Git veya dosya işlemlerini açık kullanıcı talebi olmadan çalıştırmayın.
- İlgisiz mevcut değişiklikleri geri almayın veya üzerine yazmayın.

## 12. Tamamlama Ölçütü

Bir görev ancak aşağıdakiler sağlandığında tamamlanmış sayılır:

- Kullanıcının açık talebi karşılanmıştır.
- Değişiklik `intent.md` ve bu dosyadaki değişmez kurallarla uyumludur.
- İlgili testler ve kalite kontrolleri geçmiştir veya çalıştırılamama nedeni açıkça belirtilmiştir.
- Kaynak CV'de olmayan bilgi üretme riski artırılmamıştır.
- Kişisel veri güvenliği ve dil politikası korunmuştur.
- İlgisiz dosya veya davranış değiştirilmemiştir.
- Kullanıcıya yapılan değişiklikler, doğrulama sonucu ve varsa kalan riskler kısa ve net biçimde bildirilmiştir.

Bu kurallar; daha küçük ve izlenebilir değişiklikler, daha az gereksiz yeniden yazım, uygulama öncesinde görünür kılınan belirsizlikler ve doğrulanabilir ürün davranışı sağladığında amacına ulaşmış olur.
