---
version: alpha
name: Kanıt Odaklı Güven
description: AI destekli ATS uyumlu CV optimizasyon uygulaması için koyu mürekkep ve ölçülü pembe vurgular kullanan, profesyonel ve açıklanabilir görsel sistem.
colors:
  primary: "#0B051D"
  primary-hover: "#211735"
  primary-pressed: "#000000"
  on-primary: "#FFFFFF"
  secondary: "#FFA8CD"
  secondary-strong: "#FFB3C7"
  on-secondary: "#0B051D"
  tertiary: "#0F766E"
  background: "#FFFFFF"
  surface: "#FFFFFF"
  surface-subtle: "#F7F7F8"
  surface-accent: "#FFF0F6"
  on-surface: "#0B051D"
  on-surface-muted: "#4A4458"
  border: "#DDD9E2"
  border-strong: "#A9A3B2"
  success: "#157A55"
  success-surface: "#ECFDF5"
  warning: "#7A4F00"
  warning-surface: "#FFF8E6"
  error: "#B42318"
  error-surface: "#FFF1F0"
  focus: "#7C3AED"
typography:
  headline-display:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 40px
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 32px
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: -0.015em
  headline-md:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 24px
    fontWeight: 650
    lineHeight: 1.3
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 20px
    fontWeight: 650
    lineHeight: 1.35
  body-lg:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
  body-md:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.55
  body-sm:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  label-lg:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 16px
    fontWeight: 600
    lineHeight: 1.3
  label-md:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.3
  label-sm:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: 0.02em
  score-display:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: 56px
    fontWeight: 750
    lineHeight: 1
    letterSpacing: -0.03em
rounded:
  none: 0px
  sm: 6px
  md: 10px
  lg: 16px
  xl: 24px
  full: 9999px
spacing:
  "0": 0px
  "1": 4px
  "2": 8px
  "3": 12px
  "4": 16px
  "5": 20px
  "6": 24px
  "8": 32px
  "10": 40px
  "12": 48px
  "16": 64px
  page-gutter-mobile: 20px
  page-gutter-tablet: 32px
  page-gutter-desktop: 48px
  content-max-width: 1120px
  reading-max-width: 720px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 48px
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.on-primary}"
  button-primary-active:
    backgroundColor: "{colors.primary-pressed}"
    textColor: "{colors.on-primary}"
  button-secondary:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-secondary}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 48px
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 48px
  upload-zone:
    backgroundColor: "{colors.surface-accent}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 24px
  analysis-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 24px
  score-card:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.score-display}"
    rounded: "{rounded.xl}"
    padding: 32px
  chip-supported:
    backgroundColor: "{colors.success-surface}"
    textColor: "{colors.success}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 8px
  chip-missing:
    backgroundColor: "{colors.warning-surface}"
    textColor: "{colors.warning}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 8px
  alert-error:
    backgroundColor: "{colors.error-surface}"
    textColor: "{colors.error}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.md}"
    padding: 16px
  progress-step-active:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-secondary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    size: 32px
  progress-step-complete:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    size: 32px
---

# DESIGN.md — AI Destekli ATS Uyumlu CV Optimizasyon Uygulaması

Bu dosya ürünün kalıcı görsel tasarım kaynağıdır. YAML bölümündeki tokenlar normatif değerlerdir; aşağıdaki açıklamalar bu değerlerin neden ve nasıl kullanılacağını tanımlar. Ürün davranışı için [`intent.md`](./intent.md), geliştirme kuralları için [`AGENTS.md`](./AGENTS.md) esas alınır.

## Overview

Tasarım yaklaşımının adı **Kanıt Odaklı Güven**'dir. Arayüz; sakin, profesyonel, açıklanabilir ve kullanıcı kontrolünü önceleyen bir çalışma alanı gibi hissettirmelidir. Kullanıcı, kişisel ve kariyeri açısından önemli bir belgeyi sisteme teslim ettiği için ürün ilk bakışta güvenilir olmalı; yapay zekâyı gösterişli bir yenilik olarak değil, denetlenebilir bir yardımcı olarak sunmalıdır.

