"""
nerveOSC messages

format:
token types:
	path/value 
	time - @time
	env - {name:value, name:value}

implementing only path and value for now

"""
import socket

def parse(nerveOSC_str):
	nerveOSC_l = nerveOSC_str.split(" ")
	path = None
	host = None
	innerpath = ""
	value = None
	time = None
	env = None
	for token in nerveOSC_l:
		if token[0] == "/":
			path = token
		if token[0] == "@":
			time = token
		if token[0] == "{":
			env = token
	path_l = path.split("/")
	value  = path_l[-1:][0]
	# replace w/ join or other string function
	innerpath = "/"+"/".join(path_l[1:-1])
	path = "/"+"/".join(path_l[1:])
	return {
		"host":path_l[1],
		"path":path,
		"innerpath":innerpath,
		"value":value,
		"time":time,
		"env":env
	}

def assemble(innerpath, value):
	return "/%s%s/%s" % (socket.gethostname(),innerpath,str(value))
