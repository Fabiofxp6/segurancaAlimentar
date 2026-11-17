const entrada = document.getElementById("form-entrada");
if (entrada) {
    const botao = entrada.querySelector('button[type="submit"]');
    const estado = document.getElementById("status-entrada");
    entrada.addEventListener("submit", (evento) => {
        if (botao.disabled) {
            evento.preventDefault();
            return;
        }
        botao.disabled = true;
        estado.hidden = false;
        estado.textContent = "Aguarde a confirmação do acesso.";
    });
    addEventListener("pageshow", () => {
        botao.disabled = false;
        estado.hidden = true;
    });
}

for (const botao of document.querySelectorAll("[data-mostrar-senha]")) {
    const campo = document.getElementById(botao.dataset.mostrarSenha);
    botao.hidden = false;
    botao.addEventListener("click", () => {
        const mostrar = campo.type === "password";
        campo.type = mostrar ? "text" : "password";
        botao.setAttribute("aria-pressed", String(mostrar));
        botao.setAttribute("aria-label", mostrar ? "Ocultar senha" : "Mostrar senha");
    });
}

for (const contador of document.querySelectorAll("[data-contador-saida]")) {
    const campo = document.getElementById(contador.dataset.contadorSaida);
    const atualizar = () => { contador.textContent = campo.value.length + "/" + campo.maxLength; };
    campo.addEventListener("input", atualizar);
    campo.form?.addEventListener("envio-confirmado", atualizar);
    atualizar();
}

for (const botao of document.querySelectorAll("[data-abrir-dialogo]")) {
    const dialogo = document.getElementById(botao.dataset.abrirDialogo);
    botao.hidden = false;
    botao.addEventListener("click", () => dialogo.showModal());
}

document.addEventListener("keydown", (evento) => {
    if (evento.key !== "Escape") return;
    const menu = document.querySelector("[data-menu][open]");
    if (menu) {
        menu.open = false;
        menu.querySelector("summary").focus();
    }
});
document.addEventListener("click", (evento) => {
    const menu = document.querySelector("[data-menu][open]");
    if (menu && !menu.contains(evento.target)) menu.open = false;
});
