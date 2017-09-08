# vnaasgui

## Installation

Having a profile deployed via Ansible is required. To use the GUI, include the following in the profile manifest
being used in `cord/build/platform-install/profile_manifests`.

```
enabled_gui_extensions:
  - name: vnaasgui
    path: orchestration/vnaas/xos/gui
    extra-files:
        - app/style/style.css
        - mapconstants.js
```

## Features

 - Maps all UserNetworkInterface locations, and displays the status of created ELine connections
 - Allows for the creation of new and modification of exisiting ELine connections using the map
 
## Interface

![vnaasgui Screenshot](http://i.imgur.com/f4YxuyV.png)