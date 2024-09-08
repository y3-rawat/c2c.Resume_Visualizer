
var maxParticleCount = 150; //set max confetti count
var particleSpeed = 2; //set the particle animation speed
var startConfetti; //call to start confetti animation
var stopConfetti; //call to stop adding confetti
var toggleConfetti; //call to start or stop the confetti animation depending on whether it's already running
var removeConfetti; //call to stop the confetti animation and remove all confetti immediately

(function () {
    startConfetti = startConfettiInner;
    stopConfetti = stopConfettiInner;
    toggleConfetti = toggleConfettiInner;
    removeConfetti = removeConfettiInner;
    var colors = ["DodgerBlue", "OliveDrab", "Gold", "Pink", "SlateBlue", "LightBlue", "Violet", "PaleGreen", "SteelBlue", "SandyBrown", "Chocolate", "Crimson"];
    var streamingConfetti = false;
    var animationTimer = null;
    var particles = [];
    var waveAngle = 0;

    function resetParticle(particle, width, height) {
        particle.color = colors[(Math.random() * colors.length) | 0];
        particle.x = Math.random() * width;
        particle.y = Math.random() * height - height;
        particle.diameter = Math.random() * 10 + 5;
        particle.tilt = Math.random() * 10 - 10;
        particle.tiltAngleIncrement = Math.random() * 0.07 + 0.05;
        particle.tiltAngle = 0;
        return particle;
    }

    function startConfettiInner() {
        var width = window.innerWidth;
        var height = window.innerHeight;
        window.requestAnimFrame = (function () {
            return window.requestAnimationFrame ||
                window.webkitRequestAnimationFrame ||
                window.mozRequestAnimationFrame ||
                window.oRequestAnimationFrame ||
                window.msRequestAnimationFrame ||
                function (callback) {
                    return window.setTimeout(callback, 16.6666667);
                };
        })();
        var canvas = document.getElementById("confetti-canvas");
        if (canvas === null) {
            canvas = document.createElement("canvas");
            canvas.setAttribute("id", "confetti-canvas");
            document.body.appendChild(canvas);
            canvas.width = width;
            canvas.height = height;
            window.addEventListener("resize", function () {
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
            }, true);
        }
        var context = canvas.getContext("2d");
        while (particles.length < maxParticleCount)
            particles.push(resetParticle({}, width, height));
        streamingConfetti = true;
        if (animationTimer === null) {
            (function runAnimation() {
                context.clearRect(0, 0, window.innerWidth, window.innerHeight);
                if (particles.length === 0)
                    animationTimer = null;
                else {
                    updateParticles();
                    drawParticles(context);
                    animationTimer = requestAnimFrame(runAnimation);
                }
            })();
        }
        // Show the canvas
        canvas.style.display = 'block';
    }

    function stopConfettiInner() {
        streamingConfetti = false;
        // Hide the canvas
        var canvas = document.getElementById("confetti-canvas");
        if (canvas) {
            canvas.style.display = 'none';
        }
    }

    function removeConfettiInner() {
        stopConfetti();
        particles = [];
    }

    function toggleConfettiInner() {
        if (streamingConfetti)
            stopConfettiInner();
        else
            startConfettiInner();
    }

    function drawParticles(context) {
        var particle;
        var x;
        for (var i = 0; i < particles.length; i++) {
            particle = particles[i];
            context.beginPath();
            context.lineWidth = particle.diameter;
            context.strokeStyle = particle.color;
            x = particle.x + particle.tilt;
            context.moveTo(x + particle.diameter / 2, particle.y);
            context.lineTo(x, particle.y + particle.tilt + particle.diameter / 2);
            context.stroke();
        }
    }

    function updateParticles() {
        var width = window.innerWidth;
        var height = window.innerHeight;
        var particle;
        waveAngle += 0.01;
        for (var i = 0; i < particles.length; i++) {
            particle = particles[i];
            if (!streamingConfetti && particle.y < -15)
                particle.y = height + 100;
            else {
                particle.tiltAngle += particle.tiltAngleIncrement;
                particle.x += Math.sin(waveAngle);
                particle.y += (Math.cos(waveAngle) + particle.diameter + particleSpeed) * 0.5;
                particle.tilt = Math.sin(particle.tiltAngle) * 15;
            }
            if (particle.x > width + 20 || particle.x < -20 || particle.y > height) {
                if (streamingConfetti && particles.length <= maxParticleCount)
                    resetParticle(particle, width, height);
                else {
                    particles.splice(i, 1);
                    i--;
                }
            }
        }
    }
})();

