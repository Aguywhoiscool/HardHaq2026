"""Build the additional-research bibliography, excluding duplicates and starter content."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
report = (ROOT / 'FINAL_ION_TRAP_RESEARCH_REPORT.md').read_text(encoding='utf-8')
resources = {}
for label, url in re.findall(r'\[([^\]]+)\]\((https?://[^\s]+)\)', report):
    resources.setdefault(url, label)

# Use publication metadata already established in the notebooks/research.
# Unverified fields are omitted rather than guessed.
full = {
1: 'A. H. Nizamani and W. K. Hensinger, “Optimum electrode configurations for fast ion separation in microfabricated surface ion traps,” arXiv:1007.3542, 2011.',
2: 'D. T. C. Allcock et al., “Implementation of a symmetric surface electrode ion trap with field compensation using a modulated Raman effect,” New J. Phys., vol. 12, Art. no. 053026, 2010, doi: 10.1088/1367-2630/12/5/053026.',
3: 'J. H. Wesenberg, “Electrostatics of surface-electrode ion traps,” arXiv:0808.1623, 2008.',
4: 'J. Chiaverini et al., “Surface-electrode architecture for ion-trap quantum information processing,” Quantum Inf. Comput., vol. 5, no. 6, pp. 419–439, 2005, doi: 10.26421/QIC5.6-1.',
5: 'J. Britton, “Microfabrication techniques for trapped ion quantum information processing,” Ph.D. dissertation, 2008.',
6: 'K. McCormick, “Control and measurement of a single-ion quantum harmonic oscillator,” Ph.D. dissertation.',
7: 'R. Schmied, “Electrostatics of gapped and finite surface electrodes,” New J. Phys., vol. 12, Art. no. 023038, 2010, doi: 10.1088/1367-2630/12/2/023038.',
8: 'J. Tao et al., “Functional surface ion traps on a 12-inch glass wafer for quantum applications,” arXiv:2002.11470, 2020.',
9: 'R. A. Matula, “Electrical resistivity of copper, gold, palladium, and silver,” J. Phys. Chem. Ref. Data, vol. 8, p. 1147, 1979.',
10: 'Massachusetts Institute of Technology, “Section 14.9,” Electromagnetic Fields and Energy.',
11: 'J. Chiaverini and J. M. Sage, “Insensitivity of the rate of ion motional heating to trap-electrode material over a large temperature range,” Phys. Rev. A, vol. 89, Art. no. 012318, 2014, doi: 10.1103/PhysRevA.89.012318.',
12: 'S. X. Wang, G. H. Low, N. S. Lachenmyer, Y. Ge, P. F. Herskind, and I. L. Chuang, “Laser-induced charging of microfabricated ion traps,” arXiv:1108.0092, 2012.',
13: '“Analytic procedure for the evaluation of copper intermetallic diffusion in electroplated gold coatings with energy dispersive X-ray microanalysis,” 2023.',
14: 'M. G. House, “Analytic model for electrostatic fields in surface-electrode ion traps,” Phys. Rev. A, vol. 78, Art. no. 033402, 2008, doi: 10.1103/PhysRevA.78.033402.',
15: 'D. Leibfried, R. Blatt, C. Monroe, and D. Wineland, “Quantum dynamics of single trapped ions,” Rev. Mod. Phys., vol. 75, p. 281, 2003, doi: 10.1103/RevModPhys.75.281.',
16: 'I. Gerasin et al., “Optimized surface ion trap design for tight confinement and separation of ion chains,” Quantum Rep., vol. 6, no. 3, 2024, doi: 10.3390/quantum6030029.',
17: 'T. Abbasov, S. Zibrov, and I. Sherstov, “Surface-electrode ion trap development,” JETP Lett., vol. 118, no. 3, pp. 215–219, 2023, doi: 10.1134/S0021364023602063.',
18: 'A. H. Nizamani and W. K. Hensinger, “Optimum electrode configurations for fast ion separation in microfabricated surface ion traps,” Appl. Phys. B, vol. 106, no. 2, pp. 327–338, 2012, doi: 10.1007/s00340-011-4803-x.',
19: 'Flexcompute, “photonforge.Technology,” PhotonForge documentation.',
20: 'Flexcompute, “photonforge.PortSpec,” PhotonForge documentation.',
21: '“Guidelines for designing surface ion traps using the boundary element method,” Sensors, vol. 16, no. 5, Art. no. 616, 2016, doi: 10.3390/s16050616.',
22: '“Guidelines for designing surface ion traps using the boundary element method,” Sensors, vol. 16, no. 5, Art. no. 616, 2016. PubMed Central copy.',
23: '“Controlling trapping potentials and stray electric fields in a microfabricated ion trap through design and compensation,” New J. Phys., vol. 14, Art. no. 073012, 2012, doi: 10.1088/1367-2630/14/7/073012.',
24: '“Optimization of two-dimensional ion trap arrays for quantum simulation,” New J. Phys., vol. 14, Art. no. 085009, 2012, doi: 10.1088/1367-2630/14/8/085009.',
25: '“Surface ion trap for fast microwave gates,” MDPI, vol. 4, no. 4, Art. no. 41.',
26: '“Electron impact ionization loading of a surface electrode ion trap,” arXiv:quant-ph/0603142, 2006.',
27: '“Demonstration of a microfabricated surface electrode ion trap,” arXiv:1008.0990, 2010.',
28: '“Cryogenic surface ion trap based on intrinsic silicon,” New J. Phys., vol. 16, Art. no. 113068, 2014, doi: 10.1088/1367-2630/16/11/113068.',
29: '“Fabrication and heating rate study of microscopic surface electrode ion traps,” arXiv:1009.2834, 2010.',
30: '“Ion trap with gold-plated alumina: Substrate and surface characterization,” arXiv:2207.06878, 2022.',
32: '“Design of a surface electrode trap for parallel ion strings,” J. Phys. B, vol. 47, Art. no. 035301, 2014, doi: 10.1088/0953-4075/47/3/035301.',
36: '“TSV-integrated surface electrode ion trap for scalable quantum information processing,” arXiv:2101.00869, 2021.',
37: '“Fabrication of surface ion traps with integrated current carrying wires enabling high magnetic field gradients,” arXiv:2202.02313, 2022.',
38: '“Large-scale fabrication of surface ion traps on a 300 mm glass wafer,” Phys. Status Solidi B, Art. no. 2000589, 2021, doi: 10.1002/pssb.202000589.',
39: 'J. Tao et al., “3D integration of CMOS-compatible surface electrode ion trap and silicon photonics for scalable quantum computing,” in Proc. IEEE Electron. Compon. Technol. Conf. (ECTC), 2019, pp. 1735–1743, doi: 10.1109/ECTC.2019.00266.',
40: '“Reduction of heating rate in a microfabricated ion trap by pulsed-laser cleaning,” New J. Phys., vol. 13, Art. no. 123023, 2011, doi: 10.1088/1367-2630/13/12/123023.',
42: 'Leibniz University Hannover, Institute of Quantum Optics, “Surface-electrode trap fabrication.”',
44: '“ECTI 2010 conference booklet,” 2010. Includes NPL poster, “Development of monolithic 3D ion traps microfabricated using Si-on-SiO₂.”',
50: 'neQxt, “Ion trap Gen1.”',
51: '“Ion trap manufacturing methods,” European Patent EP4645178B1.',
52: '“Device for trapping an ion, method for forming the same, and method for controlling the same,” Patent Application WO2021006811A1, 2021.',
53: 'National Institute of Standards and Technology, “Effects of barrier composition and electroplating chemistry on adhesion and voiding in copper/dielectric diffusion barrier films.”',
56: '“Electroplated products and electroplating bath for providing such products,” European Patent Application EP3540097A1.',
57: '“The influence of the skin phenomenon on the impedance of thin conductive layers,” Electronics, vol. 12, no. 23, Art. no. 4834, 2023, doi: 10.3390/electronics12234834.',
58: '“Electromagnetic characterisation of materials by using transmission/reflection (T/R) devices,” Electronics, vol. 6, no. 4, Art. no. 95, 2017, doi: 10.3390/electronics6040095.',
59: '“Thin Ohmic or superconducting strip with an applied ac electric current,” arXiv:cond-mat/0603416, 2006.',
60: '“Study of the anomalous skin effect of normal conducting film,” arXiv:2004.11462, 2020.',
63: '“High-precision reflectometer for submillimeter wavelengths,” J. Opt. Soc. Am. B, vol. 12, no. 2, p. 212, 1995.',
}

# These entries only had descriptive/truncated link labels in the research log.
# Explicitly identify descriptions instead of presenting them as verified titles.
descriptions = {
43: '“Engineered microwave control for trapped ions,” thesis, TIB-hosted copy.',
45: 'University of Oxford, “Thesis concerning benchmarking” [repository document; full title and author not verified].',
46: 'University of Oxford, “Thesis concerning high-fidelity microwave-driven ion control” [repository document; full title and author not verified].',
47: 'J. Joger, “Diploma thesis” [full title not verified], 2013.',
48: 'National Institute of Standards and Technology, “Trapped-ion review” [hosted PDF; bibliographic metadata not verified].',
49: '“Nanoscale interfacial structure for novel opto-electronic and ion-trapping” [dissertation; complete title and author not verified].',
62: 'U.S. Particle Accelerator School, “Normal-conducting surface resistance” [lecture slides].',
64: 'Research Measurements, “Low temperature materials data.”',
65: 'Academia.edu, “Optimum electrode configurations for fast ion separation in microfabricated surface ion traps” [secondary copy].',
66: 'ResearchGate, “The planar trap designs” [figure from Nizamani and Hensinger].',
67: 'Academia.edu, “Implementation of a symmetric surface-electrode ion trap with field compensation using a modulated Raman effect” [secondary copy].',
68: 'ArxivLens, “Functional surface ion traps on a 12-inch glass wafer for quantum applications” [secondary copy].',
69: 'AlphaXiv, “Electrostatics of gapped and finite surface electrodes” [secondary record].',
70: 'MaRDI Portal, “Electrostatics of gapped and finite surface electrodes” [bibliographic record].',
71: 'R. Schmied, “Electrostatics of gapped and finite surface electrodes,” 2010 [University of Basel PDF copy].',
72: 'EurekaMag, “3D integration of CMOS-compatible surface electrode ion trap and silicon photonics for scalable quantum computing” [secondary record].',
73: 'SciRate, “au:Henner_T in:physics” [search results].',
74: 'Wikipedia, “Electrical resistivity and conductivity.”',
75: 'Wikipedia, “Electrical resistivities of the elements (data page).”',
76: 'Wikipedia, “Gold.”',
77: 'Wikipedia, “Gold plating.”',
78: 'Wikipedia, “Skin effect.”',
79: 'The Physics Factbook, “Resistivity of gold.”',
80: 'Refmanual, “Electrical resistivity chart.”',
81: 'Distymap, “Metal electrical resistivity reference table (293 K and 300 K)” [English description of Japanese page].',
82: 'Engineering LibreTexts, “2.7: Resistance and conductance.”',
}

header = '''# IEEE-style bibliography — additional research

This bibliography contains 12 sources that contribute evidence beyond `starter_file_given.ipynb`: constrained geometry optimization, mode rotation, practical fabrication thicknesses, finite-gap corrections, Cu/Au electrodes, conductor losses, surface charging and diffusion.

Removed: the starter's Chiaverini, House and Leibfried references and PhotonForge documentation; duplicate preprint/journal records and mirrors; general introductions that repeat the starter; search listings, secondary tables, commercial pages and background discoveries not needed to support our conclusions. Nizamani and Hensinger is retained because its geometry-ratio and asymmetry analysis goes beyond the starter. The complete historical resource trail remains in the research report.

Known publication metadata is included. Unestablished fields are omitted rather than guessed. No access dates are invented.

'''
lines = [header]
# One record per retained work; order follows the reasoning in the investigation.
keep = [18, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 42]
indexed = list(resources.items())
for number, index in enumerate(keep, 1):
    url, label = indexed[index-1]
    entry = full.get(index, descriptions.get(index, f'“{label}.”'))
    lines.append(f'[{number}] {entry} [Online]. Available: <{url}>\n')

assert len(resources) == 82
out = ROOT / 'IEEE_BIBLIOGRAPHY.md'
out.write_text('\n'.join(lines), encoding='utf-8')
print(f'Created {out.name} with {len(keep)} numbered entries.')
