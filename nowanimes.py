#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,string

import urlresolver
from BeautifulSoup import BeautifulSoup



pluginhandle = int(sys.argv[1])

#padrao   (\W\d+;),(\W\w+;),,(\W\w+;),,,,(\W\w+\W),,numeros(\W+\d+\W+)ou (\W+\d+;)
versao = '0.0.1'
addon_base = 'Nowanimes'
addon_id = 'plugin.video.nowanimes'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.jpg'
icones = addonfolder + '/icon.png'

base = 'https://nowanimes.com/'
refpass = '%s|referer=https://nowanimes.com/'
base_search = 'https://nowanimes.com/?s=%s&tipo=video'
players = 'https://trueliketop.org/play/blogger.php?%s'

############################################################################################################
#                                           MENU ADDON                                                 
############################################################################################################

def CATEGORIES():
	addDir('[COLOR blue]Pesquisar[/COLOR]','-',40,artfolder + 'Dublados.png')
	link  = abrir_url(base)
	texto = re.findall('class="cat-item cat-item-2">(.+?)</div>',link,re.DOTALL)[0]
	match = re.compile('href="(.*?)">(.*?)</a>').findall(texto)
	for url, name in match:
		addDir('[COLOR blue]%s[/COLOR]'%name,url,1,'')

	setViewMenu()	
	
###################################################################################
def subcategorias(url,name):
	link  = abrir_url(url)
	texto = re.findall('class="lista-filmes">(.+?)class="navigation open-sans">',link,re.DOTALL)[0]
	match = re.compile('href="(.*?)".*?<img src="(.*?)".*?alt="(.*?)"').findall(texto)
	for url, img, name in match:
		addDir('[COLOR blue]%s[/COLOR]'%name,url,2,img)
	try:
		match = re.compile('href="(.*?)">(.*?)</a>').findall(link)
		for url,ref in match:
			if '&raquo;' in ref:
				addDir('[COLOR green]Próxima Página[/COLOR]',url,3,'')
	except:pass

	setViewMenu()	


###################################################################################
#FUNCOES
'''
	    link  = abrir_url(url)		
		soup = BeautifulSoup(link)
		match = soup.findAll("div", {"id" : "content"})
	for teste in match:
		url = teste.a["href"]
		img = teste.img["src"]	
		name = teste.a["alt"].replace('Assistir ','')
		addDir(name,url,3,img)'''

############################################################################################################
#                                           OPEN SETINGS                                                
############################################################################################################	
def Addon_Settings():
    selfAddon.openSettings(sys.argv[0])

	
############################################################################################################
#                                           GENEROS                                                
############################################################################################################		

#########################################################################################################			
def pesquisa(url):
		keyb = xbmc.Keyboard('', 'Pesquisar')
		keyb.doModal()

		if (keyb.isConfirmed()):
				texto    = keyb.getText()
				pesquisa = urllib.quote(texto)
				url      = base_search % str(pesquisa)
				url_pesquisa(url)
###########################################################################################################				
def url_pesquisa(url):
	link  = abrir_url(url)
	texto = re.findall('class="lista-filmes">(.+?)class="navigation open-sans">',link,re.DOTALL)[0]
	match = re.compile('href="(.*?)".*?<img src="(.*?)".*?alt="(.*?)"').findall(texto)
	for url, img, name in match:
		if not 'Calendário' in name:
			addDir('[COLOR blue]%s[/COLOR]'%name,url,2,img)

	setViewMenu()	

############################################################################################################
def lista_urls(url):
	nam = []
	link  = abrir_url(url)
	texto = re.findall('<div class="check_lista lista_personalizada">(.+?)<div class="clear">',link,re.DOTALL)[0]
	ur = re.compile('href="(.*?)"').findall(texto)
	if len(ur) < 1:
		ur = re.compile('href="(.+)\s"').findall(texto)
	nam1 = re.compile('title="(.*?)".*?>(.*?)</a>').findall(texto)
	for i in nam1:
		a,b = i
		if not re.compile('\d').findall(a):
			nam.append(a+' '+b)
		else:
			nam.append(a)
	match = list(zip(ur,nam))
	for url,name in match:
		addDir('[COLOR blue]%s[/COLOR]'%name,url,4,iconimage)
	
	setViewMenu()

##############################################################################################################
def resurls(url,name,iconimage):
	ur = url.split('?')[1].replace('amp;','').replace('#038;','');url = players % ur
	link = abrir_url(url)
	texto = re.findall('<div class="itens">(.+?)</div>',link,re.DOTALL)[0].replace("'","")
	match = re.compile('href=(.*?)".*?</span></span>(.*?)</a>').findall(texto)
	url = []
	for i in match:
		a,b = i
		url.append({b:a})
	player(name,url,iconimage)