// Start confetti animation
startConfetti();

// Stop confetti animation after 4 seconds
setTimeout(stopConfetti, 4000);

let data;

document.addEventListener('DOMContentLoaded', function() {
    const safeDecodeURIComponent = (str) => {
        if (!str) return '';
        try {
            return decodeURIComponent(str.replace(/\+/g, ' '));
        } catch (e) {
            console.error("Error decoding:", str, e);
            return str;
        }
    };

    const urlParams = new URLSearchParams(window.location.search);
    const success = urlParams.get('success') === 'true';

    if (success) {
        try {
            const apiResponseStr = safeDecodeURIComponent(urlParams.get('apiResponse'));
            data = JSON.parse(apiResponseStr);
            initDashboard(data);
        } catch (error) {
            console.error("Error processing success response:", error);
        }
    } else {
        const errorMessage = safeDecodeURIComponent(urlParams.get('errorMessage'));
        displayError(errorMessage || "An unknown error occurred.");
    }
});

function displayError(message) {
    // Create an error message element if it doesn't exist
    let errorElement = document.getElementById('errorMessage');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.id = 'errorMessage';
        errorElement.className = 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative';
        document.body.insertBefore(errorElement, document.body.firstChild);
    }

    errorElement.textContent = message;

    // Show retry link
    const retryLink = document.getElementById('retryLink');
    if (retryLink) {
        retryLink.style.display = 'block';
    }
}

function initDashboard(data) {
    createExperienceRelevanceChart(data);
    initRecommendations(data.recommendations);
    initActionableRecommendations(data["Actionable Recommendations"]);
    initSkillsAnalysis(data);
    createProjectImpactChart(data);
    createCourseImpactChart(data);
    initStrengthsWeaknesses(data);
    initCourseSuggestions(data);
    initRecommendedPeople(data.recommended_People_linkdin, 'recommendedPeopleLinkedInList');
    initRecommendedPeople(data.recommendedPeople_instagram, 'recommendedPeopleInstagramList');
    initRecommendedPeople(data.recommendedPeople_twitter, 'recommendedPeopleTwitterList');
}

function createExperienceRelevanceChart(data) {
    const projectContainer = document.getElementById('experienceRelevanceChart');
    const experience_registence = data.experience_relevance.imp;

    function getColor(score) {
        if (score < 40) {
            const factor = score / 40;
            return `rgb(255, ${Math.round(65 + 155 * factor)}, ${Math.round(54 + 166 * factor)})`;
        } else if (score < 70) {
            const factor = (score - 40) / 30;
            return `rgb(${Math.round(255 - 209 * factor) + 40}, ${Math.round(220 - 16 * factor) - 26}, ${Math.round(0 + 64 * factor) - 18})`;
        } else {
            const factor = (score - 70) / 30;
            return `rgb(${Math.round(46 - 46 * factor) + 28}, ${Math.round(204 - 51 * factor) - 26}, ${Math.round(64 + 191 * factor) - 216})`;
        }
    }

    Object.entries(experience_registence).forEach(([proj, score]) => {
        const projectElement = document.createElement('div');
        projectElement.className = 'mb-4';
        projectElement.innerHTML = `
    <div class="flex items-center justify-between mb-1">
        <span class="text-sm font-medium text-gray-700">${proj}</span>
        <span class="text-sm font-medium text-gray-700">${score}%</span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-2.5">
        <div class="h-2.5 rounded-full transition-all duration-500 ease-out" style="width: 0%; background-color: ${getColor(score)}"></div>
    </div>
`;
        projectContainer.appendChild(projectElement);

        // Animate the proj bar
        setTimeout(() => {
            const progressBar = projectElement.querySelector('.rounded-full div');
            progressBar.style.width = `${score}%`;
        }, 100);
    });
    document.getElementById('Expre').textContent = data.experience_relevance.advice;
}

