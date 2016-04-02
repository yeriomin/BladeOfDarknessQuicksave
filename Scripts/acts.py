import Bladex
import Actions
import BInput
import string

def GetKeyList(ActionName):
	IManager=BInput.GetInputManager()
	oldInputActionsSet=IManager.GetInputActionsSet()
	IManager.SetInputActionsSet("Default")
	IActions=IManager.GetInputActions()
	IAction=IActions.Find(ActionName)
	
	result = []
	for i in range(IAction.nInputEvents()):
		IEvent=IAction.GetnInputEvent(i)
		if(IEvent.GetDevice()=="Keyboard"):
			result.append(IEvent.GetKey())
	IManager.SetInputActionsSet(oldInputActionsSet)
	return result


def ExecTravelBookNP():
	import Menu
	import MenuWidget
	import GameText
	import Scorer

	GameText.AbortText()

	if GameText.MapList.has_key(string.upper(Bladex.GetCurrentMap())) and (not Menu.MENU_PREACTIVATED):
		Menu.TB_ACTIVATED=1
		Menu.MENU_PREACTIVATED = 1
		#Menu.ExecTravelBook(0)
		pepote = Menu.Desc1
		Menu.Desc1={"Name":"TopMenu",
				"FrameKind":MenuWidget.B_BackWeapon,
				"ListDescr":[
							{
							"Name":"Back",
							"Kind":MenuWidget.B_BackWeapon
							}
				]
			}
		Menu.ActivateMenu()
		Menu.Desc1 = pepote
		Scorer.HideTBS()
		
		for kn in GetKeyList("Turn Left"):
			if kn!="Left":
				Bladex.AssocKey("Menu Dec","Keyboard",kn)

		for kn in GetKeyList("Turn Right"):
			if kn!="Right":
				Bladex.AssocKey("Menu Inc","Keyboard",kn)
	else:
		print "================"
		print "   Sorry Gary!                "
		print "   May be next time      "
		print "================"
		
      	  
ON_RELEASE=0
ON_PRESS=1	# default

FuncList = [];
def DefArgWrapper (PlayerName, Function):
	def wrapper(name=PlayerName, func=Function):	
		retval = func (name)		
		Bladex.CheckPyErrors()
		return retval

	FuncList.insert(0, wrapper) 
	return FuncList[0]


def eNetBinds(PlayerName):
	pass

NetBinds = eNetBinds

