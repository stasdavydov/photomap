# Photo Map

Interactive map for displaying geolocated photos using OpenLayers.

## Features

- 📍  Automatic GPS coordinate extraction from photo EXIF data
- 🖼️ Photo thumbnails as map markers
- 🔍  Full-size images in popups on click
- 🗑️ Photo deletion feature
- ⚡  Optimized loading with automatic thumbnail generation
- 🗺️ Automatic map centering on all photos

## Installation

1. Download `index.html` from the repo.
2. Open it in a browser locally.


## Usage

1. Choose a folder with your photos. For a better performance it is recommended to have files 
   organized via subfolders. 
2. Wait until the indexing and enjoy the gallery.


## File Structure and Static Publishing

Once a gallery is generated you can publish it into any webhosting just by copying the `.photomap/` folder.
All the photos are resized and thumnails are generated. `index.html` is provided.

```
.photomap/
├── images/                   # Resized photos
│   └── *.jpeg                # JPEG files with GPS data
├───thumbnails/               # Auto-generated thumbnails
│       └── *.jpeg
├── index.html                # Main gallery all-included file
├── gallery.json              # The gallery generated index required for this particular gallery.
└── README.md
```

## Technical Details

- **Image Format:** Only JPEG files supported
- **GPS Data:** Automatic extraction from EXIF
- **Thumbnails:** Created automatically
- **Map Base:** OpenStreetMap via OpenLayers
- **Compatibility:** Modern browsers with ES6 support

## Security

- You need to allow the app to access your local folder with photos

## Troubleshooting

**Slow map loading:**
- Organize photos in subfolders

## Use Cases

- 📸 **Travel Photo Albums** - show your trip route
- 🏡 **Property Documentation** - real estate or project mapping
- 🌿 **Scientific Research** - geotagged observations
- 👥 **Family Archives** - history of family event locations

## License

MIT