function initRecommendedPeople(recommendedPeople, listId) {
    const recommendedPeopleList = document.getElementById(listId);

    if (!recommendedPeopleList) {
        console.error(`Element with id ${listId} not found`);
        return;
    }

    recommendedPeopleList.innerHTML = ''; // Clear the list before adding new items

    if (!Array.isArray(recommendedPeople)) {
        console.error(`recommendedPeople is not an array for ${listId}`);
        return;
    }

    recommendedPeople.forEach(person => {
        const li = document.createElement('li');
        li.innerHTML = `
            <a href="${person.link}" target="_blank">
                ${person.name} - ${person.title}
            </a>
        `;
        recommendedPeopleList.appendChild(li);
    });
}

function updateScore(id, data) {
    const scoreElement = document.getElementById(`${id}Score`);
    const progressCircle = document.getElementById(`${id}ProgressCircle`);
    const descriptionElement = document.getElementById(`${id}Description`);
    const reasonElement = document.getElementById(`${id}Reason`);
    const improvementTipElement = document.getElementById(`${id}ImprovementTip`);

    if (!scoreElement || !progressCircle || !descriptionElement || !reasonElement || !improvementTipElement) {
        console.error(`Missing elements for ${id}`);
        return;
    }

    const targetScore = data.score;
    const circumference = 2 * Math.PI * 54;

    progressCircle.style.strokeDasharray = circumference;
    progressCircle.style.strokeDashoffset = circumference;

    let currentScore = 0;
    const duration = 2000; // 2 seconds
    const startTime = performance.now();

    function getColor(score) {
        if (score < 40) return [255, 65, 54]; // Red
        if (score < 70) return [255, 220, 0]; // Yellow
        return [46, 204, 64]; // Green
    }

    function interpolateColor(color1, color2, factor) {
        return color1.map((channel, index) =>
            Math.round(channel + factor * (color2[index] - channel))
        );
    }

    function easeOutQuad(t) {
        return t * (2 - t);
    }

    function animateScore(currentTime) {
        const elapsedTime = currentTime - startTime;
        if (elapsedTime < duration) {
            const progress = easeOutQuad(elapsedTime / duration);
            currentScore = Math.min(Math.floor(progress * targetScore), targetScore);
            scoreElement.textContent = currentScore + '%';

            const fillPercentage = currentScore / 100;
            const dashoffset = circumference * (1 - fillPercentage);
            progressCircle.style.strokeDashoffset = dashoffset;

            const startColor = getColor(Math.max(0, currentScore - 1));
            const endColor = getColor(currentScore);
            const interpolatedColor = interpolateColor(startColor, endColor, (elapsedTime % (duration / targetScore)) / (duration / targetScore));
            progressCircle.style.stroke = `rgb(${interpolatedColor.join(',')})`;

            requestAnimationFrame(animateScore);
        } else {
            scoreElement.textContent = targetScore + '%';
        }
    }

    requestAnimationFrame(animateScore);

    descriptionElement.textContent = data.description;
    reasonElement.textContent = data.reason;
    improvementTipElement.textContent = data.improvementTip;
}

function initActionableRecommendations(recommendations) {
    const recommendationsList = document.getElementById('actionableRecommendationsList');
    recommendationsList.innerHTML = ''; // Clear existing items

    recommendations.forEach((recommendation, index) => {
        const li = document.createElement('li');
        li.className = 'bg-white rounded-lg shadow-md p-4 transition duration-300 ease-in-out transform hover:scale-105';
        li.innerHTML = `
            <div class="flex items-center">
                <span class="text-blue-500 font-bold mr-3">${index + 1}.</span>
                <p class="text-gray-700">${recommendation}</p>
            </div>
        `;
        recommendationsList.appendChild(li);
    });
}

