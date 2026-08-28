import json
import os

out_file = r"c:\Users\dhair\OneDrive\Desktop\FINETUNING\dataset_parts\01_sequential_fundamentals.jsonl"
os.makedirs(os.path.dirname(out_file), exist_ok=True)

dataset = []
def add(inst, resp):
    dataset.append({
        "instruction": inst,
        "system": "You are ZemaxGPT, an expert AI assistant for Zemax OpticStudio optical design. You provide precise, technically accurate guidance on sequential and non-sequential design, analysis, optimization, tolerancing, and ZOS-API programming.",
        "response": resp
    })

# 1. LDE (15)
# Solves (5)
solves_data = [
    ("Marginal Ray Height", "forces the paraxial marginal ray to a specific height, typically 0 to locate the paraxial focus.", "Click the solve box on the Thickness cell. Choose 'Marginal Ray Height', set Height = 0. This calculates the exact distance to the paraxial image plane."),
    ("Chief Ray Angle", "sets a specific chief ray angle, often used to enforce telecentricity in image space.", "On the Radius cell of the last optical surface, set a Chief Ray Angle solve with Angle = 0. This bends the surface to ensure the chief ray exits parallel to the optical axis."),
    ("F-number", "constrains the focal ratio of the system.", "On the Radius of the last active surface, choose 'F-number' solve and enter the target F/#. Zemax will adjust the curvature to yield the specified speed."),
    ("Pickup", "links a parameter to another surface's parameter, ensuring they remain identical or scaled.", "Open the solve dialog on the desired cell, choose 'Pickup', specify the source Surface number, and set the Scale Factor (e.g., -1 for an equiconvex lens)."),
    ("Variable", "marks a parameter as a degree of freedom for the local or global optimizer.", "Select the cell (e.g., Radius or Thickness), press Ctrl+Z or click the solve box and choose 'Variable'. A 'V' will appear next to the value.")
]
for name, desc, steps in solves_data:
    add(f"How do I use a {name} solve in the Zemax Lens Data Editor?", f"<think>\nUser is asking about the {name} solve in the LDE.\nNeed to explain its purpose: {desc}\nNeed to give practical steps: {steps}\n</think>\nA {name} solve in the Lens Data Editor is used when your design requires a specific constraint. Specifically, it {desc}\n\nTo apply this solve:\n1. Open the LDE.\n2. {steps}\n3. The cell will update automatically, displaying a letter indicating the active solve type.")

# Glass (4)
glass_data = [
    ("SCHOTT", "N-BK7", "a common borosilicate crown glass"),
    ("OHARA", "S-LAH66", "a high-index, low-dispersion lanthanum glass"),
    ("CDGM", "H-K9L", "the CDGM equivalent to N-BK7"),
    ("HIKARI", "J-BAF8", "a barium flint glass")
]
for cat, glass, desc in glass_data:
    add(f"How do I specify the {cat} glass {glass} in OpticStudio?", f"<think>\nUser wants to load {glass} from the {cat} catalog.\nStep 1: System Explorer -> Material Catalogs -> Ensure {cat} is selected.\nStep 2: LDE -> Type {glass} into the Glass column.\n</think>\nTo use the {cat} glass {glass} ({desc}) in your sequential design:\n\n1. Open the **System Explorer** and navigate to **Material Catalogs**.\n2. Ensure the `{cat}` catalog is included in the 'Catalogs To Use' list.\n3. In the Lens Data Editor (LDE), locate the surface where you want to apply this material.\n4. Type `{glass}` directly into the **Glass** column for that surface.\n\nZemax will immediately load the dispersion formula and index data for {glass} from the {cat} catalog.")

