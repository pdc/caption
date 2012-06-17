
import os.path
import syck
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
holeGap = 4 * mm

def crossLines(cx, cy):
	return [(cx - crossRadius, cy, cx + crossRadius, cy), (cx, cy - crossRadius, cx, cy + crossRadius)]
		

g.setStrokeColorRGB(0.8, 0.95, 1)
		
for i in range(rowCount):
	x = i * (badgeWd + gutter) + margin
	for j in range(colCount):
		y = j * (badgeHt + gutter) + margin
		top = y + badgeHt
		
		# Logo image
		imgName = 'captionremix-trim-270x140.gif'
		wd = badgeWd
		ht = wd * 140 / 270
		g.drawImage(imgName, x, top - ht - 2 * holeGap - 2 * holeRadius, wd, ht)
		
		# Text at bottom
		g.setFont('Helvetica', 12)
		g.drawCentredString(x + 0.5 * badgeWd, y, 'Caption 2006')
		
		# Hole guidelines
		cx, cy = x + 0.5 * badgeWd, top - holeRadius - holeGap
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
		

