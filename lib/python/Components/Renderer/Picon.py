##
## Picon renderer by Gruffy .. some speedups by Ghost
##
from Renderer import Renderer
from enigma import ePixmap
from Tools.Directories import pathExists, fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename

class Picon(Renderer):
	searchPaths = ('/usr/share/enigma2/picon/',
				'/picon/',
				'/media/cf/picon/',
				'/media/mmc1/picon/',
				'/media/usb/picon/')

	def __init__(self):
		Renderer.__init__(self)
		if pathExists('/media/hdd/picon'):
			self.searchPaths = self.searchPaths + ('/media/hdd/picon/',)
		self.pngname = ""
		self.lastPath = None
	#	pngname = self.findPicon("picon_default")
	#	if not pngname:
	#		tmp = resolveFilename(SCOPE_CURRENT_SKIN, "picon_default.png")
	#		if fileExists(tmp):
	#			pngname = tmp
	#		else:
	#			pngname = resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/picon_default.png")
		self.defaultpngname = ""

	def applySkin(self, desktop, parent):
		attribs = [ ]
		for (attrib, value) in self.skinAttributes:
			if attrib == "path":
				self.path = value
			else:
				attribs.append((attrib,value))
		self.skinAttributes = attribs
		return Renderer.applySkin(self, desktop, parent)

	GUI_WIDGET = ePixmap

	def changed(self, what):
		if self.instance:
			pngname = ""
			if what[0] != self.CHANGED_CLEAR:
				sname = self.source.text
				# strip all after last :
				pos = sname.rfind(':')
				if pos != -1:
					sname = sname[:pos].rstrip(':').replace(':','_')
				pngname = self.findPicon(sname)
				if not pngname:
					fields = sname.split('_', 3)
					if len(fields) > 2 and fields[2] != '2':
						#fallback to 1 for tv services with nonstandard servicetypes
						fields[2] = '1'
						pngname = self.findPicon('_'.join(fields))
			if not pngname: # no picon for service found
				pngname = self.defaultpngname
			if self.pngname != pngname:
				self.instance.setScale(1)
				self.instance.setPixmapFromFile(pngname)
				self.pngname = pngname

	def findPicon(self, serviceName):
		if self.lastPath:
			pngname = self.lastPath + serviceName + ".png"
			if fileExists(pngname):
				return pngname
		for path in self.searchPaths:
			if pathExists(path):
				pngname = path + serviceName + ".png"
				if fileExists(pngname):
					self.lastPath = path
					return pngname
		return ""
