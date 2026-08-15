document.getElementById('predictionForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const annualIncome = document.getElementById('annualIncome').value;
    const spendingScore = document.getElementById('spendingScore').value;

    // Validate inputs
    if (annualIncome < 0 || annualIncome > 200) {
        alert('Annual Income must be between 0 and 200');
        return;
    }

    if (spendingScore < 1 || spendingScore > 100) {
        alert('Spending Score must be between 1 and 100');
        return;
    }

    // Show loading state
    const resultSection = document.getElementById('resultSection');
    resultSection.style.display = 'block';
    resultSection.style.opacity = '0.5';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                annual_income: parseFloat(annualIncome),
                spending_score: parseFloat(spendingScore)
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Update result section
            document.getElementById('clusterId').textContent = `Cluster ${data.cluster}`;
            document.getElementById('clusterDescription').textContent = data.description;
            document.getElementById('avgIncome').textContent = `$${data.center['Annual Income (k$)'].toFixed(2)}k`;
            document.getElementById('avgSpending').textContent = data.center['Spending Score (1-100)'].toFixed(2);

            // Update recommendations
            const recommendationsList = document.getElementById('recommendationsList');
            recommendationsList.innerHTML = '';

            // Generate recommendations based on cluster
            const recommendations = getRecommendations(data.cluster);
            recommendations.forEach(rec => {
                const li = document.createElement('li');
                li.textContent = rec;
                recommendationsList.appendChild(li);
            });

            // Show result with animation
            resultSection.style.opacity = '1';
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error making prediction: ' + error.message);
    }
});

function getRecommendations(clusterId) {
    const recommendations = {
        0: [
            'Offer premium loyalty programs with exclusive benefits',
            'Provide early access to new product launches',
            'Personal shopping assistant service for high-value customers'
        ],
        1: [
            'Highlight value-for-money products and bulk deals',
            'Create educational content showcasing product value',
            'Limited-time bundle offers to increase spending'
        ],
        2: [
            'Maintain consistent product quality and service',
            'Regular promotional offers and discounts',
            'Email newsletters with personalized recommendations'
        ],
        3: [
            'Develop budget-friendly product lines',
            'Clear pricing and transparent cost breakdowns',
            'Seasonal sales and discount coupons'
        ],
        4: [
            'Offer buy-now-pay-later payment options',
            'Create installment payment plans',
            'Showcase social proof and customer reviews'
        ]
    };

    return recommendations[clusterId] || [
        'Continue monitoring customer behavior',
        'Collect more data for better insights',
        'Maintain customer engagement'
    ];
}

// Add input validation on keypress
document.getElementById('annualIncome').addEventListener('input', function () {
    if (this.value < 0) this.value = 0;
    if (this.value > 200) this.value = 200;
});

document.getElementById('spendingScore').addEventListener('input', function () {
    if (this.value < 1) this.value = 1;
    if (this.value > 100) this.value = 100;
});