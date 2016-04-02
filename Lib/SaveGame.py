import MenuText
import Bladex
import netwidgets
import MenuWidget
import os
import time
import string
import Reference
import AuxFuncs
import stat

EMPTY_SLOT  = MenuText.GetMenuText("<Empty Slot>")
DATE_FORMAT = MenuText.GetMenuText("%d/%m %H:%M")
SaveCounter = []

for i in range(2):
        SaveCounter.append("Awesome!")

for i in range(3):
        SaveCounter.append("Heroic")

for i in range(4):
        SaveCounter.append("Bold")

for i in range(5):
        SaveCounter.append("Normal")

for i in range(6):
        SaveCounter.append("Cautious")

for i in range(7):
        SaveCounter.append("Overcautious")

SaveCounter.append("Lame")
#
# Utils to save/load games.
#

def ElUsuarioPresionaLaTeclaEscape(Salio):
    return 1


def LoadGameAux(name):
	import Language
	import SplashImage

	path="../../Save/%s_files"%(name,)
	execfile="execfile('../../Scripts/sys_init.py');execfile('../../Save/%s.py')"%(name,)

	file_data_aux=open("%s/%saux"%(path,"aux"),"rt")
	text=file_data_aux.read()
	print text
	file_data_aux.close()
	scr_name="../../Data/Menu/Save/"+Language.Current+"/Cerrando.jpg"
	SplashImage.ShowImage(scr_name,0)
	Bladex.BeginLoadGame()
	Bladex.CloseLevel(execfile,text)
	
def LoadGameFromDisk(menu_class):
	LoadGameAux("SaveGame"+menu_class.MenuDescr["Clave"])

def LoadGameQuick():
	Bladex.SetRunString("Bladex.StopTime();Bladex.PauseSoundSystem();Bladex.BeginLoadGame();execfile=\"execfile('../../Scripts/sys_init.py');execfile('../../Save/SaveGameQuick.py')\";file=open('../../Save/SaveGameQuick_files/auxaux');aux=file.read();file.close();Bladex.CloseLevel(execfile,aux);Bladex.RestartTime();Bladex.ResumeSoundSystem()");

def SaveGameAux(key, isQuick):
	import Menu
	import Scorer
	import MenuText
	import GameText
	import GotoMapVars

	global SaveGameString

	# Back to game
	if not isQuick:
		Menu._MainMenu.DeActivateMenuItem()
		Menu._MainMenu.DeActivateMenuItem()
		Menu._MainMenu.DeActivateMenuItem()
		Menu._MainMenu.DeActivateMenuItem()
	
	
	# save aditional data
	file = open("../../Save/"+key+".sv","w")

	char = Bladex.GetEntity("Player1")
	if char.Kind[0] =="K":
		cad = MenuText.GetMenuText("Knight")
	if char.Kind[0] =="B":
		cad = MenuText.GetMenuText("Barbarian")
	if char.Kind[0] =="D":
		cad = MenuText.GetMenuText("Dwarf")
	if char.Kind[0] =="A":
		cad = MenuText.GetMenuText("Amazon")
	
	cadtime = time.strftime(DATE_FORMAT,time.localtime(time.time()))
	
	cad = `char.Level+1`+" Lv. "+cad+" "+" - "+cadtime+" - "
	cad = cad + GameText.MapDescriptor(Bladex.GetCurrentMap())
	Reference.TimesSaved = Reference.TimesSaved+1

	nMaps = 1
	for v in GotoMapVars.VisitedMaps:
		if v:
			nMaps = nMaps + 1
	
	vismap = (Reference.TimesSaved-1)/nMaps
			
	if vismap >= len(SaveCounter):
	    DisgustingMessage = SaveCounter[(len(SaveCounter)-1)]
	else:
	    DisgustingMessage = SaveCounter[vismap]
	cad = cad + " - "+`Reference.TimesSaved`+" ("+MenuText.GetMenuText(DisgustingMessage)+")"
	file.write(cad)	
	file.close()
	print cad

	# save Screen shoot
	Scorer.SetVisible(0)
	Bladex.SaveScreenShot('../../Save/'+key+'.BMP',160,120)
	SaveGameString = "import GameState;state=GameState.WorldState();state.GetState();state.SaveState('../../Save/SaveGame"+key+".py');state=None;GameState=None;"

	# Save the game
	Bladex.PauseSoundSystem()
	Bladex.StopTime()
	Bladex.SetRunString(SaveGameString+"Scorer.SetVisible(1);Bladex.RestartTime();Bladex.ResumeSoundSystem()")