# Apertures (3)
apertures = [
    ("Circular", "used for standard round lenses and clear apertures"),
    ("Rectangular", "ideal for sensors, slits, or cylindrical lenses"),
    ("Spider", "used to model secondary mirror support struts in telescopes")
]
for ap, desc in apertures:
    add(f"How do I set a {ap} surface aperture in the LDE?", f"<think>\n{ap} apertures are {desc}.\nPath: Surface Properties -> Aperture -> Aperture Type.\n</think>\nTo set a {ap} aperture on a specific surface:\n\n1. Double-click the surface type column in the LDE or click the gear icon to open **Surface Properties**.\n2. Navigate to the **Aperture** tab.\n3. Change the 'Aperture Type' dropdown to **{ap} Aperture**.\n4. Enter the required dimensions (e.g., Min/Max Radius for Circular, X/Y Half Widths for Rectangular, or Arm Width/Number of Arms for Spider).\n\nThis aperture will hard-clip rays during ray tracing, which is essential for accurate vignetting and footprint analysis.")

# Coordinate Breaks (3)
cbs = [
    ("Tilt X and Y", "tilts the optical axis around the local X or Y axes"),
    ("Decenter X and Y", "translates the optical axis laterally in the X or Y direction"),
    ("Order of Execution", "determines whether Decenter or Tilt is applied first (Decenter then Tilt, or Tilt then Decenter)")
]
for cb, desc in cbs:
    add(f"How do I use a Coordinate Break to apply {cb} in sequential mode?", f"<think>\nCoordinate Breaks (CB) are fundamental for 3D geometry.\nFocusing on {cb} which {desc}.\nNeed to mention dummy surfaces or the CB surface type.\n</think>\nA Coordinate Break (CB) surface is used to define 3D orientation. Applying {cb} {desc}.\n\nTo apply this in the LDE:\n1. Insert a new surface and change its type to **Coordinate Break**.\n2. In the parameter columns, locate the specific fields for {cb}.\n3. Enter your values (e.g., degrees for tilts, lens units for decenters).\n\n*Pro tip:* OpticStudio evaluates operations in a specific order (Decenter X, Decenter Y, Tilt X, Tilt Y, Tilt Z). Use the 'Order' flag in the CB parameters if you need to reverse this sequence.")

# 2. System Setup (15)
# Wavelengths (5)
waves = [
    ("Visible (F, d, C)", "0.4861, 0.5876, 0.6563 um"),
    ("NIR", "0.7 to 1.0 um"),
    ("SWIR", "1.0 to 3.0 um"),
    ("MWIR", "3.0 to 5.0 um"),
    ("LWIR", "8.0 to 12.0 um")
]
for band, wlen in waves:
    add(f"How do I configure the wavelengths for a {band} system?", f"<think>\nSetting up wavelengths for {band} ({wlen}).\nPath: System Explorer -> Wavelengths -> Settings.\n</think>\nTo configure your system for the {band} spectral band ({wlen}):\n\n1. Open the **System Explorer** (or press F4) and expand the **Wavelengths** section.\n2. Double-click to open the Wavelength Data dialog.\n3. Enter your target wavelengths in micrometers (um). For {band}, you might enter values like {wlen}.\n4. Assign an appropriate 'Weight' to each wavelength (usually 1.0 for the primary wavelength and 1.0 for the edges of the band, depending on your source spectrum).\n5. Select a primary wavelength (usually the center wavelength) which is used for paraxial calculations.")

# Fields (4)
fields = [
    ("Angle", "infinite conjugate systems like telescopes or camera lenses"),
    ("Object Height", "finite conjugate systems like microscopes or relays"),
    ("Real Image Height", "systems where the sensor size dictates the field of view"),
    ("Paraxial Image Height", "systems with high distortion where real image height is non-linear")
]
for ft, desc in fields:
    add(f"When and how should I use the {ft} field type?", f"<think>\n{ft} field type is used for {desc}.\nPath: System Explorer -> Fields -> Type.\n</think>\nThe **{ft}** field type is typically used for {desc}.\n\nTo set this up:\n1. Go to **System Explorer** -> **Fields** and open the Field Data dialog.\n2. In the 'Type' dropdown, select **{ft}**.\n3. Enter your field points in the X and Y columns. These values will now be interpreted in the corresponding units (e.g., degrees for Angle, lens units for Heights).\n4. Ensure your normalization method (Radial or Rectangular) matches your field point distribution.")

