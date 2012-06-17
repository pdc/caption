
import os.path
import yaml
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5, A4
from reportlab.lib.units import mm, inch

fileName = 'badges.pdf'
##pageHt, pageWd = A4 # reverse coordinates to get landscape page
pageWd, pageHt = A4 # orientation: portrait 
g = canvas.Canvas(fileName, pagesize=(pageWd, pageHt), pageCompression=1)

margin = 5.6 * mm
gutter = 2 * margin
colCount = 4
rowCount = 4
badgeWd =( pageWd - (colCount - 1) * gutter - 2 * margin) / colCount 
badgeHt =( pageHt - (rowCount - 1) * gutter - 2 * margin) / rowCount 
holeRadius = 1 * mm
crossRadius = 2 * mm
holeGap = 0 * mm

image_name = 'shirt-a-680x900.gif'
image_wd = 680
image_ht = 900

def crossLines(cx, cy):
    return [(cx - crossRadius, cy, cx + crossRadius, cy), (cx, cy - crossRadius, cx, cy + crossRadius)]
        

g.setStrokeColorRGB(0.7, 0.7, 0.7)
        
for i in range(rowCount):
    x = i * (badgeWd + gutter) + margin
    for j in range(colCount):
        y = j * (badgeHt + gutter) + margin
        top = y + badgeHt
        
        # Logo image
        wd = badgeWd
        ht = wd * image_ht / image_wd
        g.drawImage(image_name, x, y + 0.5 * badgeHt - 0.5 * ht, wd, ht)
        # was: top - ht - 2 * holeGap - 2 * holeRadius
        
        # Text at bottom
        #g.setFont('Helvetica', 12)
        #g.drawCentredString(x + 0.5 * badgeWd, y, 'Caption 2006')
        
        # Hole guidelines
        cx = x + 0.5 * badgeWd
        for cy in [top - holeRadius - holeGap, y + holeRadius + holeGap]:
            g.circle(cx, cy, holeRadius, stroke=1, fill=0)
            g.lines(crossLines(cx, cy))
        
        # Cutting guidelines
        if i > 0 and j > 0:
            g.lines(crossLines(x - 0.5 * gutter, y - 0.5 * gutter))
        if i > 0 and j + 1 < rowCount:
            g.lines(crossLines(x - 0.5 * gutter, top + 0.5 * gutter))
        if i + 1 < colCount and j > 0:
            g.lines(crossLines(x + badgeWd + 0.5 * gutter, y - 0.5 * gutter))
        if i + 1 < colCount and j + 1 < rowCount:
            g.lines(crossLines(x + badgeWd + 0.5 * gutter, top + 0.5 * gutter))
            

        
g.showPage()

g.save()
        