def InitBindings (PlayerName):
	#Bladex.UnBindAll()
	import netgame
	import NetActions
	import SaveGame
	if netgame.GetNetState() == 0:
		import DefaultSelectionData
		import Scorer

		CycleShieldsFunc=Scorer.ShieldsControl.CycleElements
		CycleWeaponsFunc=Scorer.WeaponsControl.CycleElements
		CycleObjectsFunc=Scorer.CycleElements
		SelectObjectFunc=DefaultSelectionData.SelectObject
		SelectEnemyFunc=DefaultSelectionData.SelectEnemy

	Bladex.AddBoundFunc("FrwdDown",DefArgWrapper (PlayerName, Actions.FrwdDown))
	Bladex.AddBoundFunc("FrwdUp",DefArgWrapper (PlayerName, Actions.FrwdUp))	
	Bladex.AddBoundFunc("BrwdDown",DefArgWrapper (PlayerName, Actions.BrwdDown))
	Bladex.AddBoundFunc("BrwdUp",DefArgWrapper (PlayerName, Actions.BrwdUp))	


	# throws
	#Bladex.Bind2("Throw Right","Throw Release","Attack Release",500)
	#Bladex.Bind2("Throw Left","Throw Release","Block Release",500)

	Bladex.AddBoundFunc("Throw",DefArgWrapper (PlayerName, Actions.EnterThrowingMode))
	Bladex.AddBoundFunc("Toggle Weapons",DefArgWrapper (PlayerName, Actions.StdToggleWeapons))

	# simple attack
	Bladex.AddBoundFunc("Attack","Attack")	
	
	
	# simple block
	Bladex.AddBoundFunc("Block","Block")	

	if netgame.GetNetState() == 0: # not supported in multiplayer
		Bladex.AddBoundFunc("SelectObj",SelectObjectFunc)
		Bladex.AddBoundFunc("Cycle Weapons",CycleWeaponsFunc)
		Bladex.AddBoundFunc("Cycle Shields",CycleShieldsFunc)
		Bladex.AddBoundFunc("Cycle Objects",CycleObjectsFunc)
		Bladex.AddBoundFunc("UnSelectObj",SelectObjectFunc)
		Bladex.AddBoundFunc("Select Enemy",SelectEnemyFunc)
		Bladex.AddBoundFunc("Attack",DefArgWrapper (PlayerName, Actions.TestDrawBow))
		Bladex.AddBoundFunc("Attack Release",DefArgWrapper (PlayerName, Actions.TestReleaseArrow))
		Bladex.AddBoundFunc("Throw Left",DefArgWrapper (PlayerName, Actions.TestThrowLeft))
		
		Bladex.AddBoundFunc("Block",DefArgWrapper (PlayerName, Actions.TestThrowLeft))
		Bladex.AddBoundFunc("Use",DefArgWrapper (PlayerName, Actions.StdUse))
		Bladex.AddBoundFunc("LaunchTravel",ExecTravelBookNP)

	#Bladex.AddBoundFunc("UnSelectEnemy",UnSelectEnemyFunc)

	Bladex.AddBoundFunc("Attack",DefArgWrapper (PlayerName, Actions.TestThrowRight))

	Bladex.AddBoundFunc("Forwards","Forwards")
	Bladex.AddBoundFunc("Backwards","Backwards")
	
	#NO RULABA!!!
	#Bladex.Bind2("TurnInRelax","Forwards","Backwards",100)
	#Bladex.AddBoundFunc("TurnInRelax",DefArgWrapper (PlayerName, Actions.RelaxTurn180))

	Bladex.AddBoundFunc("Swim Up","Swim Up")
	Bladex.AddBoundFunc("Swim Down","Swim Down")
	Bladex.AddBoundFunc("Turn Left","Turn Left")
	Bladex.AddBoundFunc("Turn Right","Turn Right")
	Bladex.AddBoundFunc("Look Up","Look Up")
	Bladex.AddBoundFunc("Look Down","Look Down")
	Bladex.AddBoundFunc("ToggleStats","ToggleStats")
	Bladex.AddBoundFunc("ToggleSampling","ToggleSampling")
	
	#Bladex.AddBoundFunc("Throw", DefArgWrapper (PlayerName, Actions.StdThrowObject))

	Bladex.AddBoundFunc("Jump","Jump")
	Bladex.AddBoundFunc("Run","Run")
	Bladex.AddBoundFunc("Sneak","Sneak")
	Bladex.AddBoundFunc("Free Look","FreeLook")
	Bladex.AddBoundFunc("Next View","NextView")
	Bladex.AddBoundFunc("Last View","LastView")
	
	Bladex.AddBoundFunc("Dodge","Dodge")
	Bladex.AddBoundFunc("Camera Left","Camera Left")
	Bladex.AddBoundFunc("Camera Right","Camera Right")
	Bladex.AddBoundFunc("Change Camera","Change Camera")
	Bladex.AddBoundFunc("Fixed Camera","Fixed Camera")
	Bladex.AddBoundFunc("Camera Dist","Camera Dist")
	Bladex.AddBoundFunc("Change Mov","Change Mov")
	Bladex.AddBoundFunc("Toggle Sound","Toggle Sound")
	Bladex.AddBoundFunc("Bigger FOV","Bigger FOV")
	Bladex.AddBoundFunc("Smaller FOV","Smaller FOV")
	Bladex.AddBoundFunc("Toggle BB","Toggle BB")
	Bladex.AddBoundFunc("Screen Shot","Screen Shot")
	Bladex.AddBoundFunc("KillEnemy","KillEnemy")
	Bladex.AddBoundFunc("NextPOV","NextPOV")
	Bladex.AddBoundFunc("RotateX","RotateMouseX")
	Bladex.AddBoundFunc("RotateY","RotateMouseY")
	

	if netgame.GetNetState() != 0: # si hay red...		
		Bladex.AddBoundFunc("Cycle Weapons",DefArgWrapper (PlayerName, NetActions.ChangeWeapon))
		Bladex.AddBoundFunc("Cycle Shields",DefArgWrapper (PlayerName, NetActions.ChangeShield))
		Bladex.AddBoundFunc("Use", DefArgWrapper (PlayerName, Actions.AutoTake))
		
		netgame.Bind("Cycle Weapons",   NetActions.ChangeWeapon, 0)
		netgame.Bind("Use",                   Actions.AutoTake, 0)
		netgame.Bind("Cycle Shields",   NetActions.ChangeShield, 0)
		netgame.Bind("Toggle Weapons",  Actions.StdToggleWeapons,0)
		""" # suspendido el arco y flecha
		netgame.Bind("Attack",          Actions.TestDrawBow,     0)
		netgame.Bind("Attack Release",  Actions.TestReleaseArrow,1)
		"""
		NetBinds(PlayerName)
		
	
	Bladex.AddBoundFunc("ToggleProfiling",Actions.ToggleProfiling)
	Bladex.AddBoundFunc("ToggleInvincibility",Actions.ToggleInvincibility)
	Bladex.AddBoundFunc("SaveGameQuick",SaveGame.SaveGameQuick)
	Bladex.AddBoundFunc("LoadGameQuick",SaveGame.LoadGameQuick)

