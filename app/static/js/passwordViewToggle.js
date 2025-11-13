// static/js/passwordToggle.js
document.addEventListener('DOMContentLoaded', function() {

    // ATENÇÃO AQUI: IDs atualizados
    const toggleBotao = document.getElementById('togglePassword');
    const inputSenha = document.getElementById('password'); // WTForms gera 'password'

    if (toggleBotao && inputSenha) {
        toggleBotao.addEventListener('click', function() {
            // Verifica o tipo atual do input
            const type = inputSenha.getAttribute('type') === 'password' ? 'text' : 'password';
            inputSenha.setAttribute('type', type);

            // Alterna o ícone (olho aberto vs. olho fechado)
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    }
});