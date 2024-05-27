import os
from half import full_pipeline

img_dir = "input/test/images"
label_dir = "input/test/labels"
files = os.listdir(img_dir)
files = [f for f in files if os.path.isfile(img_dir+'/'+f)]
files.sort()

# idx = 1
# for file in files:
#     pure = file.rsplit('.', 1)[0]
#     ext = file.rsplit('.', 1)[1]

#     old_img = os.path.join(img_dir, f"{pure}.{ext}")
#     new_img = os.path.join(img_dir, f"{idx}.{ext}")
#     os.rename(old_img, new_img)

#     old_label = os.path.join(label_dir, f"{pure}.txt")
#     new_label = os.path.join(label_dir, f"{idx}.txt")
#     os.rename(old_label, new_label)

#     idx+=1

failed_yolo = 0
failed_cv2 = 0
success = 0

for file in files:
    print(file)
    try:
        full_pipeline(f"{img_dir}/{file}", log=True, debug=True, file_name=file)
        success += 1
    except Exception as e:
        if str(e).startswith("plate error"):
            failed_yolo += 1
        elif str(e).startswith("cv2 error"):
            failed_cv2 += 1

print(f"Detection success {success}, failed yolo {failed_yolo}, failed cv2 {failed_cv2}")