# yt_downloader

Prosty program do pobierania filmów i muzyki z YouTube z obsługą wyboru formatu, katalogów docelowych i logowaniem operacji.

## Funkcje

- Pobieranie wideo lub tylko audio z YouTube
- Wybór formatu i jakości
- Kopiowanie plików do wybranych katalogów (z możliwością dodawania/usuwania ścieżek)
- Sprawdzanie wolnego miejsca na dysku przed pobraniem
- Logowanie operacji do pliku `log.txt`
- Konfiguracja katalogów przez plik `.env`
- Testy jednostkowe

## Wymagania

- Python 3.8+
- yt-dlp
- python-dotenv

## Instalacja

```bash
pip install -r requirements.txt
```

## Użycie

1. Skonfiguruj plik `.env` (opcjonalnie) z domyślnymi ścieżkami.
2. Uruchom program:

```bash
python ytdownloader.py
```

3. Postępuj zgodnie z instrukcjami w terminalu.

## Testy

Aby uruchomić testy jednostkowe:

```bash
python test_basic.py
```

## Uwagi

- Program nie jest przeznaczony do pobierania materiałów chronionych prawem autorskim bez zgody właściciela.
- Używaj zgodnie z regulaminem YouTube.

---

**Zachęcam do zgłaszania błędów i propozycji!**
