function abrirModal(modalSelector) {
  fecharTodasModais();
  $(modalSelector).modal("show");
}

function fecharModal(modalSelector) {
  const modal = document.querySelector(modalSelector);
  modal.querySelectorAll("select[value='new']").forEach((select) => {
    select.value = "";
  });
  const form = modal.querySelector("form");
  if (form) form.reset();
  const idInput = modal.querySelector("[name='id']");
  if (idInput) idInput.value = "";
  $(modalSelector).modal("hide");
}

function fecharTodasModais() {
  $(".modal").modal("hide");
}