##############################################################################################################
def nextpage(url):
	link  = abrir_url(url)
	texto = re.findall('class="lista-filmes">(.+?)class="navigation open-sans">',link,re.DOTALL)[0]
	match = re.compile('href="(.*?)".*?<img src="(.*?)".*?alt="(.*?)"').findall(texto)
	for url, img, name in match:
		addDir('[COLOR blue]%s[/COLOR]'%name,url,2,img)
	try:
		match = re.compile('href="(.*?)">(.*?)</a>').findall(link)
		for url,ref in match:
			if '&raquo;' in ref:
				addDir('[COLOR green]Próxima Página[/COLOR]',url,3,'')
	except:pass

	setViewMenu()	
###################################################################################
from unicodedata import normalize

def remover_acentos(txt, codif='utf-8'):
	return normalize('NFKD', txt.decode(codif)).encode('ASCII', 'ignore')
##############################################################################################################
def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l

############################################################################################################
def resolvendo(y,keys,x,ns):
	try:
		new = re.sub(keys[0],x.get(keys[0]),str(y))
	except:
		new = re.sub(keys[0],keys[0],str(y))
	del(keys[0])
	if len(keys) == 0:
		ns.append(new)
		if '"' in ns[0]:
			return re.compile("'([A-Z].*?\W)'").findall(ns[0].replace('"',"'").replace(' - ',' '))
		else:
			return re.compile("'(.*?)'").findall(ns[0])
	resolvendo(new,keys,x,ns)
	return re.compile("'(.*?)'").findall(ns[0].replace('"',"'").replace(' - ',' '))
        
def decor(y):
	ns = []
	x = {'&Aacute;':'Á','&aacute;':'á','&Acirc;':'Â','&acirc;':'â','&Agrave;':'À','&agrave;':'à','&Aring;':'Å','&aring;':'å','&Atilde;':'Ã','&atilde;':'ã','&Auml;':'Ä','&auml;':'ä','&AElig;':'Æ','&aelig;':'æ','&Eacute;':'É','&eacute;':'é','&Ecirc;':'Ê','&ecirc;':'ê','&Egrave;':'È','&egrave;':'è','&Euml;':'Ë','&euml;':'ë','&ETH;':'Ð','&eth;':'ð','&Iacute;':'Í','&iacute;':'í','&Icirc;':'Î','&icirc;':'î','&Igrave;':'Ì','&igrave;':'ì','&Iuml;':'Ï','&iuml;':'ï','&Oacute;':'Ó','&oacute;':'ó','&Ocirc;':'Ô','&ocirc;':'ô','&Ograve;':'Ò','&ograve;':'ò','&Oslash;':'Ø','&oslash;':'ø','&Otilde;':'Õ','&otilde;':'õ','&Ouml;':'Ö','&ouml;':'ö','&Uacute;':'Ú','&uacute;':'ú','&Ucirc;':'Û','&ucirc;':'û','&Ugrave;':'Ù','&ugrave;':'ù','&Uuml;':'Ü','&uuml;':'ü','&Ccedil;':'Ç','&ccedil;':'ç','&Ntilde;':'Ñ','&ntilde;':'ñ','&lt;':'<','&gt;':'>','&amp;':'&','&quot;':'"','&reg;':'®','&copy;':'©','&Yacute;':'Ý','&yacute;':'ý','&THORN;':'Þ','&thorn;':'þ','&szlig;':'ß','&ndash;':'-','&acute;':'D´','&acirc;':'â','&Acirc;':'Â','&ldquo;':'`','&rdquo;':'`','&ordf;':'ª','&nbsp;':'-','&rsquo;':"´",'&sup2;':'²'}
	z = re.compile('&.*?;').findall(str(y))
	keys = remove_repetidos(z)
	if len(keys) < 1:
		return y
	else:
		w = resolvendo(y,keys,x,ns)
		return w
###########################################
def getRegexAll(text, start_with, end_with):
		r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
		
		return r

def getRegex(text, from_string, to_string, excluding=True):
		if excluding:
				try    : r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
				except : r = ''
		else:
				try    : r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
				except : r = ''
				
		return r
		