# Aperture Types (3)
ap_types = [
    ("Entrance Pupil Diameter (EPD)", "defines the size of the paraxial entrance pupil"),
    ("Image Space F/#", "defines the speed of the cone of light reaching the image"),
    ("Object Space NA", "defines the numerical aperture of rays leaving the object")
]
for apt, desc in ap_types:
    add(f"How do I define the system aperture using {apt}?", f"<think>\n{apt} {desc}.\nSystem Explorer -> Aperture.\n</think>\nDefining the system aperture via **{apt}** {desc}.\n\nSteps to configure:\n1. Open the **System Explorer** and expand the **Aperture** drop-down.\n2. Change the 'Aperture Type' to **{apt}**.\n3. Enter the target 'Aperture Value'.\n\nZemax will now scale all incoming ray bundles to satisfy this constraint. This is the primary parameter that determines how much light passes through the optical system.")

# Explorer/Units (3)
exp = [
    ("System Units", "setting the fundamental length unit (mm, cm, in, m)", "System Explorer -> Units. Set Lens Units to your preference. Millimeters are standard for most optics."),
    ("Ray Aiming", "correcting pupil aberration in wide-angle or off-axis systems", "System Explorer -> Ray Aiming. Turn on 'Real' ray aiming if the pupil shifts significantly with field angle."),
    ("Reference OPD", "defining the reference sphere for wavefront calculations", "System Explorer -> Advanced. Choose Absolute, Infinity, or Exit Pupil. Exit Pupil is the standard choice.")
]
for ex_name, desc, path in exp:
    add(f"How do I configure {ex_name} in OpticStudio?", f"<think>\n{ex_name} involves {desc}.\nPath: {path}.\n</think>\nConfiguring **{ex_name}** is crucial for {desc}.\n\nTo configure this:\n1. Open the **System Explorer**.\n2. {path}\n\nEnsuring this setting is correct early in the design process prevents significant analysis errors later, particularly when evaluating wavefront error or pupil clipping.")

# 3. Common Systems (20)
sys_list = [
    ("Singlet Lens", "a basic single element focusing light"),
    ("Achromatic Doublet", "a cemented two-lens system minimizing chromatic aberration"),
    ("Cooke Triplet", "a three-element lens capable of correcting all seven primary aberrations"),
    ("Double Gauss", "a nearly symmetrical multi-element lens used in photography"),
    ("Petzval Lens", "a design with two widely separated positive groups for fast F/# and flat fields"),
    ("Telephoto Lens", "a positive front group and negative rear group to shorten the physical length"),
    ("Retrofocus Lens", "a negative front group and positive rear group to increase back focal length"),
    ("Microscope Objective", "a high-NA, finite conjugate system with extreme magnification"),
    ("Cassegrain Telescope", "a dual-mirror system with a concave parabolic primary and convex hyperbolic secondary"),
    ("Ritchey-Chretien Telescope", "a variation of the Cassegrain using two hyperbolic mirrors to eliminate coma"),
    ("Schmidt Camera", "uses a spherical primary mirror and an aspheric corrector plate at the center of curvature"),
    ("Keplerian Telescope", "an afocal system with two positive lenses yielding an inverted image"),
    ("Galilean Telescope", "an afocal system with a positive objective and negative eyepiece yielding an upright image"),
    ("Relay Lens System", "a symmetrical 4f system used to transfer an image plane over a distance"),
    ("Collimator", "a lens system designed to take a point source and output a planar wavefront"),
    ("Beam Expander", "an afocal system designed to increase the diameter of a laser beam"),
    ("F-Theta Lens", "a scanning lens where image height is directly proportional to scan angle (h = f*theta)"),
    ("Endoscope Objective", "a miniature wide-angle lens system with a very short physical length"),
    ("Eyepiece", "a magnifier designed to match the exit pupil with the human eye's entrance pupil"),
    ("Laser Focusing Lens", "a high-performance, single-wavelength objective, often an asphere, for diffraction-limited focusing")
]
for s_name, s_desc in sys_list:
    add(f"How do I set up a {s_name} in Zemax sequential mode?", f"<think>\n{s_name} is {s_desc}.\nNeed to outline LDE structure and specific settings.\n</think>\nA **{s_name}** is {s_desc}.\n\nTo set this up in sequential mode:\n1. **System Setup**: Define your wavelengths and fields appropriate for the application.\n2. **Aperture**: Set the System Aperture (e.g., EPD or Object Space NA) based on the specification.\n3. **LDE Structure**: Build the required surfaces. For a {s_name}, this typically involves adding the specific sequence of optical elements and materials (e.g., assigning standard surface types and glasses from the catalog).\n4. **Optimization**: Set your variables (radii, thicknesses) and build a Merit Function using Default Merit Function (e.g., RMS Spot Radius or Wavefront error) to optimize the form.")

