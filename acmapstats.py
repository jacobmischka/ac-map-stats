from PIL import Image, ImageChops
import sys, math, operator, functools, os, time, shutil

import re
def sort_nicely( l ):
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
	l.sort( key=alphanum_key )

yA = 165
yB = 220
yC = 275
yD = 331
yE = 387
yF = 442

x1 = 411
x2 = 466
x3 = 521
x4 = 575
x5 = 630


class MapSquare(object):
	
	def __init__(self, name, coordinates):
		self.name = name
		self.coordinates = coordinates
		self.count = 0

class Building(object):
	
	def __init__(self, name, img, acmap):
		self.name = name
		self.img = img
		self.acmap = acmap
		self.count = 0
		
class AMap(object):
	def __init__(self):
		self.a1 = MapSquare("a1", [x1, yA])
		self.a2 = MapSquare("a2", [x2, yA])
		self.a4 = MapSquare("a4", [x4, yA])
		self.a5 = MapSquare("a5", [x5, yA])
		self.squares = [self.a1, self.a2, self.a4, self.a5]

class FMap(object):
	def __init__(self):
		self.f1 = MapSquare("f1", [x1, yF])
		self.f2 = MapSquare("f2", [x2, yF])
		self.f3 = MapSquare("f3", [x3, yF])
		self.f4 = MapSquare("f4", [x4, yF])
		self.squares = [self.f1, self.f2, self.f3, self.f4]
	
class Map(object):
	def __init__(self):
		self.c1 = MapSquare("c1", [x1, yC])
		self.c2 = MapSquare("c2", [x2, yC])
		self.c3 = MapSquare("c3", [x3, yC])
		self.c4 = MapSquare("c4", [x4, yC])
		self.c5 = MapSquare("c5", [x5, yC])
		
		self.d1 = MapSquare("d1", [x1, yD])
		self.d2 = MapSquare("d2", [x2, yD])
		self.d3 = MapSquare("d3", [x3, yD])
		self.d4 = MapSquare("d4", [x4, yD])
		self.d5 = MapSquare("d5", [x5, yD])
		
		self.e1 = MapSquare("e1", [x1, yE])
		self.e2 = MapSquare("e2", [x2, yE])
		self.e3 = MapSquare("e3", [x3, yE])
		self.e4 = MapSquare("e4", [x4, yE])
		self.e5 = MapSquare("e5", [x5, yE])
		
		self.squares = [self.c1, self.c2, self.c3, self.c4, self.c5, self.d1, self.d2, self.d3, self.d4, self.d5, self.e1, self.e2, self.e3, self.e4, self.e5]
		
class HouseMap(object):
	def __init__(self):
		self.b1 = MapSquare("b1", [x1, yB])
		self.b2 = MapSquare("b2", [x2, yB])
		self.b3 = MapSquare("b3", [x3, yB])
		self.b4 = MapSquare("b4", [x4, yB])
		self.b5 = MapSquare("b5", [x5, yB])
		
		self.c1 = MapSquare("c1", [x1, yC])
		self.c2 = MapSquare("c2", [x2, yC])
		self.c3 = MapSquare("c3", [x3, yC])
		self.c4 = MapSquare("c4", [x4, yC])
		self.c5 = MapSquare("c5", [x5, yC])
		
		self.d1 = MapSquare("d1", [x1, yD])
		self.d2 = MapSquare("d2", [x2, yD])
		self.d3 = MapSquare("d3", [x3, yD])
		self.d4 = MapSquare("d4", [x4, yD])
		self.d5 = MapSquare("d5", [x5, yD])
		
		self.e1 = MapSquare("e1", [x1, yE])
		self.e2 = MapSquare("e2", [x2, yE])
		self.e3 = MapSquare("e3", [x3, yE])
		self.e4 = MapSquare("e4", [x4, yE])
		self.e5 = MapSquare("e5", [x5, yE])
		
		self.f1 = MapSquare("f1", [x1, yF])
		self.f2 = MapSquare("f2", [x2, yF])
		self.f3 = MapSquare("f3", [x3, yF])
		self.f4 = MapSquare("f4", [x4, yF])
		self.f5 = MapSquare("f5", [x5, yF])
		
		self.squares = [self.b1, self.b2, self.b3, self.b4, self.b5, self.c1, self.c2, self.c3, self.c4, self.c5, self.d1, self.d2, self.d3, self.d4, self.d5, self.e1, self.e2, self.e3, self.e4, self.e5, self.f1, self.f2, self.f3, self.f4, self.f5]

