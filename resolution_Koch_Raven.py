import os
#os.chdir(r"C:\Users\nige\Documents\Postdoc\Projects\Phase retrieval")
import numpy as np
import matplotlib.pyplot as plt

FocalLength = 105  # mm
WD = 417  # mm
ObjectSize = 44.5  # mm

lambda_nm = 535  # nm
n_air = 1  # refractive index assumed to be air
n_sc = 1.6  # refractive index of CsI
n_sc = 1.84  # refractive index of CsI

T_arr = [3, 5, 10, 15,20,25,30, 50, 75, 100, 200]  # thickness of scintillator in µm
T_arr = [10, 15,20,25,30, 35]  # thickness of scintillator in µm

NA = np.sin(np.arctan(ObjectSize / (2 * (WD - FocalLength)))) * n_air

NA = 0.6

p90 = 0.7  # µm
p50 = 0.18  # FWHM
q90 = 0.28  # µm
q50 = 0.075  # FWHM

plt.figure()
#plt.hold(True)
for T in T_arr:
    R = lambda NA_l: np.sqrt((p90 / NA_l) ** 2 + (q90 * T * NA_l) ** 2)
    plt.plot(np.linspace(0.01, 0.8, 100), R(np.linspace(0.01, 0.8, 100)), label=f'T = {T} µm')
plt.ylim([0, 2])
plt.ylabel('Resolution [µm FW90%M]')
plt.xlabel('Numerical Aperture')
plt.title('Res 90')
#plt.hold(False)
plt.legend()

#%%

plt.figure()
#plt.hold(True)
for T in T_arr:
    R = lambda NA_l: np.sqrt((p50 / NA_l) ** 2 + (q50 * T * NA_l) ** 2)
    plt.plot(np.linspace(0.01, 1.0, 100), R(np.linspace(0.01, 0.8, 100)), label=f'T = {T} µm')
plt.ylim([0, 10])
#plt.xlim([0, 1.0])
plt.ylabel('Resolution [µm FWHM]')
plt.xlabel('Numerical Aperture')
plt.title('Res 50')
#plt.hold(False)
plt.legend()

#%%
z_opt = lambda Res: 1 / (2 * p50 * q50) * Res ** 2
NA_opt = lambda Res: np.sqrt(2) * p50 / Res

plt.figure()
plt.plot(np.linspace(0.01, 2, 100), z_opt(np.linspace(0.01, 2, 100)))
plt.ylabel('Scintillator thickness]')
plt.xlabel('Resolution [µm]')
plt.ylim([0, 100])

#%%

FocalLength = 60
WD = 1116.8
ObjectSize = 860
T = 2600
T2 = 600
NA = np.sin(np.arctan(ObjectSize / (2 * (WD - FocalLength)))) * n_air
R = lambda NA_l: np.sqrt((p90 / NA_l) ** 2 + (q90 * T * NA_l) ** 2)
plt.figure()
plt.plot(np.linspace(0, 0.5, 100), R(np.linspace(0, 0.5, 100)), label=f'T = {T} µm', linewidth=2, linestyle='-', color='r')
#plt.hold(True)
R = lambda NA_l: np.sqrt((p50 / NA_l) ** 2 + (q50 * T * NA_l) ** 2)
plt.plot(np.linspace(0, 0.5, 100), R(np.linspace(0, 0.5, 100)), label=f'T = {T} µm', linewidth=2, linestyle='--', color='r')
R = lambda NA_l: np.sqrt((p90 / NA_l) ** 2 + (q90 * T2 * NA_l) ** 2)
plt.plot(np.linspace(0, 0.5, 100), R(np.linspace(0, 0.5, 100)), label=f'T = {T2} µm', linewidth=2, linestyle='-', color='b')
R = lambda NA_l: np.sqrt((p50 / NA_l) ** 2 + (q50 * T2 * NA_l) ** 2)
plt.plot(np.linspace(0, 0.5, 100), R(np.linspace(0, 0.5, 100)), label=f'T = {T2} µm', linewidth=2, linestyle='--', color='b')
plt.ylim([0, 200])
plt.ylabel('Resolution [µm FW90%M/FWHM]')
plt.xlabel('Numerical Aperture')
#plt.hold(False)
plt.legend()