Görsel karakter şu dengeleri korur:

- **Profesyonel ama soğuk değil:** Kurumsal netlik, açık yüzeyler ve yumuşak köşelerle dengelenir.
- **Teknik ama anlaşılır:** Skor ve anahtar kelime verileri görünürdür; kullanıcıya bir kontrol paneli karmaşası yaşatılmaz.
- **Güven veren ama iddialı değil:** Tahmini uyum oranı güçlü biçimde gösterilir fakat kesin sonuç veya garanti izlenimi yaratmaz.
- **AI destekli ama “AI estetiği”ne bağımlı değil:** Mor–pembe gradyanlar, parlayan küreler, robot görselleri ve dekoratif teknoloji klişeleri kullanılmaz.
- **Eylem odaklı ama baskıcı değil:** Her ekranda tek bir baskın birincil eylem bulunur; “Hayır” seçeneği açık ve erişilebilir kalır.

Arayüzün temel metaforu bir **kanıt masasıdır**: CV, iş ilanı, analiz gerekçeleri ve optimize edilmiş çıktı birbirinden ayrılabilen, karşılaştırılabilen ve izlenebilen katmanlar olarak sunulur. Görsel tasarım, kaynak CV'de bulunmayan hiçbir bilginin eklenemeyeceği ürün ilkesini desteklemelidir.

Varsayılan deneyim açık temadır. Koyu tema, ayrı ve eksiksiz semantik token seti tanımlanmadan renkleri otomatik ters çevirerek oluşturulmamalıdır.

## Colors

Renk sistemi, Klarna'nın görsel dilindeki en yararlı prensibi bu ürüne uyarlar: yapısal yükü koyu mürekkep rengi taşır, pembe ise sınırlı ve ayırt edici bir marka vurgusu olarak kalır. Böylece arayüz enerjik görünürken kişisel veri işleyen profesyonel bir araç olma niteliğini korur. Renk hiçbir zaman tek başına anlam taşımaz; ikon, başlık veya açıklayıcı metinle desteklenir.

- **Primary / Mürekkep (`#0B051D`):** Ana metin, birincil CTA, skor kartı ve yüksek önem düzeyindeki yüzeyler için kullanılan siyaha yakın sıcak laciverttir. Ürünün güven ve ciddiyet temelini oluşturur.
- **Primary Hover (`#211735`):** Koyu CTA'ların hover durumudur. Etkileşim geri bildirimi verirken marka tonundan kopmaz.
- **Secondary / Marka Pembesi (`#FFA8CD`):** Seçili adım, ikincil vurgu, yumuşak CTA ve marka anları için kullanılır. Uzun metin zemini veya hata rengi değildir.
- **Secondary Strong (`#FFB3C7`):** Pembenin alternatif marka yüzeyidir; aynı görünümde `secondary` ile birlikte gereksiz renk çeşitliliği yaratacak biçimde kullanılmaz.
- **On Secondary (`#0B051D`):** Pembe yüzey üzerindeki zorunlu metin rengidir. Pembe üzerinde beyaz metin yeterli kontrast sağlamadığı için kullanılmaz.
- **Tertiary / Doğrulama Yeşili (`#0F766E`):** Tamamlanan adımlar ve doğrulanmış eşleşmeler için ölçülü biçimde kullanılır. Dekoratif vurgu değildir.
- **Background (`#FFFFFF`):** Varsayılan parlak ve temiz sayfa zeminidir.
- **Surface Subtle (`#F7F7F8`):** Bölüm ayrımları, ikincil alanlar ve sakin içerik grupları için kullanılan soğuk açık gridir.
- **Surface Accent (`#FFF0F6`):** Dosya yükleme ve rehberlik gibi dikkat isteyen fakat kritik olmayan alanlarda kullanılan açık pembe yıkamadır.
- **On Surface (`#0B051D`):** Ana başlık ve gövde metni rengidir; saf siyaha göre daha karakterli bir mürekkep etkisi verir.
- **On Surface Muted (`#4A4458`):** Yardımcı metin, açıklama ve metadata için kullanılır; temel bilgi veya form etiketi bu renge indirgenmez.
- **Border (`#DDD9E2`):** Kart ve form sınırlarında kullanılan hafif mor alt tonlu nötrdür. Etkileşimli öğelerde yalnızca sınır rengi değişimine güvenilmez.
- **Success (`#157A55`):** CV tarafından desteklenen nitelikler ve başarıyla tamamlanan işlemler içindir.
- **Warning (`#7A4F00`):** İş ilanında önemli olup CV'de görünmeyen veya doğrulanamayan alanları belirtir. Kullanıcının başarısız olduğu anlamına gelmez.
- **Error (`#B42318`):** Dosya okuma hataları, geçersiz girdiler ve tamamlanamayan işlemler içindir.
- **Focus (`#7C3AED`):** Klavye odak halkasının hem beyaz hem pembe yüzeylerden ayrışmasını sağlayan yüksek görünürlüklü mordur; dekoratif marka rengi olarak kullanılmaz.