def rms(img1, img2):
	h = ImageChops.difference(img1, img2).histogram()
	return math.sqrt(functools.reduce(operator.add, map(lambda h, i: h*(i**2), h, range(256)))/(float(img1.size[0]) * img1.size[1]))
	
shop = Building("shop", Image.open("shop.png"), AMap())
dump = Building("dump", Image.open("dump.png"), AMap())
postoffice = Building("post office", Image.open("postoffice.png"), AMap())
tailor = Building("tailor", Image.open("tailor.png"), FMap())
policestation = Building("police station", Image.open("policestation.png"), Map())
fountain = Building("fountain", Image.open("fountain.png"), Map())
museum = Building("museum", Image.open("museum.png"), Map())
buildings = [shop, dump, postoffice, tailor, policestation, fountain, museum]

cliff = Image.open("cliff.png")
cliffSquares = [MapSquare("b1", [x1, 249]), MapSquare("c1", [x1, 305]), MapSquare("d1", [x1, 361]), MapSquare("e1", [x1, 417])]

houseMap = HouseMap()

def main():
	startTime = time.time()
	fileCount = 0
	twoLayers = 0
	threeLayers = 0
	directory = "./"
	skip = 0
	most = 0
	current = 0
	possiblyDecentMaps = 0
	printStats = True
	if len(sys.argv) > 1:
		directory = sys.argv[1]
	if len(sys.argv) > 2:
		skip = int(sys.argv[2])
	if len(sys.argv) > 3:
		printStats = sys.argv[3]
	
	if printStats == 0 or printStats == "0" or printStats == "false":
		printStats = False
		
	files = os.listdir(directory)
	sort_nicely(files)
	for file in files:
		if file.endswith(".png"):
			fileCount += 1
			if fileCount <= skip:
				continue
			yOffset = 0
			im = Image.open(directory+file)
			region = im.crop((330, 140, 331, 141))
			colors = region.getcolors(1)
			if colors is None or colors[0][1] != (255, 255, 85, 255): #make sure it's a screenshot of the map
				print(str(file) + " No map found.")
				continue
			
			#try to look to see where the map is in case it's higher or lower than expected
			region = im.crop((400, 146, 401, 147))
			colors = region.getcolors(1)
			if colors[0][1] !=	(187, 115, 60, 255) and colors[0][1] != (186, 114, 60, 255) and colors[0][1] != (202, 123, 60, 255):
				region = im.crop((400, 144, 401, 145))
				colors = region.getcolors(1)
				if colors[0][1] ==  (187, 115, 60, 255) or colors[0][1] == (186, 114, 60, 255) or colors[0][1] == (202, 123, 60, 255):
					yOffset = -2
				else:
					for y in range(0, 256):
						region = im.crop((400, y, 401, y+1))
						colors = region.getcolors(1)
						if colors[0][1] == (187, 115, 60, 255) or colors[0][1] == (186, 114, 60, 255) or colors[0][1] == (202, 123, 60, 255):
							yOffset = y-146
							break
				
			layers = 1
			shop = 0
			post = 0
			fountain = 0
			housesOkay = True
			for building in buildings:
				lowestdiff = 100
				bestmatch = 0
				for mapsquare in building.acmap.squares:
					region = im.crop((mapsquare.coordinates[0], mapsquare.coordinates[1]+yOffset, mapsquare.coordinates[0]+48, mapsquare.coordinates[1]+48+yOffset))
					diff = rms(region, building.img)
					#print(str(file)+" "+building.name+" "+mapsquare.name+" "+str(diff))
					if diff < lowestdiff:
						lowestdiff = diff
						bestmatch = mapsquare
							
				bestmatch.count += 1
				building.count += 1
				if building.name == "shop":
					shop = bestmatch
				elif building.name == "post office":
					post = bestmatch
				elif building.name == "fountain":
					fountain = bestmatch
					
				if  bestmatch.name == "c2" or bestmatch.name == "c3" or bestmatch.name == "c4":
					print(str(file) + " " + building.name + " " + bestmatch.name)
			
			for square in cliffSquares:
				region = im.crop((square.coordinates[0], square.coordinates[1]+yOffset, square.coordinates[0]+8, square.coordinates[1]+16+yOffset))
				diff = rms(region, cliff)
				if diff < 20:
					layers += 1
					
			if layers == 2:
				twoLayers += 1
			elif layers == 3:
				threeLayers += 1
				
			c1 = False
			c5 = False
			d1 = False
			d3 = False
			d5 = False
			c3ledge = False
			col1 = False
			col2 = 0
			col4 = 0
			col5 = False
			e2 = False
			e3 = False
			e4 = False
			belowShop = False
			ramp = ["z9","z9","z9","z9"]
			rampFound = 0

			for square in houseMap.squares:
				region = im.crop((square.coordinates[0], square.coordinates[1]+yOffset, square.coordinates[0]+50, square.coordinates[1]+50+yOffset))
				colors = region.getcolors(maxcolors=1000)
				
				for color in colors:
					#blue house = (90, 90, 225, 255)	purple house = (145, 70, 205, 255)	yellow house = (170, 115, 20, 255)
					if color[1] == (90, 90, 225, 255) or color[1] == (145, 70, 205, 255) or color[1] == (170, 115, 20, 255):
						if "f" in square.name:
							housesOkay = False
						elif square.name == "e2":
							e2 = True
						elif square.name == "e4":
							e4 = True
						elif square.name == "e3":
							e3 = True
						elif "e" in square.name:
							housesOkay = False
						elif square.name == "d1":
							d1 = True
						elif square.name == "d5":
							d5 = True

						if "1" in square.name:
							col1 = True
							if fountain.name == "d5" or fountain.name == "e4":
								housesOkay = False
						elif "2" in square.name:
							col2 += 1
						elif "4" in square.name:
							col4 += 1
						elif "5" in square.name:
							col5 = True
							if fountain.name == "d1" or fountain.name == "e2":
								housesOkay = False
						if square.name == "c1":
							c1 = True
						elif square.name == "c5":
							c5 = True
						elif square.name == "d3":
							d3 = True
						elif (shop.name == "a2" and square.name == "b2") or (shop.name == "a4" and square.name == "b4"):
							belowShop = True
					#ramp
					if color[1] == (66, 189, 66, 255):
						ramp[rampFound] = square.name
						rampFound += 1
					# ledge
					if color[1] == (146, 146, 146, 255) or color[1] == (148, 148, 148, 255):
						if square.name == "c3":
							c3ledge = True


			if c1 and c5:
				housesOkay = False
			elif belowShop == False:
				housesOkay = False
			elif col1 and col5:
				housesOkay = False
			elif ("e" in fountain.name and ((col4 and col1) or (col5 and col2))):
				housesOkay = False
			elif d1 and (col5 or col4 or shop.name == "a4"):
				housesOkay = False
			elif d5 and (col1 or col2 or shop.name == "a2"):
				housesOkay = False
			elif (e2 or e3 or e4) and (col1 or col5):
				housesOkay = False
			elif e2 and (shop.name != "a2" or col4):
				housesOkay = False
			elif e4 and (shop.name != "a4" or col2):
				housesOkay = False
			elif fountain.name == "d1" and (col4 or shop.name == "a4"):
				housesOkay = False
			elif fountain.name == "d5" and (col2 or shop.name == "a2"):
				housesOkay = False
			elif fountain.name == "e2" and (col4 or shop.name == "a4"):
				housesOkay = False
			elif fountain.name == "e4" and (col2 or shop.name == "a2"):
				housesOkay = False
			elif shop.name == "a2" and col5 and fountain.name != "c5":
				housesOkay = False
			elif shop.name == "a4" and col1 and fountain.name != "c1":
				housesOkay = False
			elif (e2  or e3 or e4) and shop.name == "a2" and col4:
				housesOkay = False
			elif (e2  or e3 or e4) and shop.name == "a4" and col2:
				housesOkay = False

			#check for ramps to get to fountain
			OK = False
			OK2 = False
			if housesOkay:
				for i in range (0, 4):
					if (col1 or col5) or ("e" in fountain.name and (col1 or col5)) or (fountain.name == "d4" and (shop.name == "a2" or col2)) or (fountain.name == "d2" and (shop.name == "a4" or col4)):
						if (ord(ramp[i][1:2]) == ord(fountain.name[1:2])) and ord(ramp[i][0:1]) <  ord(fountain.name[0:1]):
							OK = True
					else:
						if (abs(ord(ramp[i][1:2]) - ord(fountain.name[1:2])) <= 1 and ord(ramp[i][0:1]) <  ord(fountain.name[0:1])):
							OK = True

					if col2 > 1 and col5 and ("d" in fountain.name or fountain.name == "c5"):
						if (ord(ramp[i][1:2]) == ord(fountain.name[1:2])) and ord(ramp[i][0:1]) <  ord(fountain.name[0:1]):
							OK2 = True
					elif col4 > 1 and col1 and ("d" in fountain.name or fountain.name == "c1"):
						if (ord(ramp[i][1:2]) == ord(fountain.name[1:2])) and ord(ramp[i][0:1]) <  ord(fountain.name[0:1]):
							OK2 = True
					else:
						OK2 = True
				if not (OK and OK2):
					housesOkay = False

			#check for ramps to get to houses in d3. d2/d4 houses will always hit this condition.
			OK = False
			if d3 and c3ledge:
				for i in range (0, 4):
					#if it's 3 layers then the d ramps are either below the house, or there's another cliff at c
					#that's also in the way, so we need that anyway. If it's 2 layers then it will get us back up
					if (ramp[i] == "c2" or ramp[i] == "c3" or ramp[i] == "c4") or (layers == 2 and (ramp[i] == "d2" or ramp[i] == "d3" or ramp[i] == "d4")):
						OK = True
				if not OK:
					housesOkay = False

			if (housesOkay and ((shop.name == "a2" and post.name == "a4") or (shop.name == "a4" and post.name == "a2")) and not (fountain.name == "e1" or fountain.name == "e5" or (layers == 3 and "e" in fountain.name))):
				if not os.path.exists(directory+"maybe/"):
					os.makedirs(directory+"maybe/")
				shutil.copy(directory+file, directory+"maybe/"+file)
				possiblyDecentMaps += 1
				current = 0
			else:
				current += 1
				if current > most:
					most = current
	
	if printStats:				
		print("two layers:\t"+str(twoLayers)+"\t"+str((twoLayers/(fileCount-skip))*100)+"%")
		print("three layers:\t"+str(threeLayers)+"\t"+str((threeLayers/(fileCount-skip))*100)+"%")
		
		for building in buildings:
			print(str("\n"+building.name))
			for mapsquare in building.acmap.squares:
						print("\t"+str(mapsquare.name)+":\t"+str(mapsquare.count)+"\t"+str((mapsquare.count/building.count)*100)+"%")	
	print("\nmaps: "+str((fileCount-skip)))
	print("possibly decent maps: "+str(possiblyDecentMaps))
	print("Longest bad streak: " +str(most))
	print("elapsed time: "+str(time.time()-startTime)+" seconds")
	
	
	
if __name__ == "__main__":
	main()
