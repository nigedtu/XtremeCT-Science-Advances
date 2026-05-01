import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch

# -----------------------------
# Helper
# -----------------------------
def add_quad(ax, points, color, label, text_xy=None, alpha=0.45, lw=2, ls='--', zorder=4):
    poly = Polygon(
        points,
        closed=True,
        facecolor=color,
        edgecolor='k',
        linewidth=lw,
        linestyle=ls,
        alpha=alpha,
        zorder=zorder
    )
    ax.add_patch(poly)

    if text_xy is None:
        xs = np.array([p[0] for p in points])
        ys = np.array([p[1] for p in points])
        text_xy = (10 ** np.mean(np.log10(xs)), 10 ** np.mean(np.log10(ys)))

    ax.text(
        text_xy[0], text_xy[1], label,
        fontsize=16, weight='bold',
        ha='center', va='center',
        zorder=zorder + 1
    )
    return poly

# -----------------------------
# Figure and axes
# -----------------------------
fig, ax = plt.subplots(figsize=(10, 8.5), dpi=150)

ax.set_xscale("log")
ax.set_yscale("log")

ax.set_xlim(0.004, 2000)
ax.set_ylim(5e-11, (4000)**3)

ax.set_xlabel("Spatial resolution (μm)", fontsize=18, fontstyle='normal')
ax.set_ylabel(r"Sample volume (mm$^3$)", fontsize=18, fontstyle='normal')
#ax.set_title("Sample volume vs. resolution in 3D imaging", fontsize=24, weight="bold")

# Grid
ax.grid(True, which="major", color="gray", alpha=0.4, linewidth=1.0)

# -----------------------------
# Custom ticks
# -----------------------------
ax.set_xticks([0.01, 0.1, 1, 10, 100, 1000])
ax.set_xticklabels(['0.01', '0.1', '1', '10', '100', '1000'], fontsize=16)

y_ticks = [
    (0.001)**3,
    (0.1)**3,
    (1)**3,
    (10)**3,
    (50)**3,
    (100)**3,
    (600)**3
]
y_labels = [
    r'0.001$^3$',
    r'0.1$^3$',
    r'1$^3$',
    r'10$^3$',
    r'50$^3$',
    r'100$^3$',
    r'600$^3$'
]
ax.set_yticks(y_ticks)
ax.set_yticklabels(y_labels, fontsize=16)

# Remove tick marks but keep tick labels
ax.tick_params(axis='both', which='both', length=0, width=0, pad=6)

# -----------------------------
# Sample size smaller than resolution
# -----------------------------
x = np.logspace(np.log10(ax.get_xlim()[0]), np.log10(ax.get_xlim()[1]), 800)
y_floor = ax.get_ylim()[0]
y_limit = (x * 1e-3) ** 3

ax.fill_between(
    x,
    y_floor,
    y_limit,
    where=(y_limit > y_floor),
    color="#4a2500",
    alpha=1.0,
    zorder=1
)

ax.text(
    30, 2e-7,
    "Sample size smaller\nthan resolution",
    color="white",
    fontsize=16,
    ha="left",
    va="center",
    zorder=3
)

# Stippled diagonal guide (anchored to TEM bottom-left and MRI top-right)
# Anchor points
x1, y1 = 0.005, 1e-9          # TEM lower-left
x2, y2 = 2000, (4000)**3      # MRI upper-right

# Solve for power law y = a * x^b
b = (np.log10(y2) - np.log10(y1)) / (np.log10(x2) - np.log10(x1))
a = y1 / (x1**b)

# Plot
ax.plot(
    x,
    a * (x**b),
    linestyle=":",
    color="black",
    linewidth=3,
    zorder=5
)
#--------------------
# Imaging regimes
# -----------------------------

# FIB-SEM (serial sectioning tomography)
fibsem_points = [
    (0.005, 1e-9),   # 5 nm,   1e-9 mm^3   -> lower-left  : best resolution at smallest volume
    (0.03,  1e-9),   # 30 nm,  1e-9 mm^3   -> lower-right : worst resolution at smallest volume
    (0.05,  1e-6),   # 50 nm,  1e-6 mm^3   -> upper-right : worst resolution at largest volume
    (0.01,  1e-6),   # 10 nm,  1e-6 mm^3   -> upper-left  : best resolution at largest volume
]

add_quad(
    ax, fibsem_points,
    color="#6bc5ff",
    label="FIB-SEM",
    text_xy=(0.017, 5e-8),
    alpha=0.55,
    ls='-'
)


# TEM (3D electron tomography)
tem_points = [
    (0.001, 1e-12),   # 1 nm,   1e-12 mm^3  -> lower-left
    (0.02,  1e-12),   # 20 nm,  1e-12 mm^3  -> lower-right
    (0.02,  1e-9),    # 20 nm,  1e-9 mm^3   -> upper-right
    (0.005, 1e-9),    # 5 nm,   1e-9 mm^3   -> upper-left
]

