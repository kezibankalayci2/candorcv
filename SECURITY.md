# Güvenlik Politikası

Güvenlik açığı bildirimleri herkese açık issue içinde kişisel veri veya istismar ayrıntısı paylaşılmadan yapılmalıdır. Üretim iletişim kanalı belirlenene kadar gerçek kullanıcı CV'siyle güvenlik testi yapılmamalıdır.

## Hassas alanlar

- Kullanıcılar arası oturum izolasyonu,
- CV ve iş ilanı kişisel verileri,
- Açık onay olmadan optimizasyon,
- Kaynakta bulunmayan kariyer iddiaları,
- Dosya ayrıştırma ve prompt injection,
- API anahtarları ve üretim sırları.

Bir olayda önce ilgili uç nokta veya AI adaptörü kapatılmalı, anahtarlar döndürülmeli ve kişisel içerik loglara kopyalanmadan etki analizi yapılmalıdır.

