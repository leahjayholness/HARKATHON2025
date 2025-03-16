function updateTimers() {
    const timers = document.querySelectorAll(".remaining-time");
    const now = new Date();

    timers.forEach(timer => {
        const startTime = new Date(timer.dataset.startTime);
        const endTime = new Date(timer.dataset.endTime);
        const start = startTime - now;
        const diff = endTime - now;

        if (start >= 0) {
            timer.innerText = "Pending Start";
        }
        else if (diff <= 0) {
            timer.innerText = "Completed";
            timer.classList.add("text-success");
        } else {
            const hours = Math.floor(diff / (1000 * 60 * 60));
            const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((diff % (1000 * 60)) / 1000);
            timer.innerText = `${hours}h ${minutes}m ${seconds}s`;
        }
    });
}

function confirmModal() {
    const confirmButtons = document.querySelectorAll(".confirm-submit");
    const modal = document.getElementById("confirmationModal");
    const modalConfirmButton = document.getElementById("modalConfirm");
    const modalCancelButton = document.getElementById("modalCancel");
    let formToSubmit = null;

    confirmButtons.forEach(button => {
        button.addEventListener("click", event => {
            event.preventDefault(); // Prevent form submission
            formToSubmit = event.target.closest("form"); // Store the form to submit
            modal.style.display = "block"; // Show the modal
        });
    });

    // Confirm button inside the modal
    modalConfirmButton.addEventListener("click", () => {
        if (formToSubmit) {
            formToSubmit.submit(); // Submit the stored form
        }
        modal.style.display = "none"; // Hide the modal
    });

    // Cancel button inside the modal
    modalCancelButton.addEventListener("click", () => {
        modal.style.display = "none"; // Hide the modal
    });
}

document.addEventListener("DOMContentLoaded", () => {
    //Timer
    updateTimers();
    setInterval(updateTimers, 1000); // Update timers every second

    //Confirm Modal
    confirmModal();
});
