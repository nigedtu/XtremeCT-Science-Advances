import os
os.chdir(r"C:\Users\nige\OneDrive - Danmarks Tekniske Universitet\Dokumenter\Postdoc\Projects\Phase retrieval\GitHub")
from phase_retrieval_functions import *
from optical_constants import oc


# Change to your local directory:
os.chdir(r"C:\Users\nige\OneDrive - Danmarks Tekniske Universitet\Dokumenter\Postdoc\Projects\Detector paper\20250225 beamtimedata\process\field_corrected")
from distortion_functions import *
fnames = ['hv_pattern_100frames_500ms_corrected.h5'] # Horizontal vertical pattern
n = 10000 # number of pixels. 
with h5py.File(fnames[0], 'r') as file:
    image_data = file['corrected/image']
    hv_pattern = image_data[0:n,0:n]


fs=14    
# Create the subplots
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Plot the full corrected data
im = axs[0].imshow(hv_pattern)# cmap='gray')
axs[0].set_title("Original image",fontsize=fs)
axs[0].set_xlabel("X-axis (pixels)",fontsize=fs)
axs[0].set_ylabel("Y-axis (pixels)",fontsize=fs)

# Plot a cropped section of the corrected data
axs[1].imshow(hv_pattern[700:5300,4800:9300])# cmap='gray')
axs[1].set_title("Zoom-in Section of Original Image",fontsize=fs)
axs[1].set_xlabel("X-axis (pixels)",fontsize=fs)
axs[1].set_ylabel("Y-axis (pixels)",fontsize=fs)
plt.tight_layout()
plt.show()




# Some images are saved. Select where you want them to be saved: 
output_base = "../"
# Select data

#%%


image = hv_pattern[4470:4780,8555:8855]
matrix = np.copy(image)
start_point = (210,5) # (y,x)  (354,356)
end_point = ( 210,170) #(y,x)
line_width = 7 # Specify the width of the line
line_points, x, y = draw_parallel_lines(matrix, start_point, end_point, line_width)
line_values= np.mean(image[y[:],x[:]],axis=0)

start_point_vertical = (13,210) # (y,x)  (354,356)
end_point_vertical = (178,210) #(y,x)
line_points_vertical, x_vertical, y_vertical = draw_parallel_lines(matrix, start_point_vertical, end_point_vertical, line_width)
line_values_vertical= np.mean(image[y_vertical[:],x_vertical[:]],axis=0)




fig, ax = plt.subplots(1,1)
ax.plot(line_values,'-*',linewidth=1,label='Data', color='red')
#ax.set_yscale('log')
ax.set_xlabel(r"Distance (pixels)", fontsize = fs)
ax.set_ylabel(r"$\tilde{\phi}(f)$", fontsize = fs)
ax.grid()
ax.text(0.1, 0.7, r'3.0 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.39, 0.7, r'2.0 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.58, 0.8, r'1.5 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.73, 0.9, r'1.0 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.025, 0.07, r'(a)', transform=ax.transAxes,
        fontsize=16, verticalalignment='top')
ax.set_xlim([0, 164])
#ax.set_ylim([-0.57, -0.09])
ax.tick_params(axis='both', which='major', labelsize=12)
fig.tight_layout()




fig, ax = plt.subplots(1,1)
ax.plot(line_values_vertical,'-*',linewidth=1,label='Data', color='blue')
#ax.set_yscale('log')
ax.set_xlabel(r"Distance (pixels)", fontsize = fs)
ax.set_ylabel(r"$\tilde{\phi}(f)$", fontsize = fs)
ax.grid()
ax.text(0.1, 0.7, r'3.0 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.39, 0.7, r'2.0 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.58, 0.8, r'1.5 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.73, 0.9, r'1.0 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.025, 0.07, r'(b)', transform=ax.transAxes,
        fontsize=16, verticalalignment='top')
ax.set_xlim([0, 164])
#ax.set_ylim([-0.57, -0.09])
ax.tick_params(axis='both', which='major', labelsize=14)
fig.tight_layout()


# Constants (make sure these match your earlier definitions)
magnification = 1.0020845741512805
detector_pixelsize = 0.00000375 / 5.5  # meters → per pixel
pixel_size_um = detector_pixelsize * 1e6  # convert to micrometers
print(pixel_size_um)
# Function to add a scale bar
def add_scale_bar(ax, length_in_um, position=(50, 280), color='white', linewidth=2, magnification=1):
    pixel_size = pixel_size_um / magnification
    pixel_length = length_in_um / pixel_size

    # Draw the scale bar as a rectangle
    rect = patches.Rectangle(position, pixel_length, 10, linewidth=linewidth,
                             edgecolor=color, facecolor=color)
    ax.add_patch(rect)

    # Add text label
    ax.text(position[0] + pixel_length / 2, position[1] - 5, f'{length_in_um} µm',
            ha='center', va='bottom', color=color, fontsize=14)
# Add scale bar of 30 µm near the bottom

