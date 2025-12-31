import cv2
import numpy

QUADRANT_CODES = [
    "ROCKY_FLATS",
    "COLD_JUNGLE",
    "FIRY_DESERT",
    "SANDY_SWAMP"
]

CHECKER_CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.001)

IMAGERE_ERR_CHECKERS_NOT_FOUND = """
No checker pattern found; 
check image or change pattern size parameter
"""

class Imagere:
    def __init__(
        self, 
        calibrationImagePath="./calibration.jpg", 
        patternSize = (6, 8)
    ):
        image = cv2.imread(calibrationImagePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        hasCheckers, corners = cv2.findChessboardCorners(image, patternSize)

        if hasCheckers:
            corners = cv2.cornerSubPix(
                image, 
                corners, 
                (11,11), 
                (-1,-1), 
                CHECKER_CRITERIA
            )
        else:
            raise 

        objectPoints = numpy.zeros(
            (patternSize[0]*patternSize[1], 3), 
            numpy.float32
        )
        objectPoints[:,:2] = numpy.mgrid[
            0:patternSize[0],
            0:patternSize[1]
        ].T.reshape(
            -1,2
        )
        
        objectPointsArray = [objectPoints]
        imagePointsArray = [corners]

        result, self.matrix, self.distance, self.rVectors, self.tVectors = cv2.calibrateCamera(
            objectPointsArray, 
            imagePointsArray, 
            image.shape[::-1], 
            None, 
            None
        )

    def undistort(
        self,
        imagePath = "./input.jpg"
    ):
        rawImage = cv2.imread(imagePath)
        
        h,  w = rawImage.shape[:2]

        newCameraMatrix, rOI = cv2.getOptimalNewCameraMatrix(
            self.matrix, 
            self.distance, 
            (w,h), 
            1, 
            (w,h)
        )

        undistorted = cv2.undistort(
            rawImage, 
            self.matrix, 
            self.distance, 
            None, 
            newCameraMatrix
        )
 
        x, y, w, h = rOI
        undistorted = undistorted[y:y+h, x:x+w]

        # cv2.imshow("Undistorted Image", undistorted)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        sharpen_kernel = numpy.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
        sharpened = cv2.filter2D(undistorted, -1, sharpen_kernel)

        self.image = undistorted

        cv2.imwrite("undistorted.jpg", sharpened)

    def edgeDetect(self):
        imageGS = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

        laplacian = cv2.Laplacian(imageGS, cv2.CV_32F)
 
        # Convert to uint8
        laplacian_abs = cv2.convertScaleAbs(laplacian)
        
        scaledLP = cv2.resize(laplacian_abs, (0,0), fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)

        # Display result
        # cv2.imshow("Laplacian Edge Detection", scaledLP)
        
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def binary(self, threshold = 130):
        imageGS = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

        asBinary = numpy.where(imageGS <= threshold, 0, 255)
        asBinary = asBinary.astype(numpy.uint8)

        # kernel = numpy.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        # sharpened = cv2.filter2D(asBinary, -1, kernel)

        self.binaryImage = asBinary

        cv2.imwrite("./binaryOutput.jpg", asBinary)

        # scaledBinary = cv2.resize(
        #     sharpened, 
        #     (0,0), 
        #     fx=0.2, 
        #     fy=0.2, 
        #     interpolation=cv2.INTER_CUBIC
        # )

        # cv2.imshow("Binary Image", scaledBinary)
        
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def qrDetect(self):
        # qrCodes = []
        # for code in QUADRANT_CODES:
        #     qrCodes.append(
        #         cv2.imread(
        #             f"./{code}.jpg",
        #             cv2.IMREAD_GRAYSCALE
        #         )
        #     )

        qrDetector = cv2.QRCodeDetectorAruco()

        qrFound, decodedArray, pointsArray, foundCodes = qrDetector.detectAndDecodeMulti(
            self.image
        )

        print(qrFound)
        print(len(decodedArray))

        for name in decodedArray:
            print(f"\t{name}")

        # withBoxes = cv2.cvtColor(
        #     self.binaryImage, 
        #     cv2.COLOR_GRAY2BGR
        # )

        withBoxes = self.image

        largest = self.getLargestQRCode(pointsArray)

        print(f"Largest is {decodedArray[largest]}")

        self.calculateMMPerPixel(pointsArray[largest])

        for points in pointsArray:
            withBoxes = cv2.polylines(
                withBoxes,
                numpy.int32([points]),
                True,
                (0, 255, 0),
                3
            )

        scaledBoxed = cv2.resize(
            withBoxes, 
            (0,0), 
            fx=0.2, 
            fy=0.2, 
            interpolation=cv2.INTER_CUBIC
        )

        cv2.imshow("Boxed Image", scaledBoxed)

        # for code in decodedArray:
        #     print(code)

        # cv2.imshow("Flat QR", straightCodes[0])

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def getLargestQRCode(self, pointsOfCodes):
        asNumpy = pointsOfCodes.astype(numpy.uint16)

        largestStdDev  = 0
        indexOfLargest = 0

        for index in range(0, asNumpy.shape[0]):
            xPoints, yPoints = asNumpy[index, :, 0], asNumpy[index, :, 1]
            
            avgStdDev = (numpy.std(xPoints) + numpy.std(yPoints))/2
            
            if (avgStdDev > largestStdDev):
                largestStdDev = avgStdDev
                indexOfLargest = index

        return indexOfLargest

    def calculateMMPerPixel(self, points, sizeInMM=20):
        linePoints = points[2:4]

        mmPerPix = sizeInMM/numpy.linalg.norm(linePoints)

        print(numpy.divide(linePoints, 5))
        print(mmPerPix)
        # numpy.linalg.norm()