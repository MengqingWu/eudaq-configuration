# JTAG files generator
# calculates DAC values for different S/N cuts (3 to 12) and generates JTAG (txt) files, update creation date
# by Jan Dreyling-Eschweiler, telescope-coor@desy.de
# First version: 4. September 2015
# -----------------------

# modules
import re
import math
import numpy as np
import time

##################################################
# hard code data

input_file = "../default_jtag.txt" 
sensor_name = "7b"

# Middlepoints in DAC
IVDREF2  = 100 
IVDREF1A = 118
IVDREF1B = 121
IVDREF1C = 145
IVDREF1D = 141

# Thermal noise: TN
THN_matA = 1.053
THN_matB = 1.008
THN_matC = 1.021
THN_matD = 0.9382

# Fixed pattern noise: FPN
FPN_matA = 0.4062
FPN_matB = 0.3832
FPN_matC = 0.5435
FPN_matD = 0.483

# Offset
OFF_matA = 0.5552
OFF_matB = 0.2977
OFF_matC = 0.2768
OFF_matD = 0.3896

# slope stays constant
DAC_slope = 0.25

##################################################
# Calculations

# Offset in DAC units
IVDREF1A_offset = -(IVDREF1A * DAC_slope) 
IVDREF1B_offset = -(IVDREF1B * DAC_slope) 
IVDREF1C_offset = -(IVDREF1C * DAC_slope) 
IVDREF1D_offset = -(IVDREF1D * DAC_slope) 

# total noise
TON_matA = math.sqrt(THN_matA**2 + FPN_matA**2) 
TON_matB = math.sqrt(THN_matB**2 + FPN_matB**2) 
TON_matC = math.sqrt(THN_matC**2 + FPN_matC**2) 
TON_matD = math.sqrt(THN_matD**2 + FPN_matD**2) 
TON_avg = (TON_matA + TON_matB + TON_matC + TON_matD) / 4
#print TON_matA, TON_matB, TON_matC, TON_matD

# Sigma to noise cut
SN = np.array([3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

# mV value 
VmV_matA = (TON_matA * SN) + OFF_matA
VmV_matB = (TON_matB * SN) + OFF_matB
VmV_matC = (TON_matC * SN) + OFF_matC
VmV_matD = (TON_matD * SN) + OFF_matD
#print VmV_matA, VmV_matB, VmV_matC, VmV_matD

# DAC value
DAC_matA = (VmV_matA - IVDREF1A_offset) / DAC_slope # np.rint
DAC_matB = (VmV_matB - IVDREF1B_offset) / DAC_slope
DAC_matC = (VmV_matC - IVDREF1C_offset) / DAC_slope
DAC_matD = (VmV_matD - IVDREF1D_offset) / DAC_slope
#print DAC_matA, DAC_matB, DAC_matC, DAC_matD
#print str(int(round(DAC_matA[i]))), str(int(round(DAC_matB[i]))), str(int(round(DAC_matC[i]))), str(int(round(DAC_matD[i])))

# Adjust DAC values
# -----------------

# e.g. DAC-vlaues (XXX) of plane 0
# line 26: XXX ; :BIAS_DAC[0][10] --> IVDREF1D
# line 27: XXX ; :BIAS_DAC[0][11] --> IVDREF1C
# line 28: XXX ; :BIAS_DAC[0][12] --> IVDREF1B
# line 29: XXX ; :BIAS_DAC[0][13] --> IVDREF1A
# line 30: XXX ; :BIAS_DAC[0][14] --> IVDREF2

for i, n in enumerate(SN):
  #print i, n

  output_file = "chip" + str(sensor_name) + "_thresh" + str(SN[i]) + ".txt" 
  print "Write file:",  output_file

  # IVDREF2
  with open(input_file, "r") as sources:
      lines = sources.readlines()
  with open(output_file, "w") as sources:
      for line in lines:
          sources.write(re.sub(r'^(.*?)BIAS_DAC\[.\]\[14\]', str(IVDREF2) + ' ; :BIAS_DAC[0][14]', line))

  # IVDREF1A
  with open(output_file, "r") as sources:
      lines = sources.readlines()
  with open(output_file, "w") as sources:
      for line in lines:
          sources.write(re.sub(r'^(.*?)BIAS_DAC\[.\]\[13\]', str(int(round(DAC_matA[i]))) + ' ; :BIAS_DAC[0][13]', line))

  # IVDREF1B
  with open(output_file, "r") as sources:
      lines = sources.readlines()
  with open(output_file, "w") as sources:
      for line in lines:
          sources.write(re.sub(r'^(.*?)BIAS_DAC\[.\]\[12\]', str(int(round(DAC_matB[i]))) + ' ; :BIAS_DAC[0][12]', line))

  # IVDREF1C
  with open(output_file, "r") as sources:
      lines = sources.readlines()
  with open(output_file, "w") as sources:
      for line in lines:
          sources.write(re.sub(r'^(.*?)BIAS_DAC\[.\]\[11\]', str(int(round(DAC_matC[i]))) + ' ; :BIAS_DAC[0][11]', line))

  # IVDREF1D
  with open(output_file, "r") as sources:
      lines = sources.readlines()
  with open(output_file, "w") as sources:
      for line in lines:
          sources.write(re.sub(r'^(.*?)BIAS_DAC\[.\]\[10\]', str(int(round(DAC_matD[i]))) + ' ; :BIAS_DAC[0][10]', line))

  # date and time
  with open(output_file, "r") as sources:
      lines = sources.readlines()
  with open(output_file, "w") as sources:
      for line in lines:
          sources.write(re.sub(r'^\#JTAG\_MS(.*?)$', '#JTAG_MS ' + time.strftime("%c"), line))

# summary
print "Total noise average of sensor", str(sensor_name), "-->", TON_avg 


exit()