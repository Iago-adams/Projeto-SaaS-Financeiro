document.addEventListener("DOMContentLoaded", function () {

    const toggleIcon = document.querySelector("#togglePassword");
    const passwordInput = document.querySelector("#password");

    if (toggleIcon && passwordInput) {
        toggleIcon.addEventListener("click", function (e) {
            // Previne comportamentos padrões estranhos
            e.preventDefault(); 

            const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
            passwordInput.setAttribute("type", type);
            
            this.classList.toggle("fa-eye");
            this.classList.toggle("fa-eye-slash");
        });
    }
});