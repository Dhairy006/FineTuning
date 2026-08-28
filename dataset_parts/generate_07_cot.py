import json

system_prompt = 'You are ZemaxGPT, an expert AI assistant for Zemax OpticStudio optical design. You provide precise, technically accurate guidance on sequential and non-sequential design, analysis, optimization, tolerancing, and ZOS-API programming.'

examples = []

def make_ex(instr, think, ans):
    return {'instruction': instr, 'system': system_prompt, 'response': f'<think>\n{think}\n</think>\n\n{ans}'}

def gen_cat1(i):
    specs = [
        ('achromatic doublet', '400-700nm', 'f=100mm, F/4'),
        ('Cooke triplet', '450-650nm', 'f=50mm, F/2.8'),
        ('Double Gauss', '400-700nm', 'f=35mm, F/1.4'),
        ('microscope objective', 'visible', '10x, NA=0.25'),
        ('Cassegrain telescope', 'IR', '200mm aperture, F/10')
    ]
    spec = specs[i % 5]
    instr = f'Design a {spec[0]} for {spec[1]} with {spec[2]}. Walk through the starting point and reasoning.'
    think = f'''Problem decomposition for {spec[0]}:
1. Requirements: {spec[1]}, {spec[2]}.
2. Initial setup: Set system aperture to correspond to {spec[2]}. Wavelengths set to {spec[1]} spectrum.
3. Glass selection logic: For {spec[0]}, we need specific crown/flint pairings or appropriate materials to correct chromatic aberration and spherical aberration.
4. Power distribution: The total optical power must equal 1/f. We distribute this among the elements to balance Petzval curvature and minimize individual element power.
5. Optimization: Set up a merit function using default RMS spot size, then transition to wavefront if diffraction-limited. Include boundary constraints (MNCG, MXCG) for manufacturability.'''
    ans = f'''To design the {spec[0]} with {spec[2]} for {spec[1]} in Zemax OpticStudio, follow these steps:

1. **System Setup**: Open the System Explorer. Set the Aperture Type to Entrance Pupil Diameter (EPD) or F/# depending on your specific target. Set the wavelengths to the {spec[1]} range.
2. **Glass Selection**: Start with standard glasses appropriate for the spectrum.
3. **Lens Data Editor (LDE)**: Enter the surface radii and thicknesses. Use the marginal ray height and paraxial power equations for your initial estimates, or use a known patent starting point.
4. **Optimization**:
   - Set radii and thicknesses as variables.
   - Build a Default Merit Function (Optimization > Merit Function > Default Merit Function). Use RMS Spot Size initially.
   - Add specific operands like EFFL to constrain the focal length to {spec[2].split(',')[0]}.
   - Add glass/air thickness constraints (CTGT, MNCA, etc.) to ensure manufacturability.
5. **Refinement**: Optimize and evaluate performance using the Ray Fan and Spot Diagram. Replace glasses with "Substitute" in optimization if better chromatic correction is needed.'''
    return make_ex(instr, think, ans)

def gen_cat2(i):
    instr = f'My merit function is stuck at {0.05 + i*0.01:.2f} after DLS optimization. How do I proceed?'
    think = '''1. Diagnosis: The DLS (Damped Least Squares) optimizer is stuck in a local minimum. A merit function value of ~0.05 indicates some residual aberrations remain uncorrected by the current variable set.
2. Alternatives: Hammer optimization or Global Search can escape local minima.
3. Variable check: Are there enough degrees of freedom? Maybe add an asphere or allow glass substitution.
4. Constraints check: Are boundary constraints (e.g., edge thickness) dominating the merit function? I need to check the merit function operand contributions.
5. Physics: If it is a field curvature issue, changing glass index (Petzval sum) or splitting a lens is required. DLS cannot jump these topology boundaries.'''
    ans = '''When DLS optimization gets stuck in a local minimum, follow this systematic approach:

1. **Analyze Merit Function Contributions**: Open your Merit Function editor and look at the '% Contribution' column. If boundary constraints (like edge thickness or glass boundaries) are dominating, your design is physically constrained. You may need to relax these or change the starting topology.
2. **Use Hammer Optimization**: Go to Optimization > Hammer Current. Hammer uses a genetic algorithm approach to jump out of local minima while preserving the system's basic structure. Let it run for a few minutes to see if the merit function drops.
3. **Add Degrees of Freedom**: If Hammer doesn't help, you might lack the variables needed to correct residual aberrations. Consider:
   - Allowing glasses to vary (set glass solve to 'Substitute' and use Hammer).
   - Splitting a thick lens into two elements.
   - Adding an aspheric surface if manufacturability allows.
4. **Check Aberration Balance**: Look at the Seidel Diagram or Ray Fan. If Petzval curvature is limiting performance, you must change the glass indices or separate positive/negative lenses further, as DLS cannot easily optimize out of poor power distribution.'''
    return make_ex(instr, think, ans)