fs=18
fig, ax = plt.subplots(1,1)
im=ax.imshow(image)
ax.plot(x,y, 'r.' )
ax.plot(x_vertical,y_vertical, 'b.' )
ax.set_ylabel(r"Distance (pixels)", fontsize = fs)
ax.set_xlabel(r"Distance (pixels)", fontsize = fs)
cbar = fig.colorbar(im, ax=ax)
cbar.ax.tick_params(labelsize=14)
cbar.set_label(r"$\tilde{\phi}(f)$", fontsize=fs, labelpad=2)
cbar.ax.tick_params(labeltop=True, labelbottom=True)
add_scale_bar(ax, length_in_um=100, position=(140, image.shape[0] - 20), magnification=magnification)
ax.tick_params(axis='both', which='major', labelsize=14)
ax.text(0.02, 0.15, r'(c)', transform=ax.transAxes,
        fontsize=16, verticalalignment='top')
fig.tight_layout()


result = calculate_resolution(image , 0.6818, magnification)
print('Resolution [μm]:'+str(((result[1]+result[3])/2)))

#%%
os.chdir(r"C:\Users\nige\OneDrive - Danmarks Tekniske Universitet\Dokumenter\Postdoc\Projects\Phase retrieval\Github")

energy = 19.5  # [keV] x-ray energy   
PLANCK_CONSTANT = 4.135667696e-18  # [keV*s]
SPEED_OF_LIGHT = 299792458  # [m/s]
wlen = PLANCK_CONSTANT * SPEED_OF_LIGHT/energy
density_Au = 19.3 # g/cm**3
density_SiN = 3.44 # g/cm**3

elements_Au = ['Au'] # 
elements_SiN = ['Si','N'] # from CXRO transmission calculator

z_Au = 1500 # Thickness of gold [nm]    or 500 Å  = 0.05 mu, maybe 1.6 mu # plus minus 10 %
z_SiN = 1000 # Thickness of silicon [nm]

number_of_atoms_Au = [1]
number_of_atoms_SiN = [3,4]
oc_source = r"oc_source/NIST/"

wavelength = energy2wavelength(energy*10**3) # nm
#os.chdir(r"oc_source")
n_Au = oc(wavelength,density_Au,number_of_atoms_Au,elements_Au, oc_source)     
beta = n_Au.imag
delta = n_Au.real

n_SiN = oc(wavelength,density_SiN,number_of_atoms_SiN,elements_SiN, oc_source)    

phi_Au = (-2*np.pi*(1-n_Au.real)*(z_Au*1e-09))/(wavelength*1e-9) #- (n_Au.imag*z_Au) #  [m]
phi_SiN = (-2*np.pi*(1-n_SiN.real)*(z_SiN*1e-09))/(wavelength*1e-9) #- (n_SiN.imag*z_SiN)#   [m]
print("Phase difference for Au:"+str(phi_Au))

beta = n_Au.imag
delta = 1-n_Au.real

print(delta,beta)

#%%


detector_pixelsize = 0.00000376/5.5 # m      

SDD = 18 # mm sample to detector distance
FDD= 6730 # mm, focus to detector distance
# M = Focus-to-detector distance (FDD) / Focus-to-Object distance FOD
FOD = FDD - SDD
magnification = FDD / FOD
print("magnification="+str(magnification))
voxelsize = detector_pixelsize/magnification  # m, object voxel size
fx = np.fft.fftfreq(n,d=voxelsize)
[fx,fy] = np.meshgrid(fx,fx)

#%%
image = hv_pattern
rad = image
dist = 0.000  # in meters 0.014 
Rm = np.zeros((n, n, len([dist]))) 
degCoh = np.ones((n, n, len([dist])))
OptTrnFunc = np.ones((n, n))
for i in range(0,len([dist])):
    Rm[:,:,i] = degCoh[:,:,i] * OptTrnFunc

Sd_Paganin = Paganin(rad, wlen, dist, delta, beta, fx, fy, Rm)  

fig, ax = plt.subplots(1,1)
im=ax.imshow(Sd_Paganin)
ax.set_ylabel(r"Distance (pixels)", fontsize = fs)
ax.set_xlabel(r"Distance (pixels)", fontsize = fs)
cbar = fig.colorbar(im, ax=ax)
cbar.set_label('Phase (rads)', fontsize=fs, labelpad=-0)
cbar.ax.tick_params(labeltop=True, labelbottom=True)
fig.tight_layout()



fig, ax = plt.subplots(1,1)
im=ax.imshow(Sd_Paganin[4470:4780,8555:8855])
ax.set_ylabel(r"Distance (pixels)", fontsize = fs)
ax.set_xlabel(r"Distance (pixels)", fontsize = fs)
cbar = fig.colorbar(im, ax=ax)
cbar.set_label('Phase (rads)', fontsize=fs, labelpad=-0)
cbar.ax.tick_params(labeltop=True, labelbottom=True)
#add_scale_bar(ax, length_in_um=681, position=(1000, cropped.shape[0] - 100), magnification=magnification)
fig.tight_layout()

#%%
fig, ax = plt.subplots(1,1)
im=ax.imshow(Sd_Paganin[4475:4780,8555:8855])
ax.set_ylabel(r"Distance (pixels)", fontsize = fs)
ax.set_xlabel(r"Distance (pixels)", fontsize = fs)
cbar = fig.colorbar(im, ax=ax)
cbar.set_label('Phase (rads)', fontsize=fs, labelpad=-0)
cbar.ax.tick_params(labeltop=True, labelbottom=True)
fig.tight_layout()


#%%
phase_map_area =Sd_Paganin[4475:4780,8555:8855]
#plt.imshow(phase_map_area)


