# Getting System Information in Linux using Python script
# SANCFIS CODING ACEDEMY SNIPPET
# Dependencies : distro;

import platform

# Architecture
print("Architecture: " + platform.architecture()[0])

# Machine
print("Machine: " + platform.machine())

# Node
print("Node: " + platform.node())

# System
print("System: " + platform.system())

# Processor
# Processor information is stored in cpuinfo file. Read the file and count the number and model name of the processor.
print("Processors: ")
with open("/proc/cpuinfo", "r")  as f:
    info = f.readlines()

cpuinfo = [x.strip().split(":")[1] for x in info if "model name"  in x]
for index, item in enumerate(cpuinfo):
    print("    " + str(index) + ": " + item)

# Memory
print("Memory Info: ")
with open("/proc/meminfo", "r") as f: # Reading standar file with Python
    lines = f.readlines()

print("     " + lines[0].strip())
print("     " + lines[1].strip())