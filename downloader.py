import yt_dlp as youtube_dl
from os import path, makedirs


def download_video(url, download_path, only_audio=False):
    """
    Downloads a video or audio from YouTube.
    If only_audio is True, downloads and extracts audio as mp3.
    If only_audio is False, allows user to select video format and merges with best audio if needed.
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
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info_dict)
                print(f"Downloaded: {info_dict.get('title', 'Unknown title')}")
                print(f"Saved to: {file_path}")
                return file_path
        else:
            # Download all available formats and let user choose
            with youtube_dl.YoutubeDL({"quiet": True, "noplaylist": True}) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                formats = info_dict.get("formats", [])
                video_formats = [f for f in formats if f.get("vcodec") != "none"]
                if not video_formats:
                    print("No video formats available.")
                    return None

                # Display available formats
                for i, fmt in enumerate(video_formats):
                    resolution = fmt.get("height", "unknown")
                    filesize = fmt.get("filesize", "unknown")
                    has_audio = fmt.get("acodec") != "none"
                    audio_info = (
                        "video + audio"
                        if has_audio
                        else "video only (audio will be added)"
                    )
                    print(
                        f"{i + 1}. {fmt['format_id']} - Resolution: {resolution}p, Size: {filesize}, Type: {audio_info}"
                    )

                # User selects format
                try:
                    choice = int(input("Select format number to download: ")) - 1
                    if choice < 0 or choice >= len(video_formats):
                        print("Invalid choice. Download canceled.")
                        return None
                except ValueError:
                    print("Invalid choice. Download canceled.")
                    return None

                selected_format = video_formats[choice]
                selected_format_id = selected_format["format_id"]
                print(f"Selected format: {selected_format_id}")

                # If selected format has no audio, add bestaudio
                if selected_format.get("acodec") == "none":
                    selected_format_id += "+bestaudio"
                    print("Best available audio will be added to the format.")

            # Download with merging video and audio if needed
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
                "noplaylist": True,
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info_dict)
                print(f"Downloaded: {info_dict.get('title', 'Unknown title')}")
                print(f"Saved to: {file_path}")
                return file_path

    except Exception as e:
        print(f"Error during download: {e}")
        return None
