import os
import random
import cv2
import numpy as np

STUDENTS_DIR = "students"
BACKGROUND = "classroom_bg.jpg"

def generate_class_image():

    bg = cv2.imread(BACKGROUND)
    bg = cv2.resize(bg,(900,600))

    students = os.listdir(STUDENTS_DIR)

    # כמה תלמידים יהיו בתמונה
    num_present = random.randint(0,len(students))

    present = random.sample(students,num_present)

    for name in present:

        imgs = os.listdir(os.path.join(STUDENTS_DIR,name))
        img_path = os.path.join(STUDENTS_DIR,name,random.choice(imgs))

        face = cv2.imread(img_path)

        # שינוי גודל אקראי
        scale = random.uniform(0.5,1.0)
        face = cv2.resize(face,(0,0),fx=scale,fy=scale)

        h,w,_ = face.shape

        # מיקום אקראי
        x = random.randint(0,bg.shape[1]-w)
        y = random.randint(0,bg.shape[0]-h)

        bg[y:y+h,x:x+w] = face

    return bg,present

import streamlit as st

if st.button("צור תמונת כיתה רנדומלית"):

    img,present = generate_class_image()

    st.image(img,channels="BGR")

    st.write("נוכחים:",present)
