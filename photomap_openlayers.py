from pathlib import Path
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS
import base64
import json
import argparse


def get_gps_info(image_path):
    with Image.open(image_path) as img:
        exif_data = img._getexif()
        if exif_data is None:
            return None

        gps_info = {}
        for tag, value in exif_data.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_info[sub_decoded] = value[t]

        if gps_info:
            lat = convert_to_degrees(gps_info.get("GPSLatitude"))
            lon = convert_to_degrees(gps_info.get("GPSLongitude"))
            if gps_info.get("GPSLatitudeRef") == "S":
                lat = -lat
            if gps_info.get("GPSLongitudeRef") == "W":
                lon = -lon
            return lat, lon
        return None


def convert_to_degrees(value):
    if value is None:
        return None
    # PIL returns a tuple of IFDRational; casting directly to float
    d, m, s = [float(x) for x in value]
    return d + (m / 60.0) + (s / 3600.0)


def create_map(enable_delete=False):
    """Create photo map with optional delete functionality"""

    # Collect photo data
    image_paths = list(Path("image_source").glob("*.jpeg"))
    photo_data = []

    for img_path in image_paths:
        gps_coords = get_gps_info(img_path)
        if gps_coords:
            lat, lon = gps_coords

            # Create thumbnail for map marker
            thumb_dir = Path("image_source/thumbs")
            thumb_dir.mkdir(exist_ok=True)
            thumb_path = thumb_dir / img_path.name

            if not thumb_path.exists():
                with Image.open(img_path) as im:
                    im.thumbnail((50, 65))
                    im.save(thumb_path)

            # Encode thumbnail for marker
            with open(thumb_path, 'rb') as thumb_file:
                thumb_encoded = base64.b64encode(thumb_file.read()).decode('utf-8')

            # Encode full image for popup
            with open(img_path, 'rb') as img_file:
                img_encoded = base64.b64encode(img_file.read()).decode('utf-8')

            photo_data.append({
                'lat': lat,
                'lon': lon,
                'name': img_path.name,
                'path': str(img_path),
                'thumbnail': f"data:image/jpeg;base64,{thumb_encoded}",
                'image': f"data:image/jpeg;base64,{img_encoded}"
            })

    # Create different popup content based on delete flag
    delete_button = ''
    delete_function = ''

    if enable_delete:
        delete_button = '''
                        <button class="delete-btn" onclick="deletePhoto('${{photo.path}}', '${{photo.name}}')">
                            Удалить фото
                        </button>'''
        delete_function = '''
        // Function to delete photo
        async function deletePhoto(photoPath, photoName) {
            if (confirm(`Вы уверены, что хотите удалить фото "${{photoName}}"?`)) {
                try {
                    const response = await fetch('/delete-photo', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ path: photoPath })
                    });
                    
                    if (response.ok) {
                        alert('Фото успешно удалено!');
                        // Hide popup and remove marker from map
                        popup.setPosition(undefined);
                        
                        // Find and remove the feature from the map
                        const features = vectorLayer.getSource().getFeatures();
                        const featureToRemove = features.find(feature => {
                            const photo = feature.get('photo');
                            return photo.path === photoPath;
                        });
                        
                        if (featureToRemove) {
                            vectorLayer.getSource().removeFeature(featureToRemove);
                        }
                    } else {
                        alert('Ошибка при удалении фото');
                    }
                } catch (error) {
                    alert('Ошибка при удалении фото: ' + error.message);
                }
            }
        }'''

    # Create HTML with OpenLayers
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Photo Map - OpenLayers</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ol@v7.5.2/ol.css" type="text/css">
    <script src="https://cdn.jsdelivr.net/npm/ol@v7.5.2/dist/ol.js"></script>
    <style>
        #map {{
            width: 100%;
            height: 100vh;
        }}
        .popup {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            padding: 10px;
            max-width: 400px;
        }}
        .popup img {{
            max-width: 100%;
            border-radius: 5px;
        }}
        .popup h3 {{
            margin: 10px 0 5px 0;
            font-size: 14px;
        }}
        .popup-buttons {{
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }}
        .delete-btn {{
            background: #ff4444;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
        }}
        .delete-btn:hover {{
            background: #cc3333;
        }}
        .close-btn {{
            background: #666;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
        }}
        .close-btn:hover {{
            background: #555;
        }}
        .marker-icon {{
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
    </style>
</head>
<body>
    <div id="map"></div>
    
    <script>
        const photoData = {json.dumps(photo_data)};
        
        // Create popup overlay
        const popup = new ol.Overlay({{
            element: document.createElement('div'),
            autoPan: true,
            autoPanAnimation: {{
                duration: 250
            }}
        }});
        popup.getElement().className = 'popup';
        
        {delete_function}
        
        // Create map
        const map = new ol.Map({{
            target: 'map',
            layers: [
                new ol.layer.Tile({{
                    source: new ol.source.OSM()
                }})
            ],
            view: new ol.View({{
                center: ol.proj.fromLonLat([0, 0]),
                zoom: 2
            }}),
            overlays: [popup]
        }});
        
        // Create features for each photo
        const features = photoData.map(photo => {{
            const feature = new ol.Feature({{
                geometry: new ol.geom.Point(ol.proj.fromLonLat([photo.lon, photo.lat])),
                photo: photo
            }});
            
            // Create custom icon style with thumbnail
            const iconStyle = new ol.style.Style({{
                image: new ol.style.Icon({{
                    src: photo.thumbnail,
                    scale: 1,
                    imgSize: [50, 65],
                    anchor: [0.5, 1],
                    anchorXUnits: 'fraction',
                    anchorYUnits: 'fraction'
                }})
            }});
            
            feature.setStyle(iconStyle);
            return feature;
        }});
        
        // Create vector layer with photo markers
        const vectorLayer = new ol.layer.Vector({{
            source: new ol.source.Vector({{
                features: features
            }})
        }});
        
        map.addLayer(vectorLayer);
        
        // Fit map to show all photos
        if (features.length > 0) {{
            const extent = vectorLayer.getSource().getExtent();
            map.getView().fit(extent, {{
                padding: [50, 50, 50, 50],
                maxZoom: 15
            }});
        }}
        
        // Handle click events
        map.on('click', function(event) {{
            const feature = map.forEachFeatureAtPixel(event.pixel, function(feature) {{
                return feature;
            }});
            
            if (feature) {{
                const photo = feature.get('photo');
                const coordinate = feature.getGeometry().getCoordinates();
                
                popup.getElement().innerHTML = `
                    <img src="${{photo.image}}" style="max-width: 350px;">
                    <h3>${{photo.name}}</h3>
                    <div class="popup-buttons">{delete_button}
                        <button class="close-btn" onclick="popup.setPosition(undefined)">
                            Закрыть
                        </button>
                    </div>
                `;
                popup.setPosition(coordinate);
            }} else {{
                popup.setPosition(undefined);
            }}
        }});
        
        // Change cursor on hover
        map.on('pointermove', function(event) {{
            const hit = map.hasFeatureAtPixel(event.pixel);
            map.getTargetElement().style.cursor = hit ? 'pointer' : '';
        }});
    </script>
</body>
</html>
"""

    # Save HTML file with appropriate name
    filename = "photo_map_openlayers_edit.html" if enable_delete else "photo_map_openlayers.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    mode_text = "редактирования" if enable_delete else "просмотра"
    print(f"OpenLayers карта в режиме {mode_text} сохранена как {filename}")
    print(f"Добавлено {len(photo_data)} фотографий на карту")

    if enable_delete:
        print("⚠️  Для использования функции удаления запустите сервер: python photo_server.py")

    return filename


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Photo Map Creator")
    parser.add_argument("--delete", action="store_true", help="Enable photo deletion feature")
    args = parser.parse_args()

    create_map(enable_delete=args.delete)