def SaveGameToDisk(menu_class):
	SaveGameAux(menu_class.MenuDescr["Clave"], 0)

def SaveGameQuick():
	SaveGameAux("Quick", 1)

def GetBack(menu_class):
	import Menu
	Menu._MainMenu.DeActivateMenuItem()
	

SaveBitmaps = 	(
			("1"    , "../../Save/1.BMP"   ),
			("2"    , "../../Save/2.BMP"   ),
			("3"    , "../../Save/3.BMP"   ),
			("4"    , "../../Save/4.BMP"   ),
			("5"    , "../../Save/5.BMP"   ),
			("6"    , "../../Save/6.BMP"   ),
			("7"    , "../../Save/7.BMP"   ),
			("8"    , "../../Save/8.BMP"   ),
		)

SAVEGAMEIMAGE = "0"
LOADGAMEIMAGE = "0"

def GetSaveGameImage():
	return SAVEGAMEIMAGE

def GetLoadGameImage():
	return LOADGAMEIMAGE


def FocusOnBitmap(menu_class=0,parametro=0):
	netwidgets.ChangePlayer(menu_class.MenuDescr["Clave"])


# called when the menu is called
def CreateSaveMenu():
	import Menu
	import GameText
	
	index = InspectSaveList()

	if AllEmpty and  not GameText.MapList.has_key(string.upper(Bladex.GetCurrentMap())):
		try:
			Menu.GetMenuItem    (['GAME','LOAD GAME'])['Kind'     ] = MenuWidget.B_MenuItemTextNoFXNoFocus
		except:
			pass
		try:
			del Menu.GetMenuItem(['GAME','LOAD GAME'])['ListDescr']
		except:
			pass
	else:
		try:
			CreateMenu('LOAD GAME',0)
		except:
			pass
		try:
			del Menu.GetMenuItem    (['GAME','LOAD GAME'])['Kind'     ]
		except:
			pass
	
	if (Bladex.GetEntity("Player1").Life <= 0) or not GameText.MapList.has_key(string.upper(Bladex.GetCurrentMap())):
		try:
			Menu.GetMenuItem    (['GAME','SAVE GAME'])['Kind'     ] = MenuWidget.B_MenuItemTextNoFXNoFocus
		except:
			pass
	else:
		try:
			del Menu.GetMenuItem    (['GAME','SAVE GAME'])['Kind'     ] 
		except:
			pass
		try:
			CreateMenu('SAVE GAME',1)
		except:
			pass
			
		try:
			Menu.GetMenuItem    (['GAME'])['iFocus'] = 1
		except:
			pass

	try:
		if GameText.MapList.has_key(string.upper(Bladex.GetCurrentMap())):
			Menu.GetMenuItem    (['GAME','LOAD GAME'])['iFocus'] = index[0]+1
		else:
			Menu.GetMenuItem    (['GAME','LOAD GAME'])['iFocus'] = index[0]
	except:
		pass

	try:
		Menu.GetMenuItem    (['GAME','SAVE GAME'])['iFocus'] = index[1]
	except:
		pass

