console.log("form_item.html");

function initFormItems(viewsData){
    var daneJS = "{{ measurementData|escapejs }}";
    var x = daneJS.replace(/'/g, '"');
    var dataObject = JSON.parse(x);
}

    paragraph.addEventListener('change', function() {
        var selectedElement = paragraph.options[paragraph.selectedIndex];
        var checkPar = selectedElement.textContent.substring(0, 4);

        var measurementSystemNumber = document.getElementById("divMeasurementSystemNumber");
        var counterReading = document.getElementById("divCounterReading");
        var consumption = document.getElementById("divConsumption");
        var information = document.getElementById("dataInfo");

        if (checkPar === "4260") {

            information.removeAttribute('hidden');
            measurementSystemNumber.removeAttribute('hidden');
            counterReading.removeAttribute('hidden');
            consumption.removeAttribute('hidden');

        } else if (checkPar === "4210") {

            var labelConsumption = document.querySelector('label[for="id_consumption"]');

            if (labelConsumption){

                labelConsumption.textContent = "Ilość surowca";
            };

            consumption.removeAttribute('hidden');
            console.log(labelConsumption.value);
            measurementSystemNumber.setAttribute('hidden', 'true');
            counterReading.setAttribute('hidden', 'true');
            information.setAttribute('hidden', 'true');

        } else {
            measurementSystemNumber.setAttribute('hidden', 'true');
            counterReading.setAttribute('hidden', 'true');
            consumption.setAttribute('hidden', 'true');
            information.setAttribute('hidden', 'true');
        }
    });


    var unit = document.getElementById("id_unit");
    var unitSelected = unit.addEventListener('change', function() {
        var selectedUnit = unit.value;
        var selectedUnitext = unit.options[unit.selectedIndex].text;
        console.log("Wybrany unit: " + selectedUnitext);
    });

    var type = document.getElementById("id_contract_types");
    var typeSelect = type.addEventListener('change', function() {
        var typeText = type.options[type.selectedIndex].text;
        console.log("Wybrany type: " + typeText);
    });

    var paragraphSelect = paragraph.addEventListener('change', function() {
        var selectedElement = paragraph.options[paragraph.selectedIndex];
        var parText = selectedElement.text;
        var checkParagraph = parText.substring(0, 7);
        console.log("Wybrany paragraph: " + checkParagraph);
    });

    function checkData(){
        $(dataObject).each(function(i, element) {
            if( element.unit_id == unit.value) {

                var elementData = element.data;
                var information = document.getElementById("dataInfo");

                for (let y = 0; y < elementData.length; y++ ){
                    console.log("elementData.length: "+elementData.length);
                    console.log("wchodze do  for (let y = 0; y < elementData.length; y++ )");

                    console.log("elementData");
                    console.log(elementData);

                    if(elementData[y].type === type.options[type.selectedIndex].text && elementData[y].par === paragraph.options[paragraph.selectedIndex].text.slice(0,7)){

                        console.log("wchodze do  if(elementData[y].type === type.options[type.selectedIndex].text && elementData[y].par === paragraph.options[paragraph.selectedIndex].text.slice(0,7)) -> True");
                        console.log("elementData[y].type");
                        console.log(elementData[y].type);
                        console.log("type.options[type.selectedIndex].text");
                        console.log(type.options[type.selectedIndex].text);
                        console.log(elementData[y].type === type.options[type.selectedIndex].text);

                        console.log("elementData[y].par");
                        console.log(elementData[y].par);
                        console.log("paragraph.options[paragraph.selectedIndex].text.slice(0,7)");
                        console.log(paragraph.options[paragraph.selectedIndex].text.slice(0,7));
                        console.log(elementData[y].par === paragraph.options[paragraph.selectedIndex].text.slice(0,7));

                        var measureData = document.getElementById("id_measurementSystemNumber");
                        console.log("measureData");
                        console.log(measureData);

                        if(measureData){

                        information.removeAttribute('hidden');
                        information.textContent = " Ostatni okres rozliczeniowy: " + elementData[y].period + ", " + "stan licznika:"+ elementData[y].counterReading;
                        measureData.value = elementData[y].measurement;

                        };

                    }else{

                    console.log("wchodze do else");

                    var measureData = document.getElementById("id_measurementSystemNumber");
                    measureData.value = "";
                    information.setAttribute('hidden', 'true');

                    };
                };
            }else{
                console.log("wchodze do if( element.unit_id == unit.value) -> False");
            };
        });
    };
    $('#id_contract_types').on('change', function(){
        checkData();
    });
    $('#id_paragraph').on('change', function(){
        checkData();
    });