def player(name,url,iconimage):
		OK = False
		
		nome = name
		msgDP= xbmcgui.DialogProgress()
		
		msgDP.create('NOWANIMES', 'Obtendo Fontes Para ' + name, 'Por favor aguarde...')
		msgDP.update(25)
		
		nServers = []
		uServers = []
		matriz = []
		
		servers = url
		
		for i in servers :
			for server in i:
				ns = server
				ns1 = server
				if len(ns) > 1 :
						nServers.append(ns1.upper())
						uServers.append(i[server])
		
		if not nServers : return
		
		index = xbmcgui.Dialog().select('Selecione uma das fontes suportadas :', nServers)
		
		if index == -1 : return
		
		msgDP.update(50, 'Resolvendo fonte Para ' + name, 'Por favor aguarde...')
		
		url2Resolve = uServers[index]
		legendas = '-'
		
		if 'trueliketop' in url2Resolve :
				link = abrir_url(url2Resolve)
				try:
					link = re.compile('file: "(.*?)"').findall(link)[0]
				except:
					link = re.compile('source src="(.*?)"').findall(link)[0]
				if 'videozin' in link:
					link = link.replace('?','blogger.php?')
				else:
					if  'z=' in url2Resolve:
						import requests
						try:
							link1 = requests.get(url2Resolve);link1 = link1.headers['Set-Cookie'];link1 = re.compile("\w+=.+?\w+").findall(link1)[0]
						except:
							link1 = requests.get(url2Resolve);link1 = link1.headers['Set-Cookie'];link1 = re.compile("\w+=.+?\w+").findall(link1)[0]
						headers = {'cookie': link1,'referer': base}
						try:
							r = requests.get(link, headers = headers, timeout=0.250)
						except:
							pass
				urlV = refpass%link
				linkVT = urlV
				url2Play = linkVT
				OK = True
		if 'videozin' in url2Resolve :
				print url2Resolve
				link = abrir_url(url2Resolve)
				link = re.compile('iframe.*?src="(.*?)"').findall(link)[0]
				link = abrir_url(link)
				link = re.compile('play_url":"(.*?)"').findall(link)[0].replace('\u003d','=').replace('\u0026','&')
				linkVT = link
				url2Play = linkVT
				
				OK = True
				
		if not OK : url2Play = urlresolver.HostedMediaFile(url2Resolve).resolve()

		msgDP.update(75,'Abrindo Sinal Para ' + nome, 'Por favor aguarde...')
		
		playlist = xbmc.PlayList(1)
		playlist.clear()
		
		listitem = xbmcgui.ListItem(name,thumbnailImage=iconimage)
		
		listitem.setPath(url2Play)
		
		listitem.setProperty('mimetype','video/mp4')
		listitem.setProperty('IsPlayable', 'true')
		
		playlist.add(url2Play,listitem)
		
		xbmcPlayer = xbmc.Player()
		xbmcPlayer.play(playlist)

		msgDP.update(100)
		msgDP.close()
		
		if legendas != '-' : xbmcPlayer.setSubtitles(legendas)
############################################################################################################
#                                           FUNÇOES FEITAS                                                 #
############################################################################################################		
def setViewMenu() :
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		
		opcao = selfAddon.getSetting('menuVisu')
		
		if   opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
		elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
		elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
		
def setViewFilmes() :
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')

		opcao = selfAddon.getSetting('filmesVisu')

		if   opcao == '0': xbmc.executebuiltin("Container.SetViewMode(50)")
		elif opcao == '1': xbmc.executebuiltin("Container.SetViewMode(51)")
		elif opcao == '2': xbmc.executebuiltin("Container.SetViewMode(500)")
		elif opcao == '3': xbmc.executebuiltin("Container.SetViewMode(501)")
		elif opcao == '4': xbmc.executebuiltin("Container.SetViewMode(508)")
		elif opcao == '5': xbmc.executebuiltin("Container.SetViewMode(504)")
		elif opcao == '6': xbmc.executebuiltin("Container.SetViewMode(503)")
		elif opcao == '7': xbmc.executebuiltin("Container.SetViewMode(515)")
		
		
def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link



def addDir(name,url,mode,iconimage,pasta=True,total=1,plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo( type="video", infoLabels={ "title": name, "plot": plot } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok


def CheckUpdate():

	Versao = '20.10.2020'

	uversao = urllib2.urlopen("https://raw.githubusercontent.com/setokaiba3/meu_addon/main/versao.txt").read().replace('','').replace('','')

	uversao = re.compile('[a-zA-Z\.\d]+').findall(uversao)[0]

	if uversao != Versao:

		Update()

		

def Update():

	Path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path') ).decode("utf-8");print Path

	try:

		fonte = urllib2.urlopen("https://raw.githubusercontent.com/setokaiba3/meu_addon/main/nowanimes.py").read()

		prog = re.compile('.+').findall(fonte)

		if prog:

			py = os.path.join(Path, "nowanimes.py")

			file = open(py, "w")

			file.write(fonte)

			file.close()

	except:

		xbmcgui.Dialog().ok(addonfolder, "[COLOR white][B]Não foi possível atualizar no momento, tente mais tarde.[/COLOR][/B]")
############################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################
              
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

      
params=get_params()
url=None
name=None
mode=None
iconimage=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)



###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

if mode==None or url==None or len(url)<1:
        CheckUpdate()
        CATEGORIES()

elif mode==1: subcategorias(url,name)
elif mode==2: lista_urls(url)
elif mode==3: nextpage(url)
elif mode==4: resurls(url,name,iconimage)
###########################         listar videos

###########################             OPEN SETINGS
elif mode==40: pesquisa(url)
elif mode==80: Addon_Settings()

#########################################          
###########################             player
elif mode==96: player(name,url,iconimage)

#########################################          FIM
xbmcplugin.endOfDirectory(int(sys.argv[1]))
