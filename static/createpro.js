// Obtener categorías desde el backend para llenar el select
fetch("/category")
  .then((response) => response.json())
  .then((categories) => {
    const categorySelect = document.getElementById("category");
    categories.forEach((category) => {
      const option = document.createElement("option");
      option.value = category.id;
      option.textContent = category.name;
      categorySelect.appendChild(option);
    });
  })
  .catch((error) => console.error("Error al cargar categorías:", error));

// Enviar formulario de productos
const productForm = document.getElementById("productForm");
productForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(productForm);

  try {
    const response = await fetch("/product/create", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      alert("Producto creado correctamente");
      productForm.reset();
    } else {
      const error = await response.json();
      alert(`Error al crear el producto: ${error.detail}`);
    }
  } catch (err) {
    console.error("Error al crear el producto:", err);
  }
});
