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
