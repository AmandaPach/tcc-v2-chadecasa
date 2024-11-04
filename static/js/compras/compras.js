const totalDisplay = document.getElementById("total");
const totalInput = document.getElementById("valor_total");

function removeItem(btn) {
  btn.closest("tr").remove();
}

const updateTotalValue = () => {
  let formset = document.querySelectorAll("#formset-items-produtos tbody tr");
  var total = 0;
  formset.forEach(form => {
    var quantidade = form.querySelector("input[name$=quantidade]").value;
    var custo = form.querySelector("input[name$=custo]").value;
    var desconto = form.querySelector("input[name$=desconto]").value ?? 0;
    var unidadeDisplay = form.querySelector("input[name$=unidadeCusto]");
    const unidadeCusto = quantidade * (custo - desconto);
    unidadeDisplay.value = unidadeCusto.toFixed(2);
    total += unidadeCusto;
  });
  totalDisplay.innerText = total.toFixed(2);
  totalInput.value = total.toFixed(2);
};

function addProdutoInput() {
  var formIdx = document.querySelectorAll("#formset-items-produtos tbody tr").length;
  var newForm = document
    .querySelector("#empty-form-produto")
    .innerHTML.replace(/__prefix__/g, formIdx);
  document
    .querySelector("#formset-items-produtos tbody")
    .insertAdjacentHTML("beforeend", newForm);

  setFields();
}

function verifyFornecedor(elem) {
  if (elem.value != "new") return;
  abrirModal("#modal-fornecedor");
}

function verifyProduto(elem) {
  if (elem.value != "new") return;
  abrirModal("#modal-produto");
}

const today = new Date(new Date().toLocaleString("en-US", { timeZone: "America/Sao_Paulo" }));
const formattedToday = today.toISOString().split("T")[0];

function verifyDates() {
  const dataEmissaoComp = document.getElementById("data_emissao");
  const dataChegadaComp = document.getElementById("data_chegada");

  const dataEmissaoValue = dataEmissaoComp.value;
  const dataChegadaValue = dataChegadaComp.value;
  
  if (dataEmissaoValue && dataEmissaoValue > formattedToday) {
    dataEmissaoComp.value = formattedToday;
  }

  if (!dataEmissaoValue || !dataChegadaValue) return;

  if (dataChegadaValue < dataEmissaoValue) {
    dataChegadaComp.value = dataEmissaoValue;
  }
}

function verifyNotaFiscal() {
  const notaFiscal = document.getElementById("nota_fiscal");
  const modelo = document.getElementById("modelo_nota");
  const serie = document.getElementById("serie");
  const fornecedor = document.getElementById("fornecedor_id");

  if (!notaFiscal.value || !modelo.value || !serie.value || !fornecedor.value) return;

  fetch('/compras/nota/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      nota_fiscal: notaFiscal.value,
      modelo_nota: modelo.value,
      serie: serie.value,
      fornecedor: fornecedor.value
    })
  }).then(response => {
    if (response.status === 200) return;
    alert("Nota fiscal já cadastrada para esse fornecedor.");
    notaFiscal.value = "";
    modelo.value = "";
    serie.value = "";
    fornecedor.value = "";
  });
}

addProdutoInput();
