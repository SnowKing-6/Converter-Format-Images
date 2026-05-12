import tkinter as tk
from tkinter import filedialog
import os

def get_image_path():
    """
    الطور العادي: دالة تفتح نافذة لاختيار ملف صورة واحد فقط وتعود بمساره الكامل.
    """
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    # تحديد الصيغ التي سيسمح البرنامج للمستخدم برؤيتها واختيارها
    file_types = [
        ("All Supported Images", "*.jpg *.jpeg *.png *.gif *.bmp *.webp *.tiff *.tif *.ico *.jfif *.heic *.avif"),
        ("JPEG Files", "*.jpg *.jpeg *.jfif"),
        ("PNG Files", "*.png"),
        ("WebP Files", "*.webp"),
        ("AVIF Files", "*.avif"),
        ("All Files", "*.*")
    ]
    
    # فتح نافذة اختيار الملف وتخزين المسار المختار في متغير
    image_path = filedialog.askopenfilename(
        title="اختر صورة واحدة للتحويل 🖼️",
        filetypes=file_types
    )
    return image_path

def get_input_folder():
    """
    الطور الاحترافي: دالة تفتح نافذة لاختيار مجلد المصدر (الذي يحتوي على الصور المراد تحويلها).
    """
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    # فتح نافذة اختيار المجلد (Directory)
    folder_path = filedialog.askdirectory(title="اختر المجلد الذي يحتوي على الصور الأصلية 📁")
    
    return folder_path

def get_output_folder():
    """
    دالة مخصصة لاختيار مجلد الحفظ: حيث سيتم وضع الصور المحولة بعد المعالجة.
    """
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    # فتح نافذة لاختيار أين سيتم حفظ النتائج
    save_path = filedialog.askdirectory(title="اختر المجلد الذي تود حفظ الصور الجديدة فيه 💾")
    
    return save_path

# هذا الجزء مخصص للاختبار المباشر فقط، ولن يعمل إذا استدعيت الملف كمكتبة خارجية
if __name__ == "__main__":
    print("--- اختبار أدوات اختيار المسارات ---")
    
    # اختبار الطور العادي
    img = get_image_path()
    if img: print(f"✅ تم اختيار الملف: {img}")
    
    # اختبار الطور الاحترافي (مجلد المصدر)
    in_folder = get_input_folder()
    if in_folder: print(f"✅ مجلد الصور الأصلية: {in_folder}")
    
    # اختبار مجلد الحفظ
    out_folder = get_output_folder()
    if out_folder: print(f"✅ مجلد حفظ النتائج: {out_folder}")