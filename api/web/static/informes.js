



const button_buscar = document.getElementById('button_buscar');
const fieldFechaDesde = document.getElementById('field_fecha')
const btnRefreshSelected = document.getElementById('btn-refresh-selected') 

let myChartInstance = null;
let myChartTotalInstance = null;





fieldFechaDesde.addEventListener("change", function() {        
         runGetData(this.value)
});

button_buscar.addEventListener("click", function() {
        fichajesmediahora(fieldFechaDesde.value);
});




btnRefreshSelected.addEventListener("click", async function(){

    theDay = fieldFechaDesde.value;
    console.log(theDay)

    var dd =  theDay.split('-')[2]
    var mm =  theDay.split('-')[1]
    var yyyy =  theDay.split('-')[0]

    var patronFichero = "Movimientos" + dd + "_" + mm  + "_" + yyyy + ".txt"

    var  resp = await fetch(`/api/actualizarFromFile?nombre_fichero=` + patronFichero);
    var  data = await resp.json();
    console.log(data);    

    console.log(patronFichero)

        appendAlert('Datos de hoy actualizados correctamente', 'success')

    runGetData(fieldFechaDesde.value)
    //Movimientos08_05_2026.txt

});



const fichajesComerdor = async function(ahora) {
    if (ahora === null){
        var  ahora = new Date().toISOString().split('T')[0];
    }    
    var  resp = await fetch(`/api/fichajesComedor?fecha=` + ahora);
    var  data = await resp.json();
    console.log(data);    
}


const totalizadorFichajes = async function(ahora) {
    if (ahora === null){
        var  ahora = new Date().toISOString().split('T')[0];
    }    
    var  resp = await fetch(`/api/totalizadorFichajes?fecha=` + ahora);
    var  data = await resp.json();

    await totalizadorFichajesChart(data)
    
}


const totalizadorFichajesChart = async function(data){

    //{"dentro":[228],"entrada":[341],"salida":[127],"comedor":[4]}

    entradas  = data.entrada[0];
    salidas   = data.salida[0];
    comedor   = data.comedor[0];
    dentro    = data.dentro[0];

    const ctx = document.getElementById('totalFichajesChart');

    //Si ya existe un gráfico, lo destruimos
    if (myChartTotalInstance) {
        myChartTotalInstance.destroy();
    }    

    myChartTotalInstance = new Chart(ctx, {
                                        type: 'bar',
                                        data: {
                                            labels: [ 'Total'],
                                            datasets: [
                                                        {
                                                            label: 'Entradas',
                                                            data: [entradas],
                                                            backgroundColor: '#1fe270', // Color de relleno azul                                                            
                                                            borderWidth: 1
                                                        },
                                                        {
                                                            label: 'Salidass',
                                                            data: [salidas],
                                                            backgroundColor: '#ff0000', // Color de relleno azul                                                            
                                                            borderWidth: 1
                                                        },
                                                        {
                                                            label: 'Comedor',
                                                            data: [comedor],
                                                            backgroundColor: 'rgba(195, 202, 94, 0.6)', // Color de relleno azul
                                                            borderColor: 'rgb(54, 162, 235)',           // Color del borde
                                                            borderWidth: 1
                                                        },
                                                        {
                                                            label: 'Ocupacion',
                                                            data: [dentro],
                                                            backgroundColor: '#9696dd', // Color de relleno azul                                                            
                                                            borderWidth: 1
                                                        }

                                            ]
                                            
                                        },
                                        options: {
                                            responsive: true,
                                            scales: {
                                                x: {
                                                    stacked: false, // Cambia a true si quieres barras una encima de otra
                                                    title: {
                                                        display: true,
                                                        text: 'Hora del día'
                                                    }
                                                },
                                                y: {
                                                    beginAtZero: true,
                                                    // max: 100, // Si quieres mantener el tamaño máximo que definimos antes
                                                    title: {
                                                        display: true,
                                                        text: 'Número de fichajes'
                                                    },
                                                    ticks: {
                                                        precision: 0
                                                    }
                                                }
                                            },
                                            plugins: {
                                                title: {
                                                    display: true,
                                                    text: 'Valores Maximos Fichajes y ocupacion'
                                                }
                                            }
                                        }
                                    });

    }

const fichajesmediahora = async function(ahora) {

    if (ahora === null){
        var  ahora = new Date().toISOString().split('T')[0];
    }
    
    var  resp = await fetch(`/api/fichajesmediahora?fecha=` + ahora);
    var  data = await resp.json();
    

    entradas = data.entradas;
    salidas = data.salidas;
    labels = data.labels;
    dentro = data.personas_dentro;
    
    const ctx = document.getElementById('fichajesChart');

    //Si ya existe un gráfico, lo destruimos
    if (myChartInstance) {
        myChartInstance.destroy();
    }

     myChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
            {
                label: 'Entradas',
                data: entradas,
                borderWidth: 2,
                tension: 0,
                borderColor: '#1fe270',

            },
            {
                label: 'Salidas',
                data: salidas,
                borderWidth: 2,
                tension: 0,
                borderColor: '#ff0000',
            },
            {
                label: 'Ocupacion',
                data: dentro,
                borderWidth: 2,
                tension: 0, 
                borderColor: '#9696dd',
            }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Fichajes de entrada y salida durante el día'
            },
            tooltip: {
                callbacks: {
                label: function(context) {
                    return `${context.dataset.label}: ${context.raw} `;
                }
                }
            }
            },
            scales: {
            x: {                
                title: {
                display: true,
                text: 'Hora del día'
                }
            },
            y: {                
                beginAtZero: true,
                title: {
                display: true,
                text: 'Número de fichajes'
                },
                ticks: {
                precision: 0
                }
            }
            }
        }
        });

  /*  */

}


function runGetData(ahora){

    fichajesComerdor(ahora)
    fichajesmediahora(ahora);
    totalizadorFichajes(ahora)
}

window.onload = function() {     
    ahora = new Date().toISOString().split('T')[0];
    runGetData(ahora)
   fieldFechaDesde.value = ahora;
}

    