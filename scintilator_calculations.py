import os
# Change to your local directory:
os.chdir(r"C:\Users\nige\OneDrive - Danmarks Tekniske Universitet\Dokumenter\Postdoc\Projects\Phase retrieval\GitHub")


from phase_retrieval_functions import *
from optical_constants import oc





# Constants
E_photon_keV = 19.55  # Photon energy in keV
keV_to_J = 1.60218e-16  # Conversion factor from keV to Joules
flux = 5.25e10  # Photon flux in photons/s
density = 6710  # Density of LuAg in kg/m^3
C_p = 0.419  # Specific heat capacity in J/g·K
thickness = 20e-6  # Thickness of the scintillator in meters 20 micrometer
h = 6.62607015e-34  # Planck's constant in J·s
c = 299792458  # Speed of light in m/s
d_beam = 11e-3  # Diameter of the beam in meters (11 mm)
elements_LuAg = ['Lu','Al','O'] #  Lu3Al5O12
number_of_atoms_LuAg = [3,5,12]
oc_source = r"oc_source/NIST/"
wavelength_LuAg = energy2wavelength(E_photon_keV*10**3) # nm
n_LuAg = oc(wavelength_LuAg,density*1e-3,number_of_atoms_LuAg,elements_LuAg, oc_source)   

beta = n_LuAg.imag#.25570345e-7  # Imaginary part of refractive index
#%%








# Step 1: Calculate photon energy in Joules
E_photon_J = E_photon_keV * keV_to_J

# Step 2: Calculate the wavelength of the X-ray
wavelength = h * c / E_photon_J

# Step 3: Calculate the absorption coefficient (mu)
mu = (4 * math.pi * beta) / wavelength

# Step 4: Calculate power delivered by the beam
P_beam = flux * E_photon_J  # Power in Watts

# Step 5: Calculate energy absorbed by the scintillator (assuming e^(-mu * d) for simplicity)
E_abs = P_beam * (1 - mu * thickness)  # Simplified absorption model

# Step 6: Calculate the area of the beam (which interacts with the scintillator)
A_beam = math.pi * (d_beam / 2) ** 2  # Area in m^2

# Step 7: Calculate the mass of the scintillator
mass = density * A_beam * thickness  # Mass in kg

# Step 8: Calculate the temperature increase
delta_T = E_abs / (mass * C_p * 1e3)  # Convert specific heat capacity to J/kg·K

# Step 9: Calculate energy absorbed per unit mass (Delta E)
delta_E = E_abs / (mass * 1e3)  # J/g

# Step 10: Calculate temperature coefficient
alpha = delta_T / delta_E

# Step 11: Calculate percentage of the beam absorbed by the scintillator
E_beam = flux * E_photon_J  # Total energy delivered by the beam
percentage_absorbed = (E_abs / E_beam) * 100  # Percentage absorbed by the scintillator

# Print the results
print("Photon Energy (J):", E_photon_J)
print("Wavelength (m):", wavelength)
print("Absorption Coefficient (mu):", mu)
print("Power Delivered by the Beam (W):", P_beam)
print("Energy Absorbed by the Scintillator (J):", E_abs)
print("Beam Area (m^2):", A_beam)
print("Mass of the Scintillator (kg):", mass)
print("Temperature Increase (K):", delta_T)
print("Energy Absorbed per Unit Mass (J/g):", delta_E)
print("Temperature Coefficient (K^-1):", alpha)
print("Percentage of the Beam Absorbed by the Scintillator:", percentage_absorbed, "%")
