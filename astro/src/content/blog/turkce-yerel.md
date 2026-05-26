---
title: Türkçe içerik için yerelleştirme
deck: Bir CSS özelliği, bir HTML niteliği, ve Türkçe doğru büyük harfe geçer.
date: 2026-05-01
lang: tr
brand: agustos
---

Türkçe, Latin alfabesinin standart varsayımlarına meydan okuyan bir dildir.

Çoğu dilde küçük `i` harfi, büyük yazıldığında noktasız `I` olur. Türkçede ise `i` büyüdüğünde noktasını korur ve `İ` olur; ayrıca noktasız bir `ı` harfi vardır ve bu büyüdüğünde noktasız `I` olur. Bu fark sadece bir tipografik tercih değil, **doğru-yanlış** meselesidir.

## Üç yerde uygulanır

İçeriğin doğru görünmesi için üç ayar gerekir.

### 1. HTML

Her Türkçe içerik bloğu `lang="tr"` taşır:

```html
<article lang="tr">
  <h1>Işığın mimariyle buluştuğu yer.</h1>
</article>
```

### 2. CSS

Genel stillerde `locl` OpenType özelliği aktiftir:

```css
html {
  font-feature-settings: "locl" on, "kern" on;
}
```

### 3. Markdown / Pandoc

Belge düzeyinde başlık olarak:

```yaml
---
lang: tr
---
```

## Neden zorunlu

Çünkü `text-transform: uppercase` kuralı varsayılan olarak yanlış çalışır:

- `iyi günler` → İngilizce varsayımıyla `IYI GÜNLER` (yanlış)
- `iyi günler` → `lang="tr"` ile `İYİ GÜNLER` (doğru)

Eyebrow etiketleri, marka isimleri, tablo başlıkları, H4 sınıfı; bunların hepsi büyük harf taşır. Yerel ayarı doğru yapmadığınız sürece her biri sessizce yanlış Türkçe üretir.

---

Bu kuralı sisteme bir ayar olarak değil, bir doğruluk gerekliliği olarak yazdık. Çünkü öyledir.