#%%
f = 60  # mm
A = f / 4  # aperture on 60/4 lens
s0 = 1116  # mm image distance

DOF = lambda d: 2 * A * d * s0 * (s0 - f) * f ** 2 / (f ** 4 - A ** 2 * d ** 2 * s0 ** 2)

plt.figure()
plt.plot(np.linspace(5e-3, 1e-1, 100), DOF(np.linspace(5e-3, 1e-1, 100)))
#%%
mu_luag_15keV = 78.5  # cm2/g
mu_luag_20keV = 37
dens_luag = 6.71  # g/cm3
lambda_luag = 540  # nm
n_luag = 1.84
refl = 0.1
Res = 1.4
eta_ly = 20 / 10 * 160  # 20keV

IM411_pp = 3.76  # micrometer
L_mag = 5.4
trans = 1
eta_vqe = 0.9
NA = 0.6
dif_lim = 0.61 * lambda_luag / 1000 / NA

delta = 0.61 * lambda_luag / NA / 1e3

eta_xqe = lambda d: 1 - np.exp(-mu_luag_20keV * dens_luag * d / 10000)

d_opt = lambda NA_sim: (lambda_luag / 1000) * n_luag / NA_sim ** 2 + n_luag * IM411_pp / (L_mag * NA_sim)

plt.figure()
plt.plot(np.linspace(0.2, 0.8, 100), d_opt(np.linspace(0.2, 0.8, 100)))

eta_ce = lambda NA_sim: 0.5 * (1 - np.sqrt(1 - (NA_sim / n_luag) ** 2)) * trans * (1 + refl)

DQE = lambda NA_sim: eta_xqe(d_opt(NA_sim)) / (1 + 1 / (eta_ly * eta_ce(NA_sim) * eta_vqe))

plt.figure()
plt.plot(np.linspace(0.1, 0.8, 100), DQE(np.linspace(0.1, 0.8, 100)))
print(eta_xqe(d_opt(NA)))
print(NA)


#%% 
# Calculate number of lenses 

# at 20 keV, density 6.71, thickness is 0.001 cm, np.exp(-3.70E+01*6.71*0.001)=0.78. how do i get -3.70


os.chdir(r"C:\Users\nige\OneDrive - Danmarks Tekniske Universitet\Dokumenter\PhD\XRR_Fitting_tool")
from optical_constants import oc
from unit_conversion import wavelength2energy, energy2wavelength, thickness2energy, energy2thickness

energy = np.arange(1,50,0.1) # [keV], Incident energy 
density = 6.71 # g/cm**3
T = 0.003 # thickness, cm
elements = ['Lu','Al','O']#,"Ce"] # Lu3 Al5 O12 (cerium)
number_of_atoms = [3,5,12]#,1]
oc_source = "oc_source/LLNL/"

wavelength = energy2wavelength(energy*10**3) # nm
n = oc(wavelength,density,number_of_atoms,elements, oc_source)      

i_i0 = np.exp((-4*np.pi*np.imag(n)*T) /  (wavelength*10**(-7))) # I/I0 attenuation


fig, (ax1) = plt.subplots(nrows=1, ncols=1,figsize=(6,4.5))
fig.tight_layout(pad=3.0)
ax1.plot(energy,1-i_i0,'k-',label ='*')
ax1.set_ylabel("Absorption [%]")
ax1.set_xlabel("Energy [keV]")
#ax1.set_yscale('log')
#ax1.set_xscale("log")



#%% For paper: luag_energy_vs_absorption

energy = np.arange(1,40,0.1) # [keV], Incident energy 
T = np.arange(0.001,0.0040,0.0005) # thickness, cm
T = [0.0015,0.0020,0.0025,0.0030,0.0035,0.005,0.01] # thickness, cm
#T = [10, 15,20,25,30, 35]  # thickness of scintillator in µm