def gen_cat3(i):
    instr = f'My ray trace shows vignetted rays at field {i%5+1} but the aperture looks fine. What is wrong?'
    think = '''1. Root Cause Analysis: Vignetting implies rays are physically blocked by a surface clear aperture, or total internal reflection (TIR) is occurring, or the aperture stop is not properly placed.
2. Zemax mechanics: OpticStudio uses semi-diameters in the LDE. If 'Clear Semi-Diameter' is forced, it might clip rays.
3. Ray aiming: If the system has high NA, large field angles, or strong pupil aberration, paraxial entrance pupil calculations fail. Ray Aiming must be turned on.
4. Vignetting factors: VDX, VDY, VCX, VCY might be set manually and incorrectly in the Field Data editor.
5. Conclusion: The most common causes are disabled Ray Aiming for wide-angle systems or artificial manual vignetting factors/hard apertures.'''
    ans = '''If you are seeing vignetted rays (often indicated by "Cannot trace ray" errors or missing rays in the 3D Layout) despite the aperture appearing correct, check the following common issues:

1. **Ray Aiming**: For systems with large field angles, high NA, or significant pupil aberration, the paraxial entrance pupil assumption fails. Go to System Explorer > Ray Aiming and turn on "Robust Ray Aiming". This forces Zemax to iteratively find the real stop surface, which often fixes apparent vignetting at high fields.
2. **Clear Semi-Diameters**: Check the LDE. If there is an 'U' (User-defined) next to the Semi-Diameter, it acts as a hard aperture. If rays expand beyond this during optimization, they clip. Remove the 'U' (press Ctrl+Z on the cell or calculate it automatically) unless you specifically need a mechanical aperture there.
3. **Vignetting Factors**: Open the Field Data Editor. If you have manual vignetting factors (VDX, VDY, VCX, VCY) applied, OpticStudio intentionally scales the pupil at that field. Clear these factors unless you specifically generated them to model physical clipping.
4. **Total Internal Reflection (TIR)**: A ray might not be physically clipped, but it undergoes TIR at a steeply curved surface, preventing it from tracing through. Check the Ray Fan or Single Ray Trace for "TIR" error messages at specific surfaces.'''
    return make_ex(instr, think, ans)

def gen_cat4(i):
    instr = f'Should I use N-BK7 or S-BSL7? Cost vs performance analysis for lens {i}.'
    think = '''1. Material properties: N-BK7 (Schott) and S-BSL7 (Ohara) are practically identical in optical properties (nd ~1.5168, Vd ~64.17).
2. Differences: Minor differences in exact dispersion coefficients, thermal properties (CTE), and transmission at UV/IR extremes.
3. Cost and Sourcing: S-BSL7 is often cheaper in Asia, while N-BK7 might be easier to source in Europe. Both are cheap, ubiquitous "preferred" glasses.
4. Zemax implication: In Zemax, replacing one with the other will cause a tiny change in aberrations (like a focal shift of a few microns).
5. Recommendation: Choose based on supplier availability and mechanical constraints rather than optical performance, but lock the design to one before final tolerancing.'''
    ans = '''From an optical performance perspective, Schott **N-BK7** and Ohara **S-BSL7** are functionally equivalent for the vast majority of applications.

**Performance Analysis:**
- **Index and Dispersion:** Both have a nominal refractive index ($n_d$) of 1.5168 and an Abbe number ($V_d$) of 64.17. The actual dispersion curves differ only slightly in the 5th decimal place.
- **Transmission:** Both offer excellent transmission in the visible and near-IR.
- **Thermal:** Minor differences exist in the Coefficient of Thermal Expansion (CTE) and $dn/dT$, which only matter in extreme athermalization scenarios.

**Cost and Manufacturing:**
- **Cost:** Both are among the cheapest optical glasses available (relative cost ~1.0).
- **Sourcing:** The choice usually depends on your manufacturer's location. Asian manufacturers heavily stock Ohara (S-BSL7) or CDGM (H-K9L), while European or American shops might prefer Schott (N-BK7).

**Zemax Recommendation:**
If you switch from N-BK7 to S-BSL7 in OpticStudio, you will notice a microscopic shift in your focal plane due to the slight index difference. Always re-optimize your back focal length (thickness of the last air gap) after swapping. For mass production, design with the glass your chosen vendor prefers to minimize lead times and cost.'''
    return make_ex(instr, think, ans)

