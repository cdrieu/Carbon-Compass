document.addEventListener("DOMContentLoaded", function () {
    initializeFootprintChart();
    initializeRecommendationCarousel();
});


function initializeFootprintChart() {
    const canvas = document.getElementById("footprintChart");
    const chartData = window.footprintChartData;

    if (!canvas || !chartData || typeof Chart === "undefined") {
        return;
    }

    const total = chartData.values.reduce(function (sum, value) {
        return sum + Number(value);
    }, 0);

    new Chart(canvas, {
        type: "doughnut",

        data: {
            labels: chartData.labels,

            datasets: [
                {
                    data: chartData.values,

                    backgroundColor: [
                        "#C0CAAD", // Housing — sage
                        "#B26E63", // Transportation — terracotta
                        "#CEC075", // Food — golden sand
                        "#9DA9A0", // Waste — ash grey
                        "#BAD7F2", // Digital — pale blue
                        "#F2BAC9"  // Shopping — soft pink
                    ],

                    borderColor: "#FAF7EF",
                    borderWidth: 4,

                    hoverBorderColor: "#FAF7EF",
                    hoverBorderWidth: 4,
                    hoverOffset: 8
                }
            ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            devicePixelRatio: Math.min(window.devicePixelRatio || 1, 2),
            resizeDelay: 150,
            cutout: "56%",
            animation: {
                duration: 850,
                easing: "easeOutQuart"
    },

            plugins: {
                legend: {
                    display: false
                },

                tooltip: {
                    displayColors: true,

                    backgroundColor: "#654C4F",
                    titleColor: "#FFFFFF",
                    bodyColor: "#FFFFFF",

                    padding: 12,
                    cornerRadius: 10,

                    callbacks: {
                        label: function (context) {
                            const value = Number(context.raw);

                            const percentage =
                                total > 0
                                    ? (value / total) * 100
                                    : 0;

                            return (
                                context.label +
                                ": " +
                                percentage.toFixed(1) +
                                "%"
                            );
                        },

                        afterLabel: function (context) {
                            const tonnes =
                                Number(context.raw) / 1000;

                            return (
                                tonnes.toFixed(2) +
                                " tonnes CO₂e/year"
                            );
                        }
                    }
                }
            }
        }
    });
}


function initializeRecommendationCarousel() {
    const carousel = document.getElementById(
        "recommendationCarousel"
    );

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

        currentSlide =
            (index + slides.length) % slides.length;

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
        previousButton.addEventListener(
            "click",
            function () {
                showSlide(currentSlide - 1);
            }
        );
    }


    if (nextButton) {
        nextButton.addEventListener(
            "click",
            function () {
                showSlide(currentSlide + 1);
            }
        );
    }


    dots.forEach(function (dot, dotIndex) {
        dot.addEventListener("click", function () {
            showSlide(dotIndex);
        });
    });


    document.addEventListener("keydown", function (event) {
        if (event.key === "ArrowLeft") {
            showSlide(currentSlide - 1);
        }

        if (event.key === "ArrowRight") {
            showSlide(currentSlide + 1);
        }
    });


    showSlide(0);
}