def InspectSaveList():
	global SaveBitmaps
	global AllEmpty
	global FirstSaved
	global SAVEGAMEIMAGE
	global LOADGAMEIMAGE
	
	FirstSaved = None
	AllEmpty = 1
	
	lasttime       = 0
	indexsel       = 1

	firstime       = 10000000000000.0
	indexselfirst  = 2

	FirstEmptySlot = -1
	
	
	SaveBitmaps = []
	path = "../../Save/"
	
	ListDir = []
	for filename in os.listdir(path):
		ListDir.append(string.upper(filename))
	
	for i in range(6):
		cad = `i+1`+".BMP"
		if cad in ListDir:
			file = open(path+`i+1`+".sv","r")
			name = file.readline()
			file.close()
			
			SaveBitmaps.append(`i+1`,path+cad,name)
			AllEmpty = 0
			if not FirstSaved:
				FirstSaved = `i+1`
			filetime = os.stat (path+cad)[stat.ST_MTIME]
			if lasttime<filetime:
				lasttime = filetime
				indexsel = i+2
			if firstime>filetime:
				firstime      = filetime
				indexselfirst = i+2
		else:
			SaveBitmaps.append(`i+1`,"../../Data/Empty.BMP",EMPTY_SLOT)
			if FirstEmptySlot == -1:
				FirstEmptySlot = i+2
	
	SaveBitmaps.append("0","../../Data/Empty.BMP",EMPTY_SLOT)
	if FirstEmptySlot == -1:
		FirstEmptySlot = indexselfirst
		SAVEGAMEIMAGE = `indexselfirst-1`
	else:
		SAVEGAMEIMAGE = "0"
	
	LOADGAMEIMAGE = `indexsel-1`
		
	return indexsel, FirstEmptySlot

def RestartLevel(menu_class):
	Bladex.LoadLevel(Bladex.GetCurrentMap())

def MenuStart(EntityName):
	import AuxFuncs
	Bladex.GetEntity(EntityName).Freeze()
	print EntityName, "is  death"
	if AuxFuncs.FadeActive:
		ActivaMenuDeRegreso()
	else:
		AuxFuncs.FadeTo(1.0,1.0)
		Bladex.AddScheduledFunc(Bladex.GetTime()+1.0,ActivaMenuDeRegreso,())

def ActivaMenuDeRegreso():
	import Menu
	if Bladex.GetEntity("Player1").Life<=0:
		Menu.GetMenuItem(["BACK TO GAME"])['Kind'     ] = MenuWidget.B_MenuItemTextNoFXNoFocus
		Menu.EscapeFunction = ElUsuarioPresionaLaTeclaEscape

	Menu.Desc1["iFocus"]                 = 0
	Menu.GetMenuItem(['GAME'])["iFocus"] = 2
	
	Menu.ActivateMenu()
	Menu._MainMenu.ActivateMenuItem()
	Menu._MainMenu.ActivateMenuItem()

