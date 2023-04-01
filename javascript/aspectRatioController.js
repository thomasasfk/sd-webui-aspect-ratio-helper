// constants
const _OFF = "Off";  // Don't use the functionality at all
const _LOCK = '🔓';  // Aspect ratio is "locked"
const _IMAGE = '🖼️'; // Aspect ratio is "locked" to that of the image

const _MAXIMUM_DIMENSION = 2048;
const _MINIMUM_DIMENSION = 64;

const _TAB_STRING_TO_IMAGE_ID_MAP = {
    'img2img': 'img2img_image',
    'sketch': 'img2img_sketch',
    'inpaint': 'img2maskimg',
    'inpaint sketch': 'inpaint_sketch',
    'inpaint upload': 'img_inpaint_base',
}

const _IMAGE_INPUT_CONTAINER_IDS = Array.from(Object.values(_TAB_STRING_TO_IMAGE_ID_MAP));

const getSelectedImage2ImageTab = () => {
    return document.querySelector('#img2img_settings > div > div > button.selected').textContent.toLowerCase().trim();
}

const getCurrentImage = () => {
    const currentTab = getSelectedImage2ImageTab();
    const currentTabImageId = _TAB_STRING_TO_IMAGE_ID_MAP[currentTab];
    return document.getElementById(currentTabImageId).querySelector('img');
}

// utility functions
const roundToClosestMultiple = (num, multiple) => {
    const rounded =  Math.round(Number(num) / multiple) * multiple;
    return rounded;
}


const aspectRatioFromStr = (ar) => {
    if (!ar.includes(':')) return;
    return ar.split(':').map(x => Number(x));
}

const reverseAspectRatio = (ar) => {
    if (!ar.includes(':')) return;
    const [width, height] = ar.split(':');
    return `${height}:${width}`;
}

const clampToBoundaries = (width, height) => {
    const aspectRatio = width / height;
    width = Math.max(Math.min(width, _MAXIMUM_DIMENSION), _MINIMUM_DIMENSION);
    height = Math.max(Math.min(height, _MAXIMUM_DIMENSION), _MINIMUM_DIMENSION);
    if (width / height > aspectRatio) {
        height = Math.round(width / aspectRatio);
    } else if (width / height < aspectRatio) {
        width = Math.round(height * aspectRatio);
    }

    if (width > _MAXIMUM_DIMENSION) {
        width = _MAXIMUM_DIMENSION;
    }

    if (height < _MINIMUM_DIMENSION) {
        height = _MINIMUM_DIMENSION;
    }

    return [width, height];
}

const getOptions = () => {
    return window.opts.arh_javascript_aspect_ratio.split(',').map(o => o.trim());
}

const reverseAllOptions = () => {
    const allAspectRatioOptions = Array.from(gradioApp().querySelectorAll('.ar-option'));
    allAspectRatioOptions.forEach(el => {
        const reversed = reverseAspectRatio(el.value);
        if (reversed) {
            el.value = reversed;
            el.textContent = reversed;
        }
    });
}

class SelectController {
    constructor(page, defaultOptions, controller) {
        this.page = page;
        this.options = [...new Set([...defaultOptions, ...getOptions()])];
        this.switchButton = gradioApp().getElementById(page + '_res_switch_btn');

        const wrapperDiv = document.createElement('div');
        wrapperDiv.setAttribute("id", `${this.page}_size_toolbox`);
        wrapperDiv.setAttribute("class", "flex flex-col relative col gap-4");
        wrapperDiv.setAttribute("style", "min-width: min(320px, 100%); flex-grow: 0");
        wrapperDiv.innerHTML = `
        <div id="${this.page}_ratio" class="gr-block gr-box relative w-full border-solid border border-gray-200 gr-padded">
            <select id="${this.page}_select_aspect_ratio" class="gr-box gr-input w-full disabled:cursor-not-allowed">
                ${this.options.map(r => {
                    return '<option class="ar-option">' + r + '</option>'
                }).join('\n')}
            </select>
        </div>
        `;

        const parent = this.switchButton.parentNode;
        parent.removeChild(this.switchButton);
        wrapperDiv.appendChild(this.switchButton);
        parent.insertBefore(wrapperDiv, parent.lastChild.previousElementSibling);

        const originalBGC = this.switchButton.style.backgroundColor;
        this.getSelectElement().onchange = () => {
            const picked  = this.getCurrentOption();
            if (_IMAGE === picked) {
                this.switchButton.disabled = true;
                this.switchButton.style.backgroundColor = 'black';
            } else {
                this.switchButton.removeAttribute('disabled')
                this.switchButton.style.backgroundColor = originalBGC;
            }

            controller.setAspectRatio(picked);
        };

        this.switchButton.onclick = () => {
            reverseAllOptions();
            const picked = this.getCurrentOption();
            if (_LOCK === picked) {
                controller.setAspectRatio(`${controller.heightRatio}:${controller.widthRatio}`);
            } else {
                controller.setAspectRatio(picked);
            }
        };
    }

