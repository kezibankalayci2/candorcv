# ADR-0001: Bağımlılığı Düşük Python MVP Mimarisi

## Durum

Kabul edildi.

## Karar

İlk sürüm Python standart kütüphanesi tabanlı HTTP servisi, SQLite ve çerçevesiz HTML/CSS/JavaScript kullanacaktır. PDF metni için `pypdf`, DOCX için standart ZIP/XML ayrıştırması kullanılacaktır.

## Gerekçe

Boş depodan hızlı ve denetlenebilir başlangıç, az bağımlılık, tek süreçte güvenlik kurallarının görünürlüğü ve kolay test edilebilirlik.

## Sonuçlar

Yüksek trafik veya uzun süren işler oluştuğunda HTTP katmanı, iş kuyruğu ve veri deposu ayrıştırılmalıdır. Bu ADR, kalıcı olarak tek süreçte kalma zorunluluğu getirmez.

