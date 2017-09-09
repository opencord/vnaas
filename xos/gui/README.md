# vnaasgui

## Installation

Having a profile deployed via Ansible is required. To use the GUI, include the following in the profile manifest
being used in `cord/build/platform-install/profile_manifests`.

```yaml
enabled_gui_extensions:
  - name: vnaasgui
    path: orchestration/vnaas/xos/gui
    extra-files:
        - app/style/style.css
        - mapconstants.js
```

### Usage in China
The usual Google Maps API is not available in China. To fix this problem, change the API url in 
`src/app/components/vnaasMap.component.html`.

#### Before
```html
<div map-lazy-load="https://maps.googleapis.com/maps/api/js?key={API_KEY}">
``` 

#### After
```html
<div map-lazy-load="http://maps.google.cn/maps/api/js?key={API_KEY}">
```

## Features

 - Maps all UserNetworkInterface locations, and displays the status of created ELine connections
 - Allows for the creation of new and modification of exisiting ELine connections using the map
 
## Interface

![vnaasgui Screenshot](http://i.imgur.com/f4YxuyV.png)