density = 6.73 # g/cm**3
elements = ['Lu','Ce','Al','O',] # Lu3 Al5 O12 (cerium)
number_of_atoms = [2.9,0.01,5,12]
oc_source = "oc_source/LLNL/"

wavelength = energy2wavelength(energy*10**3) # nm
n = oc(wavelength,density,number_of_atoms,elements, oc_source)      

i_i0=np.empty((len(energy), len(T))) 
for i in range(len(T)):
    i_i0[:,i] = np.exp((-4*np.pi*np.imag(n)*T[i]) /  (wavelength*10**(-7))) # I/I0 attenuation



fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(6, 4.5))

# Plot data
ax1.plot(energy, 1 - i_i0, '-', label='*')

# Axis labels with larger font
ax1.set_ylabel("Absorption (%)", fontsize=14)
ax1.set_xlabel("Energy (keV)", fontsize=14)
plt.title(r"Lu$_{2.99}$Al$_5$O$_{12}$Ce$_{0.01}$")
# Axis tick labels with larger font
ax1.tick_params(axis='both', labelsize=12)

# Grid on
ax1.grid(True)

# Legend with upright micrometer symbol
ax1.legend((
    '15 µm',
    '20 µm',
    '25 µm',
    '30 µm',
    '35 µm',
    '50 µm',
    '100 µm'
), handlelength=3, fontsize=12)

# Tight layout
fig.tight_layout(pad=1.5)

plt.show()


#%%
fig2, ax1 = plt.subplots(figsize=(6, 4.5))
ax1.plot(energy, 1 - i_i0, '-', label='*')
ax1.set_xlabel("Energy (keV)", fontsize=14)
ax1.set_ylabel("Absorption (%)", fontsize=14)

# Tick font sizes
ax1.tick_params(axis='both', labelsize=12)

# Grid and legend
ax1.grid(True)
ax1.legend((
    '15 µm',
    '20 µm',
    '25 µm',
    '30 µm',
    '35 µm',
    '50 µm',
    '100 µm'
), handlelength=3, fontsize=12)

# Consistent layout
fig2.tight_layout(pad=1.5)
plt.show()
#%%
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# LENS SYSTEM PARAMETERS
# -----------------------------
FocalLength = 105  # [mm] Focal length of the lens
WD = 417  # [mm] Working distance from object to lens
ObjectSize = 44.5  # [mm] Object field diameter (used to estimate NA)
#NA = np.sin(np.arctan(ObjectSize / (2 * (WD - FocalLength)))) * 1  # n_air = 1

# Wavelength of LuAG emission light (typically green)
lambda_nm = 535  # [nm] (LuAG:Ce emits around 520–550 nm)

# Numerical aperture (NA) – determines resolving power of the optical system
# Calculated from geometry, but overridden below
NA = 0.6  # Override with a realistic fixed value

# -----------------------------
# SCINTILLATOR PARAMETERS
# -----------------------------
# Refractive index of LuAG:Ce
n_sc = 1.84  # Close to CsI; minor variation

# Scintillator thickness values [µm]
T_arr = [15, 20, 25, 30, 35, 50 ,100]

# -----------------------------
# RESOLUTION MODEL PARAMETERS FOR LuAG
# -----------------------------
# These values are estimated for LuAG:Ce, which has less lateral spread than CsI

# For 90% full-width resolution (FW90%M)
p90 = 0.5   # [µm] diffraction term (LuAG has slightly sharper PSF)
q90 = 0.12  # [1/(µm·NA)] reduced light spread vs CsI

# For 50% full-width resolution (FWHM)
p50 = 0.12  # [µm]
q50 = 0.03  # [1/(µm·NA)]

# -----------------------------
# PLOT FW90%M RESOLUTION (Res 90)
# -----------------------------
plt.figure()
NA_vals = np.linspace(0.01, 0.8, 100)

