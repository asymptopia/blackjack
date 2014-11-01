#!/usr/bin/env python
"""
/**********************************************************
	
	Organization	:Dona Ana Cycle Salvage
					 915 Dona Ana Rd., Las Cruces, NM 88007
					 (575) 526-8278
	
	Website			:http://www.dacyclesalvage.com
					
    License         :GPLv3

***********************************************************/
"""
import os,sys
APPNAME='bj'

for sitepkgdir in sys.path:
	if sitepkgdir[-13:]=='site-packages':break

rm_path=os.path.join('/var/games/',APPNAME)
if os.path.exists(rm_path):
	cmd="rm -rf %s"%rm_path
	os.system(cmd)

rm_path=os.path.join(sitepkgdir,APPNAME)
if os.path.exists(rm_path):
	cmd="rm -rf %s"%rm_path
	print cmd
	os.system(cmd)

if len(sys.argv)>1 and sys.argv[1]=='uninstall':
	print 'application sucessfully removed.'
	sys.exit()
	
#Added 1/6/08 b/c Macs don't (apparantly) have /var/games by default (some linux distros may not, either)
if not os.path.exists('/var'):os.mkdir('/var')
if not os.path.exists('/var/games'):os.mkdir('/var/games')
if not os.path.exists('/var/games/bj'):os.mkdir('/var/games/bj')

path='/var/games/bj'

cmd="chmod -R 755 /var/games/%s"%(APPNAME)
print cmd
os.system(cmd)

cmd="cp .blackjack_config_master %s"%(path)
print cmd
os.system(cmd)

path=os.path.join(sitepkgdir,APPNAME)
if not os.path.exists(path):os.mkdir(path)

cmd="cp -r %s %s"%(APPNAME,sitepkgdir)
print cmd
os.system(cmd)

cmd="cp blackjack.py /usr/local/bin/blackjack"
print cmd
os.system(cmd)

cmd="chmod -R 755 %s/%s"%(sitepkgdir,APPNAME)
print cmd
os.system(cmd)


##########################################################	
print '**********************************************'
print '*                                            *'
print '*           Setup Complete                   *'
print '*                                            *'
print '* Run: /usr/local/bin/blackjack  -help       *'
print '*                                            *'
print '*      For all your motorcycle needs:        *'
print '*      http://www.dacyclesalvage.com         *'
print '*                                            *'
print '**********************************************'