function initSkillsAnalysis(data) {
    const skillsContainer = document.getElementById('skillsAnalysis');
    const showMoreContainer = document.getElementById('showMoreContainer');
    const showMoreBtn = showMoreContainer.querySelector('.show-more-btn');
    let isExpanded = false;

    const skills = data.skill_Score.skills_ratio;
    const skillEntries = Object.entries(skills);

    function getColor(score) {
        if (score < 40) {
            const factor = score / 40;
            return `rgb(255, ${Math.round(65 + 155 * factor)}, ${Math.round(54 + 166 * factor)})`;
        } else if (score < 70) {
            const factor = (score - 40) / 30;
            return `rgb(${Math.round(255 - 209 * factor) + 40}, ${Math.round(220 - 16 * factor) - 26}, ${Math.round(0 + 64 * factor) - 18})`;
        } else {
            const factor = (score - 70) / 30;
            return `rgb(${Math.round(46 - 46 * factor) + 28}, ${Math.round(204 - 51 * factor) - 26}, ${Math.round(64 + 191 * factor) - 216})`;
        }
    }

    function renderSkills() {
        skillsContainer.innerHTML = '';
        const visibleSkills = isExpanded ? skillEntries : skillEntries.slice(0, 4);

        visibleSkills.forEach(([skill, score]) => {
            const skillElement = document.createElement('div');
            skillElement.className = 'mb-4';
            skillElement.innerHTML = `
                <div class="flex items-center justify-between mb-1">
                    <span class="text-sm font-medium text-gray-700">${skill}</span>
                    <span class="text-sm font-medium text-gray-700">${score}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                    <div class="skill-bar h-2.5 rounded-full" style="width: 0%; background-color: ${getColor(score)}"></div>
                </div>
            `;
            skillsContainer.appendChild(skillElement);

            setTimeout(() => {
                const progressBar = skillElement.querySelector('.skill-bar');
                progressBar.style.width = `${score}%`;
            }, 100);
        });

        showMoreContainer.classList.toggle('hidden', skillEntries.length <= 4);
        showMoreBtn.textContent = isExpanded ? 'Show Less' : 'Show More';
    }

    showMoreBtn.addEventListener('click', () => {
        isExpanded = !isExpanded;
        renderSkills();
    });

    renderSkills();
    document.getElementById('skillsAdvice').textContent = data.skill_Score.advice;
}

function createProjectImpactChart(data) {
    const projectContainer = document.getElementById('projectAnalysis');
    const pjt = data.project_impact.impact;

    function getColor(score) {
        if (score < 40) {
            const factor = score / 40;
            return `rgb(255, ${Math.round(65 + 155 * factor)}, ${Math.round(54 + 166 * factor)})`;
        } else if (score < 70) {
            const factor = (score - 40) / 30;
            return `rgb(${Math.round(255 - 209 * factor) + 40}, ${Math.round(220 - 16 * factor) - 26}, ${Math.round(0 + 64 * factor) - 18})`;
        } else {
            const factor = (score - 70) / 30;
            return `rgb(${Math.round(46 - 46 * factor) + 28}, ${Math.round(204 - 51 * factor) - 26}, ${Math.round(64 + 191 * factor) - 216})`;
        }
    }

    Object.entries(pjt).forEach(([proj, score]) => {
        const projectElement = document.createElement('div');
        projectElement.className = 'mb-4';
        projectElement.innerHTML = `
    <div class="flex items-center justify-between mb-1">
        <span class="text-sm font-medium text-gray-700">${proj}</span>
        <span class="text-sm font-medium text-gray-700">${score}%</span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-2.5">
        <div class="h-2.5 rounded-full transition-all duration-500 ease-out" style="width: 0%; background-color: ${getColor(score)}"></div>
    </div>
`;
        projectContainer.appendChild(projectElement);

        // Animate the proj bar
        setTimeout(() => {
            const progressBar = projectElement.querySelector('.rounded-full div');
            progressBar.style.width = `${score}%`;
        }, 100);
    });

    document.getElementById('projectImpactAdvice').textContent = data.project_impact.advice;

    const suggestionsContainer = document.getElementById('projectSuggestions');
    const suggestions = [
        data.project_impact.suggestion1,
        data.project_impact.suggestion2,
        data.project_impact.suggestion3,
    ];

    suggestions.forEach((suggestion, index) => {
        const li = document.createElement('li');
        li.className = 'bg-blue-50 p-3 rounded-lg shadow-sm';
        li.innerHTML = `                    
            <p class="mt-1 text-sm text-gray-700">${suggestion}</p>
        `;
        suggestionsContainer.appendChild(li);
    });
}

