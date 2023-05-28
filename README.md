# Aspect Ratio Helper  [![pytest](https://github.com/thomasasfk/sd-webui-aspect-ratio-helper/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/thomasasfk/sd-webui-aspect-ratio-helper/actions/workflows/pytest.yml)

Simple extension to easily maintain aspect ratio while changing dimensions.

Install via the extensions tab on the [AUTOMATIC1111 webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui).

## Features

**(note this list is a little out of date, will need to find time to update it)**

- JavaScript aspect ratio controls
  - Adds a dropdown of configurable aspect ratios, to which the dimensions will auto-scale
  - When selected, you will only be able to modify the higher dimension
    - The smaller or equivalent dimension will scale accordingly
  - If "Lock/🔒" is selected, the aspect ratio of the current dimensions will be kept
  - If "Image/🖼️" is selected, the aspect ratio of the current image will be kept (img2img only)
  - If you click the "Swap/⇅" button, the current dimensions will swap
    - Configurable aspect ratios will also flip, reducing the need for duplication of config

https://user-images.githubusercontent.com/22506439/227396634-7a63671a-fd38-419a-b734-a3d26647cc1d.mp4

<br/>

- Scale to maximum dimension
  - Upon clicking, the width and height will scale according to the configured maximum value
  - Aspect ratio will be retained, the smaller or equivalent dimension will be scaled to match
- Scale to aspect ratio
  - Upon clicking, the current dimensions will be scaled to the given aspect ratio, using the highest width or height
    - i.e `4:3 of 256x512 = 512x384` `9:16 of 512x256 = 288x512` `1:1 of 256x300 = 300x300`
  - You can optionally toggle this to use the "Maximum dimension" slider value
    - i.e `4:3 of 512 = 512x384` `9:16 of 512 = 288x512` `1:1 of 300 = 300x300`
- Scale by percentage
  - Upon clicking, the current dimensions will be multiplied by the given percentage, with aspect ratio maintained
  - i.e `-25% of 512x256 = 384x192` `+50% of 512x512 = 768x768`
    - You can also change the display of these if you find it more intuitive
    - i.e `75% of 512x256 = 384x192` `150% of 512x512 = 768x768`
    - i.e `x0.75 of 512x256 = 384x192` `x1.5 of 512x512 = 768x768`

![user-interface.png](docs%2Fui.png)

## Settings

- Hide accordion by default (`False`)
- Expand accordion by default (`False`)
  - Determines whether the 'Aspect Ratio Helper' accordion expands by default
- UI Component order (`MaxDimensionScaler, PredefinedAspectRatioButtons, PredefinedPercentageButtons`)
  - Determines the order in which the UI components will render
- Enable JavaScript aspect ratio controls
- JavaScript aspect ratio buttons `(1:1, 4:3, 16:9, 9:16, 21:9)`
  - i.e `1:1, 4:3, 16:9, 9:16, 21:9` `2:3, 1:5, 3:5`
- Show maximum dimension button (`True`)
- Maximum dimension default (`1024`)
- Show pre-defined aspect ratio buttons (`True`)
- Use "Maximum dimension" for aspect ratio buttons (`False`)
- Pre-defined aspect ratio buttons (`1:1, 4:3, 16:9, 9:16, 21:9`)
  - i.e `1:1, 4:3, 16:9, 9:16, 21:9` `2:3, 1:5, 3:5`
- Show pre-defined percentage buttons (`True`)
- Pre-defined percentage buttons (`25, 50, 75, 125, 150, 175, 200`)
  - i.e `25, 50, 75, 125, 150, 175, 200` `50, 125, 300`
- Pre-defined percentage display format (`Incremental/decremental percentage (-50%, +50%)`)
  - `Incremental/decremental percentage (-50%, +50%)`
  - `Raw percentage (50%, 150%)`
  - `Multiplication (x0.5, x1.5)`

![settings.png](docs%2Fopts.png)


JavaScript & accordion aspect ratios _might_ not play well together - I don't think many users will use both simultaneously, but we'll see.

## Contributing

- Open an issue for suggestions
- Raise a pull request

## Dependencies

Developed using existing [AUTOMATIC1111 webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) dependencies.

It's recommended to use the python version specified by A1111 webui.

However - for running unit tests, we use pytest.

```bash
pip install pytest
```

## Testing
From the root of the repository.
```bash
pytest
```
