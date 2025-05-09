import yt_dlp as youtube_dl
from os import path, makedirs


def download_video(url, download_path, only_audio=False):
    """
    Pobiera wideo z YouTube w wybranej rozdzielczości.
    Jeśli wybrany format nie zawiera audio, zostanie połączony z najlepszym audio.
    """
    try:
        if not path.exists(download_path):
            makedirs(download_path)

        if only_audio:
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": path.join(download_path, "%(title)s.%(ext)s"),
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "noplaylist": True,
                "quiet": True,
            }
        else:
            # Pobranie wszystkich formatów
            ydl_opts = {"quiet": True, "noplaylist": True}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                all_formats = info_dict.get("formats", [])

                # Filtrowanie: tylko formaty zawierające wideo (czyli HD, FHD itd.)
                video_formats = [
                    fmt
                    for fmt in all_formats
                    if fmt.get("vcodec") != "none"
                    and isinstance(fmt.get("height"), int)
                    and fmt.get("height", 0) >= 720
                ]

                if not video_formats:
                    print("Nie znaleziono żadnych formatów wideo.")
                    return None

                print("Dostępne formaty wideo:")
                for i, fmt in enumerate(video_formats):
                    resolution = fmt.get("height", "Brak rozdzielczości")
                    filesize = fmt.get("filesize", "Nieznany rozmiar")
                    has_audio = fmt.get("acodec") != "none"
                    audio_info = (
                        "video + audio"
                        if has_audio
                        else "video only (audio będzie dodane)"
                    )
                    print(
                        f"{i + 1}. {fmt['format_id']} - Rozdzielczość: {resolution}p, Rozmiar: {filesize}, Typ: {audio_info}"
                    )

                # Wybór użytkownika
                try:
                    choice = int(input("Wybierz numer formatu do pobrania: ")) - 1
                    if choice < 0 or choice >= len(video_formats):
                        print("Nieprawidłowy wybór. Pobieranie anulowane.")
                        return None
                except ValueError:
                    print("Nieprawidłowy wybór. Pobieranie anulowane.")
                    return None

                selected_format = video_formats[choice]
                selected_format_id = selected_format["format_id"]
                print(f"Wybrano format: {selected_format_id}")

                # Jeśli wybrany format nie ma audio, dodajemy bestaudio
                if selected_format.get("acodec") == "none":
                    selected_format_id += "+bestaudio"
                    print("Do formatu zostanie dodany najlepszy dostępny dźwięk.")

            # Opcje pobierania z łączeniem dźwięku i wideo
            ydl_opts = {
                "outtmpl": path.join(download_path, "%(title)s.%(ext)s"),
                "format": selected_format_id,
                "merge_output_format": "mp4",
                "postprocessors": [
                    {
                        "key": "FFmpegVideoConvertor",
                        "preferedformat": "mp4",
                    }
                ],
                "ffmpeg_location": "/usr/bin/ffmpeg",
                "noplaylist": True,  # <-- dodaj to tutaj
            }

        # Pobieranie i zapisywanie pliku
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
            print(f"Pobrano: {info_dict.get('title', 'Unknown title')}")
            print(f"Zapisano w: {file_path}")
            return file_path

    except Exception as e:
        print(f"Wystąpił błąd podczas pobierania: {e}")
        return None
