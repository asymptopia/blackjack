"""
/**********************************************************
	
	Organization	:Dona Ana Cycle Salvage
					 915 Dona Ana Rd., Las Cruces, NM 88007
					 (575) 526-8278
	
	Website			:http://www.dacyclesalvage.com
					
    License         :GPLv3

***********************************************************/
"""
import wx,os
import wx.lib.scrolledpanel as scrolled
import wx.html as html

from cfgctrlobj import *
from dict_formatter import *

DEBUG=0

class CfgCtrl(wx.Panel):
	def __init__(self,admin,nb):
		self.sizer=None
		self.cp=None
		self.cpsizer=None
		self.name=None
		self.cfgctrlobjs=[]
		self.SHOW_ALL=False
		self.admin=admin
		self.global_config=admin.global_config
		wx.Panel.__init__(self,nb,wx.NewId(),wx.DefaultPosition,wx.DefaultSize,style=wx.FULL_REPAINT_ON_RESIZE)
		
	def setup(self,name):
		self.name=name
		button_height=35
		if self.admin.env.OS=='win':button_height=20
		if self.admin.env.OS=='win':button_height=20
		button_size=wx.Size(100,button_height)
		
		toolbar=wx.ToolBar(self,wx.NewId(),style=wx.TB_HORIZONTAL)
		self.sizer=wx.BoxSizer(wx.VERTICAL);
		self.sizer.Add(toolbar,0,wx.EXPAND);
		
		xpos=0
		if name=='Globals':
			#SAVE BUTTON
			xid=wx.NewId()
			saveB=wx.Button(toolbar,xid,"Save+Apply",size=button_size,pos=wx.Point(xpos,0))
			toolbar.AddControl(saveB)
			saveB.SetToolTip(wx.ToolTip('Save these configuration options'))
			wx.EVT_BUTTON(toolbar,xid,self.saveCB)
			xpos+=100
	
			#LOGOUT BUTTON
			xid=wx.NewId()
			logoutB=wx.Button(toolbar,xid,"Hide Window",size=button_size,pos=wx.Point(xpos,0))
			logoutB.SetToolTip(wx.ToolTip('Hide the Administrator Control Panel.'))
			toolbar.AddControl(logoutB)
			wx.EVT_BUTTON(toolbar,xid,self.logoutCB)
			xpos+=100
			
			#SHOW_ALL TOGGLE
			xid=wx.NewId()
			showallB=wx.CheckBox(toolbar,xid,"ShowAll",size=button_size,pos=wx.Point(xpos,0))
			showallB.SetValue(False)
			showallB.SetToolTip(wx.ToolTip('Show all configurable parameters, including those hidden by default'))
			#toolbar.AddControl(showallB)
			wx.EVT_CHECKBOX(toolbar,xid,self.showallCB)
		
			self.load()

		elif self.name=='GPL':self.reload('GPL')
		#elif self.name=='Asymptopia':self.reload('Asymptopia')
		#elif self.name=='Readme':self.reload('Readme')
		
		self.SetSizer(self.sizer)
		self.SetAutoLayout(True)
		self.Layout()
		#panel.get_installed()
		
	def reload(self,target):
		if False:pass
		elif target=='Readme':
			editor=wx.TextCtrl(self,wx.NewId(),style=wx.TE_MULTILINE|wx.TE_PROCESS_TAB)
			inf=open(os.path.join(self.admin.env.sitepkgdir,'bj','README'))
			gpl=inf.read()
			inf.close()
			if DEBUG:print dir(editor)
			editor.WriteText(gpl)
			editor.SetEditable(0)
			self.cp=editor
			self.cp.SetSizer(self.sizer)
			self.sizer.Add(self.cp,1,wx.EXPAND,1)
			
		elif target=='GPL':
			try:
				#editor=html.HtmlWindow(self.cp,wx.NewId(),style=wx.NO_FULL_REPAINT_ON_RESIZE)
				infname=os.path.join(self.admin.env.sitepkgdir,'bj','LICENSE')
				#print 'fname=',infname
				#editor.LoadPage(infname)
				#print 'okay'
				editor=wx.TextCtrl(self,wx.NewId(),style=wx.TE_MULTILINE|wx.TE_PROCESS_TAB)
				inf=open(infname)
				gpl=inf.read()
				inf.close()
				#if DEBUG:print dir(editor)
				editor.WriteText(gpl)
				editor.SetEditable(0)
				self.cp=editor
				self.cp.SetSizer(self.sizer)
				self.sizer.Add(editor,1,wx.EXPAND,1)
			except Exception,e:print e

		elif target=='Asymptopia':
			editor=wx.TextCtrl(self,wx.NewId(),style=wx.TE_MULTILINE|wx.TE_PROCESS_TAB)
			inf=open(os.path.join(self.admin.env.sitepkgdir,'bj','ASYMPTOPIA'))
			gpl=inf.read()
			inf.close()
			if DEBUG:print dir(editor)
			editor.WriteText(gpl)
			editor.SetEditable(0)
			self.cp=editor
			self.cp.SetSizer(self.sizer)
			self.sizer.Add(self.cp,1,wx.EXPAND,1)
			
		
	def recreate_cp(self):
		
		self.cfgctrlobjs=[]
		
		if self.cp:
			self.sizer.Detach(self.cp)
			del self.cp
			self.cp=None

		self.cp=wx.ScrolledWindow(self,-1,wx.DefaultPosition,wx.DefaultSize,wx.VSCROLL)
		#self.cp.SetBackgroundColour(wx.Colour(0,100,100))
		self.cp.SetScrollRate(0,10)
		self.cpsizer=wx.BoxSizer(wx.VERTICAL)
		self.cp.SetSizer(self.cpsizer)
		self.cpsizer.Fit(self.cp)
		self.cp.SetAutoLayout(True)
		self.cp.Layout()
		self.cp.Refresh()
		self.sizer.Add(self.cp,2,wx.GROW)
	
	def load(self):
		self.recreate_cp()
		obj_keys=self.global_config.keys()
		obj_keys.sort()
		for idx in range(len(obj_keys)):
			obj_dict=self.global_config[obj_keys[idx]]
			if type(obj_dict).__name__ != 'dict':continue
			if obj_dict['SHOWME']!= True and self.SHOW_ALL != True:continue
			if obj_dict['SHOWME']<0:continue
			obj=CfgCtrlObj(self.cp,obj_keys[idx],obj_dict)
			self.cpsizer.Add(obj,0,wx.EXPAND)#WRONG ARG FORMAT .. needs wx.Size()
			self.cfgctrlobjs.append(obj);

		self.Layout()
		wx.ToolTip.Enable(True)
		wx.ToolTip.SetDelay(2000)
		
	def saveCB(self,e):
		
		for obj in self.cfgctrlobjs:
			obj.update()#widget.value -> obj.val['value']
			self.global_config[obj.key]=obj.obj_dict
			
		if self.global_config.has_key('letters'):del self.global_config['letters']
		if self.global_config.has_key('distribution'):del self.global_config['distribution']
		if self.global_config.has_key('scoring'):del self.global_config['scoring']
		
		oufdir=os.getenv('HOME')
		if not oufdir:oufdir=os.getenv('USERPROFILE')
		
		oufname=os.path.join(oufdir,'.blackjack_config')
		ouf=open(oufname,'w')
		rval=format_dict(self.global_config,0)
		ouf.write(rval)
		ouf.close()
		
		try:
			self.reload_config()
		except Exception,e:
			print e
		
		

	def reload_config(self):
		self.admin.reload_config()
		self.global_config=self.admin.global_config

	def logoutCB(self,e):
		self.admin.EndModal(0)
	
	def showallCB(self,e):
		if self.SHOW_ALL==False:
			self.SHOW_ALL=True
		else:
			self.SHOW_ALL=False
		self.load()
