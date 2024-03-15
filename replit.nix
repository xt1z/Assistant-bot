{ pkgs }: {
  # Specify the list of packages to be installed
  deps = [
    pkgs.ffmpeg.bin
  ];
  packages = [
    pkgs.ffmpeg
    pkgs.ffprobe
  ];
}
