document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generate');
    const usernameInput = document.getElementById('username');
    const receiptContainer = document.getElementById('receipt-container');
    const errorDiv = document.getElementById('error');
    const downloadBtn = document.getElementById('download');
    const shareBtn = document.getElementById('share');

    generateBtn.addEventListener('click', generateReceipt);
    downloadBtn.addEventListener('click', downloadReceipt);
    shareBtn.addEventListener('click', shareReceipt);

    async function generateReceipt() {
        const username = usernameInput.value.trim();
        if (!username) {
            showError("Veuillez entrer un nom d'utilisateur");
            return;
        }

        try {
            const response = await fetch(`/api/user/${username}`);
            const data = await response.json();

            if (response.ok) {
                updateReceipt(data.data);
                receiptContainer.classList.remove('d-none');
                errorDiv.classList.add('d-none');
            } else {
                showError(data.error || "Erreur lors de la récupération des données");
            }
        } catch (error) {
            showError("Erreur de connexion au serveur");
        }
    }

    function updateReceipt(userData) {
        const receipt = document.getElementById('receipt');
        
        // Format numbers with French locale
        const formatNumber = (num) => new Intl.NumberFormat('fr-FR').format(num);
        
        // Update receipt content
        receipt.querySelector('.date').textContent = new Date().toLocaleDateString('fr-FR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        receipt.querySelector('.username').textContent = `Nom: ${userData.name}\nPseudo: @${userData.username}`;
        receipt.querySelector('.joined').textContent = `Compte créé le: ${new Date(userData.created_at).toLocaleDateString('fr-FR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        })}`;
        receipt.querySelector('.followers').textContent = `Abonnés: ${formatNumber(userData.public_metrics.followers_count)}`;
        receipt.querySelector('.following').textContent = `Abonnements: ${formatNumber(userData.public_metrics.following_count)}`;

        // Add print artifacts
        addPrintArtifacts();
    }

    function addPrintArtifacts() {
        const receipt = document.getElementById('receipt');
        // Clear existing artifacts
        receipt.querySelectorAll('.print-artifact').forEach(el => el.remove());
        
        // Add random print artifacts
        for (let i = 0; i < 5; i++) {
            const artifact = document.createElement('div');
            artifact.classList.add('print-artifact');
            artifact.style.top = `${Math.random() * 100}%`;
            receipt.appendChild(artifact);
        }
    }

    async function downloadReceipt() {
        try {
            const receipt = document.getElementById('receipt');
            const dataUrl = await domtoimage.toPng(receipt);
            
            const link = document.createElement('a');
            link.download = 'x-receipt.png';
            link.href = dataUrl;
            link.click();
        } catch (error) {
            showError("Erreur lors du téléchargement");
        }
    }

    function shareReceipt() {
        if (navigator.share) {
            domtoimage.toBlob(document.getElementById('receipt'))
                .then(blob => {
                    const file = new File([blob], 'x-receipt.png', { type: 'image/png' });
                    navigator.share({
                        files: [file],
                        title: 'Mon reçu X',
                        text: 'Voici mon reçu X généré!'
                    }).catch(error => {
                        showError("Erreur lors du partage");
                    });
                });
        } else {
            showError("Le partage n'est pas supporté sur votre appareil");
        }
    }

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('d-none');
        receiptContainer.classList.add('d-none');
    }
});
