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



import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,string,base64,os



import urlresolver

from BeautifulSoup import BeautifulSoup







pluginhandle = int(sys.argv[1])



#padrao   (\W\d+;),(\W\w+;),,(\W\w+;),,,,(\W\w+\W),,numeros(\W+\d+\W+)ou (\W+\d+;)

versao = '0.0.1'

addon_base = 'Redecanais'

addon_id = 'plugin.video.redecanais'

selfAddon = xbmcaddon.Addon(id=addon_id)

addonfolder = selfAddon.getAddonInfo('path')

artfolder = addonfolder + '/resources/img/'

fanart = addonfolder + '/fanart.jpg'

icones = addonfolder + '/icon.png'



base = 'https://redecanais.bz/browse-%s-%s-videos-1-date.html'

base1 = 'https://redecanais.bz/'

base_search = 'https://www.google.com/search?q=%s+site:redecanais.ws&hl=pt-BR'

base_search1 = 'https://www.google.com'

JPG = '/imgs-videos/%s/%s Capa.jpg'

ref = '|referer=https://canaismax.com/'



############################################################################################################

#                                           MENU ADDON                                                 

############################################################################################################



def CATEGORIES():

	addDir('[COLOR blue]Canais[/COLOR]','https://canaismax.com/tvaovivo/',10,artfolder + 'filmes.jpg')

	addDir('[COLOR blue]Filmes[/COLOR]',base,1,artfolder + 'filmes.jpg')

	addDir('[COLOR blue]Animes[/COLOR]',base,1,artfolder + 'animes.png')

	addDir('[COLOR blue]Desenhos[/COLOR]',base,1,artfolder + 'cartoons.jpg')

	addDir('[COLOR blue]Series[/COLOR]',base,1,artfolder + 'series.jpg')

	addDir('[COLOR blue]Novelas[/COLOR]',base,1,artfolder + 'novelas.jpeg')

	addDir('[COLOR blue]Pesquisar[/COLOR]','-',40,artfolder + 'pesquisar.jpg')

	setViewMenu()	

	

###################################################################################

def subcategorias(url,name):

	name = name.replace('[COLOR blue]','').replace('[/COLOR]','').lower()

	if 'filmes' in name:

		cat = ['Lançamentos','Dublado','Legendado','Nacional']

		for i in cat:

			i1 = remover_acentos(i).lower()

			addDir('[COLOR blue]%s[/COLOR]'%i,url%(name,i1),2,artfolder + 'artes.jpg')

	else:

		letras = list(string.ascii_uppercase);letras.insert(0, "#")

		for i in letras:

			if '#' in i:

				i1 = i.replace('#','numerosesimbolos')

			else:

				i1 = 'letra-'+i.lower()

			addDir('[COLOR blue]%s[/COLOR]'%i,url%(i1,name),5,artfolder + 'artes.jpg')





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

		keyb = xbmc.Keyboard('', 'Pesquisar Filmes')

		keyb.doModal()



		if (keyb.isConfirmed()):

				texto    = keyb.getText()

				pesquisa = urllib.quote(texto)

				url      = base_search % str(pesquisa)

                                print url				

				url_pesquisa(url,texto)

###########################################################################################################				

def url_pesquisa(url,name1):

	link  = abrir_url(url)

	nome = re.compile('<span class="CVA68e qXLe6d">(.*?)</span>  <span class="qXLe6d dXDvrc">').findall(link)

	ur = re.compile('class="fuLhoc ZWRArf" href="(.*?)&amp;').findall(link)

	texto = list(zip(ur,nome))

	for url,name in texto:

		if 'html' in url or 'php' in url:

			if 'url?q=' in url:

				if not 'google' in url:

					url = re.compile('url.q=(.+)').findall(url)[0]

					url = urllib.unquote(url)

					name = re.sub('\s\W\s\w+.\w+$','',name)

					addDir('[COLOR blue]%s[/COLOR]'%name,url,6,iconimage)

	try:

		url = re.compile('class="frGj1b" href="(.*?)"').findall(link)[0].replace('amp;','')

		addDir('[COLOR green]Próxima Página[/COLOR]',base_search1+url,7,iconimage)

	except:pass



	setViewMenu()



