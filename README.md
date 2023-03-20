# Aspect Ratio Helper

Simple extension to easily maintain aspect ratio while changing dimensions.

Install via the extensions tab on the [AUTOMATIC1111 webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui).

## Main features:

- Scale to maximum width or dimension
  - Upon clicking, the dimensions will scale the highest value to the maximum configured value
  - Aspect ratio will be maintained, the smaller or equivalent value will be scaled to match
- Scale by percentage
  - Upon clicking, the current dimensions will be multiplied by the given percentage, with aspect ratio maintained
  - i.e `150% of 512x512 = 768x768` `75% of 512x256 = 384x192` etc.

![user-interface.png](docs%2Fuser-interface.png)

## Settings:

- Expand by default
  - Determines whether the 'Aspect Ratio Helper' accordion expands by default
- Show maximum width of height button
- Maximum width or height default
- Show percentage buttons
- Percentage buttons
  - Comma separated list of percentages
  - i.e `25, 50, 75, 125, 150, 175, 200` `50, 125, 300` etc.

![settings.png](docs%2Fsettings.png)

## Contributing:

- Open to suggestions
- Pull requests are appreciated
- Write tests if possible and useful
- Run pre-commit!
