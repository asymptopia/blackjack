"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@gmail.com

    Copyright       :(C) 2006-2008 Asymptopia Software

    License         :GPL2

***********************************************************/
"""
import os,sys,string,time,types

def format_dict(d,level):
	
	cfg="{\n"
	
	keys=d.keys()
	keys.sort()
	for idx in range(len(keys)):
		 key=keys[idx]
		 if isinstance(d[key],types.ListType):
		 	cfg="%s%s\'%s\':%s,\n"%(cfg,(level+1)*'\t',key,format_list(d[key],level+1))
		 elif isinstance(d[key],types.DictType):
		 	cfg="%s%s\'%s\':%s,\n"%(cfg,(level+1)*'\t',key,format_dict(d[key],level+1))
		 elif isinstance(d[key],types.StringType):
		 	cfg="%s%s\'%s\':\'%s\',\n"%(cfg,(level+1)*'\t',key,d[key])
		 else:
		 	cfg="%s%s\'%s\':%s,\n"%(cfg,(level+1)*'\t',key,d[key])
	
	cfg="%s%s}"%(cfg,(level)*'\t')
	
	return cfg


def format_list(l,level):
	
	cfg="[\n"
	
	for idx in range(len(l)):
		if isinstance(l[idx],types.StringType):
			cfg="%s%s\'%s\',\n"%(cfg,(level+1)*'\t',l[idx])
		elif isinstance(l[idx],types.ListType):
			cfg="%s%s%s,\n"%(cfg,(level+1)*'\t',format_list(l[idx],level+1))
		else:
			cfg="%s%s%s,\n"%(cfg,(level+1)*'\t',l[idx])
	cfg="%s%s]"%(cfg,(level)*'\t')
	
	return cfg