add_quad(
    ax, tem_points,
    color="#ff6b6b",
    label="TEM",
    text_xy=(0.009, 2e-10),
    alpha=0.65,
    ls='-'
)

# X-ray microscopy (3D)
xrm_points = [
    (0.063, 1.7e-5),   # 63 nm,   1.7e-5 mm^3   -> lower-left  : best resolution at smallest volume
    (0.5,   1e-4),   # 0.5 µm,  1e-4 mm^3   -> lower-right : worst resolution at smallest volume
    (14,    10),     # 14 µm,   10 mm^3     -> upper-right : worst resolution at largest volume
    (1,     10),     # 1 µm,    10 mm^3     -> upper-left  : best resolution at largest volume
]
add_quad(
    ax, xrm_points,
    color="#a8c5d6",
    label="X-ray\nmicroscopy",
    text_xy=(1.3, 0.11),
    alpha=0.48,
    ls='-'
)

# XtremeCT

xtremect_points = [
    (0.1,  1.0),   # 0.1 µm (100 nm),   1 mm^3    -> best resolution at small volume
    (0.5, 1.0),
    (5.0,  2700),
    (1.0,  2700),  # 1.5 µm,         2700 mm^3    -> best resolution at largest volume    19.4 mm × 19.4 mm × 7.3 mm  gives ~2700 mm³  (14176*0.68363636363*2)*(14176*0.68363636363*2)*(10640*0.68363636363)
]

add_quad(
    ax, xtremect_points,
    color="#7CFC00",
    label="XtremeCT",
    text_xy=(0.3, 5),
    alpha=0.45,
    ls='-'
)


# in vivo microCT
invivo_points = [
    (20,   20),      # lower-left  : best resolution at smallest volume
    (100,  20),      # lower-right : worse resolution at smallest volume
    (200, 2000),     # upper-right : worse resolution at largest volume
    (30,  2000),     # upper-left  : best resolution at largest volume
]


add_quad(
    ax, invivo_points,
    color="#f0b47a",
    label="in vivo\nμCT",
    text_xy=(58, 120),
    alpha=0.45,
    ls='-'
)

# MRI (3D)
mri_points = [
    (100,   1e3),           # lower-left  : best resolution, smaller volume
    (1000,  1e3),           # lower-right : typical resolution, smaller volume

    (2000,  (4000)**3),     # upper-right : worst realistic MRI resolution at max volume
    (150,   (4000)**3),     # upper-left  : best resolution at max volume
]

add_quad(
    ax, mri_points,
    color="#c49ae8",
    label="MRI",
    text_xy=(400, 2.2e4),
    alpha=0.50,
    ls='-'
)

# Clinical CT (hospital CT)
ct_points = [
    (300,  1e6),    # 300 µm,  1e6 mm^3   -> lower-left  : best resolution at smaller volume
    (1000, 1e6),    # 1 mm,    1e6 mm^3   -> lower-right : worst resolution at smaller volume
    (1000, 1e8),    # 1 mm,    1e8 mm^3   -> upper-right : worst resolution at largest volume
    (300,  1e8),    # 300 µm,  1e8 mm^3   -> upper-left  : best resolution at largest volume
]

add_quad(
    ax, ct_points,
    color="#b0b0b0",   # neutral gray (clinical modality)
    label="CT",
    text_xy=(550, 9e6),
    alpha=0.5,
    ls='-'
)
# -----------------------------
# Blue guide lines
# -----------------------------
ax.axvline(1.0, color="blue", linestyle="--", linewidth=1.4, alpha=0.8)
ax.axhline(20.0, color="blue", linestyle="--", linewidth=1.4, alpha=0.8)

# -----------------------------
# Arrows (equal visual size using axes coords)
# -----------------------------

# Cells arrow (leftward) - more left
cells_arrow = FancyArrowPatch(
    posA=(0.38, 0.78),
    posB=(0.28, 0.78),
    transform=ax.transAxes,
    arrowstyle="simple",
    mutation_scale=45,
    fc="blue",
    ec="navy",
    alpha=0.7,
    zorder=6
)
ax.add_patch(cells_arrow)

ax.text(
    0.24, 0.81, "visualise cell structure",
    transform=ax.transAxes,
    color="blue",
    fontsize=15,
    ha="center"
)

# Tissue arrow (upward) - more up
tissue_arrow = FancyArrowPatch(
    posA=(0.25, 0.63),
    posB=(0.25, 0.73),
    transform=ax.transAxes,
    arrowstyle="simple",
    mutation_scale=45,
    fc="blue",
    ec="navy",
    alpha=0.7,
    zorder=6
)
ax.add_patch(tissue_arrow)

ax.text(
    0.18, 0.6, "visualise tissue organisation",
    transform=ax.transAxes,
    color="blue",
    fontsize=15,
    ha="center"
)
# -----------------------------
# Final polish
# -----------------------------
for spine in ax.spines.values():
    spine.set_linewidth(1.2)

plt.tight_layout()
plt.show()