from PIL import Image, ImageChops
import sys, math, operator, functools, os, time, shutil, multiprocessing
from multiprocessing.managers import BaseManager
import re
def sort_nicely( l ):
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
	l.sort( key=alphanum_key )


class MapSquare(object):
	
	def __init__(self, name, coordinates):
		self.name = name
		self.coordinates = coordinates
		self.count = multiprocessing.Value("i", 0)

class Building(object):
	
	def __init__(self, name, img, acmap):
		self.name = name
		self.img = img
		self.acmap = acmap
		self.count = multiprocessing.Value("i", 0)
		
class AMap(object):
	def __init__(self):
		self.a1 = MapSquare("a1", [409,163])
		self.a2 = MapSquare("a2", [464,163])
		self.a4 = MapSquare("a4", [573,163])
		self.a5 = MapSquare("a5", [628,163])
		self.squares = [self.a1, self.a2, self.a4, self.a5]

class FMap(object):
	def __init__(self):
		self.f1 = MapSquare("f1", [409, 441])
		self.f2 = MapSquare("f2", [464, 441])
		self.f3 = MapSquare("f3", [519, 441])
		self.f4 = MapSquare("f4", [574, 441])
		self.squares = [self.f1, self.f2, self.f3, self.f4]
	
class Map(object):
	def __init__(self):
		self.c1 = MapSquare("c1", [411, 275])
		self.c2 = MapSquare("c2", [466, 275])
		self.c3 = MapSquare("c3", [520, 275])
		self.c4 = MapSquare("c4", [575, 275])
		self.c5 = MapSquare("c5", [629, 275])
		
		self.d1 = MapSquare("d1", [411, 331])
		self.d2 = MapSquare("d2", [466, 331])
		self.d3 = MapSquare("d3", [520, 331])
		self.d4 = MapSquare("d4", [575, 331])
		self.d5 = MapSquare("d5", [629, 331])
		
		self.e1 = MapSquare("e1", [411, 387])
		self.e2 = MapSquare("e2", [466, 387])
		self.e3 = MapSquare("e3", [520, 387])
		self.e4 = MapSquare("e4", [575, 387])
		self.e5 = MapSquare("e5", [629, 387])
		
		self.squares = [self.c1, self.c2, self.c3, self.c4, self.c5, self.d1, self.d2, self.d3, self.d4, self.d5, self.e1, self.e2, self.e3, self.e4, self.e5]
		
class HouseMap(object):
	def __init__(self):
		self.b1 = MapSquare("b1", [411, 219])
		self.b2 = MapSquare("b2", [466, 219])
		self.b3 = MapSquare("b3", [520, 219])
		self.b4 = MapSquare("b4", [575, 219])
		self.b5 = MapSquare("b5", [629, 219])
		
		self.c1 = MapSquare("c1", [411, 275])
		self.c2 = MapSquare("c2", [466, 275])
		self.c3 = MapSquare("c3", [520, 275])
		self.c4 = MapSquare("c4", [575, 275])
		self.c5 = MapSquare("c5", [629, 275])
		
		self.d1 = MapSquare("d1", [411, 331])
		self.d2 = MapSquare("d2", [466, 331])
		self.d3 = MapSquare("d3", [520, 331])
		self.d4 = MapSquare("d4", [575, 331])
		self.d5 = MapSquare("d5", [629, 331])
		
		self.e1 = MapSquare("e1", [411, 387])
		self.e2 = MapSquare("e2", [466, 387])
		self.e3 = MapSquare("e3", [520, 387])
		self.e4 = MapSquare("e4", [575, 387])
		self.e5 = MapSquare("e5", [629, 387])
		
		self.f1 = MapSquare("f1", [411, 443])
		self.f2 = MapSquare("f2", [466, 443])
		self.f3 = MapSquare("f3", [520, 443])
		self.f4 = MapSquare("f4", [575, 443])
		self.f5 = MapSquare("f5", [629, 443])
		
		self.squares = [self.b1, self.b2, self.b3, self.b4, self.b5, self.c1, self.c2, self.c3, self.c4, self.c5, self.d1, self.d2, self.d3, self.d4, self.d5, self.e1, self.e2, self.e3, self.e4, self.e5, self.f1, self.f2, self.f3, self.f4, self.f5]

