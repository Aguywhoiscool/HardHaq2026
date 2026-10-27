# standard python imports
import matplotlib.pyplot as plt
import numpy as np
import tidy3d as td
from tidy3d import web

td.config.local_cache.enabled = False

# Wavelength and frequency range
freq_range = (200e12, 400e12)
lambda_range = (td.constants.C_0 / freq_range[1], td.constants.C_0 / freq_range[0])
freq0 = np.sum(freq_range) / 2
Nfreq = 301

# frequencies and wavelengths of monitor
monitor_freqs = np.linspace(freq_range[0], freq_range[1], Nfreq)
monitor_lambdas = td.constants.C_0 / monitor_freqs

# central frequency, frequency pulse width and total running time
lambda0 = td.C_0 / freq0
bandwidth = 0.18  # bandwidth of source in units of delta frequency.  0.38 for broadband

freqw = bandwidth * (freq_range[1] - freq_range[0])
t_stop = 100 / freq0

# Thickness and refractive index of slab
t_slab = 0.5
n_slab = 3.5
mat_slab = td.Medium(permittivity=n_slab**2, name="silicon")

# Grid resolution (cells per um)
# dl = lambda_range[0] / 30 / n_slab
dl = 6e-3

# space between slabs and sources and PML
spacing = 1 * lambda_range[-1]

# simulation size
sim_size = Lx, Ly, Lz = (2.0, 2.0, 2 * spacing + t_slab)

def slab_analytical(d, n, wvl):
    """computes transmission as a function of slab thickness (d), refractive index (n), and wavelength (wvl)."""
    rho = (n - 1) / (n + 1)
    t = ((1 + rho) * (1 - rho) * np.exp(-2j * np.pi * n * d / wvl)) / (
        1 - rho**2 * np.exp(-4j * np.pi * n * d / wvl)
    )
    return np.abs(t) ** 2
transmission_analytical = slab_analytical(t_slab, n_slab, monitor_lambdas)
plt.figure()
plt.plot(monitor_freqs / 1e12, transmission_analytical, "k", label="analytical")
plt.xlabel("frequency (THz)")
plt.ylabel("Transmitted")
plt.legend()
plt.show()

slab = td.Structure(
    geometry=td.Box(
        center=(0, 0, -Lz / 2 + spacing + t_slab / 2),
        size=(td.inf, td.inf, t_slab),
    ),
    medium=mat_slab,
    name="slab",
)

# Here we define the planewave source, placed just in advance (towards negative z) of the slab
source = td.PlaneWave(
    source_time=td.GaussianPulse(freq0=freq0, fwidth=freqw),
    size=(td.inf, td.inf, 0),
    center=(0, 0, -Lz / 2 + spacing / 2),
    direction="+",
    pol_angle=0,
    name="planewave",
)

# We are interested in measuring the transmitted flux, so we set it to be an oversized plane.
monitor = td.FluxMonitor(
    center=(0, 0, Lz / 2 - spacing / 2),
    size=(td.inf, td.inf, 0),
    freqs=monitor_freqs,
    name="flux",
)

sim = td.Simulation(
    center=(0, 0, 0),
    size=sim_size,
    grid_spec=td.GridSpec.uniform(dl=dl),
    structures=[slab],
    sources=[source],
    monitors=[monitor],
    run_time=t_stop,
    boundary_spec=td.BoundarySpec.pml(z=True),
    normalize_index=None,
)

sim.plot(x=0)
plt.show()

# plot the permittivity
freqs_plot = (freq_range[0], freq_range[1])
fig, ax = plt.subplots(1, tight_layout=True, figsize=(8, 4))
sim.plot_eps(x=0, freq=None, ax=ax)
plt.show()

times = np.arange(0, sim.run_time, sim.dt)
amps = np.real(sim.sources[0].source_time.amp_time(times))

# Check probe and source
f, (ax1, ax2) = plt.subplots(1, 2, tight_layout=True, figsize=(8, 4))
ax1 = sim.sources[0].source_time.plot(times=np.linspace(0, sim.run_time, 1001), ax=ax1)
ax1.set_xlim(0, sim.run_time)
ax1.legend(("source amplitude",))
ax2 = sim.sources[0].source_time.plot_spectrum(
    times=np.linspace(0, sim.run_time, 1001), val="abs", ax=ax2
)
fill_max = 30e-16  # 10e-16
ymax = 50e-16  # 20e-16
ax2.fill_between(
    freq_range, [-0e-16, -0e-16], [fill_max, fill_max], alpha=0.4, color="g"
)
ax2.legend(("source spectrum", "measurement"))
ax2.set_ylim(-1e-16, ymax)
plt.show()

