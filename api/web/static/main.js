
const filterForm = document.getElementById("filter-form");
const btnRefresh = document.getElementById("btn-refresh");
const btnHoy = document.getElementById("buscar-hoy");
const btnAyer = document.getElementById("buscar-ayer"); 


filterForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearAllResults()
  const formData = new FormData(e.target);

  const params = new URLSearchParams();
  for (const [key, value] of formData) {
    if (value) params.append(key, value);
  }

  
  const resp = await fetch(`/api/indice?${params}`);
  const data = await resp.json(); 

  const resultsEl = document.getElementById("results");

  let lastDate = null;

  resultsEl.innerHTML = data
  .map(r => {

    const currentDate = r.datetime.split(' ')[0]; 
    const separator = lastDate !== null && lastDate !== currentDate
          ? "<br><div class='text-center my-2'><strong>" + currentDate + "</strong></div><hr>"
          : "";

    lastDate = currentDate;

    const rowClass =
      r.codigo === "01"
        ? "entrada"
        : r.codigo === "51"
        ? "salida"
        : r.codigo === "02"
        ? "taberu"
        : "nada"; // clase por defecto si no es ni 1 ni 51


    const acceso = r.Access_id === null
      ? ""
      : r.Access_id !== null && r.emp_id !== null
      ? `${r.Access_id} - ${r.emp_id}`
      : "Desconocido";
    
    const fullName = 
      r.Nombre === null || r.Apellido === null
        ? ""
        : r.Nombre !== null || r.Apellido !== null
        ? `${r.Nombre} ${r.Apellido}`
        : "";

    const showButton = r.emp_id === null 
    ? "no-display"
    : "";
 
    return `
      ${separator}
      <div class="row m-1 p-1 align-items-start ${rowClass}">
        <div class='col-1'>${r.dni}</div>
        <div class='col-1'>${acceso}</div>
        <div class='col-1'>${r.num_empleado}</div>
        <div class='col-2'>${fullName}</div>
        <div class='col-2'>${r.datetime}</div>
        <div class='col'>${r.codigo}</div>
        <div class='col'>${r.codificado}</div>
        <div class='col-1'>${r.maquina}</div>
        <div class='col'>${r.nombre_archivo.replaceAll('Movimientos', '').replaceAll('.txt', '')}</div>
        <div class='col-1 pt-2 text-end'><button type="button" class="btn btn-success ${showButton} " onclick="getEmpleadoShifts(${r.emp_id}, '${r.datetime.split(' ')[0].replaceAll('/', '-')}', '${r.datetime.split(' ')[0].replaceAll('/', '-')}')"> 
          <svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-info-circle' viewBox='0 0 16 16'>
            <path d='M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16'/>
            <path d='m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0'/>
          </svg> </button></div>
      </div>
    `;

    /*<div class='col'><a href="javascript:getEmpleadoShifts(${r.emp_id}, '${r.datetime.split(' ')[0].replaceAll('/', '-')}', '${r.datetime.split(' ')[0].replaceAll('/', '-')}')">${r.nombre_archivo.replaceAll('Movimientos', '').replaceAll('.txt', '')}</a></div>*/

  })
  .join("");
});


function getEmpleadoShifts(idEmpleado, fechaInicio, fechaFin) {
    resp = fetch(`/api/empleadoShifts?idEmpleado=${idEmpleado}&fechaInicio=${fechaInicio}&fechaFin=${fechaFin}`)
    .then(response => response.json())
    .then(data => {
      console.log('Shifts obtenidos:', data);
      appendShiftsModal(data);
     })
    .catch(error => console.error('Error al obtener los shifts del empleado:', error));
    
}


