# Photo Map Generator

Interactive map for displaying photos with GPS coordinates using OpenLayers.

## Description

This project creates an interactive web map where each photo with GPS data is displayed as a marker with an image thumbnail. Clicking on a marker opens a popup with the full-size image.

## Features

- 📍 Automatic GPS coordinate extraction from photo EXIF data
- 🖼️ Photo thumbnails as map markers
- 🔍 Full-size images in popups on click
- 🗑️ Optional photo deletion feature (edit mode)
- ⚡ Optimized loading with automatic thumbnail generation
- 🗺️ Automatic map centering on all photos

## Installation

1. Make sure you have Python 3.6+ installed
2. Install required dependencies:
```bash
pip install pillow
```

3. Create an `image_source` folder and place your JPEG photos with GPS data:
```
photomap/
├── image_source/
│   ├── photo1.jpeg
│   ├── photo2.jpeg
│   └── ...
├── photomap_openlayers.py
├── photo_server.py
└── README.md
```

## Usage

### View Mode (Default)

Creates a map for viewing photos only, without deletion capability:

```bash
python photomap_openlayers.py
```

**Result:**
- Creates `photo_map_openlayers.html` file
- Map ready for publishing or local viewing
- Opens directly in browser

### Edit Mode

Creates a map with photo deletion capability:

```bash
python photomap_openlayers.py --delete
```

**Result:**
- Creates `photo_map_openlayers_edit.html` file
- "Delete photo" button appears in popups
- Requires web server for deletion functionality

## Edit Mode with Web Server

To use the photo deletion feature:

1. **Create map in edit mode:**
```bash
python photomap_openlayers.py --delete
```

2. **Start web server:**
```bash
python photo_server.py
```

3. **Open browser and go to:**
```
http://localhost:8000/photo_map_openlayers_edit.html
```

4. **Use features:**
   - Click any photo to view
   - Press "Delete photo" to remove original file
   - Marker disappears from map without page reload

## File Structure

```
photomap/
├── image_source/              # Source photos
│   ├── *.jpeg                # JPEG files with GPS data
│   └── thumbs/               # Auto-generated thumbnails
│       └── *.jpeg
├── photomap_openlayers.py    # Main map generation script
├── photo_server.py           # Web server for edit mode
├── photo_map_openlayers.html      # View-only map
├── photo_map_openlayers_edit.html # Edit mode map
└── README.md
```

## Publishing the Map

### Static Publishing (View Only)

1. Create map in view mode:
```bash
python photomap_openlayers.py
```

2. The `photo_map_openlayers.html` file is ready for publishing:
   - Upload to any web hosting
   - Open locally in browser
   - All images embedded in HTML (base64)
   - No additional server required

### Interactive Publishing (With Deletion)

1. Create map in edit mode:
```bash
python photomap_openlayers.py --delete
```

2. Deploy on server with Python support:
   - Upload all project files
   - Run `photo_server.py` on server
   - Configure web server (nginx/apache) for proxying

## Technical Details

- **Image Format:** Only JPEG files supported
- **GPS Data:** Automatic extraction from EXIF
- **Thumbnails:** Created automatically (50x65 pixels)
- **Map Base:** OpenStreetMap via OpenLayers
- **Compatibility:** Modern browsers with ES6 support

## Security

- Server validates file paths to prevent access outside `image_source/`
- Deletion requires user confirmation
- When deleting a file, corresponding thumbnail is also removed

## Troubleshooting

**Photos don't appear on map:**
- Ensure files have `.jpeg` extension
- Check for GPS data in EXIF (many editors remove it)

**Delete button doesn't work:**
- Check that `photo_server.py` is running
- Make sure you open map via `http://localhost:8000/`

**Slow map loading:**
- Reduce number of photos
- Thumbnails are created automatically for optimization

## Use Cases

- 📸 **Travel Photo Albums** - show your trip route
- 🏡 **Property Documentation** - real estate or project mapping
- 🌿 **Scientific Research** - geotagged observations
- 👥 **Family Archives** - history of family event locations

## License

Free to use. Based on open technologies: OpenLayers, OpenStreetMap.