result = calculate_resolution(phase_map_area , detector_pixelsize, magnification)
print('Resolution [μm]:'+str(((result[1]+result[3])/2)*10**6))

result = calculate_resolution(phase_map_area , 0.68, magnification)
print('Resolution [μm]:'+str(((result[1]+result[3])/2)))
#phase = calculate_average_height(phase_map_area)
#print('Max Min Phase, area 1='+str(phase))
#new_phase = calculate_matrix_height_difference(phase_map_area)
#print(new_phase)


#%%
magnification = 1.0020845741512805
detector_pixelsize = 0.00000376 / 5.5  # meters per detector pixel
# Effective pixel size at sample
effective_pixel_size = detector_pixelsize / magnification  # meters
effective_pixel_size_um = effective_pixel_size * 1e6



image = Sd_Paganin[4470:4780,8555:8855]
matrix = np.copy(image)
start_point = (210,5) # (y,x)  (354,356)
end_point = ( 210,170) #(y,x)
line_width = 1 # Specify the width of the line
#start_point = (430,252) # (y,x)
#end_point = ( 792,272) #(y,x)
#line_width = 91 # Specify the width of the line
# Call the function to draw parallel lines
line_points, x, y = draw_parallel_lines(matrix, start_point, end_point, line_width)
line_values= np.mean(image[y[:],x[:]],axis=0)

start_point_vertical = (13,210) # (y,x)  (354,356)
end_point_vertical = (178,210) #(y,x)
line_points_vertical, x_vertical, y_vertical = draw_parallel_lines(matrix, start_point_vertical, end_point_vertical, line_width)
line_values_vertical = np.mean(image[y_vertical[:],x_vertical[:]],axis=0)



distance_um = np.arange(len(line_values)) * effective_pixel_size_um
distance_um_vertical = np.arange(len(line_values_vertical)) * effective_pixel_size_um