Tahmini uyum skoru yalnızca kırmızı–sarı–yeşil ölçeğiyle anlatılmamalıdır. Yüzde, açıklayıcı seviye metni ve gerekçeler birlikte gösterilmelidir. Düşük skor için saldırgan kırmızı kullanımından kaçınılmalı; kırmızı yalnızca gerçek hata durumlarına ayrılmalıdır.

Tüm normal metinler için WCAG AA düzeyinde en az 4.5:1, büyük metin ve temel grafik öğeleri için en az 3:1 kontrast hedeflenir. Klavye odağı arka plandan net biçimde ayrılmalıdır.

## Typography

Tipografi, uzun CV metinlerinin rahat okunmasını ve analiz verilerinin hızlı taranmasını destekler. Ana yazı ailesi **Inter**'dır; yüklenemediğinde sistem arayüz yazı tiplerine düşer. Ürün genelinde ikinci bir dekoratif yazı tipi kullanılmaz.

- **Display ve başlıklar:** 650–750 ağırlık aralığında, kısa ve doğrudan kullanılır. Başlıklar güven verir; pazarlama sloganı gibi davranmaz.
- **Gövde metni:** Varsayılan 16px ve 1.55 satır yüksekliğidir. Analiz gerekçeleri ve CV önizlemesi için uzun okuma konforu korunur.
- **Etiketler:** 12–16px aralığında ve 600 ağırlıktadır. Tümü büyük harf yapılmaz; Türkçe ve İngilizce metinlerde doğal okuma biçimi korunur.
- **Skor:** `score-display` yalnızca ana tahmini uyum yüzdesinde kullanılır. Sayısal ağırlık görsel vurgu sağlar ancak yanında “estimated match” benzeri açıklayıcı ifade bulunur.

Bir ekranda mümkün olduğunca üçten fazla yazı ağırlığı kullanılmamalıdır. Paragrafların satır uzunluğu yaklaşık 60–75 karakterle sınırlandırılır. CV önizlemesinin tipografisi uygulama arayüzü tipografisinden ayrılabilir ancak ATS uyumlu, sade ve kolay okunur kalmalıdır.

İngilizce analiz ve CV içeriği ile Türkçe proje dokümantasyonu farklı dil kurallarına sahiptir. Arayüz metinleri hangi dilde sunulursa sunulsun kesilme, taşma ve özel karakterler için test edilmelidir.

## Layout

Yerleşim, kullanıcının tek bir doğrusal akışı takip etmesini sağlar: **yükle → iş ilanını gir → analiz et → karar ver → gerekirse optimize et**.

