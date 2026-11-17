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

const sumario = document.querySelector("[data-foco-erros]");
sumario?.focus();

for (const botao of document.querySelectorAll("[data-abrir-dialogo]")) {
    const dialogo = document.getElementById(botao.dataset.abrirDialogo);
    if (typeof dialogo?.showModal !== "function") continue;
    botao.hidden = false;
    botao.setAttribute("aria-haspopup", "dialog");
    botao.addEventListener("click", () => {
        dialogo.addEventListener("close", () => botao.focus({preventScroll: true}), {once: true});
        dialogo.showModal();
    });
}

for (const form of document.querySelectorAll("[data-confirmar-dialogo]")) {
    const dialogo = document.getElementById(form.dataset.confirmarDialogo);
    if (typeof dialogo?.showModal !== "function") continue;
    const acao = form.querySelector('button[type="submit"]');
    acao.setAttribute("aria-haspopup", "dialog");
    let confirmou = false;
    form.addEventListener("submit", (evento) => {
        if (confirmou) return;
        evento.preventDefault();
        dialogo.returnValue = "";
        dialogo.showModal();
    });
    dialogo.addEventListener("close", () => {
        if (dialogo.returnValue === "confirmar") {
            confirmou = true;
            form.requestSubmit();
        } else {
            acao.focus({preventScroll: true});
        }
    });
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
