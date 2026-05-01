
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt


os.chdir(r"C:\Users\nige\OneDrive - Danmarks Tekniske Universitet\Dokumenter\Postdoc\Projects\Phase retrieval\GitHub")
from phase_retrieval_functions import *
from optical_constants import oc

# ----------------------------
# Load H5 from Downloads
# ----------------------------
#fname = "npos_5_z1_0.745_z2_6.242_lam_0.05.h5"
fname = "npos_15_z1_0.74_z2_6.247_lam_0.05_its_2000_pos1.h5"
downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
path = os.path.join(downloads_dir, fname)

base_dir = r"C:\Users\nige\OneDrive - Danmarks Tekniske Universitet\Dokumenter\Postdoc\Projects\Detector paper\20250604 beamtimedata\Nano"
path = os.path.join(base_dir, fname)

with h5py.File(path, "r") as f:
    # Preferred: read complex q from real/imag
    if "q_real" in f and "q_imag" in f:
        q = f["q_real"][...] + 1j * f["q_imag"][...]
        phase = np.angle(q)
        amp = np.abs(q)

    # Fallback
    else:
        phase = f["phase"][...] if "phase" in f else None
        amp   = f["amp"][...]   if "amp" in f else None
        if phase is None or amp is None:
            raise KeyError(
                "H5 file doesn't contain (q_real,q_imag) or (phase,amp)."
            )

# Absorbance from amplitude
absorb = -np.log(amp + 1e-12)

phase_m = np.fliplr(phase)
absorb_m = np.fliplr(absorb)


print("Loaded:", path)
print("phase:", phase.shape, phase.dtype, "min/max:", phase.min(), phase.max())
print("absorb:", absorb.shape, absorb.dtype, "min/max:", absorb.min(), absorb.max())

# ----------------------------
# Plot phase + absorbance
# ----------------------------
fs = 14
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

im0 = axs[0].imshow(phase_m, cmap="gray")
axs[0].set_title("Phase (rad)", fontsize=fs)
axs[0].set_xlabel("X-axis (pixels)", fontsize=fs)
axs[0].set_ylabel("Y-axis (pixels)", fontsize=fs)
plt.colorbar(im0, ax=axs[0], fraction=0.046, pad=0.04)

im1 = axs[1].imshow(absorb_m, cmap="gray")
axs[1].set_title("Absorbance (-log(|q|))", fontsize=fs)
axs[1].set_xlabel("X-axis (pixels)", fontsize=fs)
axs[1].set_ylabel("Y-axis (pixels)", fontsize=fs)
plt.colorbar(im1, ax=axs[1], fraction=0.046, pad=0.04)

plt.tight_layout()
plt.show()
#%%


#%%

detector_pixelsize = 0.00000376/5.5 # [m], camera pixel size and custom lens magnification

focusToDetectorDistance = 6.987 # correct 6.987  # [m] 
z1 = 0.74 # [m], focus to sample 
z2 = focusToDetectorDistance-z1 # [m], sample to detector
distances = (z1*z2)/focusToDetectorDistance
magnification = focusToDetectorDistance/z1
voxelsize = np.abs(detector_pixelsize/magnification)  # object voxel size
print("detector pixel size [m]="+str(detector_pixelsize))
print("magnification="+str(magnification))
print("voxel size [m]="+str(voxelsize))

n=np.shape(phase)[0]
fx = np.fft.fftfreq(n,d=voxelsize)
[fx,fy] = np.meshgrid(fx,fx)


#%%
fig, ax = plt.subplots(1,1)
im=ax.imshow(phase_m)
ax.set_ylabel(r"Distance (pixels)", fontsize = fs)
ax.set_xlabel(r"Distance (pixels)", fontsize = fs)
cbar = fig.colorbar(im, ax=ax)
cbar.set_label('Phase (rads)', fontsize=fs, labelpad=-0)
cbar.ax.tick_params(labeltop=True, labelbottom=True)
fig.tight_layout()

result = calculate_resolution(phase_m , detector_pixelsize, magnification)
print('Resolution [μm]:'+str(((result[1]+result[3])/2)*10**6))

#%%
import numpy as np

