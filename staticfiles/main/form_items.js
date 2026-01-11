function initFormItems(viewsData) {
  let daneJS = "{{ measurementData|escapejs }}";
  let x = daneJS.replace(/'/g, '"');
  let dataObject = JSON.parse(x);
}

paragraph.addEventListener("change", function () {
  let selectedElement = paragraph.options[paragraph.selectedIndex];
  let checkPar = selectedElement.textContent.substring(0, 4);

  let measurementSystemNumber = document.getElementById(
    "divMeasurementSystemNumber"
  );
  let counterReading = document.getElementById("divCounterReading");
  let consumption = document.getElementById("divConsumption");
  let information = document.getElementById("dataInfo");

  if (checkPar === "4260") {
    information.removeAttribute("hidden");
    measurementSystemNumber.removeAttribute("hidden");
    counterReading.removeAttribute("hidden");
    consumption.removeAttribute("hidden");
  } else if (checkPar === "4210") {
    let labelConsumption = document.querySelector(
      'label[for="id_consumption"]'
    );

    if (labelConsumption) {
      labelConsumption.textContent = "Ilość surowca";
    }

    consumption.removeAttribute("hidden");
    console.log(labelConsumption.value);
    measurementSystemNumber.setAttribute("hidden", "true");
    counterReading.setAttribute("hidden", "true");
    information.setAttribute("hidden", "true");
  } else {
    measurementSystemNumber.setAttribute("hidden", "true");
    counterReading.setAttribute("hidden", "true");
    consumption.setAttribute("hidden", "true");
    information.setAttribute("hidden", "true");
  }
});

let unit = document.getElementById("id_unit");
let unitSelected = unit.addEventListener("change", function () {
  let selectedUnit = unit.value;
  let selectedUnitext = unit.options[unit.selectedIndex].text;
  console.log("Wybrany unit: " + selectedUnitext);
});

let type = document.getElementById("id_contract_types");
let typeSelect = type.addEventListener("change", function () {
  let typeText = type.options[type.selectedIndex].text;
  console.log("Wybrany type: " + typeText);
});

let paragraphSelect = paragraph.addEventListener("change", function () {
  let selectedElement = paragraph.options[paragraph.selectedIndex];
  let parText = selectedElement.text;
  let checkParagraph = parText.substring(0, 7);
  console.log("Wybrany paragraph: " + checkParagraph);
});

function checkData() {
  $(dataObject).each(function (i, element) {
    if (element.unit_id == unit.value) {
      let elementData = element.data;
      let information = document.getElementById("dataInfo");

      for (let y = 0; y < elementData.length; y++) {
        console.log("elementData.length: " + elementData.length);
        console.log(
          "wchodze do  for (let y = 0; y < elementData.length; y++ )"
        );

        console.log("elementData");
        console.log(elementData);

        if (
          elementData[y].type === type.options[type.selectedIndex].text &&
          elementData[y].par ===
            paragraph.options[paragraph.selectedIndex].text.slice(0, 7)
        ) {
          console.log(
            "wchodze do  if(elementData[y].type === type.options[type.selectedIndex].text && elementData[y].par === paragraph.options[paragraph.selectedIndex].text.slice(0,7)) -> True"
          );
          console.log("elementData[y].type");
          console.log(elementData[y].type);
          console.log("type.options[type.selectedIndex].text");
          console.log(type.options[type.selectedIndex].text);
          console.log(
            elementData[y].type === type.options[type.selectedIndex].text
          );

          console.log("elementData[y].par");
          console.log(elementData[y].par);
          console.log(
            "paragraph.options[paragraph.selectedIndex].text.slice(0,7)"
          );
          console.log(
            paragraph.options[paragraph.selectedIndex].text.slice(0, 7)
          );
          console.log(
            elementData[y].par ===
              paragraph.options[paragraph.selectedIndex].text.slice(0, 7)
          );

          let measureData = document.getElementById(
            "id_measurementSystemNumber"
          );
          console.log("measureData");
          console.log(measureData);

          if (measureData) {
            information.removeAttribute("hidden");
            information.textContent =
              " Ostatni okres rozliczeniowy: " +
              elementData[y].period +
              ", " +
              "stan licznika:" +
              elementData[y].counterReading;
            measureData.value = elementData[y].measurement;
          }
        } else {
          let measureData = document.getElementById(
            "id_measurementSystemNumber"
          );
          measureData.value = "";
          information.setAttribute("hidden", "true");
        }
      }
    } else {
      console.log("wchodze do if( element.unit_id == unit.value) -> False");
    }
  });
}
$("#id_contract_types").on("change", function () {
  checkData();
});

$("#id_paragraph").on("change", function () {
  checkData();
});
