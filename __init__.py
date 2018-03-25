#!/usr/bin/python3

import sys
import subprocess
import term

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def command(s):
	return term.format(s, term.magenta)

def uri(s):
	return term.format(s, term.white)

def ok(s):
	return term.format(s, term.green)

def info(s):
	return term.format(s, term.blue)

def warning(s):
	return term.format(s, term.yellow)

def error(s):
	return term.format(s, term.red)

class RunError(Exception):
	def __init__(self, cmd, cmd_str, process, output, error_output):
		self.cmd = cmd
		self.cmd_str = cmd_str
		self.process = process
		self.output = output
		self.error_output = error_output
	
	def __str__(self):
		return (error(" [ERROR]") + " " + command(self.cmd_str) + " -> " + error(self.process.returncode) + "\n" + error(self.error_output))
		

def run(cmd, cmd_str=None, error_fatal=True):
	if cmd_str == None:
		cmd_str = cmd
	term.saveCursor()
	print(" [ ? ]   " + command(cmd_str), flush=True)
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	output, error_output = process.communicate()
	output = output.decode("ascii")
	error_output = error_output.decode("ascii")
	
	if process.returncode == None:
		raise "Undefined return code after execution!"
	elif process.returncode == 0:
		term.restoreCursor()
		print(ok(" [OK]") + "   ", flush=True)
		eprint(error_output, end="", flush=True)
		return output
	else:
		term.restoreCursor()
		if error_fatal:
			print(error(" [ERROR]") + " " + command(cmd_str) + " -> " + error(process.returncode), flush=True)
			eprint(error(error_output), end="", flush=True)
			raise(RunError(cmd, cmd_str, process, output, error_output))
		else:
			print(warning(" [WARN]") + "  " + command(cmd_str) + " -> " + error(process.returncode), flush=True)
			eprint(warning(error_output), end="", flush=True)
			return None

def test():
	run("ls")
	run("lss", error_fatal=False)
	run("lss")
