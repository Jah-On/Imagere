import fpdf.fpdf as pdf
import math
import qrcode

QUADRANT_CODES = [
    "ROCKY_FLATS",
    "COLD_JUNGLE",
    "FIRY_DESERT",
    "SANDY_SWAMP"
]

def dotsToMM(point: tuple):
    asMM = []

    for node in point:
        asMM.append(node/72 * 25.4)

    return tuple(asMM)

def distortion_map(
    pageFormat = "a4",
    checkerSize = 20,
    outputPath = "./distortion_map.pdf"
):
    (pageWidth, pageHeight) = dotsToMM(pdf.PAGE_FORMATS[pageFormat])

    doc = pdf.FPDF()

    doc.add_page(format=pageFormat)

    lastNotFilled = False
    lastStartFilled = False
    for y in range(0, round(pageHeight), checkerSize):
        lastNotFilled = not lastStartFilled

        for x in range(0, round(pageWidth), checkerSize):
            if lastNotFilled:
                doc.rect(x=x, y=y, w=checkerSize, h=checkerSize, style="F")
            
            lastNotFilled = not lastNotFilled

        lastStartFilled = not lastStartFilled

    doc.output(outputPath)

def reference_sheet(
    pageFormat = "a4",
    lineSpacing = 20,
    codeGapCount = 3,
    outputPath = "./reference_sheet.pdf"
):
    (pageWidth, pageHeight) = dotsToMM(pdf.PAGE_FORMATS[pageFormat])

    doc = pdf.FPDF()

    doc.add_page(format=pageFormat)

    # for x in range(lineSpacing, round(pageWidth), lineSpacing):
    #     doc.line(x1=x, y1=0, x2=x, y2=pageHeight)

    # for y in range(lineSpacing, round(pageHeight), lineSpacing):
    #     doc.line(x1=0, y1=y, x2=pageWidth, y2=y)

    qcSize     = lineSpacing # - 1

    gap        = codeGapCount * lineSpacing
    leadingGap = gap # + 0.5
    xBackGap   = math.floor(pageWidth/lineSpacing)*lineSpacing - gap # + 0.5
    yBackGap   = math.floor(pageHeight/lineSpacing)*lineSpacing - gap # + 0.5

    # Quadrant 2
    qrCode = qrcode.make(QUADRANT_CODES[1], border=0).get_image()

    doc.image(qrCode, leadingGap, leadingGap, qcSize, qcSize)

    # Quadrant 1
    qrCode = qrcode.make(QUADRANT_CODES[0], border=0).get_image()
    
    doc.image(qrCode, xBackGap, leadingGap, qcSize, qcSize)

    # Quadrant 3
    qrCode = qrcode.make(QUADRANT_CODES[2], border=0).get_image()
    
    doc.image(qrCode, leadingGap, yBackGap, qcSize, qcSize)

    # Quadrant 4
    qrCode = qrcode.make(QUADRANT_CODES[3], border=0).get_image()
    
    doc.image(qrCode, xBackGap, yBackGap, qcSize, qcSize)

    doc.output(outputPath)

def exportQRCodes():
    for code in QUADRANT_CODES:
        qrCode = qrcode.make(code, border=0).get_image()

        qrCode.save(f"{code}.jpg")