- Masaüstünde içerik en fazla `1120px` genişliğindedir ve sayfada ortalanır.
- Uzun açıklamalar ve form metinleri `720px` okuma genişliğini aşmaz.
- Temel ritim 4px tabanlıdır; günlük bileşen aralıklarında çoğunlukla 8px, 16px, 24px ve 32px kullanılır.
- Mobilde tek sütun, geniş ekranlarda yalnızca karşılaştırma gerçekten faydalıysa iki sütun kullanılır.
- CV ile iş ilanı giriş ekranında iki sütun kullanılabilir; dar görünümde CV alanı önce gelir.
- Analiz ekranında skor üstte özetlenir; güçlü yönler, eksik görünen alanlar, anahtar kelimeler ve geliştirme noktaları ayrı kartlarda devam eder.
- Yeniden düzenleme onayı, analizden sonra bağımsız ve açık bir karar alanı olarak gösterilir. Kullanıcı analiz sonuçlarını görmeden bu karar alanına zorlanmaz.
- Optimize edilmiş CV ekranında kaynak ile sonuç yan yana karşılaştırılabiliyorsa geniş ekranda iki panel; mobilde sekmeli veya ardışık görünüm kullanılır.

Sayfa üstündeki adım göstergesi kullanıcının konumunu açıklar ancak tamamlanmamış adımlara atlayarak doğrulama kurallarını aşmasına izin vermez. Birincil eylemler masaüstünde içerik akışının sonunda, mobilde erişilebilir bir konumda yer alır; önemli içeriği örten kalıcı butonlardan kaçınılır.

Boş alan dekorasyon değil, kararları gruplama aracıdır. Aynı karta ait başlık, açıklama ve eylem birbirine yakın; farklı karar alanları birbirinden belirgin uzaklıkta tutulur.

## Elevation & Depth

Derinlik ağır gölgeler yerine **tonal katmanlar, sınırlar ve boşluk** ile kurulur. Sayfa zemini `background`, ana içerik kartları `surface` rengindedir.

- Standart kartlarda 1px `border` kullanılır; gölge zorunlu değildir.
- Açılır menü, modal veya sürüklenen dosya gibi gerçekten üst katmanda bulunan öğelerde hafif ve geniş bir gölge kullanılabilir.
- Skor kartı renk kontrastıyla öne çıkar; ek olarak büyük gölge verilmez.
- Hover durumunda kartların yer değiştirmesi veya yükseliyormuş gibi sıçraması kullanılmaz.
- Modal yalnızca kullanıcı kararını kesintisiz biçimde gerektiren durumlarda tercih edilir. Analiz ve onay akışı mümkün olduğunca sayfa içinde kalır.

Katman sırası açık olmalıdır: sayfa → içerik kartı → geçici menü → modal → kritik sistem bildirimi. Z-index değerleri rastgele artırılmamalı, uygulama genelinde tanımlı bir ölçek izlemelidir.

## Shapes

Şekil dili kontrollü yumuşaklıktır. Formlar ve kartlar ulaşılabilir görünür; aşırı yuvarlak, oyuncak benzeri bir arayüz oluşmaz.

- Form kontrolleri ve standart butonlar `10px` köşe yarıçapı kullanır.
- Büyük analiz ve skor kartları `16px` veya `24px` kullanabilir.
- Chip, durum rozeti ve adım göstergeleri `full` kullanır.
- Metin alanları, kartlar ve butonlar aynı görünüm içinde tutarlı köşe ailesini izler.
- Dekoratif organik şekiller, blob arka planlar ve içerikle ilişkisi olmayan geometrik desenler kullanılmaz.
- İkonlar sade, tek renkli ve 1.5–2px çizgi kalınlığında olmalıdır. Aynı ekranda dolu ve çizgisel ikon aileleri karıştırılmaz.

Etkileşim hedefleri en az 44×44px olmalıdır. Küçük ikon butonları görünür odak, erişilebilir ad ve tooltip içermelidir.