############################################################################################################

def respesquisar(url):

	nun = 'start='+str(int(re.compile('start=(\d+)').findall(url)[0])+10)

	ur = re.sub('start=(\d+)',nun,url)

	link  = abrir_url(url)

	nome = re.compile('<span class="CVA68e qXLe6d">(.*?)</span>  <span class="qXLe6d dXDvrc">').findall(link)

	ur1 = re.compile('class="fuLhoc ZWRArf" href="(.*?)&amp;').findall(link)

	texto = list(zip(ur1,nome))

	for url,name in texto:

		if 'html' in url or 'php' in url:

			if 'url?q=' in url:

				if not 'google' in url:

					url = re.compile('url.q=(.+)').findall(url)[0]

					url = urllib.unquote(url)

					name = re.sub('\s\W\s\w+.\w+$','',name)

					addDir('[COLOR blue]%s[/COLOR]'%name,url,6,iconimage)

	try:

		url = ur

		addDir('[COLOR green]Próxima Página[/COLOR]',url,7,iconimage)

	except:pass



	setViewMenu()



############################################################################################################

def lista_urls(url):

	link  = abrir_url(url)

	texto = re.findall('<ul class="row pm-ul-browse-videos list-unstyled"(.+?)list-unstyled',link,re.DOTALL)[0]

	match = re.compile('href="(.*?)" title="(.*?)">\s.*?\s.*?\s.*?data-echo="(.*?)"').findall(texto)

	for url, name, img in match:

		addDir('[COLOR blue]%s[/COLOR]'%name,base1+url,4,base1+img)

	try:

		match = re.compile('href="(.*?)">(.*?)</a>').findall(link)

		for url,ref in match:

			if '&raquo;' in ref:

				addDir('[COLOR green]Próxima Página[/COLOR]',base1+url,3,iconimage)

	except:pass

	

	setViewMenu()

##############################################################################################################

def seriesurls(url):

	url1 = url

	n = []

	link  = abrir_url(url)

	texto = re.findall('pm-category-description(.+?)</div>',link,re.DOTALL)[0]

	ur = re.compile('href="(.*?)"').findall(texto)

	match = re.compile('>(.*?) - .*?href="(.*?)"').findall(texto)

	for i,i1 in match:

		if not 'strong' in i:

			n.append(i.replace("'","`"))

		else:

			n.append(re.compile('/>(.+)').findall(i.replace("'","`"))[0])

	n = decor(n)

	match = list(zip(n,ur))

	jpg = re.compile('(\w+)\W\w+\W\d').findall(url)[0]

	for name,url in match:

		img = base1+JPG % (jpg,name);img = resimg(img,url1)

		addDir('[COLOR blue]%s[/COLOR]'%name.replace("'",''),base1+url,4,img)

##############################################################################################################

def resimg(x,y):

	x = re.sub('\s\W.+\W\s',' ',x);x = x.replace('&','e').replace('à','a').replace('animes','Legado').replace('Animes','Legado')

	if 'animes' in y:

		return x.replace(' Capa','')

	return x

##############################################################################################################

