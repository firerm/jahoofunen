Automate your Laughter 🤖😂
<div align="center">
  <img src="logoen2.png" width="600px" alt="Daily Cartoon Logo">
</div>

<div align="center">

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![GitHub stars](https://img.shields.io/github/stars/firerm/jahoofunen?style=for-the-badge)](https://github.com/firerm/jahoofunen/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/firerm/jahoofunen?style=for-the-badge)](https://github.com/firerm/jahoofune/issues)


</div>
We automate our lights. We automate our heating. Why not automate our humor?

Introducing the Daily Cartoon & Meme Viewer for Home Assistant. Because frankly, looking at your server CPU usage isn't funny (unless it's at 100%, then it's a tragedy).

Features:

🎨 High-Quality Imagery: Crispy cartoons and memes.

👉 Interactive: Browse through previous days if you missed the fun.

🧩 Plug & Play: Works out of the box.

Just Click here : 
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=firerm&repository=jahoofunen&category=integration)

## 💿 Installation

Once you have added this repository to HACS:
  When you add The repo ** automaticaly**
1.  **Restart:** Restart Home Assistant completely. * When you done : 
2.  **Add Integration:**
    * Go to **Settings** > **Devices & Services**.
    * Click the **+ ADD INTEGRATION** button (bottom right).
    * Search for **"Jahoo"**.
    * Click on it to install.

Done! You can now add the card ** choose manual ** to your dashboard using the YAML code above.
you can customize it !

PS: when you press the arrows wait 10 sec to change the photo this is protection for Home Assistant OS to not flood the system. Its normal.

## 🎨 Dashboard Configuration (YAML) * choose MANUAL *

> [!NOTE]
> **SETUP INSTRUCTION**
>
> The YAML code below creates a full card with the image, description, and navigation controls.
>
> **Please verify your Entity IDs:** The code uses default names like `camera.jfen_daily_cartoon`.


```yaml
type: vertical-stack
cards:
  # -----------------------------------------------------------
  # 1. IMAGE CARD (Camera Entity)
  # -----------------------------------------------------------
  - type: picture-entity
    # REPLACE below if your entity ID is different
    entity: camera.jfen_daily_cartoon
    show_name: false
    show_state: false
    tap_action:
      action: none

  # -----------------------------------------------------------
  # 2. TEXT & CONTENT (Sensor Entity)
  # -----------------------------------------------------------
  - type: markdown
    content: |
      ## {{ states('sensor.jfen_daily_cartoon') }}
      {{ state_attr('sensor.jfen_daily_cartoon', 'description') }}

      <small style="display: block; text-align: right; margin-top: 10px; opacity: 0.6; line-height: 1.6;">
        <a href="{{ state_attr('sensor.jfen_daily_cartoon', 'viewer_url') }}" target="_blank" style="text-decoration: none; color: inherit;">
           VIEW FULL SIZE
        </a><br>
        <a href="[https://jahoo.gr](https://jahoo.gr)" target="_blank" style="text-decoration: none; color: inherit;">
           jahoo.gr
        </a>
      </small>

  # -----------------------------------------------------------
  # 3. CONTROLS (Buttons)
  # -----------------------------------------------------------
  - type: horizontal-stack
    cards:
      - type: button
        # Check your 'Previous' button entity ID
        entity: button.previous_image
        show_name: false
        icon: mdi:arrow-left
        tap_action:
          action: toggle
      - type: button
        # Check your 'Next' button entity ID
        entity: button.next_image
        show_name: false
        icon: mdi:arrow-right
        tap_action:
          action: toggle