function createCourseImpactChart(data) {
    const projectContainer = document.getElementById('courseImpact_Chart');
    const course_imt = data.course_impact.course_impact.impt;

    function getColor(score) {
        if (score < 40) {
            const factor = score / 40;
            return `rgb(255, ${Math.round(65 + 155 * factor)}, ${Math.round(54 + 166 * factor)})`;
        } else if (score < 70) {
            const factor = (score - 40) / 30;
            return `rgb(${Math.round(255 - 209 * factor) + 40}, ${Math.round(220 - 16 * factor) - 26}, ${Math.round(0 + 64 * factor) - 18})`;
        } else {
            const factor = (score - 70) / 30;
            return `rgb(${Math.round(46 - 46 * factor) + 28}, ${Math.round(204 - 51 * factor) - 26}, ${Math.round(64 + 191 * factor) - 216})`;
        }
    }

    Object.entries(course_imt).forEach(([proj, score]) => {
        const course_element = document.createElement('div');
        course_element.className = 'mb-4';
        course_element.innerHTML = `
    <div class="flex items-center justify-between mb-1">
        <span class="text-sm font-medium text-gray-700">${proj}</span>
        <span class="text-sm font-medium text-gray-700">${score}%</span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-2.5">
        <div class="h-2.5 rounded-full transition-all duration-500 ease-out" style="width: 0%; background-color: ${getColor(score)}"></div>
    </div>
`;
        projectContainer.appendChild(course_element);

        // Animate the proj bar
        setTimeout(() => {
            const progressBar = course_element.querySelector('.rounded-full div');
            progressBar.style.width = `${score}%`;
        }, 100);
    });

    document.getElementById('courseAdvice').textContent = data.course_impact.course_advice;
}

function initStrengthsWeaknesses(data) {
    const strengthsList = document.getElementById('strengthsList');
    const weaknessesList = document.getElementById('weaknessesList');

    // Populate strengths
    Object.entries(data.Strengths).forEach(([key, value]) => {
        const strengthItem = document.createElement('div');
        strengthItem.className = 'strength-item';
        strengthItem.innerHTML = `<strong>${key}:</strong> ${value}`;
        strengthsList.appendChild(strengthItem);
    });

    // Populate weaknesses
    Object.entries(data.Weaknesses).forEach(([key, value]) => {
        const weaknessItem = document.createElement('div');
        weaknessItem.className = 'weakness-item';
        weaknessItem.innerHTML = `<strong>${key}:</strong> ${value}`;
        weaknessesList.appendChild(weaknessItem);
    });
}

function initCourseSuggestions(data) {
    const suggestionsList = document.getElementById('courseSuggestionsList');
    suggestionsList.innerHTML = ''; // Clear existing items

    const suggestions = [
        { title: "Course Suggestion 1", content: data.course_impact.suggestion1 },
        { title: "Course Suggestion 2", content: data.course_impact.suggestion2 },
        { title: "Course Suggestion 3", content: data.course_impact.suggestion3 }
    ];

    suggestions.forEach((suggestion, index) => {
        const li = document.createElement('li');
        li.className = 'suggestion-item';
        li.innerHTML = `
            <p class="mt-1 text-sm text-gray-700">${suggestion.content}</p>
        `;
        suggestionsList.appendChild(li);
    });
}

function initRecommendations(recommendations) {
    const recommendationsList = document.getElementById('recommendationsList');
    recommendationsList.innerHTML = ''; // Clear existing items

    recommendations.forEach((recommendation, index) => {
        const li = document.createElement('li');
        li.className = 'recommendation-item opacity-0 transform translate-y-4 transition-all duration-500 ease-out';
        li.textContent = recommendation;
        recommendationsList.appendChild(li);

        setTimeout(() => {
            li.classList.remove('opacity-0', 'translate-y-4');
        }, index * 200);
    });
}

function initPrintFunction() {
    document.getElementById('printButton').addEventListener('click', () => {
        window.print();
    });
}

function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
}

document.getElementById('printButton').addEventListener('click', function () {
    // Options for the PDF
    var opt = {
        margin: 0, // Reduce margins to fit content better
        filename: 'Full_report.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 3 }, // Increase scale for better resolution
        jsPDF: { unit: 'px', format: [window.innerWidth, document.body.scrollHeight], orientation: 'portrait' } // Use px and set dimensions to cover entire height
    };

    // Get the entire dashboard content
    var element = document.body;

    // Generate the PDF
    html2pdf().set(opt).from(element).save();
});
