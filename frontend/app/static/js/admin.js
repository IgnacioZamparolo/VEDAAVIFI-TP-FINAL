const botonAgregarProd = document.getElementById("btn-agregar-menu")
const botonEliminarProd = document.getElementById("btn-eliminar-menu")
const botonEditarProd = document.getElementById("btn-editar-menu")

const formAgregarProd = document.getElementById("agregar_prod")
const formEliminarProd = document.getElementById("eliminar_prod")
const formEditarProd = document.getElementById("editar_prod")

const botonEditarCombo= document.getElementById("btn-editar-combo")
const botonEliminarCombo= document.getElementById("btn-eliminar-combo")
const botonAgregarCombo = document.getElementById("btn-agregar-combo")
const formAgregarCombo = document.getElementById("agregar_combo")
const formEliminarCombo = document.getElementById("eliminar_combo")
const formEditarCombo = document.getElementById("editar_combo")

const botonEditarCombov= document.getElementById("btn-editar-combo-version")
const botonEliminarCombov= document.getElementById("btn-eliminar-combo-version")
const botonAgregarCombov = document.getElementById("btn-agregar-combo-version")
const formAgregarCombov = document.getElementById("agregar_combo_version")
const formEliminarCombov = document.getElementById("eliminar_combo_version")
const formEditarCombov = document.getElementById("editar_combo_version")

const botonAgregarCombod = document.getElementById("btn-agregar-combo-detalle")
const formAgregarCombod = document.getElementById("agregar_combo_detalle")

const botonEliminarResenias = document.getElementById("btn-eliminar-resenia")
const formEliminarResenias = document.getElementById("eliminar_resenia")

const botonAgregarServicio = document.getElementById("btn-agregar-servicio")
const botonEliminarServicio = document.getElementById("btn-eliminar-servicio")
const botonEditarServicio = document.getElementById("btn-editar-servicio")

const formAgregarServicio = document.getElementById("agregar_servicio")
const formEliminarServicio = document.getElementById("eliminar_servicio")
const formEditarServicio = document.getElementById("editar_servicio")

if (botonEliminarResenias) {
    botonEliminarResenias.addEventListener("click", () =>{
        formEliminarResenias.style.display = 'block'
    })
}

if (botonAgregarServicio) {
    botonAgregarServicio.addEventListener("click", () =>{
        formAgregarServicio.style.display = 'block'
        formEditarServicio.style.display ='none'
        formEliminarServicio.style.display ='none'
    })
}

if (botonEditarServicio) {
    botonEditarServicio.addEventListener("click", () =>{
        formAgregarServicio.style.display = 'none'
        formEditarServicio.style.display ='block'
        formEliminarServicio.style.display ='none'
    })
}

if (botonEliminarServicio) {
    botonEliminarServicio.addEventListener("click", () =>{
        formAgregarServicio.style.display = 'none'
        formEditarServicio.style.display ='none'
        formEliminarServicio.style.display ='block'
    })
}

if (botonAgregarProd) {
    botonAgregarProd.addEventListener("click", () =>{
        formAgregarProd.style.display = 'block'
        formEditarProd.style.display ='none'
        formEliminarProd.style.display ='none'
    })
}

if (botonEditarProd) {
    botonEditarProd.addEventListener("click", () =>{
        formAgregarProd.style.display = 'none'
        formEditarProd.style.display ='block'
        formEliminarProd.style.display ='none'
    })
}
const inputIdProductoEditar = formEditarProd.querySelector('input[name="id_producto"]')
inputIdProductoEditar.addEventListener("input", () => {
    const id = inputIdProductoEditar.value
    formEditarProd.querySelector('form').action = `/productos/${id}/editar`
})

if (botonEliminarProd) {
    botonEliminarProd.addEventListener("click", () =>{
        formAgregarProd.style.display = 'none'
        formEditarProd.style.display ='none'
        formEliminarProd.style.display ='block'
    })
}
const inputIdProductoEliminar = formEliminarProd.querySelector('input[name="id_producto"]')
inputIdProductoEliminar.addEventListener("input", () => {
    const id = inputIdProductoEliminar.value
    formEliminarProd.querySelector('form').action = `/productos/${id}/eliminar`
})

if (botonEliminarCombo) {
    botonEliminarCombo.addEventListener("click", () =>{
        formAgregarCombo.style.display = 'none'
        formEditarCombo.style.display ='none'
        formEliminarCombo.style.display ='block'
    })
}
const inputIdComboEliminar = formEliminarCombo.querySelector('input[name="id_combo"]')
inputIdComboEliminar.addEventListener("input", () => {
    const id = inputIdComboEliminar.value
    formEliminarCombo.querySelector('form').action = `/combos/${id}/eliminar`
})

if (botonAgregarCombo) {
    botonAgregarCombo.addEventListener("click", () =>{
        formAgregarCombo.style.display = 'block'
        formEditarCombo.style.display ='none'
        formEliminarCombo.style.display ='none'
    })
}

if (botonEditarCombo) {
    botonEditarCombo.addEventListener("click", () =>{
        formAgregarCombo.style.display = 'none'
        formEditarCombo.style.display ='block'
        formEliminarCombo.style.display ='none'
    })
}
const inputIdComboEditar = formEditarCombo.querySelector('input[name="id_combo"]')
inputIdComboEditar.addEventListener("input", () => {
    const id = inputIdComboEditar.value
    formEditarCombo.querySelector('form').action = `/combos/${id}/editar`
})


if (botonAgregarCombod) {
    botonAgregarCombod.addEventListener("click", () =>{
        formAgregarCombod.style.display = 'block'
    })
}

if (botonEditarCombov) {
    botonEditarCombov.addEventListener("click", () =>{
        formAgregarCombov.style.display = 'none'
        formEditarCombov.style.display ='block'
        formEliminarCombov.style.display ='none'
    })
}
const inputIdVersionEditar = formEditarCombov.querySelector('input[name="id_version"]')
inputIdVersionEditar.addEventListener("input", () => {
    const id = inputIdVersionEditar.value
    formEditarCombov.querySelector('form').action = `/combo_version/${id}/editar`
})

if (botonAgregarCombov) {
    botonAgregarCombov.addEventListener("click", () =>{
        formAgregarCombov.style.display = 'block'
        formEditarCombov.style.display ='none'
        formEliminarCombov.style.display ='none'
    })
}

if (botonEliminarCombov) {
    botonEliminarCombov.addEventListener("click", () =>{
        formAgregarCombov.style.display = 'none'
        formEditarCombov.style.display ='none'
        formEliminarCombov.style.display ='block'
    })
}
const inputIdVersionEliminar = formEliminarCombov.querySelector('input[name="id_version"]')
inputIdVersionEliminar.addEventListener("input", () => {
    const id = inputIdVersionEliminar.value
    formEliminarCombov.querySelector('form').action = `/combo_version/${id}/eliminar`
})