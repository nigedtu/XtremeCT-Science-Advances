import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# =========================================================
# FILE PATH (Downloads)
# =========================================================
h5_path = r"C:\Users\nige\Downloads\oblique_flipped.h5"

if not os.path.exists(h5_path):
    raise FileNotFoundError(f"File not found:\n{h5_path}")

# =========================================================
# LOAD DATA
# =========================================================
with h5py.File(h5_path, "r") as f:
    print("Datasets in file:", list(f.keys()))
    dset = f["oblique_flipped"]
    img = dset[:]   # load into RAM

nz, nt = img.shape
print("Image shape:", img.shape)

# =========================================================
# GEOMETRY / PIXEL SIZE
# =========================================================
detector_distance_mm = 6730.0
sample_to_detector_mm = 20.0

pixel_size_detector_um = 3.76 / 5.5  # µm

magnification = detector_distance_mm / (detector_distance_mm - sample_to_detector_mm)
pixel_size_um = pixel_size_detector_um / magnification

print("Magnification:", magnification)
print("Effective pixel size (µm):", pixel_size_um)

# Physical size in µm
width_um = nt * pixel_size_um
height_um = nz * pixel_size_um

extent = [0, width_um, 0, height_um]

# =========================================================
# SCALE BAR FUNCTION (label BELOW bar)
# =========================================================
def add_scalebar(ax,
                 scale_length_um,
                 bar_thickness_um=50,
                 pad_fraction=0.04,
                 color="white",
                 fontsize=18):

    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()

    width = x_max - x_min
    height = y_max - y_min

    pad_x = width * pad_fraction
    pad_y = height * pad_fraction

    bar_x = x_max - scale_length_um - pad_x
    bar_y = y_min + pad_y

    # horizontal bar
    rect = patches.Rectangle(
        (bar_x, bar_y),
        scale_length_um,
        bar_thickness_um,
        color=color
    )
    ax.add_patch(rect)

    # label BELOW bar
    ax.text(
        bar_x + scale_length_um / 2,
        bar_y - pad_y * 0.3,
        f"{scale_length_um:.0f} µm",
        color=color,
        ha="center",
        va="top",
        fontsize=fontsize
    )

# =========================================================
# PLOT FULL IMAGE
# =========================================================
fig, ax = plt.subplots(figsize=(14, 6))

im = ax.imshow(img,
               cmap="bone",
               aspect="auto",
               extent=extent)

ax.set_xlabel("Distance along line (µm)")
ax.set_ylabel("Z position (µm)")
ax.set_title("Oblique slice")

# Add scale bar (5000 µm)
add_scalebar(ax, 5000)

# Panel label (a)
ax.text(0.02, 0.02, '(a)',
        transform=ax.transAxes,
        fontsize=22,
        color='white',
        ha='left',
        va='bottom')

plt.tight_layout()
plt.show()
#%%
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# -------------------------------------------------
# Define red boxes in IMAGE pixel coordinates
# (x = column index, y = row index)
# -------------------------------------------------

# Upper red box
x1_start, x1_end = 9500, 10800
y1_start, y1_end = 1900, 3100

# Lower red box
x2_start, x2_end = 9500, 11119
y2_start, y2_end = 3925, 5125


# =================================================
# Plot image
# =================================================
fig, ax = plt.subplots(figsize=(14, 6))

ax.imshow(img, cmap="bone", aspect="auto")

# -------------------------------------------------
# Draw red boxes
# -------------------------------------------------
ax.add_patch(
    patches.Rectangle(
        (x1_start, y1_start),
        x1_end - x1_start,
        y1_end - y1_start,
        edgecolor="red",
        facecolor="none",
        linewidth=2
    )
)

ax.add_patch(
    patches.Rectangle(
        (x2_start, y2_start),
        x2_end - x2_start,
        y2_end - y2_start,
        edgecolor="red",
        facecolor="none",
        linewidth=2
    )
)

# Panel label
ax.text(0.02, 0.02, "(a)",
        transform=ax.transAxes,
        fontsize=22,
        color="white",
        ha="left",
        va="bottom")

plt.tight_layout()
plt.show()


#%%


import matplotlib.patches as patches

def add_scalebar(ax,
                 scale_length_um,
                 pixel_size_um,
                 x_offset_fraction=0.95,   # 0=left, 1=right
                 y_offset_fraction=0.05,   # 0=bottom, 1=top
                 bar_thickness_px=40,
                 text_offset_px=20,
                 color="white",
                 fontsize=25):

    # Get axis limits (pixel coords)
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()

    width = x_max - x_min
    height = y_max - y_min

    # Convert scale length to pixels
    scale_length_px = scale_length_um / pixel_size_um

    # Compute position
    bar_x = x_min + width * x_offset_fraction - scale_length_px
    bar_y = y_min + height * y_offset_fraction

    # Draw bar
    rect = patches.Rectangle(
        (bar_x, bar_y),
        scale_length_px,
        bar_thickness_px,
        color=color
    )
    ax.add_patch(rect)

    # Draw text (below bar)
    ax.text(
        bar_x + scale_length_px / 2,
        bar_y - text_offset_px,
        f"{scale_length_um:.0f} µm",
        color=color,
        ha="center",
        va="top",
        fontsize=fontsize
    )

#%%

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# -------------------------------------------------
# Your fixed box coordinates
# -------------------------------------------------

# Upper red box → (b)
x1_start, x1_end = 9500, 10800
y1_start, y1_end = 1900, 3100

# Lower red box → (c)
x2_start, x2_end = 9500, 11119
y2_start, y2_end = 3925, 5125


