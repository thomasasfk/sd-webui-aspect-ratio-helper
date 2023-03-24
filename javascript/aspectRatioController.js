// https://github.com/Gerschel/stable-diffusion-webui/blob/742d86eed4d07eef7db65b3d943f85bdbafc26e4/javascript/ComponentControllers.js#L176
class ContainerController {
    constructor(element) {
        this.element = element;
        this.num = this.element.querySelector('input[type=number]');
        this.range = this.element.querySelector('input[type=range]');
    }

    getVal() {
        return this.num.value;
    }

    disable() {
        this.num.setAttribute('disabled', true);
        this.range.setAttribute('disabled', true);
    }

    enable() {
        this.num.removeAttribute('disabled');
        this.range.removeAttribute('disabled');
    }

    updateVal(text) {
        this.num.value = text;
        this.range.value = text;
    }

    updateMin(text) {
        this.num.min = text;
        this.range.min = text;
    }

    eventHandler() {
        this.element.dispatchEvent(
            new Event("input")
        );
        this.num.dispatchEvent(
            new Event("input")
        );
        this.range.dispatchEvent(
            new Event("input")
        );
    }

    setVal(text) {
        this.updateVal(text);
        this.eventHandler();
    }
}

function _reverseAspectRatio(ar) {
    if (['Off', '🔓'].includes(ar)) return;
    const [width, height] = ar.split(":");
    return `${height}:${width}`;
}

class AspectRatioController {
    constructor(widthContainer, heightContainer, aspectRatio = "Off") {
        this.widthContainer = new ContainerController(widthContainer);
        this.heightContainer = new ContainerController(heightContainer);
        this.max = 2048;
        this.min = 64;

        this.dimensions = {
            widthInput: this.widthContainer.num,
            widthRange: this.widthContainer.range,
            heightInput: this.heightContainer.num,
            heightRange: this.heightContainer.range,
        };

        Object.values(this.dimensions).forEach(dimension => {
            dimension.step = 1;
            dimension.addEventListener('change', (e) => {
                e.preventDefault()
                this._syncValues(dimension);
            });
        })

        this.setAspectRatio(aspectRatio);
    }

    setAspectRatio(aspectRatio) {
        this.aspectRatio = aspectRatio;

        if (aspectRatio === "Off") {
            this.widthContainer.enable();
            this.heightContainer.enable();
            this.widthContainer.updateMin(this.min);
            this.heightContainer.updateMin(this.min);
            return;
        }

        const lockedSetting = [
            this.widthContainer.getVal(),
            this.heightContainer.getVal(),
        ];

        const [widthRatio, heightRatio] = this._clampToBoundaries(
            ...(
                aspectRatio !== '🔓'
                    ? aspectRatio.split(':')
                    : lockedSetting
            ).map(Number)
        )

        this.widthRatio = widthRatio;
        this.heightRatio = heightRatio;
        if (widthRatio >= heightRatio) {
            this.heightContainer.disable();
            this.widthContainer.enable();
            const minimum = Math.max(
                Math.round(this.min * widthRatio / heightRatio), this.min
            );
            this.widthContainer.updateMin(minimum);
            this.heightContainer.updateMin(this.min);
        } else {
            this.widthContainer.disable();
            this.heightContainer.enable();
            const minimum = Math.max(
                Math.round(this.min * heightRatio / widthRatio), this.min
            );
            this.heightContainer.updateMin(minimum);
            this.widthContainer.updateMin(this.min);
        }

        this._syncValues();
    }

    _syncValues(changedElement) {
        if (this.aspectRatio === "Off") return;
        if (!changedElement) {
            changedElement = {
                value: Math.max(
                    ...Object.values(this.dimensions).map(x => x.value)
                )
            }
        }

        const aspectRatio = this.widthRatio / this.heightRatio;
        let w, h;
        if (this.widthRatio >= this.heightRatio) {
            w = Math.round(changedElement.value);
            h = Math.round(changedElement.value / aspectRatio);
        } else {
            h = Math.round(changedElement.value);
            w = Math.round(changedElement.value * aspectRatio);
        }

        const [width, height] = this._clampToBoundaries(w, h)
        this.widthContainer.setVal(width);
        this.heightContainer.setVal(height);
    }


