import yt_dlp
import sys

url = sys.argv[1] if len(sys.argv) > 1 else input("B站视频链接: ").strip()
if not url:
    sys.exit(1)

# 列出可用格式
print("\n获取可用格式中...")
ydl = yt_dlp.YoutubeDL({
    "http_headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
})
try:
    info = ydl.extract_info(url, download=False)
except Exception as e:
    print(f"获取信息失败: {e}")
    sys.exit(1)

print(f"\n标题: {info.get('title', 'N/A')}")
print(f"时长: {info.get('duration', 0)}秒\n可选格式:")
for f in info.get("formats", []):
    note = f.get("format_note", "") or f.get("resolution", "")
    ext = f.get("ext", "")
    size = f.get("filesize") or f.get("filesize_approx", 0)
    size_str = f"{size/1024/1024:.0f}MB" if size else "?"
    if note and ext:
        print(f"  {f['format_id']:>6} | {note:<10} | {ext:<4} | {size_str}")

fmt_id = input("\n输入要下载的format_id (回车默认最佳): ").strip() or "best"
out = input("保存路径 (回车默认当前目录): ").strip() or "./%(title)s.%(ext)s"

opts = {
    "format": fmt_id,
    "outtmpl": out,
    "http_headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
    "noplaylist": True,
    "merge_output_format": "mp4",
    "progress_hooks": [lambda d: print(f"\r{d.get('_percent_str','').strip()} {d.get('speed','').strip()}", end="") if d["status"] == "downloading" else None],
}

with yt_dlp.YoutubeDL(opts) as ydl:
    ydl.download([url])

print("\n完成!")