def resurls(url,name,iconimage):

	nam = []

	ur = []

	link  = abrir_url(url)

	if 'iframe name' in link:

		resplayer(url,name,iconimage)

	else:

		link = abrir_url(url)

		try:

			texto = re.findall('<p><img(.*?)</div',link,re.DOTALL)[0].replace('</p>','<br')

		except:

			nextpage(url)

			return

		img = re.compile('src="(.*?)"').findall(texto)[0]

		id = re.compile('<strong>(.*?)</a><br').findall(texto)

		if len(id) == 0:

			id = re.compile('<strong>(.*?)</a></strong><br').findall(texto)

		for i in id:

			i = i.replace(' - ','').replace('Assistir','')

			if '&ordf;' in i:

				temporadas = re.compile('(\d+&ordf;.+?)<').findall(i)[0]

			try:

				if '&ordf;' in i:

					tt0 = i;tt = re.sub('<.+?>',' ',tt0);tt = re.sub('\s+',' ',tt)

				else:

					tt0 = temporadas+' '+i;tt = re.sub('<.+?>',' ',tt0);tt = re.sub('\s+',' ',tt)

			except:

				tt0 = i;tt = re.sub('<.+?>',' ',tt0);tt = re.sub('\s+',' ',tt)

			if 'Dub' in tt:

				nam.append(re.sub('\s/.+','',tt))

				ur.append(re.compile('href="(.*?)"').findall(tt0)[0])

			if 'Leg' in tt:

				nam.append(re.sub('\s\w+\s/','',tt))

				try:

					ur.append(re.compile('href="(.*?)"').findall(tt0)[1])

				except:

					ur.append(re.compile('href="(.*?)"').findall(tt0)[0])

			else:

				nam.append(tt)

				ur.append(re.compile('href="(.*?)"').findall(tt0)[0])

	try:

		nam = decor(nam)

	except:pass

	match = list(zip(nam,ur))

	for name,url in match:

		addDir('[COLOR blue]%s[/COLOR]'%name.replace("'",""),base1+url,6,base1+img)



##############################################################################################################

def next_pesquisa(url,name,iconimage):

	if not 'date' in url:

		resurls(url,name,iconimage)



##############################################################################################################

def nextpage(url):

	link  = abrir_url(url)

	texto = re.findall('<ul class="row pm-ul-browse-videos list-unstyled"(.+?)list-unstyled',link,re.DOTALL)[0]

	match = re.compile('href="(.*?)" title="(.*?)">\s.*?\s.*?\s.*?data-echo="(.*?)"').findall(texto)

	if len(match) < 1:

		url = re.compile('href="(.*?)" title').findall(texto)[::2]

		nome = re.compile('href=".*?title="(.*?)"').findall(texto)[::2]

		img = re.compile('data-echo="(.*?)"').findall(texto)

		match = list(zip(url,nome,img))

	for url, name, img in match:

		addDir('[COLOR blue]%s[/COLOR]'%name,base1+url,4,base1+img)

	try:

		match = re.compile('href="(.*?)">(.*?)</a>').findall(link)

		for url,ref in match:

			if '&raquo;' in ref:

				addDir('[COLOR green]Próxima Página[/COLOR]',base1+url,3,iconimage)

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

		return re.compile("'(.*?)'").findall(ns[0])

	del(keys[0])

	if len(keys) == 0:

		ns.append(new)

	resolvendo(new,keys,x,ns)

	return re.compile("'(.*?)'").findall(ns[0])

        

def decor(y):

	ns = []

	x = {'&Aacute;':'Á','&aacute;':'á','&Acirc;':'Â','&acirc;':'â','&Agrave;':'À','&agrave;':'à','&Aring;':'Å','&aring;':'å','&Atilde;':'Ã','&atilde;':'ã','&Auml;':'Ä','&auml;':'ä','&AElig;':'Æ','&aelig;':'æ','&Eacute;':'É','&eacute;':'é','&Ecirc;':'Ê','&ecirc;':'ê','&Egrave;':'È','&egrave;':'è','&Euml;':'Ë','&euml;':'ë','&ETH;':'Ð','&eth;':'ð','&Iacute;':'Í','&iacute;':'í','&Icirc;':'Î','&icirc;':'î','&Igrave;':'Ì','&igrave;':'ì','&Iuml;':'Ï','&iuml;':'ï','&Oacute;':'Ó','&oacute;':'ó','&Ocirc;':'Ô','&ocirc;':'ô','&Ograve;':'Ò','&ograve;':'ò','&Oslash;':'Ø','&oslash;':'ø','&Otilde;':'Õ','&otilde;':'õ','&Ouml;':'Ö','&ouml;':'ö','&Uacute;':'Ú','&uacute;':'ú','&Ucirc;':'Û','&ucirc;':'û','&Ugrave;':'Ù','&ugrave;':'ù','&Uuml;':'Ü','&uuml;':'ü','&Ccedil;':'Ç','&ccedil;':'ç','&Ntilde;':'Ñ','&ntilde;':'ñ','&lt;':'<','&gt;':'>','&amp;':'&','&quot;':'"','&reg;':'®','&copy;':'©','&Yacute;':'Ý','&yacute;':'ý','&THORN;':'Þ','&thorn;':'þ','&szlig;':'ß','&ndash;':'-','&acute;':'D´','&acirc;':'â','&Acirc;':'Â','&ldquo;':'`','&rdquo;':'`','&ordf;':'ª','&nbsp;':'-','&rsquo;':"´",'&sup2;':'²','&sup3;':'³'}

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



