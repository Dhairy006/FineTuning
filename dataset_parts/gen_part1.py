import json

system_prompt = "You are ZemaxGPT, an expert AI assistant for Zemax OpticStudio optical design. You provide precise, technically accurate guidance on sequential and non-sequential design, analysis, optimization, tolerancing, and ZOS-API programming."

data = [
    # NSC Object Types & Setup (20 examples)
    {
        "instruction": "How do I model a Source Ellipse in Non-Sequential Mode, and what parameters control the emission?",
        "response": "<think>Need to explain Source Ellipse setup, defining its spatial extent, angular emission, and power.</think>To model a Source Ellipse in Non-Sequential Mode (NSC), add a 'Source Ellipse' object to the Non-Sequential Component Editor (NSCE). The key parameters controlling emission are:\n- **X Half-Width / Y Half-Width**: Defines the spatial extent of the emitting elliptical area.\n- **Source Distance**: The distance from the source to the apparent point of divergence.\n- **Cosine Exponent**: Controls the angular emission profile (e.g., 1 for Lambertian).\n- **Layout Rays / Analysis Rays**: Number of rays for drawing and ray tracing.\n- **Power**: Total optical power in Watts or Lumens. Adjust these to shape the beam spatial and angular distribution."
    },
    {
        "instruction": "Explain the difference between a Detector Rectangle and a Detector Color in Zemax.",
        "response": "In Zemax OpticStudio, a **Detector Rectangle** records spatial and angular data for rays striking its surface, typically outputting incoherent irradiance, radiant intensity, or coherent phase/amplitude. It assumes monochromatic or broadband energy but does not display true color.\n\nA **Detector Color**, on the other hand, explicitly calculates and displays the photometric color (RGB and CIE chromaticity coordinates) of the incident light based on the wavelength and spectral power of the rays. It is essential for illumination systems like LEDs or automotive displays where color mixing and color uniformity are design requirements."
    },
    {
        "instruction": "What is a Source DLL object and when should I use it instead of built-in sources?",
        "response": "A **Source DLL** object uses an external Dynamic Link Library (DLL) to define the ray positions, angles, and wavelengths. You should use a Source DLL when the built-in source models (like Source Ellipse or Source Diode) cannot accurately represent your physical source. For example, complex LED emission profiles, fluorescent volumetric scattering, or vendor-provided rayfiles (like ProSource or Radiant Vision Systems models) are often loaded via a Source DLL. You assign the appropriate DLL (e.g., `rayfile.dll`) in the object's properties."
    },
    {
        "instruction": "How do I set up a blackbody spectrum for a Source Rectangle?",
        "response": "<think>Steps: Object Properties -> Sources tab -> Spectrum -> Blackbody -> Set Temperature.</think>To set up a blackbody spectrum for a Source Rectangle:\n1. Open the Object Properties for the Source Rectangle.\n2. Navigate to the **Sources** tab.\n3. In the Spectrum drop-down menu, select **Blackbody**.\n4. Enter the desired color temperature in Kelvin (e.g., 3000 for warm white, 5800 for solar equivalent).\n5. Specify the minimum and maximum wavelengths to limit the spectral band, and set the number of wavelengths to sample. OpticStudio will automatically weight the rays according to Planck's law during the ray trace."
    },
    {
        "instruction": "Describe the Nesting Rule for overlapping objects in Zemax Non-Sequential mode.",
        "response": "In Non-Sequential Mode, the **Nesting Rule** resolves conflicts when rays pass through overlapping volumes. The rule states: **If two objects overlap, the properties of the object listed further down (higher object number) in the Non-Sequential Component Editor (NSCE) override the properties of the earlier object.**\n\nFor example, if Object 2 is a glass sphere and Object 3 is a smaller air sphere located entirely inside Object 2, rays entering the inner sphere will correctly see the index of Air, because Object 3's material overrides Object 2 in the overlapping region."
    },
    {
        "instruction": "How does Boolean Native (AND, OR, XOR) work in the NSCE?",
        "response": "The **Boolean Native** object allows you to combine two existing objects using boolean logic to create complex geometries. It supports:\n- **AND (Intersect)**: The resulting volume is where both parent objects overlap.\n- **OR (Union)**: The resulting volume is the combination of both parent objects.\n- **XOR (Difference)**: Subtracts the volume of the second object from the first.\n\nTo use it, add a Boolean Native object, specify the reference numbers of the two parent objects in its parameter columns, and set the parent objects' 'Do Not Draw' and 'Do Not Trace' flags to true, so only the resultant Boolean object interacts with rays."
    },
    {
        "instruction": "What is the proper way to assign material to a Rectangular Volume in NSC?",
        "response": "To assign a material to a Rectangular Volume in NSC, locate the object in the Non-Sequential Component Editor (NSCE). In the **Material** column for that object, type the name of the glass (e.g., `N-BK7`) or the material definition. \nEnsure that the material catalog containing your chosen material is loaded (System Explorer > Materials > Catalogs). If you want a perfect reflector, you can type `MIRROR`. To model absorption, ensure the material catalog has transmission data, or apply a Bulk Absorption coefficient in the object properties."
    },
    {
        "instruction": "How do I model an annular volume, such as a pipe, in NSC?",
        "response": "<think>Can use Annular Volume object or cylinder volume with nesting.</think>You can model an annular volume in two primary ways:\n1. **Annular Volume Object**: Add an 'Annular Volume' object to the NSCE. Set the Front/Rear Radius, thickness, and define the inner and outer radial extents. This natively supports a hollow center.\n2. **Nesting**: Create a solid 'Cylinder Volume' for the outer pipe (Material: Glass). Place another smaller 'Cylinder Volume' inside it (Material: Air) with a higher object number. Due to nesting rules, the inner air cylinder overwrites the glass, creating a pipe."
    },
    {
        "instruction": "What are the parameters for a Source Ray, and when is it useful?",
        "response": "A **Source Ray** emits a single ray from a defined position along a specific vector. Its parameters include the origin (X, Y, Z), direction cosines (L, M, N), wavelength, and power. \n\nIt is extremely useful for debugging complex optical paths, verifying total internal reflection (TIR) conditions at specific incident angles, or testing exact ray hit locations on detectors without the noise of millions of rays from a larger source."
    },
    {
        "instruction": "How do I define a Source File using a .DAT or .SDF format?",
        "response": "To use a pre-calculated ray set, add a **Source File** object. In its parameters, specify the filename of the ray data file (e.g., an `.SDF` or `.DAT` file). These files must be located in the `<Zemax Data folder>\\Objects\\Sources` directory. \nIn the object properties, you can also define the total power to override the file's default power, and apply wavelength filters or angular scaling if needed. This is standard for importing measured LED ray data from vendors."
    },
    {
        "instruction": "Explain the use of the Detector Polar object.",
        "response": "The **Detector Polar** object captures the angular distribution of rays originating from a specific point. It projects the intensity data onto a far-field spherical surface, typically outputting radiant intensity (Watts/steradian). \nIt is widely used in illumination design to evaluate the far-field emission pattern (beam angle, FWHM) of LEDs, luminaires, and automotive headlamps. The parameters define the radial and angular resolution (bins) and the maximum angle to capture."
    },
    {
        "instruction": "How do I create a Standard Lens object in NSC?",
        "response": "Add a **Standard Lens** object in the NSCE. You must define the Radius 1 (front surface), Radius 2 (back surface), Thickness (center thickness), and the Clear 1 / Clear 2 semi-diameters. \nAssign a glass in the Material column. If you need aspheric profiles, you can use the 'Even Asphere Lens' object instead. The Standard Lens simplifies importing basic sequential components into NSC, avoiding the need for front, back, and edge surface assembly."
    },
    {
        "instruction": "What is a Detector Volume and what is its primary application?",
        "response": "<think>Volume detector captures absorbed flux inside a bulk material, useful for laser crystals, tissue, fluorescence.</think>A **Detector Volume** is a 3D rectangular grid of voxels that records the incident or absorbed flux within a given volume. Its primary application is analyzing bulk absorption, fluorescence, or scattering inside a material. \nFor instance, it is used to calculate the pump absorption profile in solid-state laser rods, or to model light penetration and absorption in biological tissues. You define the X, Y, Z widths and the number of pixels (voxels) in each dimension."
    },
    {
        "instruction": "How do I model a simple Source Diode (laser diode emission)?",
        "response": "Use the **Source Diode** object. It allows you to model the asymmetric astigmatic emission typical of edge-emitting laser diodes. \nKey parameters include:\n- **X/Y Divergence**: The FWHM emission angles for the fast and slow axes.\n- **Astigmatism**: The longitudinal distance between the apparent X and Y source points.\nYou can also specify the far-field distribution shape (Gaussian vs. Super-Gaussian) to accurately match the diode's beam profile."
    },
    {
        "instruction": "What happens if I forget to place a detector in my NSC system?",
        "response": "If you run an NSC Ray Trace without a detector object, the ray trace will complete, but no quantitative irradiance, intensity, or phase data will be recorded or available for analysis. However, you can still view the ray paths visually in the 3D Layout window if 'Save Rays' is enabled, but you will lack the mathematical performance metrics (like spot size or uniformity) required for optimization."
    },
    {
        "instruction": "Explain how to set up a wavelength-weighted source spectrum in NSC.",
        "response": "To create a custom wavelength-weighted spectrum:\n1. Open the System Explorer > Wavelengths and define the specific wavelengths required.\n2. Open the Object Properties of your source > **Sources** tab.\n3. Under Spectrum, choose **Wavelengths**.\n4. You must define a custom spectrum file (`.SPCD`) that specifies the relative weight of each wavelength, or assign weights directly in the System Explorer if using the system wavelengths option. This precisely controls the spectral power distribution."
    },
    {
        "instruction": "How do I apply an anti-reflection (AR) coating to a rectangular volume in NSC?",
        "response": "In the NSCE, expand the properties for the Rectangular Volume. Navigate to the **Coat/Scatter** tab. Here, you will see a list of the object's faces (e.g., Front, Back, Side). \nSelect the desired face, check the box to apply a coating, and select your AR coating (e.g., `AR`) from the drop-down list. Ensure the coating definition exists in your currently loaded coating file (e.g., `COATING.DAT`)."
    },
    {
        "instruction": "What is the difference between a Cylinder Volume and a Cylinder Pipe object?",
        "response": "A **Cylinder Volume** represents a solid cylindrical block of material (like a rod lens or a solid light pipe). A **Cylinder Pipe** represents a hollow tube where only the outer wall has material thickness. Rays passing through a Cylinder Volume interact with the bulk material, while rays in a Cylinder Pipe travel through the hollow center (typically air) and only interact with the inner and outer walls of the pipe."
    },
    {
        "instruction": "Can I define a custom 3D shape directly in the NSCE without importing CAD?",
        "response": "Yes, for mathematically definable shapes, you can use the **User Defined Object** (UDO) compiled via a DLL, or combine multiple standard shapes using **Boolean Native** operations. For complex faceted shapes, you can use the **Polygon Object** by writing a `.POB` file that explicitly lists the vertices and faces of the 3D structure without needing external CAD software."
    },
    {
        "instruction": "How do I verify that an NSC object is correctly placed and oriented?",
        "response": "The best way to verify placement is to open a **NSC 3D Layout** or **Shaded Model** window. Visually inspect the system from different angles. Additionally, you can check the object's Global XYZ coordinates and rotation angles (Tilt X, Y, Z) in the NSCE. Using the 'Measure' tool in the Shaded Model or tracing a single Source Ray can also confirm physical intersections and alignments."
    },
    
    # NSC Ray Tracing & Analysis (15 examples)
    {
        "instruction": "How do I execute a ray trace in Non-Sequential mode?",
        "response": "<think>Explain Analyze > Ray Trace dialog, hitting Clear & Trace.</think>To execute a ray trace, navigate to the **Analyze** tab and click **Ray Trace** (or use the shortcut Ctrl+Shift+R). In the Ray Trace Control dialog:\n1. Check **Clear Detectors** to erase previous data.\n2. Check **Use Polarization** if computing Fresnel reflections or thin films.\n3. Check **Ignore Errors** if you want to skip ray geometry errors.\n4. Click **Clear & Trace** to run. The summary will show the number of traced rays and the total flux striking the detectors."
    },
    {
        "instruction": "What is the Detector Viewer and how is it used?",
        "response": "The **Detector Viewer** is the primary analysis window for NSC detectors. Once a ray trace is complete, open the Detector Viewer (Analyze > Detector Viewer). \nIt displays the recorded data (e.g., Irradiance, Radiant Intensity) as a 2D color map, contour plot, or 1D cross-section. You can use its settings to change the displayed data type, apply smoothing, view color data, or check the total flux (Watts) and peak irradiance."
    },
    {
        "instruction": "Explain the difference between coherent and incoherent ray tracing in NSC.",
        "response": "In **Incoherent** ray tracing, Zemax tracks optical power (flux) geometrically. When rays hit a detector, their powers simply add up. This is standard for LED and illumination design.\n\nIn **Coherent** ray tracing, Zemax tracks the complex amplitude and phase of the rays. When rays hit a detector, they interfere, and the irradiance is calculated from the squared magnitude of the complex sum. Coherent tracing is required for analyzing interferometers or diffraction effects in NSC."
    },
    {
        "instruction": "How do I enable Ray Splitting, and why is it important?",
        "response": "Enable **Ray Splitting** in the Ray Trace Control dialog. When a ray hits an interface where partial reflection and transmission occur (like an uncoated glass surface), ray splitting spawns two separate rays: one reflected and one transmitted, allocating power based on Fresnel coefficients. \nThis is essential for stray light analysis, ghost reflection tracking, and accurately modeling light guides where partial reflections are critical."
    },
    {
        "instruction": "What is a Filter String and give an example of how to use it?",
        "response": "<think>Filter strings allow isolating rays based on their history (hits, objects, scattering).</think>A **Filter String** isolates specific rays in the layout or detector viewer based on their physical path history. \nFor example, the filter `H2 & !H3` displays only rays that hit Object 2 AND did NOT hit Object 3. \nThe filter `G4` shows only rays that generated a ghost reflection at Object 4. \nYou apply this in the 'Filter' field of the Detector Viewer or NSC 3D Layout settings to analyze specific stray light or signal paths."
    },
    {
        "instruction": "How does OpticStudio handle Total Internal Reflection (TIR) in NSC?",
        "response": "TIR is handled automatically in NSC based on Snell's Law and the refractive indices of the materials. When a ray hits an interface at an angle greater than the critical angle, 100% of the ray's energy is reflected back into the denser medium. \nYou do not need to enable polarization or ray splitting for TIR to occur, though enabling polarization will accurately calculate the phase shift incurred during the TIR event."
    },
    {
        "instruction": "How do I model bulk scattering inside a material like a diffuser?",
        "response": "To model bulk scattering:\n1. Open the Object Properties of the volume (e.g., Rectangular Volume).\n2. Go to the **Volume Physics** tab.\n3. Under 'Bulk Scattering', select a model like **Angle Scattering** or **Henyey-Greenstein**.\n4. Define the Mean Free Path (distance between scattering events), Transmission, and the scattering angle parameters.\nWhen traced, rays will randomly scatter inside the volume based on this probabilistic model."
    },
    {
        "instruction": "How can I export the irradiance data from a Detector Rectangle?",
        "response": "To export detector data, open the **Detector Viewer** for the specific detector. Click the **Text** tab at the bottom to view the raw numeric grid. You can click 'Save' to export it as a text file (`.TXT`).\nAlternatively, in the main Ray Trace dialog, you can check 'Save Ray Data' to output a `.ZRD` (Zemax Ray Data) file containing full ray history, which can be parsed via ZOS-API or the Ray Database Viewer."
    },
    {
        "instruction": "What is the purpose of the 'Minimum Relative Ray Intensity' setting?",
        "response": "During ray splitting or bulk absorption, ray power decreases. Tracing very low-power rays infinitely consumes computational time without affecting the final result. \nThe **Minimum Relative Ray Intensity** (found in System Explorer > Non-Sequential) sets a threshold (e.g., $10^{-4}$). If a ray's relative power drops below this threshold compared to the source, OpticStudio terminates that ray, optimizing simulation speed."
    },
    {
        "instruction": "How do I trace rays backward from a detector in NSC?",
        "response": "OpticStudio NSC primarily traces rays forward from sources. However, you can effectively run a 'reverse trace' by placing a Source at the detector's location with the emission angles matching the detector's field of view, and placing a Detector where the original source was. This is often used to map the 'acceptance cone' or field of view of a sensor system."
    },
    {
        "instruction": "Explain the use of 'Ignore Errors' in the Ray Trace dialog.",
        "response": "When CAD objects have small geometric gaps or when precision errors cause rays to get 'stuck' exactly on boundaries, OpticStudio throws a Geometry Error and stops the trace. \nChecking **Ignore Errors** forces the engine to terminate the specific problematic ray and continue tracing the remaining rays. This is highly recommended for complex imported CAD geometries where minor meshing anomalies exist."
    },
    {
        "instruction": "How do I visualize the exact point where rays are lost in my system?",
        "response": "<think>Use Save Rays, Ray Database Viewer, or Filter strings for Missed rays.</think>To visualize lost rays:\n1. Run a ray trace with **Save Rays** enabled to generate a `.ZRD` file.\n2. Open the **NSC 3D Layout** and apply the filter string `_L` (Lost rays) or `_E` (Error rays).\n3. Only the terminated rays will display, showing exactly where they missed a surface, hit a totally absorbing object, or encountered a geometry error."
    },
    {
        "instruction": "Can I trace rays using multiple CPU threads in NSC?",
        "response": "Yes, Non-Sequential ray tracing is highly parallelized. By default, OpticStudio will use all available CPU threads. You can manage this in the **Project Preferences > General** tab by setting the 'Number of Cores' to use. Multi-threading drastically reduces trace times for simulations requiring millions of rays."
    },
    {
        "instruction": "What is the Ray Database Viewer?",
        "response": "The **Ray Database Viewer** (Analyze > Ray Database Viewer) reads the `.ZRD` file generated by saving rays during a trace. It provides a detailed, segment-by-segment tabular history of every ray, including XYZ coordinates, direction cosines, intensity, optical path length, and the object hit at each segment. It is invaluable for deep debugging of complex stray light paths."
    },
    {
        "instruction": "How do I calculate Optical Path Difference (OPD) in Non-Sequential mode?",
        "response": "To calculate OPD in NSC, you must enable **Coherent** ray tracing. Set your Source to emit a single wavelength and ensure a phase reference is defined. \nOn the Detector Rectangle, set the 'Data' type to **Phase**. The Detector Viewer will then plot the phase wavefront. Note that calculating true classical OPD maps is often much easier in Sequential mode; NSC requires careful coherent setup."
    }
]

with open('c:/Users/dhair/OneDrive/Desktop/FINETUNING/dataset_parts/02_nonsequential_mode.jsonl', 'w') as f:
    for item in data:
        item["system"] = system_prompt
        f.write(json.dumps(item) + '\\n')