def CreateMenu(MenuName,SaveFlag):
	import Menu
	import MenuText
	import GameText
	global EmptyImage
		
	menuItem = Menu.GetMenuItem(['GAME',MenuName])

	if menuItem == 1:
		return

	Save_Menu = []
	
	EmptyImage = (not SaveFlag) and GameText.MapList.has_key(string.upper(Bladex.GetCurrentMap()))
		
	Save_Menu.append(  {"Name"    : MenuText.GetMenuText(MenuName),
	                    "VSep"    : 30,
	                    "Font"    : Menu.MenuFontBig,
	                    "Kind"    : MenuWidget.B_MenuItemTextNoFXNoFocus,
	                     })
	
	if SaveFlag:
		Save_Menu.append(  {"Name":"GameList",
		                    "Kind":netwidgets.B_ImageListWidget,
		                    "ImageList":SaveBitmaps,
		                    "GetCharType":GetSaveGameImage,
		                    "VSep":10
		                   })
	else:
		Save_Menu.append(  {"Name":"GameList",
		                    "Kind":netwidgets.B_ImageListWidget,
		                    "ImageList":SaveBitmaps,
		                    "GetCharType":GetLoadGameImage,
		                    "VSep":10
		                   })
	
	if EmptyImage:
		Save_Menu.append(  {"Name"           : MenuText.GetMenuText("Restart")+' "'+GameText.MapDescriptor(Bladex.GetCurrentMap())+'"',
		                    "VSep"           : 10,
		                    "Clave"          : "0",
		                    "FocusCallBack"  : FocusOnBitmap,
		                    "Font"           : Menu.MenuFontMed,
		                    "Kind"           : MenuWidget.B_MenuItemTextNoFX,
		                    "Command"        : RestartLevel
		                     })

	if (not SaveFlag) and (os.path.exists("../../Save/SaveGameQuick.py")):
		Save_Menu.append(  {"Name"           : MenuText.GetMenuText("Quick Load"),
		                    "VSep"           : 10,
		                    "Clave"          : "Quick",
		                    "FocusCallBack"  : FocusOnBitmap,
		                    "Font"           : Menu.MenuFontMed,
		                    "Kind"           : MenuWidget.B_MenuItemTextNoFX,
		                    "Command"        : LoadGameFromDisk
		                     })

	
	####################################
	for i in range(6):
		SaveGameName = SaveBitmaps[i][2]
		if SaveFlag:
			val =              {"Name"           : SaveGameName,
			                    "VSep"           : 10,
			                    "Font"           : Menu.MenuFontMed,
			                    "FocusCallBack"  : FocusOnBitmap,
			                    "Clave"          : `i+1`,
			                    "iFocus"         : 2,
			                    "ListDescr"      : [
			                                        {"Name":MenuText.GetMenuText("Overwrite a previously saved game?"),
			                                         "VSep":200,
			                                         "Font":Menu.MenuFontBig,
			                                         "Kind":MenuWidget.B_MenuItemTextNoFXNoFocus
			                                        },
			                                        {"Name"    : MenuText.GetMenuText("Yes"),
			                                         "VSep"    : 20,
			                                         "Command" : SaveGameToDisk,
			                                         "Font"    : Menu.MenuFontMed,
			                                         "Clave"   :  `i+1`,
			                                        },
			                                        {"Name":MenuText.GetMenuText("No"),
			                                         "VSep":10,
			                                         "Font":Menu.MenuFontMed,
			                                         "Command" : GetBack
			                                        },
			                                        {"Name":"Back",
			                                         "Kind":MenuWidget.B_BackBlank
			                                        }
			                                      ]
			                     }
			if SaveGameName == EMPTY_SLOT:
				del val["ListDescr"]
				val["Command"] = SaveGameToDisk
			Save_Menu.append(val)
		else:
			val =              {"Name"           : SaveGameName,
			                    "VSep"           : 10,
			                    "Font"           : Menu.MenuFontMed,
			                    "FocusCallBack"  : FocusOnBitmap,
			                    "Clave"          : `i+1`,
			                    "iFocus"         : 2,
			                    "ListDescr"      : [
			                                        {"Name":MenuText.GetMenuText("ARE YOU SURE?"),
			                                         "VSep":200,
			                                         "Font":Menu.MenuFontBig,
			                                         "Kind":MenuWidget.B_MenuItemTextNoFXNoFocus
			                                        },
			                                        {"Name"    : MenuText.GetMenuText("Yes"),
			                                         "VSep"    : 20,
			                                         "Command" : LoadGameFromDisk,
			                                         "Font"    : Menu.MenuFontMed,
			                                         "Clave"   :  `i+1`,
			                                        },
			                                        {"Name":MenuText.GetMenuText("No"),
			                                         "VSep":10,
			                                         "Font":Menu.MenuFontMed,
			                                         "Command" : GetBack
			                                        },
			                                        {"Name":"Back",
			                                         "Kind":MenuWidget.B_BackBlank
			                                        }
			                                       ]
			                     }


			if SaveGameName == EMPTY_SLOT:
				val["Kind"] = MenuWidget.B_MenuItemTextNoFXNoFocus
			Save_Menu.append(val)
			                     
	####################################
	                     
	Save_Menu.append(   Menu.BackOption  )
	Save_Menu.append(   {"Name":"Back",
	                     "Kind":MenuWidget.B_BackBlank
	                     })
	                     	                     
	menuItem["ListDescr"] = Save_Menu