def resplayer(url,name,iconimage):

	try:

		link = abrir_url(url)

		ur = re.compile('iframe.*?src="(.*?)"').findall(link)[0];url = server(ur)

		player(name,url,iconimage)

	except:

		resurls(url,name,iconimage)

	

def server(url):

	server1 = 'https://proxy.ec.cx/video.php?url='

	try:

		if not '&' in url:

			vid = re.compile('vid=(.+)').findall(url)[0]

		else:

			vid = re.compile('vid=(.+?)&').findall(url)[0]

	except:

		vid = re.compile('vid=(.+)').findall(url)[0]

	server = re.compile('server(.*?).php').findall(url)[0].replace('http2','').replace('http','')

	if re.compile('\D').findall(server):

		char = re.compile('\D+').findall(server)[0]

		try:

			dig = re.compile('\d+').findall(server)[0]

		except:

			dig = 1

		ur = server1+'RC%sServer%s/ondemand/%s.mp4?attachment=true'%(char,dig,vid)

		ur1 = server1+'RC%sServer%s/videos/%s.mp4?attachment=true'%(char,dig,vid)

		url = valide(ur,ur1)

		return url

	else:

		if int(server) < 10:

			ur = server1+'RCServer0%s/ondemand/%s.mp4?attachment=true'%(server,vid)

			ur1 = server1+'RCServer0%s/videos/%s.mp4?attachment=true'%(server,vid)

			url = valide(ur,ur1)

			return url

		else:

			ur = server1+'RCServer%s/ondemand/%s.mp4?attachment=true'%(server,vid)

			ur1 = server1+'RCServer%s/videos/%s.mp4?attachment=true'%(server,vid)

			url = valide(ur,ur1)

			return url

			

def valide(ur,ur1):

	try:

		req = urllib2.Request(ur)

		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')

		response = urllib2.urlopen(req)

		return ur

	except:

		return ur1

		

def canais(url):

	link = abrir_url(url)

	texto = re.findall('class="grid">(.+?)class="grid">',link,re.DOTALL)[0]

	match = re.compile('href="(.*?)".*?\s.*?data-src="(.*?)" title="(.*?)"').findall(texto)

	match.append(('https://topcanais.com/assistir-zoomoo-ao-vivo-24-horas-online/','https://topcanais.com/wp-content/uploads/2019/08/zoomoo-364x205.jpg','Assistir Zoomoo Ao Vivo'));match.append(('https://www.youtube.com/watch?v=BipSktLb09E&ab_channel=PeppaPigemPortugu%C3%AAsBrasil-CanalOficial','http://www.cxtv.com.br/img/Tvs/Logo/18ea65bed320f0bc861d2060551f78f8.jpg','Pepa Pig'))

	for url, img, name in match:

		addDir('[COLOR blue]%s[/COLOR]'%name,url,11,img)

		

