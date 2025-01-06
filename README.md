# CSY Tools Add-On for Blender

CSY Tools is a Blender add-on designed to streamline workflows for creating bounds, managing mesh data, and preparing objects for Midtown Madness 2 export. It provides a set of utilities accessible via the N-Panel in the 3D View under the "CSY Tools" tab.

![image](https://github.com/user-attachments/assets/246ef124-3d69-4253-a265-444593016b9d)

---

## Features

### **Bound Tools**
- **Create BOUND**: Creates a bounding box for the selected object with optional loop cuts for customization.

### **Export Tools**
- **Apply Origin and Transformations**: Sets the origin to the 3D cursor and applies all transformations (location, rotation, scale).
- **Apply Rotation & Scale + Origin**: Applies rotation and scale to the object and sets the origin to the center of mass (surface).
- **Sanity Check Collection**: Verifies that the required objects (`BODY_H`, `WHL0_H`, etc.) exist within the `Collection`. Ignores all other collections.

### **Material Tools**
- **Set Specular to 0.500**: Adjusts the Specular value of all materials in the selected objects to `0.500`.

### **Mesh Tools**
- **Rename UVs and VTX Colors**: Renames all UV maps to `"UV"` and vertex color layers to `"VTX"` for the selected objects.

---

## Installation

1. Download the add-on script file (`csy_tools.py`).
2. Open Blender and go to `Edit > Preferences > Add-ons`.
3. Click `Install...`, navigate to the script file, and select it.
4. Enable the add-on by checking the box next to **CSY Tools (N-Panel)**.
5. The tools will appear in the **N-Panel** of the 3D View under the "CSY Tools" tab.

---

## Usage

### Accessing the Tools
- Open the **N-Panel** in the 3D View (`N` key).
- Navigate to the **CSY Tools** tab.

### Using the Features
1. **Create BOUND**:
   - Select an object in the scene.
   - Click `Create BOUND` in the **Bound Tools** section.
   - Adjust the number of loop cuts in the operator panel (optional).

2. **Apply Origin and Transformations**:
   - Select an object in the scene.
   - Click `Apply Origin and Transformations` in the **Export Tools** section.

3. **Apply Rotation & Scale + Origin**:
   - Select an object in the scene.
   - Click `Apply Rotation & Scale + Origin` in the **Export Tools** section.

4. **Sanity Check Collection**:
   - Click `Sanity Check Collection` in the **Export Tools** section.
   - The add-on will verify that the required objects exist within the `Collection`.

5. **Set Specular to 0.500**:
   - Select one or more objects in the scene.
   - Click `Set Specular to 0.500` in the **Material Tools** section.

6. **Rename UVs and VTX Colors**:
   - Select one or more objects in the scene.
   - Click `Rename UVs and VTX Colors` in the **Mesh Tools** section.

---

## Requirements

- Blender 2.83 or later.

---

## FAQ

### **Q: What happens if the required objects are missing from the `Collection`?**
- The **Sanity Check Collection** tool will display a warning and list the missing objects.

### **Q: Can I adjust the Specular value to something other than `0.500`?**
- This feature is currently hardcoded to set the Specular value to `0.500`. If you need a custom value, you can modify the script or request an enhancement.

### **Q: What if the `Collection` does not exist in my scene?**
- The **Sanity Check Collection** tool will notify you that the `Collection` is missing.

---

## License

This add-on is provided under the MIT License. See the `LICENSE` file for more details.

---

## Credits

- **Author**: chasseyblue.com
- **Version**: 1.8.0
- **Support**: COMMUNITY

---

## Greets
- All members of Midtown Club Discord, f(x)^3 / Dummiesman, MDX, and Drogosław.
