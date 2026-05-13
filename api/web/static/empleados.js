

/* empleados.js */
const filterForm = document.getElementById("filter-form");
const btnFilter = document.getElementById("filterBtn");
const updateUsersBtn = document.getElementById("updateUsersBtn");

updateUsersBtn.addEventListener("click", async (e) => { 
    e.preventDefault();

        if(confirm("¿Estás seguro de que deseas actualizar los usuarios? Esto puede tardar.")) {
            const resp = await fetch(`/api/insertAllEmpleados`);
            const data = await resp.json();
            console.log(data);
            alert("Usuarios actualizados correctamente.");
        }

    const resp = await fetch(`/api/insertAllEmpleados`);
    const data = await resp.json();
    console.log(data);
});


btnFilter.addEventListener("click", async (e) => {
    e.preventDefault();
    clearAllResults();
    clearTableBodyAllResults();

    const formData = new FormData(filterForm);
    const params = new URLSearchParams();
    for (const [key, value] of formData) {
        if (value) params.append(key, value);
    }

        const resp = await fetch(`/api/empleados?${params}`);
        const data = await resp.json(); 
        const resultsEl = document.getElementById("empleadosTableBody");     
        myData = data['data'];

        resultsEl.innerHTML = myData.map(r => {

            const fullName = 
            r.full_name === null 
              ? "Nombre no disponible"
                : r.full_name;

            const activo = 
            r.active === null
              ? "Desconocido"
              : r.active === true
                ? "<span class='badge bg-success'>Activo</span>"
                 : "<span class='badge bg-danger'>Inactivo</span>";

            return `
             <tr>
                <td>${r.id}</td>
                <td>${fullName}</td>
                <td>${r.email}</td>
                <td>${activo}</td>
                <td>${r.terminated_on || ''}</td>
                <td>
                    <button type="button" class="btn btn-info text-primary" onclick="getEmpleadoInfo(${r.id})"> 
                    <svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-info-circle' viewBox='0 0 16 16'>
                        <path d='M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16'/>
                        <path d='m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0'/>
                    </svg>
                    </button>
                </td>
            </tr>
            `;
        });
});


const getEmpleadoInfo = async function(empId) {
    const resp = await fetch(`/api/empleado?id=${empId}`);
    const data = await resp.json();
    await appendEmpleadosModal(data);
}

const calculateStep = function(){
    const stepInput = document.getElementById("step");
    const stepValue = parseInt(stepInput.value, 10);
    return isNaN(stepValue) || stepValue <= 0 ? 10 : stepValue;
}

const calculateOffset = function(){
    const stepInput = document.getElementById("step");
    const offsetInput = document.getElementById("offset");
    const offsetValue = parseInt(offsetInput.value, stepInput);
    return isNaN(offsetValue) || offsetValue < 0 ? 0 : offsetValue;
}

const moreResults = function(){
    const step = calculateStep();
    const offset = calculateOffset() + step;
    document.getElementById("offset").value = offset;
    btnFilter.click();
}

const lessResults = function(){
    const step = calculateStep();
    const offset = Math.max(calculateOffset() - step, 0);
    document.getElementById("offset").value = offset;
    btnFilter.click();
}

window.onload = function() {
        prevPageBtn = document.getElementById("prevPageBtn");
        nextPageBtn = document.getElementById("nextPageBtn");
        prevPageBtn.addEventListener("click", lessResults);
        nextPageBtn.addEventListener("click", moreResults);
        btnFilter.click(); // Carga inicial de datos al abrir la página
};

async function appendEmpleadosModal(data) {
    const modalElement = document.getElementById('EmpleadosModalContent');
    const modalBody = modalElement.querySelector('.modal-body');  

    myData = data;
        
    if (myData.length === 0) {
        modalBody.innerHTML = '<p>No se encontraron datos para el empleado seleccionado.</p>';
    } else {

        var contenidoShifts = '';       
          contenidoShifts = contenidoShifts +  `
            <div class="shift-entry">            
                <p><strong>Shift ID:</strong> ` +  myData.id + `</p>
                <p><strong>Nombre:</strong> ` +  myData.full_name + `</p>                
                <p><strong>Email:</strong> ` + myData.email + `</p>
                <p><strong>Terminando:</strong> ` + myData.is_terminating + `</p>
                <p><strong>Fecha de terminación:</strong> ` + myData.terminated_on + `</p> 
                <pre class="shift-details border text-success p-2"><strong>Detalles del Empleado:</strong>` + JSON.stringify(myData, null, 2) + `</pre>
                <hr>
            </div>`     

       modalBody.innerHTML = contenidoShifts;
    }

      const modal = new bootstrap.Modal(modalElement);
      modal.show();
}