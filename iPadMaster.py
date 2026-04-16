# iPad Mini 1 (A1432) Legacy Media Master 🚀

### Why this exists
Modern smartphones (like the Google Pixel 4XL) capture media in formats that legacy iOS devices (iPad Mini 1, iPad 2, etc.) cannot understand. Issues include:
*   **HEIC/WebP/PNG Compatibility**: Legacy iOS only likes standard JPEGs.
*   **High Resolution**: 12MP+ photos crash the 512MB RAM of older iPads.
*   **Video Encodings**: Modern "High Profile" H.264/H.265 videos won't sync via iTunes 12.6.
*   **The "50-Photo Sync Wall"**: iTunes often stops syncing after 50 items due to hardware indexing timeouts.

### How it works
This Python tool "pre-optimizes" your entire library specifically for **iOS 9.3.5** hardware:
1.  **Smart Batching**: Splits media into groups of 45 to bypass iTunes timeout limits.
2.  **Legacy Encoding**: Forces videos into **H.264 Baseline Level 3.0** with **YUV420P** color space (the only format guaranteed to work).
3.  **Smart Scaling**: Upscales low-res images and downscales high-res images to a "Retina-Sweet-Spot" of **2048px**.
4.  **GIF to MP4**: Automatically converts animations into playable video clips.
5.  **Duplicate Safety**: Handles naming conflicts (e.g., `image.jpg` and `image.webp`) by intelligently renaming them.

### Quick Start
1. Install requirements: `pip install pillow moviepy`
2. Place `ipad_master.py` in your photo directory.
3. Run `python ipad_master.py`.
4. Point iTunes to the generated `iPadSync` folders.

"""
iPad Mini 1 (A1432) Legacy Media Master
Created to bridge the gap between modern Android/iPhone media and iOS 9 legacy hardware.
"""

import os, shutil, sys
from PIL import Image

try:
    from moviepy.editor import VideoFileClip
    VIDEO_READY = True
except ImportError:
    try:
        from moviepy import VideoFileClip
        VIDEO_READY = True
    except ImportError:
        VIDEO_READY = False

def make_even(n):
    """Force number to be even for H.264 compliance."""
    n = int(round(n))
    return n if n % 2 == 0 else n + 1

def process_smart_batches(src, dest_base, batch_size=45):
    img_exts = ('.webp', '.png', '.bmp', '.tiff', '.jpeg', '.jpg')
    vid_exts = ('.mp4', '.mov', '.m4v', '.gif')
    
    all_items = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]
    target_files = [f for f in all_items if f.lower().endswith(img_exts + vid_exts)]
    
    # Sort: Images first (0), then Videos (1)
    target_files.sort(key=lambda x: 0 if x.lower().endswith(img_exts) else 1)
    
    total = len(target_files)
    print(f"\n🚀 Processing {total} items (Images first, then Videos)...")

    for i in range(0, total, batch_size):
        current_batch = target_files[i:i + batch_size]
        temp_dest = os.path.join(os.getcwd(), "temp_work_folder")
        if os.path.exists(temp_dest): shutil.rmtree(temp_dest)
        os.makedirs(temp_dest)

        used_names = set()
        v_count, i_count = 0, 0

        for file in current_batch:
            path = os.path.join(src, file)
            file_name_only, ext_only = os.path.splitext(file)
            ext = ext_only.lower()
            is_video = ext in vid_exts
            target_ext = ".mp4" if is_video else ".jpg"
            
            final_name = f"{file_name_only}{target_ext}"
            counter = 1
            while final_name.lower() in used_names:
                final_name = f"{file_name_only}_{counter}{target_ext}"
                counter += 1
            used_names.add(final_name.lower())

            try:
                if is_video and VIDEO_READY:
                    print(f"🎬 Optimising Video: {file}...")
                    clip = VideoFileClip(path)
                    
                    # Calculate new dimensions (Force even numbers)
                    target_h = 480
                    target_w = make_even(clip.w * (target_h / clip.h))
                    
                    # Apply resize using tuple to ensure MoviePy handles it correctly
                    try:
                        clip = clip.resized(new_size=(target_w, target_h))
                        clip = clip.with_fps(24)
                    except AttributeError:
                        clip = clip.resize(newsize=(target_w, target_h))
                        clip = clip.set_fps(24)
                    
                    clip.write_videofile(
                        os.path.join(temp_dest, final_name),
                        codec="libx264", audio_codec="aac",
                        preset="ultrafast", threads=4,
                        ffmpeg_params=["-profile:v", "baseline", "-level", "3.0", "-pix_fmt", "yuv420p"],
                        logger=None
                    )
                    clip.close()
                    v_count += 1
                else:
                    with Image.open(path) as img:
                        img = img.convert('RGB')
                        w, h = img.size
                        # Upscale/Downscale to 2048px (Best for iPad Mini 1)
                        if w < 2048 and h < 2048:
                            ratio = 2048 / float(max(w, h))
                            img = img.resize((int(w * ratio), int(h * ratio)), Image.Resampling.LANCZOS)
                        else:
                            img.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
                        img.save(os.path.join(temp_dest, final_name), 'JPEG', quality=90)
                    i_count += 1
                print(f"✅ Done: {final_name}")
            except Exception as e:
                print(f"❌ Failed {file}: {e}")

        final_batch_name = f"{dest_base} - {i//batch_size + 1} ({i_count}i, {v_count}v)"
        final_path = os.path.join(os.getcwd(), final_batch_name)
        if os.path.exists(final_path): shutil.rmtree(final_path)
        os.rename(temp_dest, final_path)
        print(f"📦 Batch Ready: {final_batch_name}")

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== IPAD MINI 1 (A1432) PIXEL-PERFECT MASTER ===")
        print("1. Start Fresh Batch Convert")
        print("2. Delete All 'Sync' Folders")
        print("3. Exit")
        
        choice = input("\nSelect: ")
        if choice == '1':
            folders = [d for d in os.listdir('.') if os.path.isdir(d) and "Sync" not in d and d != "__pycache__"]
            for i, f in enumerate(folders, 1): print(f"{i}. {f}")
            try:
                idx = int(input("\nFolder #: "))
                src = folders[idx-1]
                process_smart_batches(src, "iPadSync")
                input("\nFinished! Press Enter...")
            except (ValueError, IndexError):
                input("Invalid selection. Press Enter...")
        elif choice == '2':
            for d in os.listdir('.'):
                if os.path.isdir(d) and "Sync" in d: shutil.rmtree(d)
            input("Deleted. Press Enter...")
        elif choice == '3': break

if __name__ == "__main__": main_menu()
