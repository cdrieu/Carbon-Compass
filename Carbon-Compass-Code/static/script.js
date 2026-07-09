document.addEventListener("DOMContentLoaded", function () {
    const steps = Array.from(document.querySelectorAll(".quiz-step"));
    const progressFill = document.getElementById("progressFill");
    const stepText = document.getElementById("stepText");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const submitBtn = document.getElementById("submitBtn");

    const vehicleCheckboxes = Array.from(document.querySelectorAll('input[name="vehicle_types"]'));
    const vehicleQuestions = document.getElementById("vehicle-questions");
    const dietSelect = document.getElementById("dietSelect");
    const beefQuestion = document.getElementById("beef-lamb-question");

    let currentStep = 0;

    function wireSlider(sliderId, valueId, hiddenId, suffix) {
        const slider = document.getElementById(sliderId);
        const valueDisplay = document.getElementById(valueId);
        const hiddenInput = document.getElementById(hiddenId);

        if (!slider || !valueDisplay || !hiddenInput) return;

        function updateSlider() {
            valueDisplay.textContent = slider.value + " " + suffix;
            hiddenInput.value = slider.value;
        }

        slider.addEventListener("input", updateSlider);
        updateSlider();
    }

    function updateStepUI() {
        steps.forEach((step, index) => {
            step.classList.toggle("active", index === currentStep);
        });

        progressFill.style.width = ((currentStep + 1) / steps.length * 100) + "%";
        stepText.textContent = "Step " + (currentStep + 1) + " of " + steps.length;

        prevBtn.style.display = currentStep === 0 ? "none" : "inline-block";
        nextBtn.style.display = currentStep === steps.length - 1 ? "none" : "inline-block";
        submitBtn.style.display = currentStep === steps.length - 1 ? "inline-block" : "none";
    }

    function toggleVehicleQuestions() {
        const noneBox = vehicleCheckboxes.find(box => box.value === "None");
        const selectedVehicles = vehicleCheckboxes.filter(box => box.checked && box.value !== "None");

        if (noneBox && noneBox.checked && selectedVehicles.length > 0) {
            noneBox.checked = false;
        }

        vehicleQuestions.classList.toggle("hidden", selectedVehicles.length === 0);
    }

    function toggleBeefQuestion() {
        const show = dietSelect.value === "Omnivore" || dietSelect.value === "Heavy meat-eater";
        beefQuestion.classList.toggle("hidden", !show);
    }

    nextBtn.addEventListener("click", function () {
        if (currentStep < steps.length - 1) {
            currentStep++;
            updateStepUI();
        }
    });

    prevBtn.addEventListener("click", function () {
        if (currentStep > 0) {
            currentStep--;
            updateStepUI();
        }
    });

    vehicleCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            const noneBox = vehicleCheckboxes.find(box => box.value === "None");

            if (checkbox.value === "None" && checkbox.checked) {
                vehicleCheckboxes.forEach(box => {
                    if (box.value !== "None") box.checked = false;
                });
            }

            if (checkbox.value !== "None" && checkbox.checked && noneBox) {
                noneBox.checked = false;
            }

            toggleVehicleQuestions();
        });
    });

    dietSelect.addEventListener("change", toggleBeefQuestion);

    wireSlider("weeklyVehicleDistanceSlider", "weeklyVehicleDistanceValue", "weeklyVehicleDistance", "km");
    wireSlider("commuteLengthSlider", "commuteLengthValue", "commuteLength", "km");
    wireSlider("commuteFrequencySlider", "commuteFrequencyValue", "commuteFrequency", "days/week");
    wireSlider("streamingSlider", "streamingValue", "streamingHours", "hours/day");
    wireSlider("videoCallSlider", "videoCallValue", "videoCallHours", "hours/week");

    updateStepUI();
    toggleVehicleQuestions();
    toggleBeefQuestion();
});