# CandorCV — AI Destekli, Kanıta Dayalı ATS CV Optimizasyonu

**Every claim, grounded.**

CandorCV; İngilizce CV ile İngilizce iş ilanını karşılaştıran, açıklanabilir bir tahmini uyum analizi sunan ve yalnızca açık kullanıcı onayıyla kaynak CV'ye bağlı ATS dostu çıktı oluşturan web uygulamasıdır.

## Hızlı başlangıç

Gereksinim: Python 3.11 veya üzeri.

```powershell
Copy-Item .env.example .env
python -m app.server
```

Ardından `http://127.0.0.1:8000` adresini açın.

OpenAI destekli analiz için `.env` içinde `OPENAI_API_KEY` ayarlayın. Anahtar yoksa uygulama güvenli yerel analiz modunu kullanır; bu mod kaynak CV'yi yeniden ifade etmez veya yeni bilgi eklemez.

## Vercel dağıtımı

Depo Vercel Python Runtime için hazırdır. `api/index.py`, veriyi kalıcı sunucu diskine yazmadan kısa ömürlü ve imzalı tarayıcı oturumu kullanır.

Vercel projesinde en az şu ortam değişkenini tanımlayın:

```text
APP_SECRET=<en-az-32-karakter-rastgele-değer>
```

İsteğe bağlı AI desteği için `OPENAI_API_KEY` ve `OPENAI_MODEL` eklenebilir. GitHub deposu Vercel'e bağlandığında `main` dalındaki her push otomatik üretim dağıtımı başlatır.

## Kalite komutları

```powershell
python -m unittest discover -s tests -v
python -m compileall app tests
```

## Temel güvenlik kuralları

- Kaynak CV'de olmayan bilgi üretilemez.
- İş ilanındaki gereklilik kullanıcı becerisi sayılmaz.
- CV optimizasyonu yalnızca ilgili analiz için açık “Evet” onayından sonra yapılır.
- Oturum verileri kısa ömürlüdür; ham kişisel içerik loglanmaz.
- Gerçek kullanıcı CV'leri test verisi olarak depoya eklenmez.

## Dokümantasyon

- [Ürün niyeti](./intent.md)
- [Uygulama planı](./plan.md)
- [Tasarım sistemi](./design.md)
- [Hafıza yaklaşımı](./memory.md)
- [Mimari](./docs/architecture.md)
- [Gizlilik](./docs/privacy.md)
- [Tehdit modeli](./docs/threat-model.md)
- [Operasyon](./docs/operations.md)
- [Uygulama durumu](./docs/implementation-status.md)
- [Marka ve logo](./docs/brand.md)