    getSelectElement() {
        return gradioApp().getElementById(`${this.page}_select_aspect_ratio`);
    }

    getCurrentOption() {
        const selectElement = this.getSelectElement();
        const options = Array.from(selectElement);
        return options[selectElement.selectedIndex].value;
    }
}

class SliderController {
    constructor(element) {
        this.element = element
        this.numberInput = this.element.querySelector('input[type=number]');
        this.rangeInput = this.element.querySelector('input[type=range]');
        this.inputs = [this.numberInput, this.rangeInput];
    }

    getVal() {
        return Number(this.numberInput.value);
    }

    disable() {
        this.inputs.forEach(input => {
            input.disabled = true
        })
    }

    enable() {
        this.inputs.forEach(input => {
            input.disabled = false
        })
    }

    updateVal(value) {
        this.inputs.forEach(input => {
            input.value = Number(value)
        })
    }

    updateMin(value) {
        this.inputs.forEach(input => {
            input.min = roundToClosestMultiple(Number(value), 8);
        })
    }

    triggerEvent(event) {
        this.numberInput.dispatchEvent(event)
    }

    setVal(value) {
        value = Number(value)
        const newValue = roundToClosestMultiple(value, 8)
        this.updateVal(newValue);
    }

}

class AspectRatioController {
    constructor(page, widthContainer, heightContainer, defaultOptions) {
        this.widthContainer = new SliderController(widthContainer);
        this.heightContainer = new SliderController(heightContainer);
        this.inputs = [...this.widthContainer.inputs, ...this.heightContainer.inputs];
        this.inputs.forEach(input => {
            input.addEventListener('change', (e) => {
                e.preventDefault()
                this.maintainAspectRatio(input);
            });
        })

        this.selectController = new SelectController(page, defaultOptions, this);
        this.setAspectRatio(_OFF);
    }

    updateInputStates() {
        if (this.isLandscapeOrSquare()) {
            this.heightContainer.disable();
            this.widthContainer.enable();
            const minByAr = Math.round(_MINIMUM_DIMENSION * this.widthRatio / this.heightRatio);
            const minimum = Math.max(minByAr, _MINIMUM_DIMENSION);
            this.widthContainer.updateMin(minimum);
            this.heightContainer.updateMin(_MINIMUM_DIMENSION);
        } else {
            this.widthContainer.disable();
            this.heightContainer.enable();
            const minByAr = Math.round(_MINIMUM_DIMENSION * this.heightRatio / this.widthRatio)
            const minimum = Math.max(minByAr, _MINIMUM_DIMENSION);
            this.heightContainer.updateMin(minimum);
            this.widthContainer.updateMin(_MINIMUM_DIMENSION);
        }
    }

    disable() {
        this.widthContainer.enable();
        this.heightContainer.enable();
        this.widthContainer.updateMin(_MINIMUM_DIMENSION);
        this.heightContainer.updateMin(_MINIMUM_DIMENSION);
    }

    isLandscapeOrSquare() {
        return this.widthRatio >= this.heightRatio;
    }

