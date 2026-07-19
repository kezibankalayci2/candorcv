# Gizlilik ve Veri Saklama

## İlk sürüm politikası

- Uygulama oturumluk bağlam kullanır; kalıcı kullanıcı profili oluşturmaz.
- Varsayılan oturum süresi 120 dakikadır ve yapılandırılabilir.
- CV, iş ilanı, analiz ve çıktı yalnızca aynı oturum içinde erişilebilir.
- Süresi dolan oturumlara ait kayıtlar bir sonraki bakım çalışmasında silinir.
- Ham kişisel içerik uygulama loglarına veya analitik olaylara yazılmaz.
- OpenAI adaptörü etkinse yalnızca analiz/optimizasyon için gerekli metin API'ye gönderilir.
- Gerçek kullanıcı verisi model eğitimi veya test fixture'ı olarak kullanılmaz.

## Kullanıcı kontrolü

Arayüz “Delete session data” işlemi sunar. Bu işlem CV metni, iş ilanı, analiz, karar ve optimize edilmiş çıktıyı aynı işlem içinde siler.

## Üretim öncesi zorunlu kararlar

Veri bölgesi, yedek saklama süresi, gizlilik bildirimi, veri işleyen alt sağlayıcılar ve silme hizmet seviyesi hukuk/güvenlik incelemesiyle kesinleştirilmelidir.