# =================================================
# (a) FULL IMAGE
# =================================================
fig_a, ax_a = plt.subplots(figsize=(14, 6))
ax_a.imshow(img, cmap="bone", aspect="auto")

# Red boxes
ax_a.add_patch(
    patches.Rectangle((x1_start, y1_start),
                      x1_end - x1_start,
                      y1_end - y1_start,
                      edgecolor="red",
                      facecolor="none",
                      linewidth=2)
)

ax_a.add_patch(
    patches.Rectangle((x2_start, y2_start),
                      x2_end - x2_start,
                      y2_end - y2_start,
                      edgecolor="red",
                      facecolor="none",
                      linewidth=2)
)

# Remove ticks/labels
ax_a.set_xticks([])
ax_a.set_yticks([])
ax_a.set_xlabel("")
ax_a.set_ylabel("")

# Panel label
#ax_a.text(0.02, 0.02, "(a)",
#          transform=ax_a.transAxes,
#          fontsize=25,
#          color="white",
#          ha="left",
#          va="bottom")

# Adjustable scale bar
add_scalebar(ax_a,
             scale_length_um=5000,
             pixel_size_um=pixel_size_um,
             x_offset_fraction=0.95,
             y_offset_fraction=0.08,
             bar_thickness_px=50,
             text_offset_px=-100)

plt.tight_layout()
plt.show()

#%%
# =================================================
# (b) UPPER ZOOM
# =================================================
crop_b = img[y1_start:y1_end, x1_start:x1_end]

fig_b, ax_b = plt.subplots(figsize=(6, 6))
ax_b.imshow(crop_b, cmap="bone", aspect="equal")

ax_b.set_xticks([])
ax_b.set_yticks([])
ax_b.set_xlabel("")
ax_b.set_ylabel("")

#ax_b.text(0.02, 0.02, "(b)",
#          transform=ax_b.transAxes,
#          fontsize=25,
#          color="white",
#          ha="left",
#          va="bottom")

add_scalebar(ax_b,
             scale_length_um=500,
             pixel_size_um=pixel_size_um,
             x_offset_fraction=0.95,
             y_offset_fraction=0.1,
             bar_thickness_px=30,
             text_offset_px=-40)

# Red box in crop_b coordinates
x_start, x_end = 609, 755
y_start, y_end = 570, 690   # FIXED order (min → max)

ax_b.add_patch(
    patches.Rectangle(
        (x_start, y_start),
        x_end - x_start,
        y_end - y_start,
        edgecolor="red",
        facecolor="none",
        linewidth=2
    )
)

plt.tight_layout()
plt.show()
#%%

# =================================================
# (e) ZOOM OF RED BOX FROM (b)
# =================================================

# Red box coordinates in crop_b coordinates
x_start, x_end = 609, 755
y_start, y_end = 570, 690   # (min → max)

# Crop the red-box region from crop_b
crop_e = crop_b[y_start:y_end, x_start:x_end]

fig_e, ax_e = plt.subplots(figsize=(6, 6))
ax_e.imshow(crop_e, cmap="bone", aspect="equal")

ax_e.set_xticks([])
ax_e.set_yticks([])
ax_e.set_xlabel("")
ax_e.set_ylabel("")

add_scalebar(ax_e,
             scale_length_um=50,   # match your (d)-style zoom
             pixel_size_um=pixel_size_um,
             x_offset_fraction=0.55,
             y_offset_fraction=0.15,
             bar_thickness_px=6,
             text_offset_px=-10)

plt.tight_layout()
plt.show()

#%%
# =================================================
# (c) LOWER ZOOM
# =================================================
crop_c = img[y2_start:y2_end, x2_start:x2_end]

fig_c, ax_c = plt.subplots(figsize=(6, 6))
ax_c.imshow(crop_c, cmap="bone", aspect="equal")

ax_c.set_xticks([])
ax_c.set_yticks([])
ax_c.set_xlabel("")
ax_c.set_ylabel("")

#ax_c.text(0.02, 0.02, "(c)",
#          transform=ax_c.transAxes,
#          fontsize=25,
#          color="white",
#          ha="left",
#          va="bottom")

add_scalebar(ax_c,
             scale_length_um=500,
             pixel_size_um=pixel_size_um,
             x_offset_fraction=0.95,
             y_offset_fraction=0.1,
             bar_thickness_px=30,
             text_offset_px=-40)

# Red box in crop_c coordinates
x_start, x_end = 465, 650
y_start, y_end = 497, 665   # IMPORTANT: use min→max

ax_c.add_patch(
    patches.Rectangle(
        (x_start, y_start),
        x_end - x_start,
        y_end - y_start,
        edgecolor="red",
        facecolor="none",
        linewidth=2
    )
)

plt.tight_layout()
plt.show()
#%%
#%%
# =================================================
# (d) ZOOM OF RED BOX FROM (c)
# =================================================

# Red box coordinates in crop_c coordinates
x_start, x_end = 465, 650
y_start, y_end = 497, 665

# Crop the red-box region from crop_c
crop_d = crop_c[y_start:y_end, x_start:x_end]

fig_d, ax_d = plt.subplots(figsize=(6, 6))
ax_d.imshow(crop_d, cmap="bone", aspect="equal")

ax_d.set_xticks([])
ax_d.set_yticks([])
ax_d.set_xlabel("")
ax_d.set_ylabel("")

add_scalebar(ax_d,
             scale_length_um=50,   # adjust if needed
             pixel_size_um=pixel_size_um,
             x_offset_fraction=0.6,
             y_offset_fraction=0.15,
             bar_thickness_px=8,
             text_offset_px=-10)

plt.tight_layout()
plt.show()
