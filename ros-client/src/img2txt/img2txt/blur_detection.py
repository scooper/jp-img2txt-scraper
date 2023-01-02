import cv2

def image_blurred(img):
    threshhold = 28 # variable per camera device, should be in config?
    variance_of_laplacian = cv2.Laplacian(img, cv2.CV_64F).var()
    print(variance_of_laplacian)
    return variance_of_laplacian < threshhold