# 4. Surface Properties (15)
surf_props = [
    ("Standard Surface", "a basic spherical or conical surface"),
    ("Even Asphere", "a surface with polynomial deformation terms (r^2, r^4, r^6...) on top of a conic"),
    ("Prolate Ellipsoid Conic", "a conic constant between -1 and 0"),
    ("Paraboloid Conic", "a conic constant of exactly -1"),
    ("Hyperboloid Conic", "a conic constant less than -1"),
    ("Toroidal Surface", "a surface with different radii of curvature in the X and Y axes"),
    ("Biconic Surface", "similar to toroidal but allows independent conic constants in X and Y"),
    ("Diffraction Grating", "a surface that bends light based on line density and diffraction order"),
    ("Optically Fabricated Hologram", "a surface modeled by the interference of two construction beams"),
    ("Radial GRIN", "a material with a varying index of refraction radially from the optical axis"),
    ("Axial GRIN", "a material with a varying index of refraction along the optical axis"),
    ("Zernike Standard Sag", "a surface defined by Zernike polynomials representing wavefront aberrations directly on the sag"),
    ("Zernike Fringe Sag", "similar to Standard but uses the Fringe ordering format, common in interferometry"),
    ("Extended Polynomial", "an advanced asphere supporting up to 230 polynomial terms"),
    ("Q-Type Asphere", "an aspheric surface using Forbes polynomials (Qcon or Qbfs) for better manufacturing optimization")
]
for sp_name, sp_desc in surf_props:
    add(f"Explain the {sp_name} type and when to use it in Zemax.", f"<think>\n{sp_name} is {sp_desc}.\nNeed to explain LDE parameters and use cases.\n</think>\nThe **{sp_name}** is {sp_desc}.\n\n**When to use it:**\nYou should use this surface type when standard spherical surfaces cannot meet the optical performance requirements, or when modeling a specific physical component like a {sp_name.split()[0].lower()} element.\n\n**How to use it:**\n1. In the LDE, click the Surface Type column and select **{sp_name}**.\n2. Expand the parameter columns to reveal the specific data fields for this surface (e.g., coefficients, conic constants, or line densities).\n3. Enter the required values. If optimizing, you can set these specific parameters as variables (Ctrl+Z) to allow the Zemax optimizer to find the ideal shape.")

