"""
/**********************************************************

    Author          :Charlie Cosse

    Email           :ccosse_at_gmail_dot_com

    License         :GPLv3

***********************************************************/
"""
import wx,os
import pygame
from bj.environment import *

DEBUG=False

class CfgCtrlObj(wx.Panel):
	def __init__(self,cp,key,obj_dict):
		self.key=key
		self.obj_dict=obj_dict
		self.label=None
		self.env=Environment("bj")
		wx.Panel.__init__(self,cp,wx.NewId(),wx.DefaultPosition,wx.DefaultSize,style=wx.FULL_REPAINT_ON_RESIZE)

		sbox=wx.StaticBox(self,-1,key,wx.DefaultPosition,wx.DefaultSize);
		self.sbsizer=wx.StaticBoxSizer(sbox,wx.HORIZONTAL);
		sizer=wx.BoxSizer(wx.HORIZONTAL)

		widget_width=200;
		widget_height=35;
		wsize=wx.Size(widget_width,widget_height);
		self.label_size=wx.Size(20,widget_height);
		self.button_size=wx.Size(widget_width,widget_height);

		sizer.Add(self.sbsizer,1,wx.GROW,1);

		wxSliderStr="wx.Slider"
		wxSpinCtrlStr="wx.SpinCtrl"
		wxComboBoxStr="wx.ComboBox"
		wxCheckBoxStr="wx.CheckBox"
		wxColourDialogStr="wx.ColourDialog"

		defaultBID=wx.NewId()
		defaultB=wx.Button(self,defaultBID,"Default",wx.DefaultPosition,self.button_size)
		self.defaultB=defaultB#for bgcolor on ColorSelect
		wx.EVT_BUTTON(defaultB,defaultBID,self.DefaultCB)

		if False:pass
		elif obj_dict.has_key('WTYPE'):
			if False:pass
			elif obj_dict['WTYPE']==wxSliderStr:self.SetupSlider()
			elif obj_dict['WTYPE']==wxSpinCtrlStr:self.SetupSpinCtrl()
			elif obj_dict['WTYPE']==wxComboBoxStr:self.SetupComboBox()
			elif obj_dict['WTYPE']==wxCheckBoxStr:self.SetupCheckBox()
			elif obj_dict['WTYPE']==wxColourDialogStr:self.SetupColourDialog()

		default_buttons_sizer=wx.BoxSizer(wx.VERTICAL)
		default_buttons_sizer.Add(defaultB,2,wx.EXPAND)
		#self.sbsizer.SetDimension(0,0,50,600)
		self.sbsizer.Add(default_buttons_sizer,0)#,wx.GROW

		self.SetSizer(sizer)
		self.SetAutoLayout(True)
		self.Layout()
		self.Refresh()

		tooltip=wx.ToolTip(self.obj_dict['TOOLTIP'])
		self.SetToolTip(tooltip)

	def SetupCheckBox(self):
		CheckBoxID=wx.NewId()
		self.widget=wx.CheckBox(self,CheckBoxID,"",size=self.button_size)
		self.widget.SetValue(int(self.obj_dict['VALUE']))
		self.sbsizer.Add(self.widget)
		wx.EVT_CHECKBOX(self.widget,CheckBoxID,self.CheckBoxCB)
		label_str=''
		self.label=wx.StaticText(self,wx.NewId(),label_str,size=self.button_size)
		self.label.SetLabel(str(self.obj_dict['VALUE']))
		self.sbsizer.Add(self.label)
		self.CheckBoxCB(None)#to set the label after label exists

	def SetupSlider(self):
		self.widget=wx.Slider(
			self,
			wx.NewId(),
			int(self.obj_dict['VALUE']*self.obj_dict['DIVISOR']),
			int(self.obj_dict['MIN']),
			int(self.obj_dict['MAX']),
			style=wx.HORIZONTAL,
			size=self.button_size
		)

		self.sbsizer.Add(self.widget)

		sliderID=wx.NewId()
		div=self.obj_dict['DIVISOR']
		if div==1.:label_str="%.0f"%(self.obj_dict['VALUE'])
		if div==10.:label_str="%.1f"%(self.obj_dict['VALUE'])
		if div==100.:label_str="%.2f"%(self.obj_dict['VALUE'])
		if div==1000.:label_str="%.3f"%(self.obj_dict['VALUE'])
		if div==10000.:label_str="%.4f"%(self.obj_dict['VALUE'])

		self.label=wx.StaticText(self,sliderID,label_str,size=self.button_size)
		self.sbsizer.Add(self.label)

		#wx.EVT_BUTTON(self.defaultB,self.defaultBID,self.defaultCB)
		wx.EVT_SCROLL(self.widget,self.SliderCB)

	def SetupColourDialog(self):
		colordata=wx.ColourData()
		colordata.SetChooseFull(True)
		colordata.SetColour(wx.Colour(self.obj_dict['VALUE'][0],self.obj_dict['VALUE'][1],self.obj_dict['VALUE'][2]))
		self.widget=wx.ColourDialog(self,colordata)

		showColourDialogBID=wx.NewId()
		self.showColourDialogB=wx.Button(self,showColourDialogBID,"ShowDialog",size=self.button_size)
		self.showColourDialogB.SetBackgroundColour(wx.Colour(self.obj_dict['VALUE'][0],self.obj_dict['VALUE'][1],self.obj_dict['VALUE'][2]))
		self.sbsizer.Add(self.showColourDialogB)
		wx.EVT_BUTTON(self.showColourDialogB,showColourDialogBID,self.ShowColourDialogCB)

		label_str=''
		self.label=wx.StaticText(self,wx.NewId(),label_str,size=self.button_size)
		self.label.SetLabel(str(self.obj_dict['VALUE']))
		self.sbsizer.Add(self.label)

		self.defaultB.SetBackgroundColour(self.obj_dict['DEFAULT'])

	def FitImg(self,png,size):
		dx=size[0]
		dy=size[1]
		aspect=float(dx)/float(dy)

		img_dx=png.GetWidth()
		img_dy=png.GetHeight()
		img_aspect=float(img_dx)/float(img_dy)

		if img_aspect>1:
			#print 'img_aspect>1'
			new_dx=dx
			new_dy=int(dx/float(img_aspect))
			png=png.Scale(new_dx,new_dy)

		else:
			#print 'img_aspect<=1'
			new_dy=dy
			new_dx=int(dy*float(img_aspect))
			png=png.Scale(new_dx,new_dy)

		return png



	def SetupComboBox(self):
		cbID=wx.NewId()
		path=os.path.join(self.env.sitepkgdir,self.obj_dict['PATH'])
		cb_choices=os.listdir(path)
		self.widget=wx.ComboBox(self,cbID,size=self.button_size,choices=cb_choices)

		self.widget.SetValue(self.obj_dict['VALUE'])
		self.sbsizer.Add(self.widget)
		wx.EVT_COMBOBOX(self,cbID,self.ComboCB)

		fname=os.path.abspath(os.path.join(self.env.sitepkgdir,self.obj_dict['PATH'],self.obj_dict['VALUE']))
		png=wx.Image(fname,wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		png=png.ConvertToImage()
		#print dir(png)
		png=self.FitImg(png,(200,200))
		png=png.ConvertToBitmap()
		self.bmp=wx.StaticBitmap(self,-1,png)
		self.sbsizer.Add(self.bmp)
		#print self.bmp.Size
		self.sbsizer.AddSpacer(200-self.bmp.Size[0])

	def SetupSpinCtrl(self):
		SpinCtrlID=wx.NewId()
		self.widget=wx.SpinCtrl(self,SpinCtrlID,size=self.button_size)
		self.widget.SetRange(self.obj_dict['MIN'],self.obj_dict['MAX'])
		self.widget.SetValue(int(self.obj_dict['VALUE']))
		self.sbsizer.Add(self.widget)
		wx.EVT_SPINCTRL(self.widget,SpinCtrlID,self.SpinCtrlCB)

		label_str=''
		self.label=wx.StaticText(self,wx.NewId(),label_str,size=self.button_size)
		self.label.SetLabel(str(self.obj_dict['VALUE']))
		self.sbsizer.Add(self.label)

	def SpinCtrlCB(self,evt):
		value_str="%02d"%(self.widget.GetValue())
		self.label.SetLabel(value_str)

	def SliderCB(self,evt):
		#if DEBUG:print 'SliderCB: ',self.widget.GetValue()
		div=self.obj_dict['DIVISOR']
		if div==1.:label_str="%.0f"%(self.widget.GetValue()/self.obj_dict['DIVISOR'])
		if div==10.:label_str="%.1f"%(self.widget.GetValue()/self.obj_dict['DIVISOR'])
		if div==100.:label_str="%.2f"%(self.widget.GetValue()/self.obj_dict['DIVISOR'])
		if div==1000.:label_str="%.3f"%(self.widget.GetValue()/self.obj_dict['DIVISOR'])
		if div==10000.:label_str="%.4f"%(self.widget.GetValue()/self.obj_dict['DIVISOR'])
		self.label.SetLabel(label_str)

	def ShowColourDialogCB(self,e):
		if self.widget.ShowModal()==wx.ID_OK:pass
		else:return
		self.label.SetLabel(str(self.obj_dict['VALUE']))
		self.showColourDialogB.SetBackgroundColour(self.widget.GetColourData().GetColour().Get())

	def CheckBoxCB(self,e):
		if self.widget.GetValue():value_str="On"
		else:value_str="Off"
		self.label.SetLabel(value_str)

	def ComboCB(self,e):
		newval=self.widget.GetValue()
		fname=os.path.abspath(os.path.join(self.env.sitepkgdir,self.obj_dict['PATH'],newval))
		png=wx.Image(fname,wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		png=png.ConvertToImage()
		png=self.FitImg(png,(200,200))
		png=png.ConvertToBitmap()

		self.bmp.SetBitmap(png)

	def DefaultCB(self,e):

		self.Layout()

		if False:pass
		elif self.obj_dict['WTYPE']=='wx.ColourDialog':
			self.obj_dict['VALUE']=self.obj_dict['DEFAULT']
			self.label.SetLabel(str(self.obj_dict['VALUE']))

			c=wx.Colour(self.obj_dict['DEFAULT'][0],self.obj_dict['DEFAULT'][1],self.obj_dict['DEFAULT'][2]);
			colordata=wx.ColourData()
			colordata.SetChooseFull(True)
			colordata.SetColour(c)
			self.widget=wx.ColourDialog(self,colordata)
			self.showColourDialogB.SetBackgroundColour(self.obj_dict['VALUE'])

		elif self.obj_dict['WTYPE']=='wx.ComboBox':
			self.widget.SetValue(self.obj_dict['VALUE'])
			self.ComboCB(None)

		elif self.obj_dict['WTYPE']=='wx.Slider':
			self.widget.SetValue(int(self.obj_dict['DEFAULT']*self.obj_dict['DIVISOR']))
			self.SliderCB(None)

		elif self.obj_dict['WTYPE']=='wx.SpinCtrl':
			self.widget.SetValue(int(self.obj_dict['DEFAULT']))
			self.SpinCtrlCB(None)

		elif self.obj_dict['wtype']=='wx.CheckBox':
			self.widget.SetValue(int(self.obj_dict['default']))
			self.CheckBoxCB(None)


	def update(self):
		if self.obj_dict['WTYPE']=='wx.ComboBox':
			self.obj_dict['VALUE']=str(self.widget.GetValue())

		elif self.obj_dict['WTYPE']=='wx.SpinCtrl':
			self.obj_dict['VALUE']=int(self.widget.GetValue())#was float
			#if DEBUG:print 'VALUE=',self.obj_dict['VALUE'],self.label.GetLabel()

		elif self.obj_dict['WTYPE']=='wx.Slider':
			self.obj_dict['VALUE']=float(self.widget.GetValue())/self.obj_dict['DIVISOR']#was float
			#if DEBUG:print 'VALUE=',self.obj_dict['VALUE'],self.label.GetLabel()

		elif self.obj_dict['WTYPE']=='wx.CheckBox':
			self.obj_dict['VALUE']=int(self.widget.GetValue())
			#if DEBUG:print 'VALUE=',self.obj_dict['VALUE'],self.label.GetLabel()

		elif self.obj_dict['WTYPE']=='wx.ColourDialog':
			#LEAVE OFF: @default need to SetColourData -- need refer to wx API...TBC.
			data=self.widget.GetColourData()
			#print data,dir(data)
			#print data.GetColour(),data.GetColour().Get()
			#print type(data.GetColour().Get())
			t=data.GetColour().Get()
			self.obj_dict['VALUE']=(t[0],t[1],t[2])
			#print t[0],t[1],t[2]
			self.label.SetLabel(str(self.obj_dict['VALUE']))
