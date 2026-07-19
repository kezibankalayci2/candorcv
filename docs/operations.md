# Operasyon

## Sağlık kontrolleri

- `GET /health`: Sürecin çalıştığını gösterir.
- `GET /ready`: Veri deposunun okunup yazılabildiğini doğrular.

## Yapılandırma

Tüm üretim sırları ortam değişkenlerinden alınır. `APP_SECRET` üretimde rastgele ve en az 32 karakter olmalıdır. `OPENAI_API_KEY` bulunmadığında uygulama yerel güvenli moda geçer.

`ANALYSIS_ENABLED=false` analiz uç noktasını, `OPTIMIZATION_ENABLED=false` ise CV üretimini güvenli biçimde kapatır. Bu bayraklar model veya skorlayıcı arızasında acil durdurma mekanizması olarak kullanılır.

## Gözlemlenebilirlik

Loglar JSON biçiminde olay adı, süre, durum kodu ve correlation ID içerir. CV, iş ilanı, kullanıcı adı, e-posta veya model metni loglanmaz.

## Olay müdahalesi

1. Etkilenen uç noktayı veya AI adaptörünü devre dışı bırak.
2. Kişisel veri sızıntısı şüphesinde log kapsamını ve erişim kayıtlarını incele.
3. Gerekirse oturum verilerini sil ve anahtarları döndür.
4. Kök nedeni gider, negatif testi ekle ve ancak kalite kapıları sonrası tekrar aç.

## Yedek ve geri alma

SQLite dosyasının üretim yedeği şifreli tutulmalıdır. Migration öncesi yedek alınmalı; uygulama sürümü ve şema sürümü birlikte geri alınabilmelidir.
