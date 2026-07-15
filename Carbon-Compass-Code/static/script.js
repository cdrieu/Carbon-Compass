document.addEventListener("DOMContentLoaded", function () {
    initializeQuiz();
    initializeRecommendationCarousel();
});


function initializeQuiz() {
    const form = document.getElementById("carbonForm");

    if (!form) {
        return;
    }

    const steps = Array.from(document.querySelectorAll(".quiz-step"));
    const progressFill = document.getElementById("progressFill");
    const stepText = document.getElementById("stepText");

    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const submitBtn = document.getElementById("submitBtn");

    const vehicleCheckboxes = Array.from(
        document.querySelectorAll('input[name="vehicle_types"]')
    );

    const vehicleQuestions = document.getElementById("vehicle-questions");

    const dietSelect = document.getElementById("dietSelect");
    const beefQuestion = document.getElementById("beef-lamb-question");

    const distanceUnit = document.getElementById("distanceUnit");

    const weeklyDistanceSlider = document.getElementById(
        "weeklyVehicleDistanceSlider"
    );

    const weeklyDistanceValue = document.getElementById(
        "weeklyVehicleDistanceValue"
    );

    const weeklyDistanceHidden = document.getElementById(
        "weeklyVehicleDistance"
    );

    const weeklyDistanceLabel = document.getElementById(
        "weeklyVehicleDistanceLabel"
    );

    const commuteLengthSlider = document.getElementById(
        "commuteLengthSlider"
    );

    const commuteLengthValue = document.getElementById(
        "commuteLengthValue"
    );

    const commuteLengthHidden = document.getElementById(
        "commuteLength"
    );

    const commuteLengthLabel = document.getElementById(
        "commuteLengthLabel"
    );

    let currentStep = 0;


    function updateStepUI() {
        steps.forEach(function (step, index) {
            step.classList.toggle("active", index === currentStep);
        });

        if (progressFill && steps.length > 0) {
            const progress = ((currentStep + 1) / steps.length) * 100;
            progressFill.style.width = progress + "%";
        }

        if (stepText) {
            stepText.textContent =
                "Step " + (currentStep + 1) + " of " + steps.length;
        }

        if (prevBtn) {
            prevBtn.style.display =
                currentStep === 0 ? "none" : "inline-flex";
        }

        if (nextBtn) {
            nextBtn.style.display =
                currentStep === steps.length - 1
                    ? "none"
                    : "inline-flex";
        }

        if (submitBtn) {
            submitBtn.style.display =
                currentStep === steps.length - 1
                    ? "inline-flex"
                    : "none";
        }

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }


    function validateCurrentStep() {
        const activeStep = steps[currentStep];

        if (!activeStep) {
            return true;
        }

        const requiredFields = Array.from(
            activeStep.querySelectorAll("[required]")
        );

        for (const field of requiredFields) {
            if (!field.checkValidity()) {
                field.reportValidity();
                return false;
            }
        }

        return true;
    }


    function toggleVehicleQuestions() {
        if (!vehicleQuestions) {
            return;
        }

        const noneCheckbox = vehicleCheckboxes.find(function (checkbox) {
            return checkbox.value === "None";
        });

        const chosenVehicles = vehicleCheckboxes.filter(function (checkbox) {
            return checkbox.checked && checkbox.value !== "None";
        });

        vehicleQuestions.classList.toggle(
            "hidden",
            chosenVehicles.length === 0
        );

        if (
            noneCheckbox &&
            noneCheckbox.checked &&
            chosenVehicles.length > 0
        ) {
            noneCheckbox.checked = false;
        }
    }


    function toggleBeefQuestion() {
        if (!dietSelect || !beefQuestion) {
            return;
        }

        const shouldShow =
            dietSelect.value === "Omnivore" ||
            dietSelect.value === "Heavy meat-eater";

        beefQuestion.classList.toggle("hidden", !shouldShow);
    }


    function updateDistanceUnit() {
        if (
            !distanceUnit ||
            !weeklyDistanceSlider ||
            !commuteLengthSlider
        ) {
            return;
        }

        const unit = distanceUnit.value;

        if (unit === "Miles") {
            weeklyDistanceSlider.max = "620";
            weeklyDistanceSlider.step = "5";

            commuteLengthSlider.max = "60";
            commuteLengthSlider.step = "1";

            if (weeklyDistanceLabel) {
                weeklyDistanceLabel.textContent =
                    "Approximately how many miles do you drive each week?";
            }

            if (commuteLengthLabel) {
                commuteLengthLabel.textContent =
                    "Approximately how many miles is your one-way commute?";
            }
        } else {
            weeklyDistanceSlider.max = "1000";
            weeklyDistanceSlider.step = "10";

            commuteLengthSlider.max = "100";
            commuteLengthSlider.step = "1";

            if (weeklyDistanceLabel) {
                weeklyDistanceLabel.textContent =
                    "Approximately how many kilometers do you drive each week?";
            }

            if (commuteLengthLabel) {
                commuteLengthLabel.textContent =
                    "Approximately how many kilometers is your one-way commute?";
            }
        }

        updateDistanceSliderValues();
    }


    function updateDistanceSliderValues() {
        if (
            weeklyDistanceSlider &&
            weeklyDistanceValue &&
            weeklyDistanceHidden
        ) {
            weeklyDistanceValue.textContent =
                weeklyDistanceSlider.value;

            weeklyDistanceHidden.value =
                weeklyDistanceSlider.value;
        }

        if (
            commuteLengthSlider &&
            commuteLengthValue &&
            commuteLengthHidden
        ) {
            commuteLengthValue.textContent =
                commuteLengthSlider.value;

            commuteLengthHidden.value =
                commuteLengthSlider.value;
        }
    }


    function wireSlider(sliderId, displayId, hiddenId) {
        const slider = document.getElementById(sliderId);
        const display = document.getElementById(displayId);
        const hidden = document.getElementById(hiddenId);

        if (!slider || !display || !hidden) {
            return;
        }

        function updateValue() {
            display.textContent = slider.value;
            hidden.value = slider.value;
        }

        slider.addEventListener("input", updateValue);
        updateValue();
    }


    if (nextBtn) {
        nextBtn.addEventListener("click", function () {
            if (!validateCurrentStep()) {
                return;
            }

            if (currentStep < steps.length - 1) {
                currentStep += 1;
                updateStepUI();
            }
        });
    }


    if (prevBtn) {
        prevBtn.addEventListener("click", function () {
            if (currentStep > 0) {
                currentStep -= 1;
                updateStepUI();
            }
        });
    }


    form.addEventListener("submit", function (event) {
        if (!validateCurrentStep()) {
            event.preventDefault();
        }
    });


    vehicleCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            const noneCheckbox = vehicleCheckboxes.find(function (item) {
                return item.value === "None";
            });

            if (checkbox.value === "None" && checkbox.checked) {
                vehicleCheckboxes.forEach(function (item) {
                    if (item.value !== "None") {
                        item.checked = false;
                    }
                });
            }

            if (
                checkbox.value !== "None" &&
                checkbox.checked &&
                noneCheckbox
            ) {
                noneCheckbox.checked = false;
            }

            toggleVehicleQuestions();
        });
    });


    if (dietSelect) {
        dietSelect.addEventListener("change", toggleBeefQuestion);
    }


    if (distanceUnit) {
        distanceUnit.addEventListener("change", updateDistanceUnit);
    }


    if (weeklyDistanceSlider) {
        weeklyDistanceSlider.addEventListener(
            "input",
            updateDistanceSliderValues
        );
    }


    if (commuteLengthSlider) {
        commuteLengthSlider.addEventListener(
            "input",
            updateDistanceSliderValues
        );
    }


    wireSlider(
        "commuteFrequencySlider",
        "commuteFrequencyValue",
        "commuteFrequency"
    );

    wireSlider(
        "streamingSlider",
        "streamingValue",
        "streamingHours"
    );

    wireSlider(
        "videoCallSlider",
        "videoCallValue",
        "videoCallHours"
    );


    toggleVehicleQuestions();
    toggleBeefQuestion();
    updateDistanceSliderValues();
    updateStepUI();
}