def rms(img1, img2):
	h = ImageChops.difference(img1, img2).histogram()
	return math.sqrt(functools.reduce(operator.add, map(lambda h, i: h*(i**2), h, range(256)))/(float(img1.size[0]) * img1.size[1]))

def do_work(file, shopImg, dumpImg, postImg, tailorImg, policeImg, fountainImg, museumImg, cliffImg, fileCount, twoLayers, threeLayers, directory, skip, possiblyDecentMaps, printStats):
	if file.endswith(".png"):
		fileCount.value += 1
		if fileCount.value <= skip:
			return
		im = Image.open(directory+file)
		layers = 1
		shop = 0
		post = 0
		fountain = 0
		housesOkay = True
		for building in buildings:
			lowestdiff = 100
			bestmatch = 0
			if building.name == "shop":
				buildingImg = shopImg
			elif building.name == "dump":
				buildingImg = dumpImg
			elif building.name == "post office":
				buildingImg = postImg
			elif building.name == "tailor":
				buildingImg = tailorImg
			elif building.name == "police station":
				buildingImg = policeImg
			elif building.name == "fountain":
				buildingImg = fountainImg
			elif building.name == "museum":
				buildingImg = museumImg
				
			for mapsquare in building.acmap.squares:
				region = im.crop((mapsquare.coordinates[0], mapsquare.coordinates[1], mapsquare.coordinates[0]+50, mapsquare.coordinates[1]+50))
				diff = rms(region, buildingImg)
				if diff < lowestdiff:
					lowestdiff = diff
					bestmatch = mapsquare
						
			bestmatch.count.value += 1
			building.count.value += 1
			if building.name == "shop":
				shop = bestmatch
			elif building.name == "post office":
				post = bestmatch
			elif building.name == "fountain":
				fountain = bestmatch
				
			if  bestmatch.name == "c2" or bestmatch.name == "c3" or bestmatch.name == "c4":
				print(str(file))
		
		for square in cliffSquares:
			region = im.crop((square.coordinates[0], square.coordinates[1], square.coordinates[0]+12, square.coordinates[1]+16))
			diff = rms(region, cliffImg)
			if diff < 20:
				layers += 1
				
		if layers == 2:
			twoLayers.value += 1
		elif layers == 3:
			threeLayers.value += 1
			
		c1 = False
		c5 = False
		belowShop = False
			
		for square in houseMap.squares:
			region = im.crop((square.coordinates[0], square.coordinates[1], square.coordinates[0]+54, square.coordinates[1]+56))
			colors = region.getcolors(maxcolors=1000)
			
			for color in colors:
				#blue house = (90, 90, 225, 255)	purple house = (145, 70, 205, 255)	yellow house = (170, 115, 20, 255)
				if color[1] == (90, 90, 225, 255) or color[1] == (145, 70, 205, 255) or color[1] == (170, 115, 20, 255):
						if "e" in square.name or "f" in square.name:
							housesOkay = False
						elif square.name == "d1" or square.name == "d5":
							housesOkay = False
						elif square.name == "c1":
							c1 = True
						elif square.name == "c5":
							c5 = True
						elif (shop.name == "a2" and square.name == "b2") or (shop.name == "a4" and square.name == "b4"):
							belowShop = True
		if c1 and c5:
			housesOkay = False
		elif belowShop == False:
			housesOkay = False
			
		if (housesOkay and ((shop.name == "a2" and post.name == "a4") or (shop.name == "a4" and post.name == "a2")) and not (fountain.name == "e1" or fountain.name == "e5" or (layers == 3 and "e" in fountain.name))):
			if not os.path.exists(directory+"maybe/"):
				os.makedirs(directory+"maybe/")
			shutil.copy(directory+file, directory+"maybe/"+file)
			possiblyDecentMaps.value += 1
			current.value = 0
		else:
			current.value += 1
			if current.value > most.value:
				most.value = current.value
		