def SetNoConfigurableActions():
	Bladex.AssocKey("LaunchTravel","Keyboard","F1")

#			                                            Kind         Action
ConfigurableActions =[
			("Forwards",       "Forwards",                [("Release",  "FrwdUp"),
			                                               ("Press",    "FrwdDown")        ]),
			("Backwards",      "Backwards",               [("Release",  "BrwdUp"),
			                                               ("Press",    "BrwdDown")        ]),
			("Turn Left",      "Turn Left",               []),
			("Turn Right",     "Turn Right",              []),
			("Look Up",        "Look Down",               []),
			("Look Down",      "Look Up",                 []),
			("Jump",           "Jump",                    []),
			("Attack",         "Attack",                  [("Release",  "Attack Release"), ]),
			("Block",          "Block",                   [("Release",  "Block Release"),  ]),
			("Throw",          "Throw",                   [("Release",  "Throw Release"),  ]),
			("Sneak",          "Sneak",                   []),			
			#("Run",            "Run",                    []),
			("Use",            "Use",                     []),
			("Draw/Sheathe Weapons", "Toggle Weapons",    []),
			("Cycle Weapons",  "Cycle Weapons",           []),
			("Cycle Shields",  "Cycle Shields",           []),
			("Cycle Inventory Objects",  "Cycle Objects", []),
			("Lock On Enemy",  "Select Enemy",            []),
			("Select Object",  "SelectObj",               []),
			("Screen Shot",    "Screen Shot",             []),
			("Free Look",      "Free Look",               []),
			("Next View",      "Next View",               []),
			("Last View",      "Last View",               []),
			("Arena Scorer",   "Show Scorer",             []),
			("Send Message",   "Send Message",            []),
			("Quick Save",     "SaveGameQuick",           []),
			("Quick Load",     "LoadGameQuick",           []),
			
			#("LaunchTravel",   "LaunchTravel",           []),

			#("Quick Save",     "Quick Save",             []),
			#("Travel Book",    "Travel Book",            []),
                     ]

def ResetDefaultControls():
	iman = BInput.GetInputManager()
	OldASet = iman.GetInputActionsSet()
	iman.SetInputActionsSet("Default")
	for i in ConfigurableActions:
		InAct = iman.GetInputActions()
		InAct.Find(i[1]).RemoveAllEvents()
		for k in i[2]:
			if   k[0] == "Press":
				InAct.Find(k[1]).RemoveAllEvents()
			elif k[0] == "Release":
				InAct.Find(k[1]).RemoveAllEvents()
			else:
				print "ERROR : '",k[0],"' is not defined yet!"
				
	execfile("../../Scripts/DefControl.py")
	iman.SetInputActionsSet(OldASet)
	
	
#InitBindings ("Player1")