def add_crosshair(ax, center, arm_length=120, angle_deg=0,
                  color="w", lw=2, alpha=1.0):
    """
    Draw a rotated crosshair on an image axis.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
    center : tuple
        (center_col, center_row) in pixels => (x, y)
    arm_length : float
        Full length of each crosshair arm (pixels)
    angle_deg : float
        Rotation angle in degrees (counterclockwise)
    color : str
    lw : float
    alpha : float
    """
    cx, cy = center
    half = arm_length / 2.0

    theta = np.deg2rad(angle_deg)
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])

    # Base (unrotated) segments around origin: horizontal and vertical
    horiz = np.array([[-half, 0.0],
                      [ half, 0.0]])
    vert  = np.array([[0.0, -half],
                      [0.0,  half]])

    # Rotate then translate to center
    horiz_rt = (horiz @ R.T) + np.array([cx, cy])
    vert_rt  = (vert  @ R.T) + np.array([cx, cy])

    ax.plot(horiz_rt[:, 0], horiz_rt[:, 1], color=color, lw=lw, alpha=alpha)
    ax.plot(vert_rt[:, 0],  vert_rt[:, 1],  color=color, lw=lw, alpha=alpha)

#%%


image = phase_m
matrix = np.copy(image)
start_point = (1319-15,150) # (y,x)  (354,356) # red line, horizontal
end_point = ( 1290-15,1266) #(y,x)
line_width = 15 # Specify the width of the line

# Call the function to draw parallel lines
line_points, x, y = draw_parallel_lines(matrix, start_point, end_point, line_width)
line_values= np.mean(image[y[:],x[:]],axis=0)

start_point_vertical = (160,1245) # (y,x)  (354,356)
end_point_vertical = (1290,1266) #(y,x)
line_points_vertical, x_vertical, y_vertical = draw_parallel_lines(matrix, start_point_vertical, end_point_vertical, line_width)
line_values_vertical= np.mean(image[y_vertical[:],x_vertical[:]],axis=0)

plot_crosshair = False
# Cross hair: horizontal red line
center_col, center_row = 463, 1311   # (x, y) in pixels
arm_length_px = 2250                 # pixels (full arm length)
rotation_angle_deg = -1.5             # degrees (CCW)    

# Cross hair: Vertical blue line
#center_col, center_row = 1246, 184   # (x, y) in pixels
#arm_length_px = 2250                 # pixels (full arm length)
#rotation_angle_deg = -1             # degrees (CCW)    