    setAspectRatio(aspectRatio) {
        this.aspectRatio = aspectRatio;

        let wR, hR;
        if (aspectRatio === _OFF) {
            return this.disable();
        } else if (aspectRatio === _IMAGE) {
            const img = getCurrentImage();
            wR = img && img.naturalWidth || 1;
            hR = img && img.naturalHeight || 1;
        } else if (aspectRatio === _LOCK) {
            wR = this.widthContainer.getVal();
            hR = this.heightContainer.getVal();
        } else {
            [wR, hR] = aspectRatioFromStr(aspectRatio);
        }

        [wR, hR] = clampToBoundaries(wR, hR);

        this.widthRatio = wR;
        this.heightRatio = hR;
        this.updateInputStates();
        this.maintainAspectRatio();
    }

    maintainAspectRatio(changedElement) {
        if (this.aspectRatio === _OFF) return;
        if (!changedElement) {
            const allValues = Object.values(this.inputs).map(x => Number(x.value));
            changedElement = {value: Math.max(...allValues)};
        }

        const aspectRatio = this.widthRatio / this.heightRatio;
        let w, h;
        if (this.isLandscapeOrSquare()) {
            w = Math.round(changedElement.value);
            h = Math.round(changedElement.value / aspectRatio);
        } else {
            h = Math.round(changedElement.value);
            w = Math.round(changedElement.value * aspectRatio);
        }

        const [width, height] = clampToBoundaries(w, h)

        const inputEvent = new Event("input", { bubbles: true});
        this.widthContainer.setVal(width);
        this.widthContainer.triggerEvent(inputEvent);
        this.heightContainer.setVal(height);
        this.heightContainer.triggerEvent(inputEvent);
    }

    static observeStartup(key, page, defaultOptions, postSetup = (_) => {}) {
        let observer = new MutationObserver(() => {
            const widthContainer = gradioApp().querySelector(`#${page}_width`);
            const heightContainer = gradioApp().querySelector(`#${page}_height`);

            // wait for width and height containers to exist.
            if (widthContainer && heightContainer)  {
                observer.disconnect();
                if (!window.opts.arh_javascript_aspect_ratio_show) {
                    return;
                }

                const controller = new AspectRatioController(
                    page,
                    widthContainer,
                    heightContainer,
                    defaultOptions,
                );

                postSetup(controller);
                window[key] = controller;
            }
        });

        observer.observe(gradioApp(), {childList: true, subtree: true});
    }

}

const addImg2ImgTabSwitchClickListeners = (controller) => {
    const img2imgTabButtons = Array.from(document.querySelectorAll('#img2img_settings > div > div > button:not(.selected):not(.hasTabSwitchListener)'));
    img2imgTabButtons.forEach(button => {
        button.addEventListener('click', (_) => {
            // set aspect ratio is RECALLED to change to the image specific to the newly selected tab.
            if (controller.selectController.getCurrentOption() === _IMAGE) {
                controller.setAspectRatio(_IMAGE);
            }

            addImg2ImgTabSwitchClickListeners(controller);
        });

        button.classList.add('hasTabSwitchListener');
    });
}

const postImageControllerSetupFunction = (controller) => {
    const scaleToImg2ImgImage = (e) => {
        const picked = controller.selectController.getCurrentOption();
        if (picked !== _IMAGE) return;
        const files = e.dataTransfer ? e.dataTransfer.files : e.target.files;
        const img = new Image();
        img.src = URL.createObjectURL(files[0]);
        img.onload = () => {
            controller.setAspectRatio(`${img.naturalWidth}:${img.naturalHeight}`)
        };
    }

    _IMAGE_INPUT_CONTAINER_IDS.forEach(imageContainerId => {
        const imageContainer = document.getElementById(imageContainerId);
        const inputElement = imageContainer.querySelector('input');
        inputElement.parentElement.addEventListener('drop', scaleToImg2ImgImage);
        inputElement.addEventListener('input', scaleToImg2ImgImage);
    })

    addImg2ImgTabSwitchClickListeners(controller);
}

document.addEventListener("DOMContentLoaded", () => {
    AspectRatioController.observeStartup(
        "__txt2imgAspectRatioController",
        "txt2img",
        [_OFF, _LOCK]
    );
    AspectRatioController.observeStartup(
        "__img2imgAspectRatioController",
        "img2img",
        [_OFF, _IMAGE, _LOCK],
        postImageControllerSetupFunction
    );
});
