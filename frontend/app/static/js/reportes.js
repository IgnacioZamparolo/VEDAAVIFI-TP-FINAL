document.addEventListener("DOMContentLoaded", () => {
  const boton = document.getElementById("btnDescargarReporte");

  if (!boton) return;

  boton.addEventListener("click", async () => {
    try {
      boton.disabled = true;
      boton.innerText = "Generando PDF...";

      const response = await fetch("/admin/reportes/estadisticas");

      if (!response.ok) {
        throw new Error("No se pudieron obtener las estadísticas");
      }

      const datos = await response.json();

      const { jsPDF } = window.jspdf;
      const pdf = new jsPDF();

      const fechaActual = new Date().toLocaleDateString("es-AR");

      // Título
      pdf.setFontSize(18);
      pdf.text("Reporte de Estadísticas", 14, 20);

      pdf.setFontSize(11);
      pdf.text("Parrilla Argentina", 14, 28);
      pdf.text(`Fecha de generación: ${fechaActual}`, 14, 35);

      // Resumen general
      pdf.setFontSize(14);
      pdf.text("Resumen general", 14, 50);

      pdf.autoTable({
        startY: 56,
        head: [["Indicador", "Cantidad"]],
        body: [
          ["Total de reservas", datos.total_reservas],
          ["Total de productos", datos.total_productos],
          ["Total de reseñas", datos.total_resenias],
          ["Total de combos", datos.total_combos]
        ]
      });

      // Reservas por estado
      pdf.setFontSize(14);
      pdf.text("Reservas por estado", 14, pdf.lastAutoTable.finalY + 15);

      pdf.autoTable({
        startY: pdf.lastAutoTable.finalY + 20,
        head: [["Estado", "Cantidad"]],
        body: [
          ["Pendientes", datos.reservas_por_estado.pendientes],
          ["Confirmadas", datos.reservas_por_estado.confirmadas],
          ["Canceladas", datos.reservas_por_estado.canceladas],
          ["Finalizadas", datos.reservas_por_estado.finalizadas],
          ["Vencidas", datos.reservas_por_estado.vencidas]
        ]
      });

      // Productos por categoría
      pdf.setFontSize(14);
      pdf.text("Productos por categoría", 14, pdf.lastAutoTable.finalY + 15);

      pdf.autoTable({
        startY: pdf.lastAutoTable.finalY + 20,
        head: [["Categoría", "Cantidad"]],
        body: datos.productos_por_categoria.map(item => [
          item.categoria,
          item.cantidad
        ])
      });

      // Reservas por día
      pdf.setFontSize(14);
      pdf.text("Reservas por día", 14, pdf.lastAutoTable.finalY + 15);

      pdf.autoTable({
        startY: pdf.lastAutoTable.finalY + 20,
        head: [["Día", "Cantidad"]],
        body: datos.reservas_por_dia.map(item => [
          item.dia,
          item.cantidad
        ])
      });

      // Horario más reservado
      let yFinal = pdf.lastAutoTable.finalY + 15;

      pdf.setFontSize(14);
      pdf.text("Horario más reservado", 14, yFinal);

      pdf.setFontSize(11);

      if (datos.horario_mas_reservado) {
        pdf.text(
          `Horario: ${datos.horario_mas_reservado.horario} - Cantidad de reservas: ${datos.horario_mas_reservado.cantidad}`,
          14,
          yFinal + 8
        );
      } else {
        pdf.text("No hay reservas registradas.", 14, yFinal + 8);
      }

      // Descargar PDF
      pdf.save("reporte-estadisticas.pdf");

    } catch (error) {
      console.error(error);
      alert("Ocurrió un error al generar el PDF.");
    } finally {
      boton.disabled = false;
      boton.innerText = "Descargar reporte PDF";
    }
  });
});