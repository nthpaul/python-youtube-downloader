import os
import sys

from pytubefix import Channel, Playlist, YouTube
from pytubefix.cli import on_progress


def clear_screen():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def print_menu():
    """Display the main menu options."""
    print("\n" + "=" * 20)
    print("  Youtube Downloader Options")
    print("=" * 20)
    print("1. Download Video")
    print("2. Download Playlist")
    print("3. Download all videos from a channel")


def get_user_input(prompt):
    """Get user input with exit check."""
    user_input = input(prompt).strip()
    if user_input.lower() in ["exit", "quit", "q", ":q", "q!", ":exit"]:
        print("Have a great day!")
        sys.exit(0)
    return user_input


def download_video():
    video_url = get_user_input("Enter the Youtube video URL: ")
    # resolution = get_user_input(
    #     "Enter the desired resolution (e.g., 144p, 240p, 360p, 720p, 1080p) or press Enter to get the highest resolution: "
    # ).lower()
    custom_directory = get_user_input(
        "Enter the directory to save the video (or press Enter to use current directory): "
    )

    try:
        video = YouTube(video_url, on_progress_callback=on_progress)
        # custom_stream = video.streams.get_by_resolution(resolution)
        highest_stream = video.streams.get_highest_resolution()
        print(f"Downloading video: {video.title} by {video.author}")
        # stream = custom_stream if custom_stream else highest_stream
        stream = highest_stream
        if custom_directory:
            stream.download(output_path=custom_directory)
        else:
            stream.download()
        print(f"Video downloaded successfully: {video.title}")
    except Exception as e:
        print(f"Error fetching video: {e}")
        return


def download_playlist():
    playlist_url = get_user_input("Enter the playlist URL: ")
    playlist = Playlist(playlist_url)
    custom_directory = get_user_input(
        "Enter the directory to save the video (or press Enter to use current directory): "
    )

    try:
        print(f"Downloading videos from playlist {playlist.title}.")
        for idx, video in enumerate(playlist.videos):
            print(f"Downloading video: {idx}_{video.title}.")
            try:
                video.register_on_progress_callback(on_progress)
                stream = video.streams.get_highest_resolution()
                if custom_directory:
                    stream.download(
                        output_path=custom_directory, filename_prefix=f"{idx}_"
                    )
                else:
                    stream.download(filename_prefix=f"{idx}_")
            except Exception as e:
                print(f"Failed to download {video.title}.")
        print(f"Finished downloading from playlist: {playlist.title}.")
    except Exception as e:
        print("Failed to download the complete playlist.")
        return


def download_channel():
    channel_url = get_user_input("Enter the channel URL: ")
    custom_directory = get_user_input(
        "Enter the directory to save the videos (or press Enter to use current directory): "
    )

    channel = Channel(channel_url)

    try:
        print(f"Downloading videos from channel {channel.title}.")
        for idx, video in enumerate(channel.videos):
            print(f"Downloading video: {idx}_{video.title}.")
            try:
                video.register_on_progress_callback(on_progress)
                stream = video.streams.get_highest_resolution()
                if custom_directory:
                    stream.download(
                        output_path=custom_directory, filename_prefix=f"{idx}_"
                    )
                else:
                    stream.download(filename_prefix=f"{idx}_")
            except Exception as e:
                print(f"Failed to download {channel.title}.")
        print(f"Finished downloading from channel: {channel.title}.")
    except Exception as e:
        print(f"Error fetching channel: {e}")
        return


def main():
    """Main application loop."""
    clear_screen()
    print_menu()

    while True:
        try:
            choice = get_user_input("\nChoose an option: ")
            if choice == "1":
                download_video()
            elif choice == "2":
                download_playlist()
            elif choice == "3":
                download_channel()
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Press Enter to continue...")
            continue


if __name__ == "__main__":
    main()