## Components

### Uygulama kabuğu ve ilerleme

Üst alan marka işareti, kısa ürün adı ve gerektiğinde gizlilik yardımına erişim içerir. Ana akışın adımları numara, ad ve durumla gösterilir. Tamamlanan adımlar yeşil, etkin adım koyu metinli marka pembesi, gelecek adımlar nötr görünür; yalnızca renkle ayrılmaz.

### CV yükleme alanı

Yükleme alanı kesik çizgili sınır, kısa yönlendirme, desteklenen dosya bilgisi ve görünür dosya seçme eylemi içerir. Sürükle–bırak tek yöntem değildir. Dosya seçildiğinde ad, tür, boyut ve kaldır/değiştir eylemi gösterilir. Yükleme ilerlemesi ve hata durumu aynı alanda açıklanır.

### İş ilanı alanı

İş ilanı geniş bir metin alanında alınır. Kalıcı etiket, kısa yardımcı metin ve gerektiğinde karakter/uzunluk geri bildirimi bulunur. Placeholder, etiket yerine kullanılmaz. CV veya ilan İngilizce değilse hata suçlayıcı olmayan bir dille açıklanır ve otomatik çeviri yapılmaz.

### Butonlar

- **Birincil:** Ekranın ana ilerleme eylemidir; örneğin “Analyze CV” veya açık onay sonrasında “Optimize CV”. Aynı karar alanında bir tane bulunur.
- **İkincil:** Geri dönme, dosyayı değiştirme veya “No, finish” gibi geçerli alternatifler içindir. Görsel olarak daha sakin olsa da erişilebilirliği düşürülmez.
- **Yıkıcı:** Yalnızca veri silme gibi gerçek yıkıcı eylemlerde hata rengi kullanır; düşük skor veya “Hayır” seçimi yıkıcı sayılmaz.
- **Yükleniyor:** Etiket mümkünse eylemin durumunu anlatacak biçimde değişir. Boyut sabit kalır ve yinelenen gönderim engellenir.

### Form kontrolleri

Tüm kontrollerde kalıcı etiket, görünür sınır, belirgin hover ve 2px odak halkası bulunur. Hata mesajı ilgili alanın hemen altında yer alır ve çözüm önerir. Devre dışı durum yalnızca işlem gerçekten kullanılamıyorsa uygulanır; açıklama gereken durumda neden belirtilir.

### Analiz özeti ve skor kartı

Ana skor kartı yüzdeyi, “tahmini” niteliğini, kısa seviye açıklamasını ve skorun garanti olmadığını belirten yardımcı metni birlikte gösterir. Dairesel grafik kullanılırsa yüzde metni grafik dışında da okunabilir olmalıdır. Gösterişli hız göstergeleri ve kesinlik hissi veren animasyonlardan kaçınılır.

Skorun altında analiz mantığının kısa özeti ve dört zorunlu bölüm bulunur:

1. Strong points
2. Missing or underrepresented areas
3. Important keywords
4. Improvement opportunities

Kart başlıkları, ikonları ve kısa özetleri hızlı taramayı destekler. Her öneri mümkün olduğunda CV'deki dayanak içerikle ilişkilendirilebilir biçimde sunulur.

### Anahtar kelime chip'leri

Chip'ler iki ana durumu ayırır: kaynak CV tarafından desteklenen ve CV'de doğrulanamayan. “Eksik” chip'leri hata kırmızısı yerine uyarı tonunu kullanır. Bir chip tek başına kullanıcıda becerinin bulunmadığını iddia etmez; açıklamada bunun CV'de görünmediği belirtilir.

### Onay alanı

“CV'nizi bu pozisyona göre yeniden düzenlemek ister misiniz?” sorusu analizden sonra ayrı bir kartta gösterilir. “Evet” ve “Hayır” seçenekleri açık metin etiketlerine sahiptir. “Hayır” gizlenmez, küçültülmez veya kullanıcıyı utandıran bir metinle sunulmaz. Varsayılan seçim yapılmaz.