    _clampToBoundaries(width, height) {
        const aspectRatio = width / height;
        const MAX_DIMENSION = this.max;
        const MIN_DIMENSION = this.min;
        if (width > MAX_DIMENSION) {
            width = MAX_DIMENSION;
            height = Math.round(width / aspectRatio);
        }
        if (height > MAX_DIMENSION) {
            height = MAX_DIMENSION;
            width = Math.round(height * aspectRatio);
        }
        if (width < MIN_DIMENSION) {
            width = MIN_DIMENSION;
            height = Math.round(width / aspectRatio);
        }
        if (height < MIN_DIMENSION) {
            height = MIN_DIMENSION;
            width = Math.round(height * aspectRatio);
        }
        if (width < MIN_DIMENSION) {
            width = MIN_DIMENSION;
        } else if (width > MAX_DIMENSION) {
            width = MAX_DIMENSION;
        }
        if (height < MIN_DIMENSION) {
            height = MIN_DIMENSION;
        } else if (height > MAX_DIMENSION) {
            height = MAX_DIMENSION;
        }

        return [width, height]
    }

    static observeStartup(page, key) {
        let observer = new MutationObserver(() => {
            const widthContainer = gradioApp().querySelector(`#${page}_width`);
            const heightContainer = gradioApp().querySelector(`#${page}_height`);
            if (widthContainer && heightContainer) {
                observer.disconnect();
                if (!window.opts.arh_javascript_aspect_ratio_show) return;

                const switchBtn = gradioApp().getElementById(page + '_res_switch_btn');
                if (!switchBtn) return;

                const wrapperDiv = document.createElement('div');
                wrapperDiv.setAttribute("id", `${page}_size_toolbox`);
                wrapperDiv.setAttribute("class", "flex flex-col relative col gap-4");
                wrapperDiv.setAttribute("style", "min-width: min(320px, 100%); flex-grow: 0");
                wrapperDiv.innerHTML = `
                <div id="${page}_ratio" class="gr-block gr-box relative w-full border-solid border border-gray-200 gr-padded">
                  <select id="${page}_select_aspect_ratio" class="gr-box gr-input w-full disabled:cursor-not-allowed">
                  ${
                      window.opts.arh_javascript_aspect_ratio.split(',').map(r => {
                          return '<option class="ar-option">' + r.trim() + '</option>'
                      }).join('\n')
                  }
                  </select>
                </div>
                `;

                const parent = switchBtn.parentNode;
                parent.removeChild(switchBtn);
                wrapperDiv.appendChild(switchBtn);
                parent.insertBefore(wrapperDiv, parent.lastChild.previousElementSibling);

                const controller = new AspectRatioController(widthContainer, heightContainer);
                const aspectRatioSelect = gradioApp().getElementById(`${page}_select_aspect_ratio`);
                aspectRatioSelect.onchange = () => {
                  const options = Array.from(aspectRatioSelect);
                  const picked = options[aspectRatioSelect.selectedIndex].value;
                  controller.setAspectRatio(picked);
                };

                switchBtn.onclick = () => {
                    Array.from(gradioApp().querySelectorAll('.ar-option')).forEach(el => {
                        const reversed = _reverseAspectRatio(el.value);
                        if (reversed) {
                            el.value = reversed;
                            el.textContent = reversed;
                        }
                    });
                    const options = Array.from(aspectRatioSelect);
                    let picked = options[aspectRatioSelect.selectedIndex].value;
                    if (picked === '🔓') {
                        picked = `${controller.heightRatio}:${controller.widthRatio}`
                    }
                    controller.setAspectRatio(picked);
                };

                window[key] = controller;
            }
        });
        observer.observe(gradioApp(), {childList: true, subtree: true});
    }

}

document.addEventListener("DOMContentLoaded", () => {
    window.__txt2imgAspectRatioController = AspectRatioController.observeStartup(
        "txt2img", "__txt2imgAspectRatioController"
    );
    window.__img2imgAspectRatioController = AspectRatioController.observeStartup(
        "img2img", "__img2imgAspectRatioController"
    );
});
