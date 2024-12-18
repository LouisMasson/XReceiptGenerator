document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generate');
    const usernameInput = document.getElementById('username');
    const receiptContainer = document.getElementById('receipt-container');
    const errorDiv = document.getElementById('error');
    const downloadBtn = document.getElementById('download');

    generateBtn.addEventListener('click', generateReceipt);
    downloadBtn.addEventListener('click', downloadReceipt);

    async function generateReceipt() {
        const username = usernameInput.value.trim();
        if (!username) {
            showError("Veuillez entrer un nom d'utilisateur");
            return;
        }

        const loadingIcon = document.getElementById('loading-icon');
        const generateBtn = document.getElementById('generate');
        
        try {
            loadingIcon.classList.remove('hidden');
            generateBtn.disabled = true;
            
            const response = await fetch(`/api/user/${username}`);
            const data = await response.json();

            if (response.ok) {
                updateReceipt(data.data);
                receiptContainer.classList.remove('hidden');
                errorDiv.classList.add('hidden');
            } else {
                showError(data.error || "Erreur lors de la récupération des données");
            }
        } catch (error) {
            console.error('Erreur de connexion:', error);
            showError("Erreur de connexion au serveur. Veuillez vérifier votre connexion internet et l'accès à l'API X.");
        } finally {
            loadingIcon.classList.add('hidden');
            generateBtn.disabled = false;
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
        // Set profile image
        const profileImg = receipt.querySelector('.profile-image');
        profileImg.src = userData.profile_image_url;
        
        // Set user information
        receipt.querySelector('.username').textContent = `Nom: ${userData.name}\nPseudo: @${userData.username}`;
        receipt.querySelector('.verified').textContent = userData.verified ? '✓ Compte vérifié' : '';
        receipt.querySelector('.bio').textContent = userData.description || '';
        receipt.querySelector('.url').textContent = userData.url ? `URL: ${userData.url}` : '';
        receipt.querySelector('.joined').textContent = `Compte créé le: ${new Date(userData.created_at).toLocaleDateString('fr-FR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        })}`;
        receipt.querySelector('.followers').textContent = `Abonnés: ${formatNumber(userData.public_metrics.followers_count)}`;
        receipt.querySelector('.following').textContent = `Abonnements: ${formatNumber(userData.public_metrics.following_count)}`;
        receipt.querySelector('.tweets').textContent = `Tweets: ${formatNumber(userData.public_metrics.tweet_count)}`;
        receipt.querySelector('.likes').textContent = `Likes: ${formatNumber(userData.public_metrics.like_count)}`;

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

    

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
        errorDiv.classList.add('shake', 'bg-red-500/20', 'border-2', 'border-red-500/50');
        receiptContainer.classList.add('hidden');
        
        setTimeout(() => {
            errorDiv.classList.remove('shake');
        }, 500);
    }
});