function appendShiftsModal(shifts) {
    const modalElement = document.getElementById('shiftsModalContent');
    const modalBody = modalElement.querySelector('.modal-body');  

    shifts = shifts['data'];
    
    if (shifts.length === 0) {
        modalBody.innerHTML = '<p>No se encontraron shifts para este empleado en las fechas seleccionadas.</p>';
    } else {

        var contenidoShifts = '';

        for(let i = 0; i < shifts.length; i++) {
            var s = shifts[i];

          contenidoShifts = contenidoShifts +  `
            <div class="shift-entry">
            
                <p><strong>Observaciones:</strong> ` +  s.observations + `</p>
                <p><strong>Shift ID:</strong> ` +  s.id + `</p>
                <p><strong>Start Time:</strong> ` + s.clock_in + `</p>
                <p><strong>End Time:</strong> ` + s.clock_out + `</p>
                <p><strong>Minutes:</strong> ` + s.minutes + `</p>
                

                <pre class="shift-details border text-success p-2"><strong>Detalles del Shift:</strong>` + JSON.stringify(s, null, 2) + `</pre>
                <hr>
            </div>`
       }     

       modalBody.innerHTML = contenidoShifts;

    }

      const modal = new bootstrap.Modal(modalElement);
      modal.show();
}





/*
btnRefresh.addEventListener("click", async function (e) {
    e.preventDefault();

    const resp = await fetch(`/api/actualizarHoy`);
    const data = await resp.json();
    // procesar data...
    appendAlert('Datos de hoy actualizados correctamente', 'success')
});
*/


btnRefresh.addEventListener("click", async function(){
    fieldFechaDesde = document.getElementById("field_fecha")
    theDay = fieldFechaDesde.value;

    var dd =  theDay.split('-')[2]
    var mm =  theDay.split('-')[1]
    var yyyy =  theDay.split('-')[0]
    var patronFichero = "Movimientos" + dd + "_" + mm  + "_" + yyyy + ".txt"
    var  resp = await fetch(`/api/actualizarFromFile?nombre_fichero=` + patronFichero);
    var  data = await resp.json();
  
    appendAlert('Datos del dia <b>' + dd + '-' + mm + '-' + yyyy + '</b> actualizados correctamente', 'success')

});




function obtenerFechaHoy() {
  const hoy = new Date();
  const dia = String(hoy.getDate()).padStart(2, '0');
  const mes = String(hoy.getMonth() + 1).padStart(2, '0'); // meses van de 0 a 11
  const año = hoy.getFullYear();
  return `${año}/${mes}/${dia}`;
}

function obtenerFechaHoyG() {
  const hoy = new Date();
  const dia = String(hoy.getDate()).padStart(2, '0');
  const mes = String(hoy.getMonth() + 1).padStart(2, '0'); // meses van de 0 a 11
  const año = hoy.getFullYear();
  console.log("Fecha hoy formateada:", `${año}-${mes}-${dia}`);
  return `${año}-${mes}-${dia}`;
}


function obtenerFechaAyer() {
  const ayer = new Date();
  ayer.setDate(ayer.getDate() - 1);
  const dia = String(ayer.getDate()).padStart(2, '0');
  const mes = String(ayer.getMonth() + 1).padStart(2, '0');
  const año = ayer.getFullYear();
  return `${año}/${mes}/${dia}`;
}

function obtenerFechaAyerG() {
  const ayer = new Date();
  ayer.setDate(ayer.getDate() - 1);
  const dia = String(ayer.getDate()).padStart(2, '0');
  const mes = String(ayer.getMonth() + 1).padStart(2, '0');
  const año = ayer.getFullYear();
  return `${año}-${mes}-${dia}`;
}



document.getElementById("buscar-hoy").addEventListener("click", function() {
    document.getElementById("field_fecha").value=obtenerFechaHoyG();
    document.getElementById("button_buscar").click();
});


document.getElementById("buscar-ayer").addEventListener("click", function() {
    document.getElementById("field_fecha").value=obtenerFechaAyerG()
    document.getElementById("button_buscar").click();
});






window.onload = function() {

  //alert("¡Bienvenido al sistema de control de accesos! Para comenzar, puedes usar los botones 'Buscar Hoy' o 'Buscar Ayer' para cargar los movimientos de esos días. También puedes aplicar filtros personalizados usando el formulario. Si necesitas actualizar los datos de los empleados, haz clic en 'Actualizar Usuarios'. ¡Explora y gestiona los accesos de manera eficiente!");


      document.getElementById("field_fecha").value=obtenerFechaHoyG();
      document.getElementById("button_buscar").click(); // Carga inicial de datos de hoy al abrir la página


      //btnAyer.click(); // Carga inicial de datos de ayer al abrir la página
      //filterForm.click(); // Carga inicial de datos al abrir la página
};