sim0 = sim.copy(update={"structures": []})
batch = {
    "lecture02_slab_narrowband_normalization": sim0,
    "lecture02_slab_narrowband_transmission": sim,
}

batch_data = web.run_async(simulations=batch, path_dir="data")

sim_data0 = batch_data["lecture02_slab_narrowband_normalization"]
sim_data = batch_data["lecture02_slab_narrowband_transmission"]

# Retrieve the power flux through the monitor plane.
transmission0 = sim_data0["flux"].flux
transmission = sim_data["flux"].flux
transmission_normalized = transmission / transmission0

f, (ax1, ax2) = plt.subplots(2, 1, figsize=(4, 7), tight_layout=True)
transmission0.plot(ax=ax1, label="no slab")
transmission.plot(ax=ax1, label="with slab")
transmission_normalized.plot(ax=ax2)
ax1.legend()
ax1.set_title("raw transmission")
ax2.set_title("normalized transmission")
plt.show()

plt.figure()
plt.plot(monitor_freqs / 1e12, transmission_analytical, "k", label="analytical")
plt.plot(monitor_freqs / 1e12, transmission_normalized, "b--", label="FDTD")
plt.xlabel("frequency (THz)")
plt.xlim([200, 400])
plt.ylabel("Transmitted")
plt.legend()
plt.show()

bandwidth = 0.38

freqw = bandwidth * (freq_range[1] - freq_range[0])

# make a copy of the original simulation, but change the frequency width of the source
bw_source = source.copy(
    update={"source_time": source.source_time.copy(update={"fwidth": freqw})}
)
sim_bw = sim.copy(update={"sources": [bw_source]})

# make the normalization simulation for this
sim_bw0 = sim_bw.copy(update={"structures": []})

# Check probe and source, looks now like the source spectrum fully covers the green square
f, (ax1, ax2) = plt.subplots(1, 2, tight_layout=True, figsize=(8, 4))
ax1 = sim_bw.sources[0].source_time.plot(
    times=np.linspace(0, sim_bw.run_time, 1001), ax=ax1
)
ax1.set_xlim(0, sim_bw.run_time)
ax1.legend(("source amplitude",))
ax2 = sim_bw.sources[0].source_time.plot_spectrum(
    times=np.linspace(0, sim_bw.run_time, 1001), val="abs", ax=ax2
)
fill_max = 15e-16
ymax = 20e-16
ax2.fill_between(
    freq_range, [-0e-16, -0e-16], [fill_max, fill_max], alpha=0.4, color="g"
)
ax2.legend(("source spectrum", "measurement"))
ax2.set_ylim(-1e-16, ymax)
plt.show()

batch = {
    "lecture02_slab_broadband_normalization": sim_bw0,
    "lecture02_slab_broadband_transmission": sim_bw,
}

batch_data = web.run_async(simulations=batch, path_dir="data")

sim_bw_data0 = batch_data["lecture02_slab_broadband_normalization"]
sim_bw_data = batch_data["lecture02_slab_broadband_transmission"]

# Retrieve the power flux through the monitor plane.
transmission0 = sim_bw_data0["flux"].flux
transmission = sim_bw_data["flux"].flux
transmission_normalized = transmission / transmission0

f, (ax1, ax2) = plt.subplots(2, 1, figsize=(4, 7), tight_layout=True)
transmission0.plot(ax=ax1, label="no slab")
transmission.plot(ax=ax1, label="with slab")
transmission_normalized.plot(ax=ax2)
ax1.legend()
ax1.set_title("raw transmission")
ax2.set_title("normalized transmission")
plt.show()


plt.figure()
plt.plot(monitor_freqs / 1e12, transmission_analytical, "k", label="analytical")
plt.plot(monitor_freqs / 1e12, transmission_normalized, "b--", label="FDTD")
plt.xlabel("frequency (THz)")
plt.xlim([200, 400])
plt.ylabel("Transmitted")
plt.legend()
plt.show()