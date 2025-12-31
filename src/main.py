import Generate
import GUI
from Imagere import Imagere as re

def main():
    Generate.exportQRCodes()
    
    reInstance = re()
    reInstance.undistort()
    reInstance.binary()
    reInstance.qrDetect()
    # Generate.distortion_map()
    # Generate.reference_sheet()

    # image = cv2.imread("./calibration.jpg")
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # checkersFound, corners = cv2.findChessboardCorners(image, PATTERN_SIZE)

    # if checkersFound:
    #     corners2 = cv2.cornerSubPix(image, corners, (11,11), (-1,-1), criteria)

    #     withCheckers = image
    #     cv2.drawChessboardCorners(withCheckers, PATTERN_SIZE, corners2, checkersFound)

    #     newSize = int(numpy.size(withCheckers, 1) * 0.2), int(numpy.size(withCheckers, 0) * 0.2)
    #     # print()
    #     resized = cv2.resize(withCheckers, newSize)
    #     cv2.imshow('Corners drawn', resized)
    # else:
    #     print("Checkers not detected!")

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # image = numpy.array(qrcode.make("COLD_JUNGLE", border=1).get_image().convert("L"))
    # print(image)
    # cv2.imshow("Name", image)

    # ui = GUI.GUI()
    # ui.start()

if __name__ == "__main__":
    main()