document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. Prediction Form Validation & Loader
    // ==========================================
    const predictForm = document.getElementById('predict-form');
    const loaderOverlay = document.getElementById('loader-overlay');
    
    if (predictForm) {
        predictForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Clear previous errors
            const errorAlerts = predictForm.querySelectorAll('.invalid-feedback');
            errorAlerts.forEach(alert => alert.style.display = 'none');
            
            const inputs = predictForm.querySelectorAll('.form-control-custom');
            inputs.forEach(input => {
                input.classList.remove('is-invalid');
                
                const val = input.value.trim();
                const name = input.getAttribute('name');
                const label = predictForm.querySelector(`label[for="${input.id}"]`).textContent.replace(':', '');
                
                // Check if empty
                if (!val) {
                    showInputError(input, `${label} is required.`);
                    isValid = false;
                } else {
                    const numVal = parseFloat(val);
                    if (isNaN(numVal)) {
                        showInputError(input, `${label} must be a valid number.`);
                        isValid = false;
                    } else if (numVal < 0) {
                        showInputError(input, `${label} cannot be negative.`);
                        isValid = false;
                    }
                    
                    // Specific logical checks
                    if (isValid && name === 'Cloud_Coverage' && numVal > 100) {
                        showInputError(input, `Cloud Coverage cannot exceed 100%.`);
                        isValid = false;
                    }
                    if (isValid && name === 'Humidity' && numVal > 100) {
                        showInputError(input, `Humidity cannot exceed 100%.`);
                        isValid = false;
                    }
                }
            });
            
            if (!isValid) {
                event.preventDefault();
            } else {
                // Show loader overlay
                if (loaderOverlay) {
                    loaderOverlay.classList.remove('d-none');
                }
            }
        });
    }
    
    function showInputError(inputElement, errorMessage) {
        inputElement.classList.add('is-invalid');
        const feedback = inputElement.parentElement.querySelector('.invalid-feedback') || 
                         inputElement.parentElement.parentElement.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.textContent = errorMessage;
            feedback.style.display = 'block';
        }
    }
    
    // Auto-fade flash messages
    const flashAlerts = document.querySelectorAll('.alert-dismissible');
    flashAlerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });

    // ==========================================
    // 2. Client-Side PDF Report Generation
    // ==========================================
    const downloadPdfBtn = document.getElementById('download-pdf-btn');
    if (downloadPdfBtn) {
        downloadPdfBtn.addEventListener('click', function() {
            try {
                // Retrieve result parameters from HTML data attributes
                const timestamp = new Date().toLocaleString();
                const predictionClass = parseInt(downloadPdfBtn.getAttribute('data-prediction'));
                const probability = downloadPdfBtn.getAttribute('data-probability');
                const modelUsed = downloadPdfBtn.getAttribute('data-model');
                
                const annualRainfall = downloadPdfBtn.getAttribute('data-annual');
                const monsoonIntensity = downloadPdfBtn.getAttribute('data-monsoon');
                const cloudCoverage = downloadPdfBtn.getAttribute('data-cloud');
                const humidity = downloadPdfBtn.getAttribute('data-humidity');
                const temp = downloadPdfBtn.getAttribute('data-temp');
                const riverDischarge = downloadPdfBtn.getAttribute('data-discharge');
                
                // Initialize jsPDF
                const { jsPDF } = window.jspdf;
                const doc = new jsPDF({
                    orientation: 'portrait',
                    unit: 'mm',
                    format: 'a4'
                });
                
                // Page width check (A4 is 210mm wide)
                const pageWidth = 210;
                
                // --- Brand Header ---
                doc.setFillColor(15, 43, 70); // Deep ocean blue
                doc.rect(0, 0, pageWidth, 40, 'F');
                
                doc.setTextColor(255, 255, 255);
                doc.setFont('Helvetica', 'bold');
                doc.setFontSize(22);
                doc.text("RISING WATERS PREDICTION SYSTEM", 15, 18);
                
                doc.setFont('Helvetica', 'normal');
                doc.setFontSize(10);
                doc.setTextColor(173, 216, 230); // light blue
                doc.text("A Machine Learning Approach to Hydrological Risk Assessment", 15, 26);
                doc.text(`Generated: ${timestamp}  |  Model: ${modelUsed}`, 15, 33);
                
                // --- Prediction Outcome Banner ---
                let outcomeText = "";
                let bgR = 0, bgG = 0, bgB = 0;
                let textR = 255, textG = 255, textB = 255;
                
                if (predictionClass === 1) {
                    outcomeText = `HIGH FLOOD RISK DETECTED (${probability}% Probability)`;
                    bgR = 239; bgG = 68; bgB = 68; // Alert Red
                } else {
                    outcomeText = `LOW FLOOD RISK DETECTED (${probability}% Probability)`;
                    bgR = 34; bgG = 197; bgB = 94; // Success Green
                }
                
                doc.setFillColor(bgR, bgG, bgB);
                doc.rect(15, 50, pageWidth - 30, 18, 'F');
                
                doc.setFont('Helvetica', 'bold');
                doc.setFontSize(14);
                doc.setTextColor(textR, textG, textB);
                doc.text(outcomeText, pageWidth / 2, 61, { align: 'center' });
                
                // --- Input Parameters Table Section ---
                doc.setTextColor(15, 43, 70);
                doc.setFontSize(14);
                doc.setFont('Helvetica', 'bold');
                doc.text("Reported Meteorological Parameters", 15, 82);
                
                // Draw line under header
                doc.setDrawColor(226, 232, 240);
                doc.setLineWidth(0.5);
                doc.line(15, 85, pageWidth - 15, 85);
                
                // Construct Grid
                const tableData = [
                    { name: "Annual Rainfall", val: `${annualRainfall} mm`, label2: "Humidity", val2: `${humidity} %` },
                    { name: "Monsoon Intensity", val: monsoonIntensity, label2: "Temperature", val2: `${temp} °C` },
                    { name: "Cloud Coverage", val: `${cloudCoverage} %`, label2: "River Discharge", val2: `${riverDischarge} m³/s` }
                ];
                
                doc.setFont('Helvetica', 'normal');
                doc.setFontSize(11);
                doc.setTextColor(30, 41, 59);
                
                let yPos = 95;
                tableData.forEach(row => {
                    // Draw cell background for headers
                    doc.setFillColor(248, 250, 252);
                    doc.rect(15, yPos - 5, 42, 8, 'F');
                    doc.rect(110, yPos - 5, 42, 8, 'F');
                    
                    doc.setFont('Helvetica', 'bold');
                    doc.text(row.name, 17, yPos);
                    doc.text(row.label2, 112, yPos);
                    
                    doc.setFont('Helvetica', 'normal');
                    doc.text(row.val, 62, yPos);
                    doc.text(row.val2, 157, yPos);
                    
                    // Draw borders
                    doc.setDrawColor(226, 232, 240);
                    doc.line(15, yPos + 5, pageWidth - 15, yPos + 5);
                    
                    yPos += 12;
                });
                
                // --- Safety Guidelines / Action Steps ---
                yPos += 5;
                doc.setTextColor(15, 43, 70);
                doc.setFontSize(14);
                doc.setFont('Helvetica', 'bold');
                doc.text("Disaster Preparedness & Action Plan", 15, yPos);
                doc.line(15, yPos + 3, pageWidth - 15, yPos + 3);
                
                yPos += 12;
                doc.setFont('Helvetica', 'normal');
                doc.setFontSize(10.5);
                doc.setTextColor(51, 65, 85);
                
                let recommendations = [];
                if (predictionClass === 1) {
                    recommendations = [
                        "1. Evacuate immediately from flood-prone lowlands if instructed by sirens.",
                        "2. Keep your emergency preparedness go-bag ready with rations, water, and documents.",
                        "3. Disconnect power supplies at main breakers to prevent electrical damage.",
                        "4. Do NOT attempt to walk, swim, or drive through high water flow zones.",
                        "5. Establish contact with disaster hotlines and follow state broadcast channels."
                    ];
                } else {
                    recommendations = [
                        "1. Weather indicators reflect low threat level; no immediate action is required.",
                        "2. Maintain active observation of local weather forecasts during wet monsoon cycles.",
                        "3. Verify that storm water systems and drainage inlets around the property are clean.",
                        "4. Keep home emergency kits stocked as a matter of standard safety preparation."
                    ];
                }
                
                recommendations.forEach(rec => {
                    doc.text(rec, 18, yPos);
                    yPos += 7.5;
                });
                
                // --- Disclaimer ---
                doc.setDrawColor(203, 213, 225);
                doc.line(15, 265, pageWidth - 15, 265);
                
                doc.setFontSize(8.5);
                doc.setTextColor(148, 163, 184);
                const disclaimer = "Disclaimer: This prediction is generated by a Machine Learning model. It is designed for informational purposes and research. Always prioritize instructions issued by local administrative authorities and state meteorological offices.";
                
                // Split disclaimer into multiple lines to avoid page run-out
                const splitDisclaimer = doc.splitTextToSize(disclaimer, pageWidth - 30);
                doc.text(splitDisclaimer, 15, 270);
                
                // Save PDF
                doc.save(`Flood_Prediction_Report_${new Date().toISOString().slice(0, 10)}.pdf`);
                
            } catch (err) {
                console.error("PDF generation failed:", err);
                alert("An error occurred while compiling the PDF report. Details have been logged in the console.");
            }
        });
    }
});
