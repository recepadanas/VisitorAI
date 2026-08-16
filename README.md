# VisitorAI

VisitorAI, ziyaretçinin verdiği birkaç iş/teknoloji odaklı cevabı yerel bir Ollama modeliyle analiz eden örnek bir AI web uygulamasıdır.

## Mimari

Tarayıcı → FastAPI → Ollama → Yapılandırılmış JSON → Kullanıcı arayüzü

## Teknolojiler

- Python
- FastAPI
- Ollama
- Llama 3.2
- HTML / CSS / JavaScript
- Cloudflare Tunnel

## Gereksinimler

- Python 3.10+
- Ollama
- `llama3.2:3b` modeli

## 1. Ollama modelini hazırla

```bash
ollama pull llama3.2:3b
```

Ollama'nın çalıştığını doğrulamak için:

```bash
ollama ls
```

## 2. Projeyi kur

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3. Uygulamayı başlat

```bash
uvicorn main:app --reload
```

Tarayıcıdan:

```text
http://127.0.0.1:8000
```

Sağlık kontrolü:

```text
http://127.0.0.1:8000/health
```

## 4. HTTPS demo

Cloudflare Quick Tunnel geliştirme/demonstrasyon amaçlı kullanılabilir:

```bash
cloudflared tunnel --url http://localhost:8000
```

Komut geçici bir `https://...trycloudflare.com` adresi üretir.

> Quick Tunnel kalıcı production yayını için değil, geliştirme ve demo amacıyla kullanılmalıdır.

## Nasıl çalışıyor?

1. Kullanıcı web formunda çalışma alanını, AI kullanım amacını, teknik seviyesini ve beklentisini girer.
2. FastAPI gelen veriyi doğrular.
3. Backend, yerel Ollama API'sine yapılandırılmış bir prompt gönderir.
4. Model sonucu JSON formatında döndürür.
5. Frontend; profil, AI seviyesi, öncelikli ihtiyaç, kullanım alanları ve kişiselleştirilmiş öneriyi gösterir.

## Gizlilik yaklaşımı

Bu demo hassas kişisel özellikleri tahmin etmeye çalışmaz. Analiz yalnızca kullanıcının kendisinin sağladığı iş, teknoloji ve kullanım ihtiyacı verilerine dayanır. Model yerel Ollama kurulumu üzerinde çalıştırılabilir.

## Projenin amacı

Bu proje, üretken yapay zekâyı yalnızca sohbet botu olarak değil; kullanıcı girdilerini yapılandırılmış içgörülere dönüştüren bir uygulama katmanı olarak kullanmanın basit bir örneğidir.
