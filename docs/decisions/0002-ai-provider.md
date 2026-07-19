# ADR-0002: Sağlayıcı Adaptörü ve Güvenli Yerel Mod

## Durum

Kabul edildi.

## Karar

Alan mantığı bir `AIProvider` arayüzüne bağlı olacaktır. İlk dış adaptör OpenAI API'dir ve varsayılan model `gpt-5.6-luna` olarak yapılandırılır. API anahtarı yoksa deterministik yerel analiz çalışır; yerel optimizasyon yalnızca kaynak metni ATS dostu düzene getirir ve yeni iddia üretmez.

## Gerekçe

Model sağlayıcısını alan mantığından ayırmak, testleri ağdan bağımsız kılmak ve servis kesintisinde sahte sonuç yerine güvenli davranmak.

## Sonuçlar

AI destekli profesyonel yeniden ifade için üretimde geçerli API anahtarı gerekir. Model ve prompt sürümleri her analiz kaydına yazılır.