for T in T_arr:
    def R_90(NA_l): return np.sqrt((p90 / NA_l) ** 2 + (q90 * T * NA_l) ** 2)
    plt.plot(NA_vals, R_90(NA_vals), label=f'T = {T} µm')

plt.ylim([0, 2])
plt.xlabel('Numerical Aperture (NA)')
plt.ylabel('Resolution [µm] (FW90%M)')
plt.title('LuAG Scintillator Resolution vs NA (90% Width)')
plt.legend()
plt.grid(True)

#%%
'''
# -----------------------------
# PLOT FWHM RESOLUTION (Res 50)
# -----------------------------
plt.figure(figsize=(6, 4.5))
for T in T_arr:
    def R_50(NA_l): return np.sqrt((p50 / NA_l) ** 2 + (q50 * T * NA_l) ** 2)
    plt.plot(NA_vals, R_50(NA_vals), label=f' {T} µm')

plt.xlim([0.5, 0.8])  # Set x-axis limits
plt.ylim([0, 2.5])      # y-axis as before

# For paper
# Axis labels with larger font
plt.xlabel('Numerical Aperture', fontsize=14)
plt.ylabel('FWHM Resolution (µm)', fontsize=14)

# Title
#plt.title('LuAG Scintillator Resolution vs NA (FWHM)', fontsize=16)

# Increase tick label sizes
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Optional: update legend font size
plt.legend(fontsize=12)

# Grid remains
plt.grid(True)

plt.tight_layout(pad=1.5)

plt.show()

'''
# for paper:
# Create consistent figure
fig1, ax1 = plt.subplots(figsize=(6, 4.5))

for T in T_arr:
    def R_50(NA_l): return np.sqrt((p50 / NA_l) ** 2 + (q50 * T * NA_l) ** 2)
    plt.plot(NA_vals, R_50(NA_vals), label=f' {T} µm')
ax1.set_xlim([0.5, 0.8]) 
ax1.set_ylim([0, 2.5]) 
#ax1.x_lim([0.5, 0.8])  # Set x-axis limits
#ax1.y_lim([0, 2.5])      # y-axis as before


ax1.set_xlabel('Numerical Aperture', fontsize=14)
ax1.set_ylabel('FWHM Resolution (µm)', fontsize=14)

# Tick sizes
ax1.tick_params(axis='both', labelsize=12)

# Legend
ax1.legend(fontsize=12)

# Grid and layout
ax1.grid(True)
fig1.tight_layout(pad=1.5)
plt.show()



#%% 


energy = np.arange(1,40,0.1) # [keV], Incident energy 
T = np.arange(0.001,0.0040,0.0005) # thickness, cm
T = [0.0015,0.0030] # thickness, cm
#T = [10, 15,20,25,30, 35]  # thickness of scintillator in µm

density = 7.08 # g/cm**3
elements = ['Gd','Ga','O','Eu'] # Lu3 Al5 O12 (cerium)
number_of_atoms = [3,5,12,0.3]
oc_source = "oc_source/LLNL/"

wavelength = energy2wavelength(energy*10**3) # nm
n = oc(wavelength,density,number_of_atoms,elements, oc_source)      

i_i0=np.empty((len(energy), len(T))) 
for i in range(len(T)):
    i_i0[:,i] = np.exp((-4*np.pi*np.imag(n)*T[i]) /  (wavelength*10**(-7))) # I/I0 attenuation



fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(6, 4.5))

# Plot data
ax1.plot(energy, 1 - i_i0, '-', label='*')

# Axis labels with larger font
ax1.set_ylabel("Absorption (%)", fontsize=14)
ax1.set_xlabel("Energy (keV)", fontsize=14)
plt.title(r"Gd$_3$Ga$_5$O$_{12}$Eu$_{0.3}$")
# Axis tick labels with larger font
ax1.tick_params(axis='both', labelsize=12)

# Grid on
ax1.grid(True)

# Legend with upright micrometer symbol
ax1.legend((
    '15 µm',
    '30 µm',
), handlelength=3, fontsize=12)

# Tight layout
fig.tight_layout(pad=1.5)

plt.show()