# 5. Multi-Config (15)
mce_configs = [
    ("2-position Zoom lens", "models two distinct focal lengths (Wide and Tele)"),
    ("3-position Zoom lens", "models Wide, Mid, and Tele focal lengths"),
    ("Continuous Zoom", "uses multiple configurations to approximate a fluid focal length sweep"),
    ("Switchable Filter", "models the insertion and removal of a glass filter in the optical path"),
    ("Beamsplitter Path", "traces the transmitted and reflected arms of a beamsplitter simultaneously"),
    ("THIC Operand", "changes the thickness of a surface across configurations"),
    ("GLSS Operand", "changes the glass material of a surface across configurations"),
    ("WAVE Operand", "changes the primary wavelength across configurations"),
    ("TEMP Operand", "defines different environmental temperatures for thermal analysis"),
    ("CRVT Operand", "changes the curvature (1/Radius) of a surface across configurations"),
    ("Athermalization (Thermal Pickup)", "uses multi-config to optimize performance across high, nominal, and low temperatures"),
    ("Afocal Zoom system", "a zoom system outputting collimated light at various magnifications"),
    ("Tolerance Monte Carlo", "using configurations to model different perturbed tolerance states"),
    ("Scan Mirror Angle", "modeling different galvanometer mirror positions using coordinate break parameters"),
    ("Focusing Mechanism", "modeling an objective focusing on objects at infinity, 1 meter, and macro distances")
]
for mc_name, mc_desc in mce_configs:
    add(f"How do I set up a Multi-Configuration Editor (MCE) for a {mc_name}?", f"<think>\nMCE setup for {mc_name}, which {mc_desc}.\nNeed to explain how to add configs and operands.\n</think>\nSetting up the Multi-Configuration Editor (MCE) for a **{mc_name}** allows you to analyze and optimize a system that {mc_desc}.\n\n**Setup Steps:**\n1. Press **F7** to open the Multi-Configuration Editor.\n2. Click the 'Insert Configuration' button in the MCE toolbar to add the required number of states.\n3. Insert Operands (rows) in the MCE. For a {mc_name}, choose the relevant operand (e.g., THIC for distances, PRAM for coordinate breaks, or TEMP for temperatures).\n4. Specify the Surface number in the operand properties.\n5. Enter the distinct values for each configuration column.\n6. Use **Ctrl+A** or the 'Make Active' button to switch the LDE view between your configurations during analysis.")

# 6. Coatings/Pol (10)
coat_pol = [
    ("Ideal Coating (I.99)", "a simple theoretical coating transmitting 99% and reflecting 1%"),
    ("Coating File (.DAT)", "a detailed thin-film layer specification defining indices and thicknesses"),
    ("Single-layer AR", "a basic quarter-wave magnesium fluoride (MgF2) anti-reflection coating"),
    ("Multi-layer BBAR", "a broad-band anti-reflection coating using alternating high/low index layers"),
    ("Polarization Ray Trace", "enabling the calculation of S and P polarization states during ray tracing"),
    ("Jones Matrix Analysis", "evaluating the complex amplitude and phase transformations of polarized light"),
    ("Surface Scattering", "modeling micro-roughness using Lambertian or ABg scatter models"),
    ("Birefringent Material", "modeling materials like Calcite with ordinary and extraordinary indices"),
    ("Phase Coating", "a coating designed to impart a specific phase shift without altering amplitude"),
    ("Dichroic Filter", "a coating transmitting one wavelength band and reflecting another")
]
for cp_name, cp_desc in coat_pol:
    add(f"How do I configure {cp_name} in OpticStudio sequential mode?", f"<think>\n{cp_name} relates to polarization/coatings.\nIt is {cp_desc}.\nPath: Surface Properties -> Coating/Scattering, or Analysis -> Polarization.\n</think>\nConfiguring **{cp_name}** ({cp_desc}) is essential for accurate transmission and polarization analysis.\n\n**Implementation:**\n1. For surface-specific properties like coatings, open the LDE and access **Surface Properties** -> **Coating**.\n2. Select or type the coating name from your loaded `COATING.DAT` file. (To edit coatings, go to Libraries -> Coating Tools).\n3. If evaluating polarization, open the specific analysis window (e.g., **Analysis -> Polarization -> Jones Matrix** or check 'Use Polarization' in the standard Spot Diagram settings).\n4. Define your input polarization state (Jx, Jy, X-Phase, Y-Phase) in the settings dialog of the analysis feature to properly trace the vector fields through your {cp_name} system.")

with open(out_file, 'w', encoding='utf-8') as f:
    for ex in dataset:
        json.dump(ex, f)
        f.write('\n')
