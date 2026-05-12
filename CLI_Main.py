# السطر: استيراد الأدوات من مكتباتنا الخاصة ونظام التشغيل
# الوظيفة: جلب كل ما نحتاجه (النوافذ، محرك التحويل، التعامل مع الملفات، وشريط التقدم)
# لماذا: لكي يعمل البرنامج كمنظومة واحدة متكاملة
from image_helper import get_image_path, get_input_folder, get_output_folder
from logic import process_conversion
import os
from tqdm import tqdm # مكتبة شريط التقدم (تحتاج تثبيت: pip install tqdm)

def main():
    # السطر: واجهة الترحيب واختيار الطور
    # الوظيفة: تحديد ما إذا كنا سنعالج صورة واحدة أو مئات الصور
    # لو حذفته: لن يعرف البرنامج أي مسار سيسلكه (عادي أم احترافي)
    print("\n" + "="*30)
    print("🎨 محول الصور الاحترافي 🎨")
    print("="*30)
    print("1 - الطور العادي (صورة واحدة)")
    print("2 - الطور الاحترافي (مجلد كامل)")
    
    choice = input("\n📥 اختر الطور (1 أو 2): ")

    # السطر: قائمة الصيغ المدعومة
    # الوظيفة: حصر الخيارات لمنع المستخدم من كتابة امتداد خاطئ
    # لماذا: لضمان أننا نرسل للمحرك صيغة يفهمها فعلياً
    formats = ["png", "jpg", "webp", "avif"]
    print("\n--- الصيغ المتاحة ---")
    for i, fmt in enumerate(formats, 1):
        print(f"{i} - {fmt}")

    try:
        # السطر: منطق اختيار الصيغة بالرقم
        # الوظيفة: تحويل رقم اختيار المستخدم إلى نص الامتداد (مثلاً 3 تصبح webp)
        # لو حذفته: سيضطر المستخدم لكتابة الامتداد يدوياً وقد يخطئ
        fmt_idx = int(input("\n🎯 اختر رقم الصيغة المطلوبة: ")) - 1
        target_format = formats[fmt_idx]
        print(target_format)
    except (ValueError, IndexError):
        # صمام أمان في حال أدخل المستخدم رقماً خاطئاً
        print("⚠️ اختيار غير دقيق، سيتم استخدام webp افتراضياً.")
        target_format = "webp"
        print(target_format)

    # --- بداية تنفيذ الطور العادي ---
    if choice == "1":
        # فتح نافذة اختيار ملف واحد
        img_path = get_image_path()
        
        if img_path:
            # فتح نافذة اختيار مكان الحفظ
            save_dir = get_output_folder()
            
            if save_dir:
                print(f"\n⚙️ جاري التحويل إلى {target_format}...")
                # استدعاء المحرك لمعالجة ملف واحد فقط
                success, result = process_conversion(img_path, save_dir, target_format, 85)
                if success:
                    print(f"✅ تم بنجاح! المسار الجديد: {result}")
                    print(target_format)
                else:
                    print(f"❌ فشل التحويل: {result}")

    # --- بداية تنفيذ الطور الاحترافي ---
    elif choice == "2":
        # اختيار مجلد الصور المصدر
        input_dir = get_input_folder()
        
        if input_dir:
            # اختيار مجلد الحفظ للصور الجديدة
            output_dir = get_output_folder()
            
            if output_dir:
                # السطر: فلترة الملفات الصورية فقط
                # الوظيفة: جلب قائمة بكل الصور داخل المجلد لاستخدامها في شريط التقدم
                # لماذا: لنعرف العدد الكلي قبل البدء (مثلاً: 0/50)
                all_files = [f for f in os.listdir(input_dir) 
                             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.avif'))]
                
                if not all_files:
                    print("⚠️ لا توجد صور مدعومة في هذا المجلد.")
                    return

                print(f"\n🚀 تم العثور على {len(all_files)} صورة. ابدأ العمل:")
                
                # السطر: حلقة التكرار مع شريط التقدم (tqdm)
                # الوظيفة: معالجة كل صورة وعرض النسبة المئوية للتقدم
                # لو حذفته: سيعالج البرنامج الصور في "صمت" ولن تعرف متى ينتهي
                for filename in tqdm(all_files, desc="جاري المعالجة", unit="صورة"):
                    full_path = os.path.join(input_dir, filename)
                    process_conversion(full_path, output_dir, target_format, 85)
                
                print(f"\n✅ مبروك! تمت معالجة كل الصور وحفظها في: {output_dir}")

    else:
        print("❌ اختيار غير صحيح للطور.")

# السطر: نقطة انطلاق البرنامج
# الوظيفة: تشغيل الدالة الأساسية main
if __name__ == "__main__":
    main()