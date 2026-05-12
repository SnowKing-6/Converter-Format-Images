import os
import threading
import customtkinter as ctk
from tkinter import messagebox

# استيراد الوظائف الخاصة بمشروعك
from image_helper import get_image_path, get_input_folder, get_output_folder
from logic import process_conversion

class RaziConverter(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- الإعدادات البصرية العامة ---
        self.title("Razi Converter v2.0")
        self.geometry("650x620")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- تعريف الخطوط (Segoe UI Bold) ---
        self.font_header = ("Segoe UI", 24, "bold")
        self.font_button = ("Segoe UI", 16, "bold")
        self.font_entry  = ("Segoe UI", 14, "bold")
        self.font_tab    = ("Segoe UI", 15, "bold")

        # --- إنشاء واجهة التبويبات ---
        self.tabs = ctk.CTkTabview(self, width=620, height=580, corner_radius=15)
        self.tabs._segmented_button.configure(font=self.font_tab) # تعيين خط التبويبات
        self.tabs.pack(padx=15, pady=15)

        # إضافة الأقسام
        self.tab_single = self.tabs.add("الوضع العادي")
        self.tab_bulk   = self.tabs.add("الوضع الاحترافي")

        # بناء المحتوى
        self.render_single_mode()
        self.render_bulk_mode()

    # ---------------------------------------------------------
    # قسم: بناء واجهة الوضع العادي (Single Mode)
    # ---------------------------------------------------------
    def render_single_mode(self):
        # العنوان الرئيسي
        ctk.CTkLabel(self.tab_single, text="تحويل صورة واحدة", font=self.font_header).pack(pady=(20, 10))

        # مدخل الصورة المصدر
        self.single_in_entry = self.create_entry(self.tab_single, "مسار الصورة المصدر...")
        self.create_button(self.tab_single, "استعراض الصورة", self.browse_single_in, is_outline=True).pack(pady=(0, 20))

        # خيار صيغة التحويل
        ctk.CTkLabel(self.tab_single, text="اختر صيغة التحويل:", font=self.font_entry).pack(pady=5)
        self.single_format = self.create_combobox(self.tab_single)

        # مدخل مجلد الحفظ
        self.single_out_entry = self.create_entry(self.tab_single, "مسار حفظ الصورة...")
        self.create_button(self.tab_single, "تحديد المجلد", self.browse_single_out, is_outline=True).pack(pady=(0, 20))

        # زر التشغيل وشريط التقدم
        self.btn_single_run = self.create_button(self.tab_single, "بدء التحويل الآن", self.run_single_thread)
        self.btn_single_run.pack(pady=20)
        
        self.single_progress = self.create_progressbar(self.tab_single)

    # ---------------------------------------------------------
    # قسم: بناء واجهة الوضع الاحترافي (Bulk Mode)
    # ---------------------------------------------------------
    def render_bulk_mode(self):
        # العنوان الرئيسي
        ctk.CTkLabel(self.tab_bulk, text="تحويل مجلد كامل", font=self.font_header).pack(pady=(20, 10))

        # مدخل المجلد المصدر
        self.bulk_in_entry = self.create_entry(self.tab_bulk, "مسار المجلد الذي يحتوي الصور...")
        self.create_button(self.tab_bulk, "استعراض المجلد", self.browse_bulk_in, is_outline=True).pack(pady=(0, 20))

        # خيار الصيغة
        ctk.CTkLabel(self.tab_bulk, text="تحويل الكل إلى صيغة:", font=self.font_entry).pack(pady=5)
        self.bulk_format = self.create_combobox(self.tab_bulk)

        # مدخل مجلد النتائج
        self.bulk_out_entry = self.create_entry(self.tab_bulk, "مسار حفظ النتائج...")
        self.create_button(self.tab_bulk, "تحديد مجلد الحفظ", self.browse_bulk_out, is_outline=True).pack(pady=(0, 20))

        # زر التشغيل وشريط التقدم
        self.btn_bulk_run = self.create_button(self.tab_bulk, "بدء التحويل الجماعي", self.run_bulk_thread)
        self.btn_bulk_run.pack(pady=20)

        self.bulk_progress = self.create_progressbar(self.tab_bulk)

    # ---------------------------------------------------------
    # أدوات مساعدة لبناء العناصر (UI Helpers) لتقليل تكرار الكود
    # ---------------------------------------------------------
    def create_entry(self, master, placeholder):
        entry = ctk.CTkEntry(master, placeholder_text=placeholder, width=450, height=40, font=self.font_entry)
        entry.pack(pady=(10, 5))
        return entry

    def create_button(self, master, text, command, is_outline=False):
        btn = ctk.CTkButton(master, text=text, command=command, font=self.font_button, height=35, corner_radius=8)
        if is_outline:
            btn.configure(fg_color="transparent", border_width=2, width=150)
        return btn

    def create_combobox(self, master):
        combo = ctk.CTkComboBox(master, values=['webp', 'png', 'jpg', 'avif'], font=self.font_entry, width=150)
        combo.set('webp')
        combo.pack(pady=(0, 20))
        return combo

    def create_progressbar(self, master):
        pb = ctk.CTkProgressBar(master, width=450, height=12)
        pb.set(0)
        pb.pack(pady=10)
        return pb

    # ---------------------------------------------------------
    # وظائف التصفح (Browsing Functions)
    # ---------------------------------------------------------
    def browse_single_in(self):
        path = get_image_path()
        if path: self.update_entry(self.single_in_entry, path)

    def browse_single_out(self):
        path = get_output_folder()
        if path: self.update_entry(self.single_out_entry, path)

    def browse_bulk_in(self):
        path = get_input_folder()
        if path: self.update_entry(self.bulk_in_entry, path)

    def browse_bulk_out(self):
        path = get_output_folder()
        if path: self.update_entry(self.bulk_out_entry, path)

    def update_entry(self, entry, text):
        entry.delete(0, 'end')
        entry.insert(0, text)

    # ---------------------------------------------------------
    # منطق التشغيل والتحويل (Execution Logic)
    # ---------------------------------------------------------
    def run_single_thread(self):
        # التحقق من البيانات ثم تشغيل الخيط
        if not self.single_in_entry.get() or not self.single_out_entry.get():
            return messagebox.showwarning("تنبيه", "يرجى تعبئة المسارات أولاً!")
        threading.Thread(target=self.task_single).start()

    def task_single(self):
        self.single_progress.set(0)
        self.single_progress.configure(mode="indeterminate")
        self.single_progress.start()
        try:
            process_conversion(self.single_in_entry.get(), self.single_out_entry.get(), self.single_format.get(), 85)
            self.single_progress.stop()
            self.single_progress.configure(mode="determinate")
            self.single_progress.set(1)
            messagebox.showinfo("نجاح", "تم التحويل بنجاح! ✅")
        except Exception as e:
            messagebox.showerror("خطأ", str(e))

    def run_bulk_thread(self):
        # التحقق من المجلد
        in_dir = self.bulk_in_entry.get()
        if not in_dir or not os.path.isdir(in_dir):
            return messagebox.showwarning("تنبيه", "المجلد المختار غير موجود!")
        threading.Thread(target=self.task_bulk).start()

    def task_bulk(self):
        in_dir = self.bulk_in_entry.get()
        out_dir = self.bulk_out_entry.get()
        fmt = self.bulk_format.get()
        
        files = [f for f in os.listdir(in_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.avif'))]
        if not files: return messagebox.showinfo("تنبيه", "لا توجد صور في هذا المجلد.")

        total = len(files)
        for i, file in enumerate(files):
            process_conversion(os.path.join(in_dir, file), out_dir, fmt, 85)
            self.bulk_progress.set((i + 1) / total) # تحديث الشريط بناءً على العدد

        messagebox.showinfo("اكتمل", f"تم تحويل {total} صور بنجاح! ✨")

if __name__ == "__main__":
    app = RaziConverter()
    app.mainloop()