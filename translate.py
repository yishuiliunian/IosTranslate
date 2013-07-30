import os
import sys
import getopt
import pdb
import codecs
def sortedDict(dic):
	keys = dic.keys()
 	keys.sort()
	print keys
	m = {}
	for key in keys:
		m[key] = dic[key]
		pass
	return m

def ensurePathExist(path):
    if not os.path.exists(path):
        os.mkdir(path)
usr_home = '~'
def AppDataPath():
    global usr_home
    if usr_home == '~':
        usr_home = os.path.expanduser('~')
    return usr_home

def pathJoin(parentPath,subPath):
    if parentPath.endswith('/'):
		return parentPath + subPath
    else:
    	return parentPath + '/' + subPath


NeedStripKey = ['\n',' ',';', ' ','[', ' ', ']', ' ','"',' ', '\'', ' ']

def cleanSentence(sentence):
	for key in NeedStripKey:
		sentence = sentence.lstrip(key)
		sentence = sentence.rstrip(key)
		pass
	return sentence 

def splitPair(pair, splitkey):
	if len(pair) == 0:
		return None, None
	strs = pair.split(splitkey)
	if len(strs) != 2:
		return None, None
	en = strs[0]
	tr = strs[1]

	en = cleanSentence(en)
	tr = cleanSentence(tr)
	return en, tr
	

def splitTranslatePair(pair):
 	return splitPair(pair, '=')



class AimModel:
	def __init__(self, name, data):
		self.name = name
		pairs = data.split(',')
		self.aimfiles = []
		self.dicfile = ''
		self.needtrfile = ''
		for pair in pairs:
			key, value = splitPair(pair, ':')
			if key == 'aim':
				self.aimfiles.append(value)
				pass
			elif key == 'dic':
				self.dicfile = value
				pass
			elif key == 'needtr':
				self.needtrfile = value
				pass
			else:
				pass
			pass
		pass


def genstrings(path, outfilepath):
	for i in os.listdir(path):
		subPath = pathJoin(path, i)
		if os.path.isdir(subPath):
			genstrings(subPath , outfilepath)
			pass
		elif i.endswith('.m') or i.endswith('.mm') or i.endswith('.h'):
			cmdstr = 'genstrings -a -o ' + outfilepath + ' ' + subPath
			os.system(cmdstr)
			pass
		pass
	pass

def loadTranslateDicFromFile(filePath):
	for encode in ['utf8', 'utf16']:
		try:
			trFile = codecs.open(filePath, 'r' , encode)
			englistDic = {}
			for pair in trFile.readlines():
				en , tr = splitTranslatePair(pair)
				if en is not None and tr is not None:
					englistDic[en] = tr
					pass
				pass
			trFile.close()
			print encode
			return englistDic
		except UnicodeError:
			continue
		except :
			pass
	return {}


def copyMap(m):
	copym = {}
	for key in m.keys():
		copym[key] = m[key]
		pass
	return copym

def writeMapToFile(m ,filepath):
	f = codecs.open(filepath, 'w','utf16')
	keys = m.keys()
	keys.sort()
	for key in keys:
		print m[key]
		f.write('"' + key + '"="' + m[key] + '";\n')
	f.close()

def initData(sourcepath):
	tempEnglishPath = pathJoin(AppDataPath(), '.translatetemp') 
	ensurePathExist(tempEnglishPath)
	genstrings(sourcepath, tempEnglishPath)
	tmpEnFile = pathJoin(tempEnglishPath, 'Localizable.strings')
	sourceDic = loadTranslateDicFromFile(tmpEnFile)
	return sourceDic 


def translateStrings(aim, sourceDic , trDic):
	resultDic = copyMap(sourceDic)
	needTrDic = {}
	for key in resultDic.keys():
		if key in trDic:
			resultDic[key] = trDic[key]
		else:
			needTrDic[key] = key
			pass
		pass
	for path in aim.aimfiles:
		writeMapToFile(resultDic, path)
		pass
	pdb.set_trace()
	if len(needTrDic):
		writeMapToFile(needTrDic, aim.needtrfile)
		


def usage():
	print 'Error Opts:'
	sys.exit(0)
if __name__ == "__main__":
	#	try:
		opts, args = getopt.getopt(sys.argv[1:], 's:h', ['setfile=', 'help'])
		setfilepath = None
		for o,a in opts:
			if o in ('-h', '--help'):
				usage()
				pass
			elif o in ('-s', '--setfile'):
				setfilepath = a
				pass
			elif True:
				usage()
			pass
		if setfilepath is None:
			usage()
			pass
		else:
			setfile = open(setfilepath, 'r')
			sourcesPath = None
			trLanguages = []
			aimsMap = {}
			for line in setfile.readlines():
				key, value = splitPair(line, '=') 
				if key == 'NEEDTRANSLATION':
					strs = value.split(',')
					for s in strs:
						trLanguages.append(cleanSentence(s))
						pass
					pass
				elif key == 'SOURCESPATH':
					sourcesPath = value
				elif True:
					aimsMap[key] = AimModel(key, value)
					pass
				pass
			print sourcesPath
			sourceDic = initData(sourcesPath)
			print sourceDic
			print trLanguages
			print aimsMap
			for key in aimsMap.keys():
				aim = aimsMap[key]
				trDic = sourceDic
				if key != 'en':
					trDic = loadTranslateDicFromFile(aim.dicfile)
					pass
				translateStrings(aim, sourceDic, trDic)
				pass
			pass
		pass
	#except:
		pass

