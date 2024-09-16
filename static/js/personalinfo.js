document.addEventListener('DOMContentLoaded', () => {
    const interestCategories = document.getElementById('interest_categories');
    const skillAreasContainer = document.getElementById('skill_areas');
    const maxCategories = 2;
    const maxSkillAreas = 8;
    const maxSubSkills = 5;

    let selectedCategories = [];
    let selectedSkillAreas = [];

    const interests = {
        'Computer_Science': [
            'Technology & Engineering',
            'AI & Machine Learning',
            'Data Science',
            'Cybersecurity',
            'Blockchain',
            'Game Development',
            'Mobile App Development',
            'Web Development',
            'Cloud Computing'
        ],
        'Mechanical_Engineering': [
            'Technology & Engineering',
            'Data Science',
            'Cybersecurity',
            'Mobile App Development'
        ],
        'Electrical_Engineering': [
            'Technology & Engineering',
            'AI & Machine Learning',
            'Data Science',
            'Cloud Computing'
        ],
        'Arts_Humanities': [
            'Graphic Design',
            'Performing Arts',
            'Fine Arts'
        ],
        'Business_Management': [
            'Marketing',
            'Sales',
            'Human Resources'
        ],
        'Software_Engineer': [
            'Technology & Engineering',
            'AI & Machine Learning',
            'Web Development'
        ],
        'Data_Analyst': [
            'Data Science',
            'AI & Machine Learning',
            'Cloud Computing'
        ]
    };

    // Set interests based on a selected value (set `selectedValue` appropriately)
    const selectedValue = 'Computer_Science'; // Example value
    const interestsToShow = interests[selectedValue] || [];
    interestCategories.innerHTML = interestsToShow.map(interest => `
        <div class="button-option" data-value="${interest.replace(/\s+/g, '_').toLowerCase()}">${interest}</div>
    `).join('');

   
    const skillAreasByDomain = {
        "technology_engineering": [
            { value: "programming_languages", text: "Programming Languages", skills: ["Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Dart"] },
            { value: "cloud_platforms", text: "Cloud Platforms", skills: ["AWS", "Azure", "Google Cloud"] },
            { value: "frontend_frameworks", text: "Frontend Frameworks", skills: ["React", "Angular", "Vue.js"] },
            { value: "backend_frameworks", text: "Backend Frameworks", skills: ["Node.js", "Django", "Flask"] },
            { value: "databases", text: "Databases", skills: ["SQL", "NoSQL", "MongoDB", "PostgreSQL", "MySQL"] },
            { value: "version_control", text: "Version Control", skills: ["Git", "GitHub", "GitLab"] },
            { value: "devops", text: "DevOps", skills: ["Docker", "Kubernetes", "Jenkins"] },
            { value: "network_security", text: "Network & Security", skills: ["TCP/IP", "DNS", "DHCP", "VPN", "Firewalls", "IDS/IPS"] }
        ],
        "ai": [
            { value: "machine_learning_algorithms", text: "Machine Learning Algorithms", skills: ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning"] },
            { value: "libraries_frameworks", text: "Libraries & Frameworks", skills: ["TensorFlow", "Keras", "PyTorch", "Scikit-Learn"] },
            { value: "data_processing", text: "Data Processing", skills: ["Pandas", "NumPy"] },
            { value: "deep_learning", text: "Deep Learning", skills: ["Neural Networks", "CNNs", "RNNs"] },
            { value: "natural_language_processing", text: "Natural Language Processing", skills: ["NLTK", "SpaCy", "BERT"] }
        ],
        "data_science": [
            { value: "data_analysis_tools", text: "Data Analysis Tools", skills: ["Excel", "SQL", "R", "Python (Pandas, NumPy)"] },
            { value: "data_visualization", text: "Data Visualization", skills: ["Tableau", "Power BI", "Matplotlib", "Seaborn", "Plotly"] },
            { value: "statistical_analysis", text: "Statistical Analysis", skills: ["Descriptive Statistics", "Inferential Statistics"] },
            { value: "big_data_tools", text: "Big Data Tools", skills: ["Hadoop", "Spark"] }
        ],
        "cybersecurity": [
            { value: "network_security", text: "Network Security", skills: ["Firewalls", "Intrusion Detection Systems (IDS)", "Intrusion Prevention Systems (IPS)"] },
            { value: "cryptography", text: "Cryptography", skills: ["Encryption", "Decryption", "Key Management"] },
            { value: "vulnerability_assessment", text: "Vulnerability Assessment", skills: ["Penetration Testing", "Vulnerability Scanning"] },
            { value: "compliance_standards", text: "Compliance & Standards", skills: ["GDPR", "HIPAA", "ISO 27001"] },
            { value: "incident_response", text: "Incident Response", skills: ["Forensics", "Incident Management"] }
        ],
        "blockchain": [
            { value: "blockchain_platforms", text: "Blockchain Platforms", skills: ["Ethereum", "Hyperledger", "Binance Smart Chain"] },
            { value: "smart_contracts", text: "Smart Contracts", skills: ["Solidity", "Web3.js"] },
            { value: "cryptocurrencies", text: "Cryptocurrencies", skills: ["Bitcoin", "Ethereum", "Altcoins"] },
            { value: "consensus_algorithms", text: "Consensus Algorithms", skills: ["Proof of Work", "Proof of Stake"] },
            { value: "decentralized_applications", text: "Decentralized Applications (dApps)", skills: ["Development", "Deployment"] }
        ],
        "game_development": [
            { value: "game_engines", text: "Game Engines", skills: ["Unity", "Unreal Engine"] },
            { value: "game_design", text: "Game Design", skills: ["Mechanics", "Level Design", "Game Balance"] },
            { value: "graphics", text: "Graphics", skills: ["2D/3D Art", "Animation", "Shader Programming"] },
            { value: "programming", text: "Programming", skills: ["C#", "C++", "Python (for scripting)"] },
            { value: "game_testing", text: "Game Testing", skills: ["Playtesting", "Bug Reporting"] }
        ],
        "mobile_app_development": [
            { value: "platforms", text: "Platforms", skills: ["iOS", "Android"] },
            { value: "programming_languages", text: "Programming Languages", skills: ["Swift", "Kotlin", "Java", "Dart"] },
            { value: "frameworks", text: "Frameworks", skills: ["React Native", "Flutter", "Xamarin"] },
            { value: "ui_ux_design", text: "UI/UX Design", skills: ["Mobile App Design Principles", "Prototyping"] },
            { value: "apis", text: "APIs", skills: ["RESTful APIs", "GraphQL"] }
        ],
        "web_development": [
            { value: "frontend", text: "Frontend", skills: ["HTML", "CSS", "JavaScript", "Frontend Frameworks (React, Angular, Vue.js)"] },
            { value: "backend", text: "Backend", skills: ["Node.js", "Django", "Flask", "Ruby on Rails"] },
            { value: "databases", text: "Databases", skills: ["SQL", "NoSQL", "MongoDB"] },
            { value: "web_design", text: "Web Design", skills: ["Responsive Design", "User Experience (UX)"] },
            { value: "deployment", text: "Deployment", skills: ["Web Hosting", "CI/CD"] }
        ],
        "cloud_computing": [
            { value: "cloud_providers", text: "Cloud Providers", skills: ["AWS", "Azure", "Google Cloud"] },
            { value: "services", text: "Services", skills: ["Compute (EC2, Azure VMs)", "Storage (S3, Blob Storage)"] },
            { value: "serverless", text: "Serverless", skills: ["AWS Lambda", "Azure Functions"] },
            { value: "containerization", text: "Containerization", skills: ["Docker", "Kubernetes"] },
            { value: "cloud_security", text: "Cloud Security", skills: ["IAM", "Encryption"] }
        ]
    };

    interestCategories.addEventListener('click', (event) => {
        if (event.target.classList.contains('button-option')) {
            const selectedCategory = event.target.getAttribute('data-value');

            if (selectedCategories.includes(selectedCategory)) {
                selectedCategories = selectedCategories.filter(cat => cat !== selectedCategory);
                event.target.classList.remove('selected');
            } else {
                if (selectedCategories.length < maxCategories) {
                    selectedCategories.push(selectedCategory);
                    event.target.classList.add('selected');
                } else {
                    alert(`You can select a maximum of ${maxCategories} categories.`);
                    return;
                }
            }

            updateSkillAreas();
        }
    });

    function updateSkillAreas() {
        skillAreasContainer.innerHTML = '';
        selectedSkillAreas = []; // Reset selected skill areas

        Object.keys(skillAreasByDomain).forEach(category => {
            const skills = skillAreasByDomain[category] || [];
            const isCategorySelected = selectedCategories.includes(category);

            skills.forEach(skill => {
                const skillDiv = document.createElement('div');
                skillDiv.classList.add('skill-category');
                skillDiv.style.display = isCategorySelected ? 'block' : 'none'; // Toggle visibility based on category selection
                skillDiv.innerHTML = `<strong>${skill.text}</strong>`;

                // Create and append skill buttons
                skill.skills.forEach(skillName => {
                    const skillButton = document.createElement('button');
                    skillButton.classList.add('skill-button');
                    skillButton.setAttribute('data-skill', skillName);
                    skillButton.textContent = skillName;

                    // Set the button's initial state based on whether it's already selected
                    if (selectedSkillAreas.includes(skillName)) {
                        skillButton.classList.add('selected');
                    }

                    skillButton.addEventListener('click', () => {
                        handleSkillSelection(skillButton, skillName);
                    });

                    skillDiv.appendChild(skillButton);
                });

                skillAreasContainer.appendChild(skillDiv);
            });
        });
    }

    function handleSkillSelection(button, skillName) {
        if (selectedSkillAreas.includes(skillName)) {
            // Skill is being deselected
            selectedSkillAreas = selectedSkillAreas.filter(skill => skill !== skillName);
            button.classList.remove('selected');
            removeSkillLevelInput(skillName);
        } else {
            if (selectedSkillAreas.length < maxSkillAreas) {
                // Skill is being selected
                selectedSkillAreas.push(skillName);
                button.classList.add('selected');
                addSkillLevelInput(skillName);
            } else {
                alert(`You can select a maximum of ${maxSkillAreas} skill areas.`);
                return;
            }
        }
    }

    function addSkillLevelInput(skillName) {
        const skillDiv = document.querySelector(`.skill-button[data-skill="${skillName}"]`).parentElement;

        // Check if the skill level input already exists
        if (skillDiv.querySelector(`.skill-level-container[data-skill="${skillName}"]`)) {
            return; // Exit if skill level input already exists
        }

        // Create a container for the skill level input and label
        const skillLevelDiv = document.createElement('div');
        skillLevelDiv.classList.add('skill-level-container');
        skillLevelDiv.setAttribute('data-skill', skillName);

        // Create a span to display the skill name
        const skillNameSpan = document.createElement('span');
        skillNameSpan.classList.add('skill-name');
        skillNameSpan.textContent = skillName;

        // Create range input for skill level
        const rangeInput = document.createElement('input');
        rangeInput.type = 'range';
        rangeInput.min = '0';
        rangeInput.max = '100';
        rangeInput.value = '50'; // Default value
        rangeInput.classList.add('range-input');
        rangeInput.setAttribute('data-skill', skillName);

        const rangeLabel = document.createElement('span');
        rangeLabel.classList.add('range-label');
        rangeLabel.textContent = getLevelFromRange(rangeInput.value);

        rangeInput.addEventListener('input', () => {
            rangeLabel.textContent = getLevelFromRange(rangeInput.value);
        });

        // Append the skill name, range input, and range label to the skillLevelDiv
        skillLevelDiv.appendChild(skillNameSpan);
        skillLevelDiv.appendChild(rangeInput);
        skillLevelDiv.appendChild(rangeLabel);

        // Append the skillLevelDiv to the skillDiv
        skillDiv.appendChild(skillLevelDiv);
    }

    function removeSkillLevelInput(skillName) {
        const skillDiv = document.querySelector(`.skill-button[data-skill="${skillName}"]`).parentElement;
        const skillLevelDiv = skillDiv.querySelector(`.skill-level-container[data-skill="${skillName}"]`);

        if (skillLevelDiv) {
            skillDiv.removeChild(skillLevelDiv);
        }
    }

    function getLevelFromRange(value) {
        value = parseInt(value, 10);
        if (value <= 20) return 'Beginner: Basic understanding, little to no practical experience';
        if (value <= 40) return 'Beginner-Intermediate: Some practical experience';
        if (value <= 60) return 'Intermediate: Practical experience and good working knowledge.';
        if (value <= 75) return 'Advanced-Expert: High level of proficiency with hands-on experience';
        if (value <= 95) return 'Expert: Extensive experience and mastery.';
        return 'Advanced';
    }

    // Function to toggle fields based on user type
    function toggleFields() {
        const userType = document.getElementById('user_type').value;
        document.getElementById('student_fields').style.display = userType === 'student' ? 'block' : 'none';
        document.getElementById('professional_fields').style.display = userType === 'professional' ? 'block' : 'none';
    }

    // Function to toggle visibility of 'other' input fields
    function toggleOtherField(selectId, otherInputId) {
        const selectElement = document.getElementById(selectId);
        const otherInput = document.getElementById(otherInputId);
        otherInput.style.display = selectElement.value === 'other' ? 'block' : 'none';
    }

    // Function to show a specific section
    function showSection(sectionId) {
        document.querySelectorAll('.form-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(sectionId).classList.add('active');
    }

    // Function to toggle 'other' fields based on selection
    function toggleOtherField(selectedValue) {
        const otherFieldDiv = document.getElementById('other_field_div');
        const otherjobDiv = document.getElementById('other_job_div');

        // Show or hide 'other' fields based on selected value
        if (selectedValue === 'other_study') {
            otherFieldDiv.style.display = 'block';
        } else {
            otherFieldDiv.style.display = 'none';
        }

        if (selectedValue === 'other_job') {
            otherjobDiv.style.display = 'block';
        } else {
            otherjobDiv.style.display = 'none';
        }
    }

    // Initialize the page
    updateSkillAreas();
});