def gen_cat5(i):
    instr = f'Design an LED collimation system for a {1+i*0.1:.1f}mm Lambertian source with ±3° output half-angle.'
    think = '''1. Conservation of Etendue: Source area A1 = pi * r1^2. Emission angle theta1 = 90 deg (Lambertian). Target angle theta2 = 3 deg. Target area A2 = A1 * (sin(90)/sin(3))^2.
2. Calculation: sin(3) ~ 0.052. Area increases by factor of (1/0.052)^2 = 366. Radius increases by ~19x.
3. Component selection: For a highly divergent LED source, a simple lens captures too little light (low efficiency). We need an RxI (Reflector-Refractor-TIR) lens or a compound parabolic concentrator (CPC).
4. Zemax NSC Setup: Add a Source Rectangle or Source Radial. Add a CPC object or Polygenic object for the TIR lens. Add a Detector Rectangle.
5. Optimization: Use Orthogonal Descent (NSC optimizer). Merit function targets spot radius or angular radius (NSDD operands).'''
    ans = f'''To design an LED collimator for a {1+i*0.1:.1f}mm Lambertian source with a tight ±3° output, follow this Non-Sequential Component (NSC) workflow:

**1. Etendue Calculation:**
Due to the conservation of etendue, collimating a Lambertian (±90°) source to ±3° requires significant area expansion. The optical aperture must be at least $r_{out} = r_{in} \\cdot \\frac{{\\sin(90^\\circ)}}{{\\sin(3^\\circ)}} \\approx 19 \\times$ the source radius. For a {1+i*0.1:.1f}mm source, your optic will be roughly {19*(1+i*0.1):.1f}mm in diameter minimum.

**2. Optic Selection:**
A standard singlet lens will only capture a fraction of the LED's light (low NA). To capture >90% of the light, use a **TIR (Total Internal Reflection) Lens** or a **CPC (Compound Parabolic Concentrator)**.

**3. Zemax Setup:**
- **Source**: Insert a `Source Rectangle` or `Source Radial`. Set the dimensions to {1+i*0.1:.1f}mm and the angular distribution to Lambertian.
- **Optic**: Insert a `CPC` object (if using a reflector) or a `TIR Lens`. Set the material to PMMA or Polycarbonate.
- **Detector**: Insert a `Detector Rectangle` placed far from the optic. Set "Angular Data" on to measure the intensity in degrees.

**4. Analysis and Optimization:**
- Trace roughly 100,000 rays to get a good baseline.
- Open the Merit Function. Use the **NSDD** operand to target the spatial spot size and angular spread on the detector.
- Optimize the length and exit aperture of the CPC, or the aspheric coefficients of the TIR lens, using the Orthogonal Descent optimizer to hit your 3° target.'''
    return make_ex(instr, think, ans)

for i in range(30):
    examples.append(gen_cat1(i))
for i in range(25):
    examples.append(gen_cat2(i))
for i in range(25):
    examples.append(gen_cat3(i))
for i in range(25):
    examples.append(gen_cat4(i))
for i in range(25):
    examples.append(gen_cat5(i))

import os
os.makedirs('c:/Users/dhair/OneDrive/Desktop/FINETUNING/dataset_parts', exist_ok=True)
with open('c:/Users/dhair/OneDrive/Desktop/FINETUNING/dataset_parts/07_reasoning_cot_part1.jsonl', 'w', encoding='utf-8') as f:
    for ex in examples:
        f.write(json.dumps(ex) + '\n')
print('Done writing 130 examples.')
