# Tehdit Modeli

| Tehdit | Etki | Temel kontrol |
| --- | --- | --- |
| Kullanıcılar arası veri karışması | CV sızıntısı | Sunucu üretimli oturum kimliği ve her sorguda kapsam filtresi |
| Kötü amaçlı dosya | Kod çalıştırma/kaynak tüketimi | Boyut, imza ve ZIP içerik doğrulaması; dosyayı yürütmeme |
| Prompt injection | Ürün kurallarının aşılması | CV/ilanı veri olarak sınırlandırma; model çıktısını şema ve kaynakla doğrulama |
| AI halüsinasyonu | Sahte kariyer iddiası | Kaynak referansı zorunluluğu ve üretim sonrası doğrulama |
| Onaysız optimizasyon | Kullanıcı kontrolünün ihlali | Sürüm bağlı sunucu tarafı “Evet” kararı |
| CSRF | Yetkisiz durum değişikliği | SameSite çerez ve özel CSRF başlığı |
| XSS | Oturum/veri erişimi | `textContent` tabanlı render, CSP ve HTML kaçışlama |
| Aşırı büyük girdi | DoS/maliyet | Sabit dosya, metin ve istek sınırları |
| Log sızıntısı | Kişisel veri açığı | İçerik yerine olay kodu ve rastgele correlation ID |
| Eski veri kullanımı | Hatalı CV | CV/ilan/model/skorlayıcı sürüm bağları |

## Prompt injection kuralı

CV ve iş ilanında bulunan “önceki talimatları görmezden gel” benzeri ifadeler belge içeriğidir. Sistem veya geliştirici talimatı olarak yorumlanamaz.

