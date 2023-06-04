// constants
const _OFF = "Off";  // Don't use the functionality at all
const _LOCK = '🔒';  // Aspect ratio is "locked"
const _IMAGE = '🖼️'; // Aspect ratio is "locked" to that of the image

const _MAXIMUM_DIMENSION = 2048;
const _MINIMUM_DIMENSION = 64;

const _IMAGE_INPUT_CONTAINER_IDS = [
    'img2img_image',
    'img2img_sketch',
    'img2maskimg',
    'inpaint_sketch',
    'img_inpaint_base',
];

const getSelectedImage2ImageTab = () => {
    const selectedButton = gradioApp().getElementById('mode_img2img').querySelector('button.selected');
    const allButtons = gradioApp().getElementById('mode_img2img').querySelectorAll('button');
    const selectedIndex = Array.prototype.indexOf.call(allButtons, selectedButton);
    return selectedIndex;
}

const getCurrentImage = () => {
    const currentTabIndex = getSelectedImage2ImageTab();
    const currentTabImageId = _IMAGE_INPUT_CONTAINER_IDS[currentTabIndex];
    return document.getElementById(currentTabImageId).querySelector('img');
}

const roundToClosestMultiple = (num, multiple) => {
    const rounded = Math.round(Number(num) / multiple) * multiple;
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
    } else if (width < _MINIMUM_DIMENSION) {
        width = _MINIMUM_DIMENSION;
    }

    if (height < _MINIMUM_DIMENSION) {
        height = _MINIMUM_DIMENSION;
    } else if (height > _MAXIMUM_DIMENSION) {
        height = _MAXIMUM_DIMENSION;
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

class OptionPickingController {
    constructor(page, defaultOptions, controller) {
        this.page = page;
        this.options = this.getOptions(defaultOptions);
        this.switchButton = gradioApp().getElementById(page + '_res_switch_btn');

        const wrapperDiv = document.createElement('div');
        wrapperDiv.setAttribute("id", `${this.page}_size_toolbox`);
        wrapperDiv.setAttribute("class", "flex flex-col relative col gap-4");
        wrapperDiv.setAttribute("style", "min-width: min(320px, 100%); flex-grow: 0");
        wrapperDiv.innerHTML = this.getElementInnerHTML();

        const parent = this.switchButton.parentNode;
        parent.removeChild(this.switchButton);
        wrapperDiv.appendChild(this.switchButton);
        parent.insertBefore(wrapperDiv, parent.lastChild.previousElementSibling);

        this.getPickerElement().onchange = this.pickerChanged(controller);
        this.switchButton.onclick = this.switchButtonOnclick(controller);
    }

    getOptions(defaultOptions) {
        return [...new Set([...defaultOptions, ...getOptions()])];
    }

    pickerChanged(controller) {
        return () => {
            const picked = this.getCurrentOption();
            if (_IMAGE === picked) {
                // this.switchButton.disabled = true;
            } else {
                this.switchButton.removeAttribute('disabled')
            }

            controller.setAspectRatio(picked);
        };
    }

    switchButtonOnclick(controller) {
        return () => {
            reverseAllOptions();
            const picked = this.getCurrentOption();
            if (_LOCK === picked) {
                controller.setAspectRatio(`${controller.heightRatio}:${controller.widthRatio}`);
            } else {
                controller.setAspectRatio(picked);
            }
        };
    }

    getElementInnerHTML() {
        throw new Error('Not implemented');
    }

    getPickerElement() {
        throw new Error('Not implemented');
    }

    getCurrentOption() {
        throw new Error('Not implemented');
    }
}


class SelectOptionPickingController extends OptionPickingController {
    constructor(page, defaultOptions, controller) {
        super(page, defaultOptions, controller);
    }

    getElementInnerHTML() {
        return `
        <div id="${this.page}_ratio" class="gr-block gr-box relative w-full border-solid border border-gray-200 gr-padded">
            <select id="${this.page}_select_aspect_ratio" class="gr-box gr-input w-full disabled:cursor-not-allowed">
                ${this.options.map(r => {
            return '<option class="ar-option">' + r + '</option>'
        }).join('\n')}
            </select>
        </div>
        `;
    }

    getPickerElement() {
        return gradioApp().getElementById(`${this.page}_select_aspect_ratio`);
    }

    getCurrentOption() {
        const selectElement = this.getPickerElement();
        const options = Array.from(selectElement);
        return options[selectElement.selectedIndex].value;
    }
}

class DefaultOptionsButtonOptionPickingController extends OptionPickingController {
    constructor(page, defaultOptions, controller) {
        super(page, defaultOptions, controller);
        this.currentIndex = 0;
        this.getPickerElement().onclick = this.pickerChanged(controller);
    }

    pickerChanged(controller) {
        return () => {
            this.currentIndex = (this.currentIndex + 1) % this.options.length;
            this.getPickerElement().querySelector('button').textContent = this.getCurrentOption();
            super.pickerChanged(controller)();
        }
    }

    getElementInnerHTML() {
        const classes = Array.from(this.switchButton.classList);
        return `
        <div id="${this.page}_ar_default_options_button" style="margin-bottom: 10px;">
            <button class="${classes.join(' ')}">
                ${this.getCurrentOption()}
            </button>
        </div>
        `;
    }

    getPickerElement() {
        return gradioApp().getElementById(`${this.page}_ar_default_options_button`);
    }

    getOptions(defaultOptions) {
        return defaultOptions;
    }

    getCurrentOption() {
        return this.options[this.currentIndex || 0];
    }
}


class SliderController {
    constructor(element) {
        this.element = element;
        this.numberInput = this.element.querySelector('input[type=number]');
        this.rangeInput = this.element.querySelector('input[type=range]');
        this.inputs = [this.numberInput, this.rangeInput];
        this.inputs.forEach(input => {
            input.isWidth = element.isWidth;
        });
    }

    getVal() {
        return Number(this.numberInput.value);
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

    updateMax(value) {
        this.inputs.forEach(input => {
            input.max = roundToClosestMultiple(Number(value), 8);
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
        widthContainer.isWidth = true;
        heightContainer.isWidth = false;
        this.widthContainer = new SliderController(widthContainer);
        this.heightContainer = new SliderController(heightContainer);
        this.inputs = [...this.widthContainer.inputs, ...this.heightContainer.inputs];
        this.inputs.forEach(input => {
            input.addEventListener('change', (e) => {
                e.preventDefault()
                this.maintainAspectRatio(input);
            });
        })

        if (window.opts.arh_ui_javascript_selection_method === 'Default Options Button') {
            this.optionPickingControler = new DefaultOptionsButtonOptionPickingController(page, defaultOptions, this);
        } else {
            this.optionPickingControler = new SelectOptionPickingController(page, defaultOptions, this);
        }

        this.setAspectRatio(_OFF);
    }

    updateInputStates() {
        if (this.isLandscapeOrSquare()) {
            const AR = this.widthRatio / this.heightRatio;

            const minWidthByAr = Math.round(_MINIMUM_DIMENSION * AR);
            const minWidth = Math.max(minWidthByAr, _MINIMUM_DIMENSION);
            this.widthContainer.updateMin(minWidth);
            this.heightContainer.updateMin(_MINIMUM_DIMENSION);

            const maxHeightByAr = Math.round(_MAXIMUM_DIMENSION / AR)
            const maxHeight = Math.min(_MAXIMUM_DIMENSION, maxHeightByAr);
            this.heightContainer.updateMax(maxHeight);
            this.widthContainer.updateMax(_MAXIMUM_DIMENSION);
        } else {
            const AR = this.heightRatio / this.widthRatio;

            const minHeightByAr = Math.round(_MINIMUM_DIMENSION * AR)
            const minHeight = Math.max(minHeightByAr, _MINIMUM_DIMENSION);
            this.heightContainer.updateMin(minHeight);
            this.widthContainer.updateMin(_MINIMUM_DIMENSION);

            const maxWidthByAr = Math.round(_MAXIMUM_DIMENSION / AR)
            const maxWidth = Math.min(_MAXIMUM_DIMENSION, maxWidthByAr);
            this.widthContainer.updateMax(maxWidth);
            this.heightContainer.updateMax(_MAXIMUM_DIMENSION);
        }
    }

    disable() {
        this.widthContainer.updateMin(_MINIMUM_DIMENSION);
        this.heightContainer.updateMin(_MINIMUM_DIMENSION);
        this.widthContainer.updateMax(_MAXIMUM_DIMENSION);
        this.heightContainer.updateMax(_MAXIMUM_DIMENSION);
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

        if (changedElement.isWidth === undefined) {
            if (this.isLandscapeOrSquare()) {
                if (changedElement.isWidth) {}
                w = Math.round(changedElement.value);
                h = Math.round(changedElement.value / aspectRatio);
            } else {
                h = Math.round(changedElement.value);
                w = Math.round(changedElement.value * aspectRatio);
            }
        } else {
            if (changedElement.isWidth) {
                w = Math.round(changedElement.value);
                h = Math.round(changedElement.value / aspectRatio);
            } else {
                h = Math.round(changedElement.value);
                w = Math.round(changedElement.value * aspectRatio);
            }
        }

        const [width, height] = clampToBoundaries(w, h)

        const inputEvent = new Event("input", {bubbles: true});
        this.widthContainer.setVal(width);
        this.widthContainer.triggerEvent(inputEvent);
        this.heightContainer.setVal(height);
        this.heightContainer.triggerEvent(inputEvent);
        this.heightContainer.inputs.forEach(input => {
            dimensionChange({target: input}, false, true);
        });
        this.widthContainer.inputs.forEach(input => {
            dimensionChange({target: input}, true, false);
        });
    }

    static observeStartup(key, page, defaultOptions, postSetup = (_) => {
    }) {
        let observer = new MutationObserver(() => {
            const widthContainer = gradioApp().querySelector(`#${page}_width`);
            const heightContainer = gradioApp().querySelector(`#${page}_height`);

            // wait for width and height containers to exist.
            if (widthContainer && heightContainer && window.opts && window.opts.arh_javascript_aspect_ratio_show !== undefined) {
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
            if (controller.optionPickingControler.getCurrentOption() === _IMAGE) {
                controller.setAspectRatio(_IMAGE);
            }

            addImg2ImgTabSwitchClickListeners(controller);
        });

        button.classList.add('hasTabSwitchListener');
    });
}

const postImageControllerSetupFunction = (controller) => {
    const scaleToImg2ImgImage = (e) => {
        const picked = controller.optionPickingControler.getCurrentOption();
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
        inputElement.addEventListener('change', scaleToImg2ImgImage);
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
        [_OFF, _LOCK, _IMAGE],
        postImageControllerSetupFunction
    );
});
