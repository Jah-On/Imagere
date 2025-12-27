import dearpygui.dearpygui as dpg
import cv2
import numpy

import Generate
import GUI

def main():
    Generate.distortion_map()
    Generate.reference_grid()

    # image = numpy.array(qrcode.make("COLD_JUNGLE", border=1).get_image().convert("L"))
    # print(image)
    # cv2.imshow("Name", image)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # ui = GUI.GUI()
    # ui.start()

if __name__ == "__main__":
    main()