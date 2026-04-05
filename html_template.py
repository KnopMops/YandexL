from config import YANDEX_MAPS_API_KEY

HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Яндекс.Карты</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://api-maps.yandex.ru/2.1/?apikey={YANDEX_MAPS_API_KEY}&lang=ru_RU"></script>
    <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
    <style>
        html, body, #map {{ height: 100%; margin: 0; padding: 0; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var map;
        var currentPlacemark = null;
        var currentAddress = "";
        var currentPostalCode = "";
        var showPostalCode = false;
        var bridge;

        function init() {{
            map = new ymaps.Map("map", {{
                center: [55.7558, 37.6173],
                zoom: 10,
                controls: ["zoomControl", "fullscreenControl"]
            }});

            map.events.add("click", function(e) {{
                var coords = e.get("coords");
                reverseGeocode(coords, false);
            }});

            map.events.add("contextmenu", function(e) {{
                var coords = e.get("coords");
                searchOrganization(coords);
            }});

            new QWebChannel(qt.webChannelTransport, function(channel) {{
                bridge = channel.bridge;
            }});
        }}

        function reverseGeocode(coords, isForOrganization) {{
            ymaps.geocode(coords, {{ results: 1 }}).then(function(res) {{
                var firstGeoObject = res.geoObjects.get(0);
                if (!firstGeoObject) return;

                var address = firstGeoObject.getAddressLine();
                var postalCode = firstGeoObject.getPostalCode() || "";
                var pointCoords = firstGeoObject.geometry.getCoordinates();

                if (!isForOrganization) {{
                    setPlacemark(pointCoords, address);
                    currentAddress = address;
                    currentPostalCode = postalCode;
                    updateAddressDisplay();
                    if (bridge) bridge.updateAddress(address + (postalCode ? ", " + postalCode : ""));
                    map.setCenter(pointCoords);
                }}
            }});
        }}

        function searchOrganization(coords) {{
            ymaps.geocode(coords, {{
                kind: "organizations",
                results: 1,
                searchCoordOrder: "longlat",
                radius: 50
            }}).then(function(res) {{
                var firstOrg = res.geoObjects.get(0);
                if (firstOrg) {{
                    var orgCoords = firstOrg.geometry.getCoordinates();
                    var orgName = firstOrg.getName();
                    var orgAddress = firstOrg.getAddressLine();
                    var postalCode = firstOrg.getPostalCode() || "";
                    var fullAddr = orgName + ", " + orgAddress;
                    if (showPostalCode && postalCode) fullAddr += ", " + postalCode;

                    setPlacemark(orgCoords, fullAddr);
                    currentAddress = orgAddress;
                    currentPostalCode = postalCode;
                    updateAddressDisplay();
                    if (bridge) bridge.updateAddress(fullAddr);
                }} else {{
                    clearPlacemark();
                    if (bridge) bridge.updateAddress("Не найдено организаций в радиусе 50 м");
                }}
            }}).catch(function(err) {{
                console.error("Ошибка поиска организации:", err);
                clearPlacemark();
                if (bridge) bridge.updateAddress("Ошибка поиска");
            }});
        }}

        function searchByText(query) {{
            if (!query) return;
            ymaps.geocode(query, {{ results: 1 }}).then(function(res) {{
                var firstGeoObject = res.geoObjects.get(0);
                if (!firstGeoObject) {{
                    if (bridge) bridge.updateAddress("Ничего не найдено");
                    return;
                }}
                var coords = firstGeoObject.geometry.getCoordinates();
                var address = firstGeoObject.getAddressLine();
                var postalCode = firstGeoObject.getPostalCode() || "";
                setPlacemark(coords, address);
                currentAddress = address;
                currentPostalCode = postalCode;
                updateAddressDisplay();
                if (bridge) bridge.updateAddress(address + (showPostalCode && postalCode ? ", " + postalCode : ""));
                map.setCenter(coords, map.getZoom());
            }}).catch(function(err) {{
                console.error("Ошибка геокодирования:", err);
                if (bridge) bridge.updateAddress("Ошибка поиска");
            }});
        }}

        function setPlacemark(coords, hintContent) {{
            if (currentPlacemark) map.geoObjects.remove(currentPlacemark);
            currentPlacemark = new ymaps.Placemark(coords, {{
                hintContent: hintContent,
                balloonContent: hintContent
            }});
            map.geoObjects.add(currentPlacemark);
        }}

        function clearPlacemark() {{
            if (currentPlacemark) {{
                map.geoObjects.remove(currentPlacemark);
                currentPlacemark = null;
            }}
            currentAddress = "";
            currentPostalCode = "";
            updateAddressDisplay();
            if (bridge) bridge.updateAddress("");
        }}

        function updateAddressDisplay() {{
            var displayAddr = currentAddress;
            if (showPostalCode && currentPostalCode) displayAddr += ", " + currentPostalCode;
            if (bridge) bridge.updateAddress(displayAddr);
        }}

        function setTheme(isDark) {{
            if (isDark) {{
                map.setType("dark");
            }} else {{
                map.setType("yandex#map");
            }}
        }}

        function setMapType(type) {{
            var typeMap = {{
                "base": "yandex#map",
                "satellite": "yandex#satellite",
                "hybrid": "yandex#hybrid",
                "people": "yandex#peopleMap"
            }};
            map.setType(typeMap[type] || "yandex#map");
        }}

        function zoomIn() {{
            var z = map.getZoom();
            if (z < 19) map.setZoom(z + 1);
        }}
        function zoomOut() {{
            var z = map.getZoom();
            if (z > 1) map.setZoom(z - 1);
        }}

        function move(dx, dy) {{
            var bounds = map.getBounds();
            var sw = bounds.getSouthWest();
            var ne = bounds.getNorthEast();
            var width = ne.getLng() - sw.getLng();
            var height = ne.getLat() - sw.getLat();

            var center = map.getCenter();
            var newLng = center.getLng() + dx * width;
            var newLat = center.getLat() + dy * height;

            newLng = Math.min(180, Math.max(-180, newLng));
            newLat = Math.min(85, Math.max(-85, newLat));

            map.setCenter([newLat, newLng]);
        }}

        ymaps.ready(init);
    </script>
</body>
</html>
"""
