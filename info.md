[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

<p><a href="https://www.buymeacoffee.com/6rF5cQl" rel="nofollow" target="_blank"><img src="https://camo.githubusercontent.com/c070316e7fb193354999ef4c93df4bd8e21522fa/68747470733a2f2f696d672e736869656c64732e696f2f7374617469632f76312e7376673f6c6162656c3d4275792532306d6525323061253230636f66666565266d6573736167653d25463025394625413525413826636f6c6f723d626c61636b266c6f676f3d6275792532306d6525323061253230636f66666565266c6f676f436f6c6f723d7768697465266c6162656c436f6c6f723d366634653337" alt="Buy me a coffee" data-canonical-src="https://img.shields.io/static/v1.svg?label=Buy%20me%20a%20coffee&amp;message=%F0%9F%A5%A8&amp;color=black&amp;logo=buy%20me%20a%20coffee&amp;logoColor=white&amp;labelColor=b0c4de" style="max-width:100%;"></a></p>

# Home Assistant custom integration for Radioactivity data in Hungary

This custom component integrates radioactivity information provided by Disaster Recovery Directorate (Katasztrofavédelem).

The state of the sensor will be the level of the environmental radioactivity. Thresholds are defined on the bottom of the page [
Háttérsugárzás - Aktuális adatsor](https://www.katasztrofavedelem.hu/modules/hattersugarzas/aktualis_adatsor)

#### Installation
The easiest way to install it is through [HACS (Home Assistant Community Store)](https://github.com/hacs/integration),
search for <i>Radioactivity HU</i> in the Integrations.<br />

#### Configuration:
Define sensor with the following configuration parameters:<br />

---
| Name | Optional | `Default` | Description |
| :---- | :---- | :------- | :----------- |
| name | **Y** | `radioactivity_hu` | name of the sensor |
| station | **Y** | `Budapest XI. ker. (Őrezred)` | name of the measuring station (see below) |
---

Measuring station names should match the 'Állomás' specified at
[Háttérsugárzás - Aktuális adatsor](https://www.katasztrofavedelem.hu/modules/hattersugarzas/aktualis_adatsor)

Example of radioactivity information:

![Radioactivity  attributes](https://raw.githubusercontent.com/amaximus/radioactivity_hu/main/radioactivity_hu.png)

## Examples
```
platform: radioactivity_hu
```

Example Lovelace UI custom button card:
```
type: custom:button-card
color_type: icon
show_label: true
show_name: false
show_icon: true
entity: sensor.radioactivity_hu
size: 30px
styles:
  label:
    - font-size: 90%
    - text-align: left
  card:
    - height: 80px
  icon:
    - color:
        [[[
          var r_val = states['sensor.radioactivity_hu'].state;
          if ( r_val > 500  ) {
            return "red";
          } else if ( r_val > 250 ) {
            return "orange";
          } 
          return "green";
        ]]]
layout: icon_label
label: Radioactivity
```

## Thanks

Thanks to all the people who have contributed!

[![contributors](https://contributors-img.web.app/image?repo=amaximus/radioactivity_hu)](https://github.com/amaximus/radioactivity_hu/graphs/contributors)
