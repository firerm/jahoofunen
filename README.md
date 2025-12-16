## 🎨 Dashboard Configuration (YAML)

> [!NOTE]
> **SETUP INSTRUCTION**
>
> The YAML code below creates a full card with the image, description, and navigation controls.
>
> **Please verify your Entity IDs:** The code uses default names like `camera.jfen_daily_cartoon`. If you changed the name during the integration setup, make sure to **update the entity IDs** in the code below to match your system.

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
