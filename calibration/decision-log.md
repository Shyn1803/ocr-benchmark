# Decision Log: Profile Calibration

**Ngày:** 2026-08-12  
**Tập calibration:** Stratified 5 tài liệu/nhóm từ DocLayNet & olmOCR (seed `20260811`)

---

## 1. Docling Profiles
- **`docling_default`**: Giữ cấu hình nhận diện OCR tự động, `table_mode="default"`.
- **`docling_scan`**: Cưỡng bức `force_full_page_ocr=True`, `ocr_languages=["vi", "en"]`, `table_mode="accurate"`, `cell_matching=True`. Tối ưu cho tài liệu scan tiếng Việt.

## 2. OpenDataLoader Profiles
- **`opendataloader_default`**: Chạy Java parser mặc định, `table_method="cluster"`, `reading_order="xycut"`.
- **`opendataloader_scan`**: Chạy chế độ hybrid `docling-fast` full mode với EasyOCR `vi,en`, tắt fallback im lặng.

## 3. Marker Profiles
- **`marker_default`**: Chạy `force_ocr=False`, `use_llm=False`.
- **`marker_scan`**: Cưỡng bức `force_ocr=True`, `use_llm=False`.

## 4. Sovereign Profiles
- **`sovereign_default`**: Khai báo môi trường không có Marker local escalation (`marker_available=False`), cưỡng bức tắt Vision API (`ocr_use_vision_api=False`).
- **`sovereign_scan`**: Khai báo môi trường có Marker local (`marker_available=True`), cưỡng bức tắt Vision API (`ocr_use_vision_api=False`).

---

## Kết luận
Cấu hình 8 profiles được khóa chính thức tại `configs/profiles.json` với `catalog_version: 2`.