def worker(fileCount, twoLayers, threeLayers, directory, skip, possiblyDecentMaps, printStats):
	shopImg = Image.open(shop.img)
	dumpImg = Image.open(dump.img)
	postImg = Image.open(postoffice.img)
	tailorImg = Image.open(tailor.img)
	policeImg = Image.open(policestation.img)
	fountainImg = Image.open(fountain.img)
	museumImg = Image.open(museum.img)
	cliffImg = Image.open(cliff)
	while True:
		file = q.get()
		do_work(file, shopImg, dumpImg, postImg, tailorImg, policeImg, fountainImg, museumImg, cliffImg, fileCount, twoLayers, threeLayers, directory, skip, possiblyDecentMaps, printStats)
		q.task_done()
	
if __name__ == "__main__":
	q = multiprocessing.JoinableQueue()
	fileCount = multiprocessing.Value("i", 0)
	twoLayers = multiprocessing.Value("i", 0)
	threeLayers = multiprocessing.Value("i", 0)
	directory = "./"
	skip = 0
	most = multiprocessing.Value("i", 0)
	current = multiprocessing.Value("i", 0)
	possiblyDecentMaps = multiprocessing.Value("i", 0)
	printStats = True
	numThreads = 1
	
	shop = Building("shop", "shop.png", AMap())
	dump = Building("dump", "dump.png", AMap())
	postoffice = Building("post office", "postoffice.png", AMap())
	tailor = Building("tailor", "tailor.png", FMap())
	policestation = Building("police station", "policestation.png", Map())
	fountain = Building("fountain", "fountain.png", Map())
	museum = Building("museum", "museum.png", Map())
	buildings = [shop, dump, postoffice, tailor, policestation, fountain, museum]

	cliff = "cliff.png"
	cliffSquares = [MapSquare("b1", [409, 249]), MapSquare("c1", [409, 305]), MapSquare("d1", [409, 361]), MapSquare("e1", [409, 417])]

	houseMap = HouseMap()
	
	startTime = time.time()
		
	if len(sys.argv) > 1:
		directory = sys.argv[1]
	if len(sys.argv) > 2:
		skip = int(sys.argv[2])
	if len(sys.argv) > 3:
		numThreads = int(sys.argv[3])
	if len(sys.argv) > 4:
		printStats = sys.argv[4]
	
	jobs = []
	for i in range(numThreads):
		p = multiprocessing.Process(target=worker, args=(fileCount, twoLayers, threeLayers, directory, skip, possiblyDecentMaps, printStats))
		p.daemon = True
		jobs.append(p)
		p.start()
	
	if printStats == 0 or printStats == "0" or printStats == "false":
		printStats = False
		
	files = os.listdir(directory)
	sort_nicely(files)
	
	for file in files:
		q.put(file)
	
	q.join()
	
	if printStats:				
		print("two layers:\t"+str(twoLayers.value)+"\t"+str((twoLayers.value/(fileCount.value-skip))*100)+"%")
		print("three layers:\t"+str(threeLayers.value)+"\t"+str((threeLayers.value/(fileCount.value-skip))*100)+"%")
		
		for building in buildings:
			print(str("\n"+building.name))
			for mapsquare in building.acmap.squares:
						print("\t"+str(mapsquare.name)+":\t"+str(mapsquare.count.value)+"\t"+str((mapsquare.count.value/(fileCount.value-skip))*100)+"%")	
		print("\nmaps: "+str((fileCount.value-skip)))
		print("possibly decent maps: "+str(possiblyDecentMaps.value))
		print("Longest bad streak: " +str(most.value))
		print("elapsed time: "+str(time.time()-startTime)+" seconds")