def rescanais(url):

	if 'watch' in url:

		addDir('[COLOR blue]%s[/COLOR]'%name,url,96,iconimage)

		return

	play = 'https://canaismax.com/assistir.php?chmax=%s'

	link = abrir_url(url)

	try:

		texto = re.findall('optsOpen(.+?)optsOpen',link,re.DOTALL)[0]

		match = re.compile('data-link="(.*?)"').findall(texto)

		for i in match:

			try:

				id = re.compile('op=(.+)').findall(i)[0]

			except:pass

		try:

			quality = base64.decodestring(id)

		except:

				xbmcgui.Dialog().ok(addon_id, "[COLOR red][B]Canal indisponível no momento, tente mais tarde.[/COLOR][/B]")

				return

		n = re.compile('q":"(.*?)","ch":"(.*?)"').findall(quality)

	except:

		n = re.compile('data-id="(.*?)".*?data-playertipo="aovivo">(.*?)</a>').findall(link)

		for c, q in n:

			addDir('[COLOR blue]%s[/COLOR]'%name+' '+'[COLOR blue]%s[/COLOR]'%q,play%c,96,iconimage)

		return

	for q, c in n:

		addDir('[COLOR blue]%s[/COLOR]'%name+' '+'[COLOR blue]%s[/COLOR]'%q,play%c,96,iconimage)

	

def player(name,url,iconimage):

		OK = False

		

		nome = name

		msgDP= xbmcgui.DialogProgress()

		

		msgDP.create('REDE CANAIS', 'Obtendo Fontes Para ' + name, 'Por favor aguarde...')

		msgDP.update(25)

		

		nServers = []

		uServers = []

		matriz = []

		

		servers = [url]

		

		for server in servers :

			ns = getRegex(server, '//','/')

			ns1 = name.replace('[COLOR blue]','').replace('[/COLOR]','')

			if len(ns) > 1 :

					nServers.append(ns1.upper())

					uServers.append(server)

		

		if not nServers : return

		

		index = xbmcgui.Dialog().select('Selecione uma das fontes suportadas :', nServers)

		

		if index == -1 : return

		

		msgDP.update(50, 'Resolvendo fonte Para ' + name, 'Por favor aguarde...')

		

		url2Resolve = uServers[index]

		legendas = '-'

		

		if 'RC' in url2Resolve :

				link = url2Resolve

				urlV = link

				linkVT = urlV

				url2Play = linkVT

				OK = True

				

		elif 'chmax' in url2Resolve :

				link = abrir_url(url2Resolve)

				urlV = re.compile('source: "(.*?)"').findall(link)[0]

				linkVT = urlV+ref

				url2Play = linkVT

				OK = True

				

		elif 'topcanais' in url2Resolve :

				link = abrir_url(url2Resolve)

				urlV = re.compile('source: "(.*?)"').findall(link)[0]

				linkVT = urlV+ref

				url2Play = linkVT

				OK = True

				

		elif 'watch' in url2Resolve :

				link = 'http://lista.lorddark.club:80/fulviodefreitas/freitass5235/933'

				urlV = link

				linkVT = urlV

				url2Play = linkVT

				OK = False

				

				

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

	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')

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

		fonte = urllib2.urlopen("https://raw.githubusercontent.com/setokaiba3/meu_addon/main/redecanais.py").read()

		prog = re.compile('.+').findall(fonte)

		if prog:

			py = os.path.join(Path, "redecanais.py")

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

elif mode==5: seriesurls(url)

elif mode==7: respesquisar(url)

elif mode==8: next_pesquisa(url,name,iconimage)

elif mode==10: canais(url)

elif mode==11: rescanais(url)

###########################         listar videos



###########################             OPEN SETINGS

elif mode==40: pesquisa(url)

elif mode==50: url_pesquisa(url)

elif mode==80: Addon_Settings()



#########################################          

###########################             player

elif mode==6: resplayer(url,name,iconimage)

elif mode==96: player(name,url,iconimage)



#########################################          FIM

xbmcplugin.endOfDirectory(int(sys.argv[1]))