fig, ax = plt.subplots(1, 1, figsize=(10, 4))
ax.plot(line_values,'-',linewidth=2,label='Data', color='red')
#ax.set_yscale('log')
ax.set_xlabel(r"Distance (pixels)", fontsize = fs)
ax.set_ylabel(r"$\tilde{\phi}(f)$", fontsize = fs)
ax.grid()
ax.text(0.075, 0.8, r'1.00 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.35, 0.8, r'0.80 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.56, 0.8, r'0.60 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.71, 0.8, r'0.40 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.77, 0.7, r'0.35 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
#ax.text(0.82, 0.6, r'0.30 $\mathrm{\mu}$m', transform=ax.transAxes,
#        fontsize=15, verticalalignment='top')
ax.text(0.025, 0.07, r'(a)', transform=ax.transAxes,
        fontsize=16, verticalalignment='top')
#ax.set_xlim([0, 164])
ax.set_ylim([-1.0, 0.1])
ax.tick_params(axis='both', which='major', labelsize=12)
fig.tight_layout()




fig, ax = plt.subplots(1, 1, figsize=(10, 4))
ax.plot(line_values_vertical,'-',linewidth=2,label='Data', color='blue')
#ax.set_yscale('log')
ax.set_xlabel(r"Distance (pixels)", fontsize = fs)
ax.set_ylabel(r"$\tilde{\phi}(f)$", fontsize = fs)
ax.grid()
ax.text(0.06, 0.9, r'1.00 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.35, 0.7, r'0.80 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.54, 0.6, r'0.60 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.69, 0.6, r'0.40 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.74, 0.52, r'0.35 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
#ax.text(0.82, 0.6, r'0.30 $\mathrm{\mu}$m', transform=ax.transAxes,
#        fontsize=15, verticalalignment='top')
ax.text(0.025, 0.07, r'(b)', transform=ax.transAxes,
        fontsize=16, verticalalignment='top')
#ax.set_xlim([0, 164])
ax.set_ylim([-1.0, 0.75])
ax.tick_params(axis='both', which='major', labelsize=14)
fig.tight_layout()


# Constants (make sure these match your earlier definitions)
#magnification = 1.0020845741512805
#detector_pixelsize = 0.00000375 / 5.4  # meters → per pixel
pixel_size_um = voxelsize * 1e6  # µm per pixel (object plane)

def add_scale_bar(ax, length_in_um, position=(50, 280), color='white', linewidth=2):
    pixel_length = length_in_um / pixel_size_um  # <-- FIXED: no extra magnification

    rect = patches.Rectangle(position, pixel_length, 10,
                             linewidth=linewidth, edgecolor=color, facecolor=color)
    ax.add_patch(rect)

    ax.text(position[0] + pixel_length / 2, position[1] - 5,
            f'{length_in_um} µm', ha='center', va='bottom',
            color=color, fontsize=14)
    
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
#add_scale_bar(ax, length_in_um=10, position=(140, image.shape[0] - 20), magnification=magnification)
add_scale_bar(ax, length_in_um=50, position=(140, image.shape[0] - 50))
ax.tick_params(axis='both', which='major', labelsize=14)
#ax.text(0.02, 0.10, r'(a)', transform=ax.transAxes,
#        fontsize=16, verticalalignment='top')
fig.tight_layout()

if plot_crosshair:
    add_crosshair(
        ax,
        center=(center_col, center_row),
        arm_length=arm_length_px,
        angle_deg=rotation_angle_deg,
        color="w",
        lw=2
    )
    
    
from mpl_toolkits.axes_grid1 import make_axes_locatable

fs = 20  # match previous script

fig, ax = plt.subplots(figsize=(6, 6))  # match figure size

im = ax.imshow(image)

ax.plot(x, y, 'r.')
ax.plot(x_vertical, y_vertical, 'b.')

ax.set_ylabel(r"Distance (pixels)", fontsize=fs)
ax.set_xlabel(r"Distance (pixels)", fontsize=fs)

# --- MATCHED colorbar ---
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)

cbar = fig.colorbar(im, cax=cax)
cbar.set_label(r"$\tilde{\phi}(f)$", fontsize=fs)
cbar.ax.tick_params(labelsize=14)
# remove ticks
cbar.set_ticks([])
# -----------------------

add_scale_bar(ax, length_in_um=50,
              position=(140, image.shape[0] - 50))

ax.tick_params(axis='both', which='major', labelsize=14)

fig.tight_layout()
    
    #%%
    
# ---- Convert pixel index -> spatial position (µm) using your voxel size ----
# voxelsize is in [m/pixel] (you already computed it earlier)
pixel_um = voxelsize * 1e6  # [µm / pixel]

# ===================== (a) red line =====================
x_um = np.arange(len(line_values)) * pixel_um  # position along the extracted line in µm

fig, ax = plt.subplots(1, 1, figsize=(10, 4))
ax.plot(x_um, line_values, '-*', linewidth=2, label='Data', color='red')

ax.set_xlabel(r"Spatial position ($\mathrm{\mu}$m)", fontsize=20)          # <-- changed
ax.set_ylabel(r"$\tilde{\phi}(f)$", fontsize=20)
ax.grid()

ax.text(0.042, 0.8, r'1.00 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.35-0.02, 0.8, r'0.80 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.56, 0.8, r'0.60 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.71+0.03, 0.8, r'0.40 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.77+0.03, 0.7, r'0.35 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')

#ax.text(0.025, 0.07, r'(c)', transform=ax.transAxes,
#        fontsize=16, verticalalignment='top')

ax.set_ylim([-1.03, 0.1])
ax.set_yticks([ 0, -0.5, -1])
ax.set_xlim([0, 81])
ax.tick_params(axis='both', which='major', labelsize=12)
fig.tight_layout()


# ===================== (b) blue line =====================
xv_um = np.arange(len(line_values_vertical)) * pixel_um  # position along the extracted line in µm

fig, ax = plt.subplots(1, 1, figsize=(10, 4))
ax.plot(xv_um, line_values_vertical, '-*', linewidth=2, label='Data', color='blue')

ax.set_xlabel(r"Spatial position ($\mathrm{\mu}$m)", fontsize=20)          # <-- changed
ax.set_ylabel(r"$\tilde{\phi}(f)$", fontsize=20)
ax.grid()

ax.text(0.06-0.03, 0.9, r'1.00 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.35-0.02, 0.7, r'0.80 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.54+0.01, 0.6, r'0.60 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.69+0.04, 0.6, r'0.40 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')
ax.text(0.74+0.05, 0.52, r'0.35 $\mathrm{\mu}$m', transform=ax.transAxes,
        fontsize=15, verticalalignment='top')

#ax.text(0.025, 0.07, r'(b)', transform=ax.transAxes,
#        fontsize=16, verticalalignment='top')

ax.set_ylim([-1.03, 0.75])
ax.set_yticks([0.5, 0, -0.5, -1])
ax.set_xlim([0, 81])
ax.tick_params(axis='both', which='major', labelsize=14)
fig.tight_layout()

#%%

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches

# --- assumes you already have: image, x,y, x_vertical,y_vertical,
#     line_values, line_values_vertical, voxelsize, fs, add_scale_bar() ---
# If you use the fixed scale bar from earlier, it should use pixel_size_um = voxelsize*1e6 internally.

# ---- x-axis in µm for the 1D plots ----
pixel_um = voxelsize * 1e6  # µm/pixel (object plane)

def arc_length_um(x, y, pixel_um):
    x = np.asarray(x)
    y = np.asarray(y)
    ds_px = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
    s_px  = np.concatenate([[0.0], np.cumsum(ds_px)])
    return s_px * pixel_um

#x_um  = arc_length_um(x, y, pixel_um)
#xv_um = arc_length_um(x_vertical, y_vertical, pixel_um)

# ---- Figure layout (left big + right 2 stacked) ----
fig = plt.figure(figsize=(14, 6))
gs = gridspec.GridSpec(
    nrows=2, ncols=2,
    width_ratios=[1.15, 1.6],   # left vs right width
    height_ratios=[1, 1],       # top vs bottom on right
    wspace=0.35, hspace=0.35
)

ax_img  = fig.add_subplot(gs[:, 0])   # span both rows on left
ax_top  = fig.add_subplot(gs[0, 1])   # top-right
ax_bot  = fig.add_subplot(gs[1, 1])   # bottom-right

# ===================== (c) Image panel =====================
im = ax_img.imshow(image)  # add cmap=... if you want
ax_img.plot(x, y, '-*',color="red", ms=2)
ax_img.plot(x_vertical, y_vertical, 'b.', ms=2)

ax_img.set_xlabel("Distance (pixels)", fontsize=fs)
ax_img.set_ylabel("Distance (pixels)", fontsize=fs)
ax_img.tick_params(axis='both', which='major', labelsize=14)

# colorbar next to the image axis (keeps layout like your example)
cbar = fig.colorbar(im, ax=ax_img, fraction=0.046, pad=0.04)
cbar.set_label(r"$\tilde{\phi}(f)$", fontsize=fs, labelpad=2)
cbar.ax.tick_params(labelsize=14)

# scale bar + panel label
add_scale_bar(ax_img, length_in_um=50, position=(140, image.shape[0] - 50))
ax_img.text(0.02, 0.15, "(c)", transform=ax_img.transAxes,
            fontsize=16, va='top')

# ===================== (b) Blue line (top-right) =====================
ax_top.plot(xv_um, line_values_vertical, '-', linewidth=2, color='blue')
ax_top.set_xlabel("Position (µm)", fontsize=fs)
ax_top.set_ylabel(r"$\tilde{\phi}(f)$", fontsize=fs)
ax_top.grid(True)
ax_top.set_xlim([0, max(x_um[-1], xv_um[-1])])  # optional: match ranges
ax_top.set_ylim([-1.03, 0.75])
ax_top.tick_params(axis='both', which='major', labelsize=12)

ax_top.text(0.03, 0.07, "(b)", transform=ax_top.transAxes, fontsize=16, va='top')
ax_top.text(0.05, 0.85, "1.00 µm", transform=ax_top.transAxes, fontsize=12)
ax_top.text(0.33, 0.60, "0.80 µm", transform=ax_top.transAxes, fontsize=12)
ax_top.text(0.50, 0.48, "0.60 µm", transform=ax_top.transAxes, fontsize=12)
ax_top.text(0.67, 0.48, "0.40 µm", transform=ax_top.transAxes, fontsize=12)
ax_top.text(0.74, 0.38, "0.35 µm", transform=ax_top.transAxes, fontsize=12)

# ===================== (a) Red line (bottom-right) =====================
ax_bot.plot(x_um, line_values, '-', linewidth=2, color='red')
ax_bot.set_xlabel("Position (µm)", fontsize=fs)
ax_bot.set_ylabel(r"$\tilde{\phi}(f)$", fontsize=fs)
ax_bot.grid(True)
ax_bot.set_xlim([0, max(x_um[-1], xv_um[-1])])  # optional: match ranges
ax_bot.set_ylim([-1.03, 0.1])
ax_bot.tick_params(axis='both', which='major', labelsize=12)

ax_bot.text(0.03, 0.07, "(a)", transform=ax_bot.transAxes, fontsize=16, va='top')
ax_bot.text(0.05, 0.78, "1.00 µm", transform=ax_bot.transAxes, fontsize=12)
ax_bot.text(0.33, 0.78, "0.80 µm", transform=ax_bot.transAxes, fontsize=12)
ax_bot.text(0.50, 0.78, "0.60 µm", transform=ax_bot.transAxes, fontsize=12)
ax_bot.text(0.67, 0.78, "0.40 µm", transform=ax_bot.transAxes, fontsize=12)
ax_bot.text(0.74, 0.68, "0.35 µm", transform=ax_bot.transAxes, fontsize=12)

fig.tight_layout()
plt.show()


#%%

def add_scale_bar(ax, length_in_um, position=(50, 280), color='white', linewidth=4):
    pixel_length = length_in_um / pixel_size_um  # <-- FIXED: no extra magnification

    rect = patches.Rectangle(position, pixel_length, 10,
                             linewidth=linewidth, edgecolor=color, facecolor=color)
    ax.add_patch(rect)

    ax.text(position[0] + pixel_length / 2, position[1] - 5,
            f'{length_in_um} µm', ha='center', va='bottom',
            color=color, fontsize=16)

os.chdir(r"C:\Users\nige\OneDrive - Danmarks Tekniske Universitet\Dokumenter\Postdoc\Projects\Detector paper")
# Load data
with h5py.File("scan-3977_112_corrected.h5", "r") as f:
    data = f["data"][:]   # assuming dataset is named "data"

from mpl_toolkits.axes_grid1 import make_axes_locatable

# Mirror in x-direction (horizontal flip)
data = np.flipud(data[0:4000,1000:5000])
data_mirrored = np.fliplr(data)

# Plot using axes
fig, ax_img = plt.subplots(figsize=(6, 6))

im = ax_img.imshow(data_mirrored,  origin='lower')

ax_img.set_xlabel("Distance (pixels)", fontsize=20)
ax_img.set_ylabel("Distance (pixels)", fontsize=20)

# --- FIX: colorbar with same height ---
divider = make_axes_locatable(ax_img)
cax = divider.append_axes("right", size="5%", pad=0.05)

cbar = plt.colorbar(im, cax=cax)
cbar.set_label("Corrected intensity (a.u.)", fontsize=20)
# remove ticks
cbar.set_ticks([])
#cbar.ax.tick_params(labelsize=12)
# -------------------------------------

# --- Your additions ---
add_scale_bar(ax_img, length_in_um=100,
              position=(1300, 200))

ax_img.tick_params(axis='both', which='major', labelsize=14)
# ----------------------

plt.tight_layout()
plt.show()
plt.show()