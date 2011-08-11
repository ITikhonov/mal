from sys import argv
from binascii import b2a_hex
from hashlib import md5
from struct import pack

def encode_name(x):
	return 'vm_'+b2a_hex(x.encode('utf-8')).decode('utf8')


class Int:
	def __init__(_,x): _.val=int(x)
	def __repr__(_): return "%s(%s)"%(_.__class__.__name__,_.val,)

class Name:
	def __init__(_,x): _.name=x
	def __repr__(_): return "%s(%s)"%(_.__class__.__name__,_.name,)
	def hash(_): return 'vm_'+_.__class__.__name__+'_'+md5(_.name.encode('utf8')).hexdigest()

class Call(Name): pass
class Str(Name): pass

class PrefixName(Name):
	def __init__(_,x): _.name=x[1:]

class Label(PrefixName): pass
class Ret: pass



def scan(x):
	if x.isdigit():		return Int(x)
	if x.startswith(':'):	return Label(x)
	if x.startswith('"'):	return Str(x)
	if x==";":		return Ret()
	return Call(x)

def scan_str(x,text):
	while not x.name.endswith('"'):
		z=text.pop(0)
		x.name=x.name+' '+z
	x.name=x.name[1:-1]
	return x

def parse_def(text,this):
	d=[]
	while True:
		x=scan(text.pop(0))
		if type(x)==Ret: return d
		if type(x)==Str: x=scan_str(x,text)
		d.append(x)

def parse(text):
	defs={}
	while text:
		x=scan(text.pop(0))
		if type(x)==Label:
			defs[x.name]=parse_def(text,x)
		else: raise
	return defs

def external(defs):
	exts={}
	for x,y in defs.items():
		for z in y:
			if type(z)==Call and (z.name not in defs):
				if z.name in exts: exts[z.name].append(x)
				else: exts[z.name]=[x]
	return exts

def strings(defs):
	strs={}
	for x,y in defs.items():
		for z in y:
			if type(z)==Str and (z.name not in strs):
				strs[z.name]=z
	return strs


def compile_output(x):
	print(x)

def compile_def(x,y):
	compile_output(encode_name(x)+': # '+x)
	for z in y:
		if type(z)==Call: compile_output('	call '+encode_name(z.name) + ' # '+z.name)
		elif type(z)==Str:
			compile_output('	call '+encode_name('dup')+' # dup')
			compile_output('	movl $'+z.hash() + ',%eax # "'+z.name+'"')
		elif type(z)==Int:
			compile_output('	call '+encode_name('dup')+' # dup');
			compile_output('	movl $'+str(z.val) + ',%eax # '+str(z.val))
		else: raise Exception(str(z))
	compile_output('	ret')

def compile_str(x):
	compile_output('%s: .asciz "%s"'%(x.hash(),x.name))
	

def compile(defs):
	compile_output(".text")
	compile_output(".global "+encode_name('main'))
	for x in defs.items():
		compile_def(*x)
	for x,y in strings(defs).items():
		compile_str(y)

	compile_output('# externals')
	for x in external(defs).keys():
		compile_output('# %s:\t\t# %s'%(encode_name(x),x))
		
			
try:
	text=open(argv[1]).read().split()
except:
	x=argv[1]
	print(encode_name(x)+': # '+x)
	exit(0)

defs=parse(text)
compile(defs)

