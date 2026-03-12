import os
import random
import cv2
import zipfile
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ZIP_PATH = os.path.join(BASE_DIR, "My_Classmates_small.zip")
EXTRACT_PATH = os.path.join(BASE_DIR, "My_Classmates")

# חילוץ ה-ZIP אם עוד לא חולץ
if not os.path.exists(EXTRACT_PATH):
    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(EXTRACT_PATH)

REFERENCE_DIR = os.path.join(EXTRACT_PATH, "content", "My_Classmates_small")
BACKGROUND = os.path.join(BASE_DIR, "הורדה.jfif")


def generate_class_image():

    bg = cv2.imread(BACKGROUND)

    if bg is None:
        st.error("Background image not found")
        st.stop()

    bg = cv2.resize(bg, (900, 600))

    if not os.path.exists(REFERENCE_DIR):
        st.error("Students folder not found")
        st.stop()

    students = os.listdir(REFERENCE_DIR)

    num_present = random.randint(0, len(students))
    present = random.sample(students, num_present)

    for name in present:

        student_dir = os.path.join(REFERENCE_DIR, name)
        imgs = os.listdir(student_dir)

        if len(imgs) > 0:

            img_path = os.path.join(student_dir, random.choice(imgs))
            face = cv2.imread(img_path)

            if face is not None:

                h, w, c = face.shape

                # הגדלה פי 3
                new_w = int(w * 3)
                new_h = int(h * 3)

                face = cv2.resize(face, (new_w, new_h))

                if new_h < bg.shape[0] and new_w < bg.shape[1]:

                    x = random.randint(0, bg.shape[1] - new_w)
                    y = random.randint(0, bg.shape[0] - new_h)

                    bg[y:y+new_h, x:x+new_w] = face

    return bg, present


st.title("מחולל תמונת כיתה")

if st.button("צור תמונת כיתה רנדומלית"):

    img, present = generate_class_image()

    st.image(img, channels="BGR")
    st.write("נוכחים:", present)