function initializeRecommendationCarousel() {
    const carousel = document.getElementById("recommendationCarousel");

    if (!carousel) {
        return;
    }

    const slides = Array.from(
        carousel.querySelectorAll(".recommendation-slide")
    );

    const previousButton = document.getElementById(
        "previousRecommendation"
    );

    const nextButton = document.getElementById(
        "nextRecommendation"
    );

    const dots = Array.from(
        document.querySelectorAll(".recommendation-dot")
    );

    let currentSlide = 0;


    function showSlide(index) {
        if (slides.length === 0) {
            return;
        }

        currentSlide = (index + slides.length) % slides.length;

        slides.forEach(function (slide, slideIndex) {
            slide.classList.toggle(
                "active",
                slideIndex === currentSlide
            );
        });

        dots.forEach(function (dot, dotIndex) {
            dot.classList.toggle(
                "active",
                dotIndex === currentSlide
            );
        });
    }


    if (previousButton) {
        previousButton.addEventListener("click", function () {
            showSlide(currentSlide - 1);
        });
    }


    if (nextButton) {
        nextButton.addEventListener("click", function () {
            showSlide(currentSlide + 1);
        });
    }


    dots.forEach(function (dot, index) {
        dot.addEventListener("click", function () {
            showSlide(index);
        });
    });


    showSlide(0);
}