fig, ax = plt.subplots(1,1)
#ax.plot(line_values,'-*',linewidth=1,label='Data', color='red')
ax.plot(distance_um, line_values, '-*', linewidth=1, label='Data', color='red')
#ax.set_xlabel(r"Distance ($\mu$m)", fontsize=fs)
ax.set_xlabel("Spatial position (µm)", fontsize=fs)
#ax.set_yscale('log')
#ax.set_xlabel(r"Distance (pixels)", fontsize = fs)
ax.set_ylabel(r"$\tilde{\phi}(f)$", fontsize = fs)
ax.grid()
ax.text(0.1, 0.95, r'3.0 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.39, 0.95, r'2.0 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.58, 0.95, r'1.5 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.73, 0.95, r'1.0 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
#ax.text(0.025, 0.07, r'(a)', transform=ax.transAxes,
#        fontsize=16, verticalalignment='top')
ax.set_xlim([0, 112.57])
ax.set_ylim([-0.65, -0.05])
ax.tick_params(axis='both', which='major', labelsize=14)
fig.tight_layout()




fig, ax = plt.subplots(1,1)
ax.plot(distance_um_vertical, line_values_vertical, '-*', linewidth=1, label='Data', color='blue')

ax.set_xlabel("Spatial position (µm)", fontsize=fs)

#ax.plot(line_values_vertical,'-*',linewidth=1,label='Data', color='blue')
#ax.set_yscale('log')
#ax.set_xlabel(r"Distance (pixels)", fontsize = fs)
ax.set_ylabel(r"$\tilde{\phi}(f)$", fontsize = fs)
ax.grid()
ax.text(0.1, 0.95, r'3.0 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.39, 0.95, r'2.0 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.58, 0.95, r'1.5 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.73, 0.95, r'1.0 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
#ax.text(0.025, 0.07, r'(b)', transform=ax.transAxes,
#        fontsize=16, verticalalignment='top')
ax.set_xlim([0, 112.57])
ax.set_ylim([-0.65, -0.05])
ax.tick_params(axis='both', which='major', labelsize=14)
fig.tight_layout()


# Constants (make sure these match your earlier definitions)
magnification = 1.0020845741512805
detector_pixelsize = 0.00000376 / 5.5  # meters → per pixel
pixel_size_um = detector_pixelsize * 1e6  # convert to micrometers
# Function to add a scale bar
def add_scale_bar(ax, length_in_um, position=(50, 280), color='white', linewidth=2, magnification=1):
    pixel_size = pixel_size_um / magnification
    pixel_length = length_in_um / pixel_size

    # Draw the scale bar as a rectangle
    rect = patches.Rectangle(position, pixel_length, 10, linewidth=linewidth,
                             edgecolor=color, facecolor=color)
    ax.add_patch(rect)

    # Add text label
    ax.text(position[0] + pixel_length / 2, position[1] - 5, f'{length_in_um} µm',
            ha='center', va='bottom', color=color, fontsize=14)
# Add scale bar of 30 µm near the bottom

fs=18
fig, ax = plt.subplots(1,1)
im=ax.imshow(image)
ax.plot(x,y, 'r.' )
ax.plot(x_vertical,y_vertical, 'b.' )
ax.set_ylabel(r"Distance (pixels)", fontsize = fs)
ax.set_xlabel(r"Distance (pixels)", fontsize = fs)
cbar = fig.colorbar(im, ax=ax)
cbar.ax.tick_params(labelsize=14)
cbar.set_label(r"$\tilde{\phi}(f)$", fontsize=fs, labelpad=2)
cbar.ax.tick_params(labeltop=True, labelbottom=True)
add_scale_bar(ax, length_in_um=100, position=(145, image.shape[0] - 20), magnification=magnification)
ax.tick_params(axis='both', which='major', labelsize=14)
#ax.text(0.02, 0.15, r'(c)', transform=ax.transAxes,
#        fontsize=16, verticalalignment='top')
fig.tight_layout()

#%%
# Condensed bar-target MTF script
# - Computes robust modulation per bar-group (percentile-based)
# - Normalizes to lowest spatial frequency
# - Computes MTF10 and MTF50 (full- & half-period) for horizontal + vertical
# - Prints everything
# - Plots combined horizontal/vertical normalized MTF + Nyquist + MTF10/50 lines
#
# Requires: numpy, matplotlib, scipy

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

# ----------------------------
# USER INPUTS (edit these)
# ----------------------------
pixel_size_um = 0.68  # sample-plane pixel size (µm)

groups = [
    {"name": "3.0 µm", "period_um": 3.0, "idx": (11, 46)},
    {"name": "2.0 µm", "period_um": 2.0, "idx": (64, 86)},
    {"name": "1.5 µm", "period_um": 1.5, "idx": (99, 117)},
    {"name": "1.0 µm", "period_um": 1.0, "idx": (124, 136)},
]

# You must already have these 1D arrays from your extraction:
# line_values           (horizontal profile)
# line_values_vertical  (vertical profile)


# ----------------------------
# FUNCTIONS
# ----------------------------
def robust_modulation(profile, smooth_sigma=1.0, top_pct=90, bottom_pct=10):
    """Nonnegative modulation estimate robust to negative-valued signals."""
    prof = np.asarray(profile, float)
    if smooth_sigma and smooth_sigma > 0:
        prof = gaussian_filter1d(prof, smooth_sigma)
    hi = np.percentile(prof, top_pct)
    lo = np.percentile(prof, bottom_pct)
    A = 0.5 * (hi - lo)
    C = np.abs(0.5 * (hi + lo))
    return np.nan if C == 0 else float(np.abs(A / C))


def mtf_points_from_groups(profile, groups, smooth_sigma=1.0):
    """Return freqs (cyc/µm), raw mods, normalized MTF, plus labels."""
    freqs, mods_raw, labels = [], [], []
    for g in groups:
        i0, i1 = g["idx"]
        seg = np.asarray(profile[i0:i1], float)
        mods_raw.append(robust_modulation(seg, smooth_sigma=smooth_sigma))
        freqs.append(1.0 / float(g["period_um"]))
        labels.append(g["name"])

    freqs = np.asarray(freqs, float)
    mods_raw = np.asarray(mods_raw, float)

    # normalize to lowest frequency point (largest period)
    idx_low = np.argmin(freqs)
    mtf_norm = mods_raw / mods_raw[idx_low] if mods_raw[idx_low] != 0 else np.full_like(mods_raw, np.nan)
    return freqs, mods_raw, mtf_norm, labels


def estimate_resolution_from_mtf(freqs, mtf, threshold):
    """
    Linear interpolation of threshold crossing.
    Returns float (full-period µm) or a bound string if not reached.
    """
    freqs = np.asarray(freqs, float)
    mtf = np.asarray(mtf, float)
    order = np.argsort(freqs)
    freqs, mtf = freqs[order], mtf[order]

    if np.all(mtf >= threshold):
        return f"< {1.0/freqs.max():.4g} µm (not reached)"
    if np.all(mtf < threshold):
        return f"> {1.0/freqs.min():.4g} µm (already below)"

    k = np.where(mtf < threshold)[0][0]
    if k == 0:
        return f"> {1.0/freqs.min():.4g} µm (already below)"

    f1, f2 = freqs[k-1], freqs[k]
    m1, m2 = mtf[k-1], mtf[k]
    f_thr = f2 if m2 == m1 else f1 + (threshold - m1) * (f2 - f1) / (m2 - m1)
    return float(1.0 / f_thr)


def print_report(name, freqs, mods_raw, mtf_norm, labels, groups, pixel_size_um):
    print("\n" + "="*70)
    print(f"Bar-target MTF analysis ({name})")
    print("="*70)

    print("\n--- Group window diagnostics ---")
    for g in groups:
        i0, i1 = g["idx"]
        window_um = (i1 - i0) * pixel_size_um
        cycles = window_um / float(g["period_um"])
        print(f"{g['name']:>6} | idx=({i0:>3},{i1:>3}) | window={window_um:6.2f} µm | cycles≈{cycles:5.2f}")

    order = np.argsort(freqs)
    print("\n--- Per-group modulation (raw + normalized) ---")
    print("Label     Period(µm)  Freq(cyc/µm)   Mod_raw      MTF_norm")
    for i in order:
        period = 1.0 / freqs[i]
        print(f"{labels[i]:<8}  {period:9.3f}   {freqs[i]:11.4f}   {mods_raw[i]:9.4f}   {mtf_norm[i]:9.4f}")

    res10 = estimate_resolution_from_mtf(freqs, mtf_norm, threshold=0.1)
    res50 = estimate_resolution_from_mtf(freqs, mtf_norm, threshold=0.5)

    print("\n--- Resolution estimates (full-period) ---")
    print("MTF10 full-period (µm):", res10)
    print("MTF50 full-period (µm):", res50)

    # half-period when numeric
    if isinstance(res10, float):
        print("MTF10 half-period (µm):", res10/2)
    if isinstance(res50, float):
        print("MTF50 half-period (µm):", res50/2)

    return res10, res50


def plot_combined_mtf(freqs_h, mtf_h, freqs_v, mtf_v, pixel_size_um, title="Normalized MTF (bar target)"):
    # sort
    oh = np.argsort(freqs_h); freqs_h, mtf_h = freqs_h[oh], mtf_h[oh]
    ov = np.argsort(freqs_v); freqs_v, mtf_v = freqs_v[ov], mtf_v[ov]

    nyquist = 1.0 / (2.0 * pixel_size_um)

    plt.figure(figsize=(6.5, 5))
    plt.plot(freqs_h, mtf_h, "-*", linewidth=2, label="Horizontal", color="red")
    plt.plot(freqs_v, mtf_v, "-*", linewidth=2, label="Vertical", color="blue")

    plt.axhline(0.5, linestyle="-.", color="gray", label="MTF50")
    #plt.axhline(0.1, linestyle=":",  color="gray", label="MTF10")
    plt.axvline(nyquist, linestyle="--", color="black", label="Nyquist")
    
    plt.xlabel("Spatial frequency (cycles/µm)", fontsize = 18)
    plt.ylabel("Normalized MTF", fontsize = 18)
    plt.text(0.02, 0.15, r'(d)', transform=ax.transAxes,
            fontsize=16, verticalalignment='top')
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def worst_numeric(a, b):
    vals = [x for x in (a, b) if isinstance(x, float) and np.isfinite(x)]
    return max(vals) if vals else None


# ----------------------------
# RUN
# ----------------------------
# Horizontal
freqs_h, mods_raw_h, mtf_h, labels_h = mtf_points_from_groups(line_values, groups, smooth_sigma=1.0)
res10_h, res50_h = print_report("horizontal", freqs_h, mods_raw_h, mtf_h, labels_h, groups, pixel_size_um)

# Vertical
freqs_v, mods_raw_v, mtf_v, labels_v = mtf_points_from_groups(line_values_vertical, groups, smooth_sigma=1.0)
res10_v, res50_v = print_report("vertical", freqs_v, mods_raw_v, mtf_v, labels_v, groups, pixel_size_um)

# Combined plot
plot_combined_mtf(freqs_h, mtf_h, freqs_v, mtf_v, pixel_size_um, title=" ")

# Worst-direction summary (use MTF50 as primary)
worst50 = worst_numeric(res50_h, res50_v)
worst10 = worst_numeric(res10_h, res10_v)

print("\n" + "="*70)
print("Worst-direction summary")
print("="*70)
print("Worst MTF50 full-period (µm):", worst50)
print("Worst MTF50 half-period (µm):", (worst50/2 if worst50 is not None else None))
print("Worst MTF10 full-period (µm):", worst10)
print("Worst MTF10 half-period (µm):", (worst10/2 if worst10 is not None else None))


#%%
image= Sd_Paganin[700:4900, 4800:9000]

plt.imshow(image)
#detector_pixelsize = 0.00000376/5.5 # m  
#magnification=1.0001
#result = calculate_resolution(image , detector_pixelsize, magnification)
#print('Resolution [μm]:'+str(((result[1]+result[3])/2)*10**6))

#%%
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Pixel size at sample (µm)
# -----------------------------
magnification = 1.00#20845741512805
detector_pixelsize = 0.00000376 / 5.5  # meters per detector pixel
effective_pixel_size_um = (detector_pixelsize / magnification) * 1e6  # µm per sample pixel

# -----------------------------
# Crop and extract line profile
# -----------------------------
image = Sd_Paganin[700:4900, 4800:9000]
matrix = np.copy(image)

# Horizontal line (red) across the bar groups
start_point = (3954, 150)     # (y, x) in the CROPPED image coordinates
end_point   = (4001, 3969)   # (y, x)
line_width = 7

line_points, x, y = draw_parallel_lines(matrix, start_point, end_point, line_width)
line_values = np.mean(image[y, x], axis=0)

# Optional vertical line (blue) – make sure it's valid for this crop
# NOTE: Your old vertical indices (13..178,210) are not in the same coordinate
# system as the new crop unless you intentionally placed them there.
start_point_vertical = (135, 3985)    # (y, x) example: vertical through the same area
end_point_vertical   = (3990,3984)  # (y, x)
line_points_v, x_v, y_v = draw_parallel_lines(matrix, start_point_vertical, end_point_vertical, line_width)
line_values_vertical = np.mean(image[y_v, x_v], axis=0)

# -----------------------------
# Distance axis in µm (for plotting)
# -----------------------------
distance_um = np.arange(len(line_values)) * effective_pixel_size_um

# -----------------------------
# Group windows (PIXEL INDICES into line_values)
# IMPORTANT: idx are in pixels (indices of line_values), not µm.
# Ensure these are strictly increasing and non-overlapping.
# -----------------------------
number= 2125
groups_full = [
    {"name": "50 µm",  "idx": (14,   693)},
    {"name": "40 µm",  "idx": (891,  1448)},
    {"name": "30 µm",  "idx": (1600,   2019)},
    
    {"name": "20 µm",  "idx": (number+0+15,   number+293-15)},
    {"name": "15 µm",  "idx": (number+356+15, number+576-10)},
    {"name": "10 µm",  "idx": (number+617+15, number+769-5)},
    {"name": "9 µm",   "idx": (number+810,number+929-5)},   # <-- changed to avoid overlap with 10 µm
    {"name": "8 µm",   "idx": (number+958+10, number+1081-7)},
    {"name": "7 µm",   "idx": (number+1096+14, number+1204-7)},
    {"name": "6 µm",   "idx": (number+1219+12, number+1309)},
    {"name": "5 µm",   "idx": (number+1336, number+1402)},
    {"name": "4 µm",   "idx": (number+1424, number+1477)},
    {"name": "3 µm",   "idx": (number+1493, number+1535)},
    {"name": "2 µm",   "idx": (number+1544+5,number+1573)},
    {"name": "1.5 µm",   "idx": (number+1582,number+1601)},
    {"name": "1 µm", "idx": (number+1611,number+1622)},
    {"name": "0.9 µm",   "idx": (number+1627,number+1638)},
    {"name": "0.8 µm",   "idx": (number+1644,number+1652)},
    {"name": "0.7 µm",   "idx": (number+1656+1,number+1665)},
    {"name": "0.6 µm",   "idx": (number+1669+1,number+1676)},
    {"name": "0.5 µm",   "idx": (3806,3810)}
]

# Sanity check: windows fit inside the profile length
assert groups_full[-1]["idx"][1] <= len(line_values), "Group idx exceeds profile length."

# -----------------------------
# Plot: line profile vs µm with shaded group regions
# -----------------------------
fs = 18
fig, ax = plt.subplots(1, 1, figsize=(8, 4))

ax.plot(distance_um, line_values, '-*', linewidth=1, color='red')

for g in groups_full:
    i0, i1 = g["idx"]

    # Convert pixel indices -> µm positions for shading
    x0 = distance_um[i0]
    x1 = distance_um[i1]

    ax.axvspan(x0, x1, alpha=0.15, color='gray')

    x_mid = 0.5 * (x0 + x1)
    ax.text(
        x_mid,
        np.percentile(line_values, 95),
        g["name"],
        ha='center',
        va='bottom',
        fontsize=12
    )

ax.set_xlabel(r"Distance ($\mu$m)", fontsize=fs)
ax.set_ylabel(r"$\tilde{\phi}(f)$", fontsize=fs)
ax.grid(True)
ax.tick_params(axis='both', which='major', labelsize=14)
fig.tight_layout()




# -----------------------------
# Plot: image with sampled points overlaid
# -----------------------------
fig, ax = plt.subplots(1, 1, figsize=(6, 5))
im = ax.imshow(image)

ax.plot(x, y, 'r.', markersize=2, label='Horizontal profile')
ax.plot(x_v, y_v, 'b.', markersize=2, label='Vertical profile')

ax.set_ylabel("Distance (pixels)", fontsize=fs)
ax.set_xlabel("Distance (pixels)", fontsize=fs)

cbar = fig.colorbar(im, ax=ax)
cbar.ax.tick_params(labelsize=14)
cbar.set_label(r"$\tilde{\phi}(f)$", fontsize=fs, labelpad=2)
#cbar.ax.tick_params(labeltop=True, labelbottom=True)

ax.tick_params(axis='both', which='major', labelsize=14)
#ax.legend(loc="upper right")
fig.tight_layout()




# -----------------------------
# Vertical group windows
# -----------------------------
number_v = 2125

groups_full_vertical = [
    {"name": "50 µm",  "idx": (14,   693)},
    {"name": "40 µm",  "idx": (891+30,  1448)},
    {"name": "30 µm",  "idx": (1600+30, 2040)},

    {"name": "20 µm",  "idx": (number_v+45,   number_v+313)},
    {"name": "15 µm",  "idx": (number_v+396,  number_v+600)},
    {"name": "10 µm",  "idx": (number_v+662,  number_v+799)},
    {"name": "9 µm",   "idx": (number_v+838,  number_v+964)},
    {"name": "8 µm",   "idx": (number_v+998,  number_v+1111)},
    {"name": "7 µm",   "idx": (number_v+1145, number_v+1237)},
    {"name": "6 µm",   "idx": (number_v+1269, number_v+1349)},
    {"name": "5 µm",   "idx": (number_v+1376, number_v+1442)},
    {"name": "4 µm",   "idx": (number_v+1462, number_v+1517)},
    {"name": "3 µm",   "idx": (number_v+1533, number_v+1570)},
    {"name": "2 µm",   "idx": (number_v+1585, number_v+1613)},
    {"name": "1.5 µm", "idx": (number_v+1620, number_v+1641)},

    {"name": "1 µm",   "idx": (3772, 3785)},
    {"name": "0.9 µm", "idx": (3790, 3801)},
    {"name": "0.8 µm", "idx": (3807, 3816)},
    {"name": "0.7 µm", "idx": (3821, 3828)},
    {"name": "0.6 µm", "idx": (3833, 3838)},
    {"name": "0.5 µm", "idx": (3844, 3848)}
]

# Safety check
assert groups_full_vertical[-1]["idx"][1] <= len(line_values_vertical)

# -----------------------------
# Distance axis (vertical)
# -----------------------------
distance_um_vertical = np.arange(len(line_values_vertical)) * effective_pixel_size_um


# -----------------------------
# Plot vertical profile + groups
# -----------------------------
fs = 18
fig, ax = plt.subplots(figsize=(8,4))

ax.plot(distance_um_vertical, line_values_vertical, '-*',
        linewidth=1, color='blue', label="Vertical")

for g in groups_full_vertical:

    i0, i1 = g["idx"]

    x0 = distance_um_vertical[i0]
    x1 = distance_um_vertical[i1]

    ax.axvspan(x0, x1, alpha=0.15, color='gray')

    x_mid = 0.5 * (x0 + x1)

    # IMPORTANT FIX → use vertical profile percentile
    ax.text(
        x_mid,
        np.percentile(line_values_vertical, 95),
        g["name"],
        ha='center',
        va='bottom',
        fontsize=12
    )

ax.set_xlabel(r"Distance ($\mu$m)", fontsize=fs)
ax.set_ylabel(r"$\tilde{\phi}(f)$", fontsize=fs)
ax.grid(True)
ax.tick_params(axis='both', which='major', labelsize=14)

fig.tight_layout()

#%%

# ---- MTF plot for HORIZONTAL profile only ----
# Assumes you already have the functions:
#   mtf_points_from_groups(profile, groups, smooth_sigma=...)
#   estimate_resolution_from_mtf(freqs, mtf, threshold=...)
# (or equivalent from your earlier code)
#
# Also assumes you already computed:
#   line_values, groups_full, effective_pixel_size_um

import numpy as np
import matplotlib.pyplot as plt

# 1) Build an MTF "groups" list from your full groups (needs period_um for each)
#    Convert "20 µm" -> 20.0 etc. (handles "0.8 µm" too)
groups_mtf = []
for g in groups_full:
    period_um = float(g["name"].replace("µm", "").strip())
    groups_mtf.append({"name": g["name"], "period_um": period_um, "idx": g["idx"]})

# 2) Compute per-group raw modulation + normalized MTF
freqs_h, mods_raw_h, mtf_h, labels_h = mtf_points_from_groups(
    line_values, groups_mtf, smooth_sigma=1.0
)

# (Optional) sort by frequency for nicer plotting/printing
order = np.argsort(freqs_h)
freqs_h = freqs_h[order]
mods_raw_h = mods_raw_h[order]
mtf_h = mtf_h[order]
labels_h = [labels_h[i] for i in order]

# 3) Estimate MTF10 and MTF50 (full-period in µm)
res_mtf10 = estimate_resolution_from_mtf(freqs_h, mtf_h, threshold=0.1)
res_mtf50 = estimate_resolution_from_mtf(freqs_h, mtf_h, threshold=0.5)

print("\n--- Horizontal MTF results ---")
print("MTF10 full-period (µm):", res_mtf10)
print("MTF50 full-period (µm):", res_mtf50)
if isinstance(res_mtf10, float):
    print("MTF10 half-period (µm):", res_mtf10 / 2)
if isinstance(res_mtf50, float):
    print("MTF50 half-period (µm):", res_mtf50 / 2)

# 4) Plot normalized MTF (horizontal only) + MTF10/MTF50 + Nyquist
nyquist_freq = 1.0 / (2.0 * effective_pixel_size_um)  # cycles/µm

plt.figure(figsize=(6.5, 5))
plt.plot(freqs_h, mtf_h, 'o-', linewidth=2, label="Horizontal")

plt.axhline(0.5, linestyle='--', color='gray', label="MTF50")
plt.axhline(0.1, linestyle=':',  color='gray', label="MTF10")
plt.axvline(nyquist_freq, linestyle='--', color='red', label="Nyquist")

plt.xlabel("Spatial frequency (cycles/µm)")
plt.ylabel("Normalized MTF")
#plt.xscale('log')   # ✔ correct function
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# 5) (Optional) print the per-group table (useful for debugging)
print("\nLabel    Period(µm)  Freq(cyc/µm)  Mod_raw   MTF_norm")
for f, mraw, mn, lab in zip(freqs_h, mods_raw_h, mtf_h, labels_h):
    period = 1.0 / f
    print(f"{lab:<7}  {period:9.3f}   {f:11.4f}  {mraw:7.4f}  {mn:8.4f}")

#%%


# ---- MTF plot for HORIZONTAL + VERTICAL (combined) ----
# Requires your existing functions:
#   mtf_points_from_groups(profile, groups, smooth_sigma=...)
#   estimate_resolution_from_mtf(freqs, mtf, threshold=...)
#
# Assumes you already have:
#   line_values, groups_full
#   line_values_vertical, groups_full_vertical
#   effective_pixel_size_um

import numpy as np
import matplotlib.pyplot as plt

def build_groups_mtf(groups_full_any):
    """Convert your plotting groups (name+idx) -> MTF groups (name+period_um+idx)."""
    groups_mtf = []
    for g in groups_full_any:
        period_um = float(g["name"].replace("µm", "").strip())
        groups_mtf.append({"name": g["name"], "period_um": period_um, "idx": g["idx"]})
    return groups_mtf

# -----------------------------
# 1) Build MTF group lists
# -----------------------------
groups_mtf_h = build_groups_mtf(groups_full)
groups_mtf_v = build_groups_mtf(groups_full_vertical)

# -----------------------------
# 2) Compute raw modulation + normalized MTF
# -----------------------------
freqs_h, mods_raw_h, mtf_h, labels_h = mtf_points_from_groups(
    line_values, groups_mtf_h, smooth_sigma=1.0
)
freqs_v, mods_raw_v, mtf_v, labels_v = mtf_points_from_groups(
    line_values_vertical, groups_mtf_v, smooth_sigma=1.0
)

# Sort by frequency
ord_h = np.argsort(freqs_h)
freqs_h, mods_raw_h, mtf_h = freqs_h[ord_h], mods_raw_h[ord_h], mtf_h[ord_h]
labels_h = [labels_h[i] for i in ord_h]

ord_v = np.argsort(freqs_v)
freqs_v, mods_raw_v, mtf_v = freqs_v[ord_v], mods_raw_v[ord_v], mtf_v[ord_v]
labels_v = [labels_v[i] for i in ord_v]

# -----------------------------
# 3) Resolution estimates
# -----------------------------
res_h_mtf10 = estimate_resolution_from_mtf(freqs_h, mtf_h, threshold=0.1)
res_h_mtf50 = estimate_resolution_from_mtf(freqs_h, mtf_h, threshold=0.5)

res_v_mtf10 = estimate_resolution_from_mtf(freqs_v, mtf_v, threshold=0.1)
res_v_mtf50 = estimate_resolution_from_mtf(freqs_v, mtf_v, threshold=0.5)

print("\n--- Horizontal MTF results ---")
print("MTF10 full-period (µm):", res_h_mtf10)
print("MTF50 full-period (µm):", res_h_mtf50)
if isinstance(res_h_mtf10, float): print("MTF10 half-period (µm):", res_h_mtf10/2)
if isinstance(res_h_mtf50, float): print("MTF50 half-period (µm):", res_h_mtf50/2)

print("\n--- Vertical MTF results ---")
print("MTF10 full-period (µm):", res_v_mtf10)
print("MTF50 full-period (µm):", res_v_mtf50)
if isinstance(res_v_mtf10, float): print("MTF10 half-period (µm):", res_v_mtf10/2)
if isinstance(res_v_mtf50, float): print("MTF50 half-period (µm):", res_v_mtf50/2)

# Worst-case (largest full-period among numeric results)
def worst_numeric(a, b):
    vals = []
    for r in [a, b]:
        if isinstance(r, float) and np.isfinite(r):
            vals.append(r)
    return max(vals) if vals else None

worst_mtf50 = worst_numeric(res_h_mtf50, res_v_mtf50)
worst_mtf10 = worst_numeric(res_h_mtf10, res_v_mtf10)

print("\n--- Worst-direction summary ---")
print("Worst MTF50 full-period (µm):", worst_mtf50)
if isinstance(worst_mtf50, float): print("Worst MTF50 half-period (µm):", worst_mtf50/2)
#print("Worst MTF10 full-period (µm):", worst_mtf10)
if isinstance(worst_mtf10, float): print("Worst MTF10 half-period (µm):", worst_mtf10/2)

# -----------------------------
# 4) Combined MTF plot + thresholds + Nyquist
# -----------------------------
nyquist_freq = 1.0 / (2.0 * effective_pixel_size_um)  # cycles/µm

plt.figure(figsize=(6.8, 5.2))

plt.plot(freqs_h, mtf_h, '-*', linewidth=2, label="Horizontal", color="red")
plt.plot(freqs_v, mtf_v, '-*', linewidth=2, label="Vertical", color="blue")

#plt.axhline(0.5, linestyle='--', color='gray', label="MTF50")
#plt.axhline(0.10, linestyle=':',  color='gray', label="MTF10", linewidth=2)
plt.axvline(nyquist_freq, linestyle='-.', color='black', label="Nyquist")

plt.xlabel("Spatial frequency (cycles/µm)", fontsize = 19)
plt.ylabel("Normalized MTF", fontsize = 19)
#plt.text(0.02, 0.15, r'(d)', transform=ax.transAxes,
#        fontsize=17, verticalalignment='top')
# plt.xscale('log')  # uncomment if desired
plt.grid(True, which="both")
plt.tick_params(axis='both', which='major', labelsize=14)
plt.legend(fontsize = 16)
plt.tight_layout()
plt.show()

# -----------------------------
# 5) Optional: per-group tables
# -----------------------------
print("\nHorizontal table:")
print("Label    Period(µm)  Freq(cyc/µm)  Mod_raw   MTF_norm")
for f, mraw, mn, lab in zip(freqs_h, mods_raw_h, mtf_h, labels_h):
    print(f"{lab:<7}  {1.0/f:9.3f}   {f:11.4f}  {mraw:7.4f}  {mn:8.4f}")

print("\nVertical table:")
print("Label    Period(µm)  Freq(cyc/µm)  Mod_raw   MTF_norm")
for f, mraw, mn, lab in zip(freqs_v, mods_raw_v, mtf_v, labels_v):
    print(f"{lab:<7}  {1.0/f:9.3f}   {f:11.4f}  {mraw:7.4f}  {mn:8.4f}")


