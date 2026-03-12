import os
import random
import cv2
import zipfile
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ZIP_PATH = os.path.join(BASE_DIR, "My_Classmates_small.zip")
EXTRACT_PATH = os.path.join(BASE_DIR, "My_Classmates")

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

    bg = cv2.resize(bg, (900, 600), interpolation=cv2.INTER_CUBIC)

    students = os.listdir(REFERENCE_DIR)

    num_present = random.randint(0, len(students))
    present = random.sample(students, num_present)

    rows = 2
    cols = 5

    cell_w = bg.shape[1] // cols
    cell_h = bg.shape[0] // rows

    positions = []

    for r in range(rows):
        for c in range(cols):
            x = c * cell_w
            y = r * cell_h
            positions.append((x, y))

    random.shuffle(positions)

    i = 0

    for name in present:

        if i < len(positions):

            student_dir = os.path.join(REFERENCE_DIR, name)
            imgs = os.listdir(student_dir)

            if len(imgs) > 0:

                img_path = os.path.join(student_dir, random.choice(imgs))
                face = cv2.imread(img_path)

                if face is not None:

                    new_w = int(cell_w * 0.8)
                    new_h = int(cell_h * 0.8)

                    face = cv2.resize(face, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

                    x, y = positions[i]

                    x = x + (cell_w - new_w) // 2
                    y = y + (cell_h - new_h) // 2

                    bg[y:y+new_h, x:x+new_w] = face

                    i = i + 1

    return bg, present


st.title("מחולל תמונת כיתה")

if st.button("צור תמונת כיתה רנדומלית"):

    img, present = generate_class_image()

    st.image(img, channels="BGR")
    st.write("נוכחים:", present)
