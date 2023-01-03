import cv2

def is_image_blurred(img):
    threshhold = 28 # variable per camera device, should be in config?
    variance_of_laplacian = cv2.Laplacian(img, cv2.CV_64F).var()
    return variance_of_laplacian < threshhold