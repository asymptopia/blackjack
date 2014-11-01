"""
/**********************************************************
	
	Organization	:Dona Ana Cycle Salvage
					 915 Dona Ana Rd., Las Cruces, NM 88007
					 (575) 526-8278
	
	Website			:http://www.dacyclesalvage.com
					
    License         :GPLv3

***********************************************************/
"""
import wx
from cfgctrl import *

class wxAdmin(wx.Dialog):

	def __init__(self,parent):

		self.parent		=parent
		self.env		=parent.env
		self.configdir	=self.env.configdir
		self.sitepkgdir	=self.env.sitepkgdir
		self.homedir	=self.env.homedir
		self.global_config=self.parent.global_config
		
		wx.Dialog.__init__(
			self,None,wx.NewId(),
			self.global_config['APPNAME']['VALUE'],
			size=wx.Size(self.global_config['WIN_W']['VALUE'],self.global_config['WIN_H']['VALUE']),
			style=wx.RESIZE_BORDER|wx.CAPTION|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX
		)
		
	def reload_config(self):
		self.parent.reload_configs()
		self.global_config=self.parent.global_config


	def setup(self):
		
		splitter = wx.SplitterWindow (self,wx.NewId(),style=wx.NO_3D)#|wxSP_3D
		splitter.SetMinimumPaneSize(150)
		
		lhp=wx.Panel(splitter,wx.NewId())
		rhp=wx.Panel(splitter,wx.NewId())
		
		fbox=wx.BoxSizer(wx.HORIZONTAL)
		fbox.Add(splitter,1,wx.GROW)
		self.SetSizer(fbox)
		self.SetAutoLayout(True)
		####fbox.Fit(self)
		fbox.Layout()
		
		
		lhp.SetSize((150,900))
		lhp.SetBackgroundColour((255,255,255))
		sidebar_fname=os.path.join(self.env.sitepkgdir,self.parent.global_config['IMG_ADMIN_SIDEBAR']['PATH'],self.parent.global_config['IMG_ADMIN_SIDEBAR']['VALUE'])
		lhp_gif=wx.Image(sidebar_fname,wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		wx.StaticBitmap(lhp,wx.NewId(),lhp_gif,(0,0))
		self.lhp_gif=lhp_gif
		
		size=wx.Size(self.global_config['WIN_W']['VALUE'],self.global_config['WIN_H']['VALUE'])
		self.SetSize(size);
		splitter.SplitVertically(lhp,rhp,lhp.GetSize()[0])
		splitter.SetSashPosition(lhp.GetSize()[0]);
		
		
		tabs=['Globals','GPL']#,'Readme','Asymptopia','GPL'
		nb=wx.Notebook(rhp,wx.NewId(),style=wx.NB_TOP|wx.NB_FIXEDWIDTH)
		
		for idx in range(len(tabs)):
			cfgctrl=CfgCtrl(self,nb)
			nb.AddPage(cfgctrl,tabs[idx],0)
			cfgctrl.setup(tabs[idx])
		
		rhpbox=wx.BoxSizer(wx.VERTICAL);
		rhpbox.Add(nb,1,wx.EXPAND);
		rhp.SetSizer(rhpbox);
		rhp.SetAutoLayout(True);
		rhpbox.Fit(rhp);
		rhpbox.Layout();
