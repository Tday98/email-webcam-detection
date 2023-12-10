import glob
import os
import cv2
import time
from send_email import send_email, get_credentials
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1


def clean_folder():
    """
    cleans out image/*.png files and leaves an empty folder
    :return:
    """
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)


service = get_credentials()
while True:
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    clean_thread = Thread(target=clean_folder)
    clean_thread.daemon = True

    # converts image to blurred grayscale to make object recognition easier.
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    cv2.imshow("My video", delta_frame)

    # This takes the grayscale image and if it is above a 60 threshold defines it as an object
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # < 5000 is how big the object must be
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        # Code that generates boxes around objects as defined by opencv library
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_images = glob.glob("images/*.png")
            image_with_object = all_images[(int(len(all_images) / 2))]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(service, image_with_object))
        email_thread.daemon = True

        email_thread.start()

    cv2.imshow("My video", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

clean_thread.start()
video.release()