### Optimize edilmiş CV ve izlenebilirlik

Sonuç ekranı optimize edilmiş CV'yi okunabilir bir belge önizlemesinde gösterir. Değişiklik özeti; yeniden sıralanan, yeniden ifade edilen ve korunmuş içerikleri ayırt eder. Kaynakta dayanağı bulunmayan bir ifade kullanıcıya gösterilmemeli; doğrulama başarısızsa çıktı durdurulup güvenli hata sunulmalıdır.

### Bildirimler ve boş durumlar

Bildirimler kısa başlık, açıklama ve gerektiğinde tek bir çözüm eylemi içerir. Toast, kalıcı veya eylem gerektiren hataların tek taşıyıcısı olmaz. Boş durumlar kullanıcıya sıradaki adımı anlatır; dekoratif illüstrasyon zorunlu değildir.

### Hareket ve geri bildirim

Geçişler işlevsel ve kısa olmalıdır: renk ve opacity için yaklaşık 150ms, panel açılışları için en fazla 250ms. Skor sayacı uzun süre dönmez ve sonucu dramatize etmez. `prefers-reduced-motion` etkin olduğunda zorunlu olmayan hareket kaldırılır. Analiz sürerken belirsiz spinner yanında “CV and job description are being analyzed” gibi durum metni gösterilir.

## Do's and Don'ts

### Yapılması gerekenler

- Her ekranda tek bir baskın birincil eylem kullanın.
- Tahmini skoru yüzde, metin ve gerekçelerle birlikte gösterin.
- Kullanıcının hangi adımda olduğunu ve sırada ne olduğunu açıkça belirtin.
- Analiz içeriğini taranabilir kartlara ve kısa bölümlere ayırın.
- Kaynak CV ile üretilen içerik arasındaki ilişkiyi görünür kılın.
- “CV'de görünmüyor” ile “kullanıcıda yok” arasındaki farkı dilde ve görsel sunumda koruyun.
- Hata, uyarı ve başarı durumlarında ikon veya metni renge ek olarak kullanın.
- Klavye erişimini, görünür odağı, ekran okuyucu adlarını ve en az 44×44px hedefleri sağlayın.
- Normal metinde en az WCAG AA kontrastını koruyun.
- Mobilde içerik sırasını masaüstündeki anlam hiyerarşisiyle tutarlı tutun.
- Yükleme, analiz ve üretim sırasında kullanıcının verisine ne olduğunu açıkça anlatın.

### Yapılmaması gerekenler

- AI klişesi olan mor–pembe gradyanlar, parlayan küreler, robotlar veya anlamsız ağ desenleri kullanmayın.
- Tahmini uyum skorunu gerçek ATS skoru veya başarı garantisi gibi sunmayın.
- Düşük skoru hata kırmızısıyla cezalandırıcı biçimde göstermeyin.
- Rengi tek anlam taşıyıcısı olarak kullanmayın.
- “Hayır” seçeneğini gizlemeyin, zayıflatmayın veya onayı varsayılan yapmayın.
- Placeholder'ı form etiketi yerine kullanmayın.
- Bir ekranda gereksiz sayıda kart, chip, grafik veya durum rengi göstermeyin.
- Ağır gölgeler, aşırı yuvarlak kartlar veya sürekli animasyonlarla güvenilirliği zayıflatmayın.
- Kullanıcının CV metnini dekoratif kısaltmalarla veya okunamayacak küçük yazıyla göstermeyin.
- Kaynak CV'de bulunmayan bir niteliği görsel olarak doğrulanmış gibi işaretlemeyin.
- Sadece hover ile görülebilen kritik açıklama veya eylem oluşturmayın.
- Eksiksiz semantik tokenlar ve kontrast testleri olmadan otomatik koyu tema üretmeyin.
