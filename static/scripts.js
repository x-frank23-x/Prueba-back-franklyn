document.addEventListener("DOMContentLoaded", () => {
  const categorySelect = document.getElementById("category");
  const minPriceInput = document.getElementById("minPrice");
  const maxPriceInput = document.getElementById("maxPrice");
  const productTableBody = document.querySelector("#productTable tbody");
  const filterForm = document.getElementById("filterForm");
  const loadingIndicator = document.getElementById("loadingIndicator");
  const errorContainer = document.getElementById("errorContainer");

  // Mostrar o esconder el indicador de carga
  function showLoading(isLoading) {
    if (loadingIndicator) {
      loadingIndicator.style.display = isLoading ? "block" : "none";
    }
  }

  // Mostrar un mensaje de error
  function showError(message) {
    if (errorContainer) {
      errorContainer.textContent = message;
      errorContainer.style.display = "block";
    }
  }

  // Cargar categorías
  async function loadCategories() {
    try {
      const response = await fetch("/category");
      if (!response.ok) {
        throw new Error(`Error en la solicitud: ${response.status}`);
      }

      const categories = await response.json();
      categorySelect.innerHTML = "<option value=''>Todas</option>";
      categories.forEach((category) => {
        const option = document.createElement("option");
        option.value = category.id;
        option.textContent = category.name;
        categorySelect.appendChild(option);
      });
    } catch (error) {
      showError("Error al cargar las categorías.");
      console.error(error);
    }
  }

  // Cargar productos
  async function loadProducts(categoryId = "", minPrice = "", maxPrice = "") {
    try {
      showLoading(true);
      errorContainer.style.display = "none";

      let url = "/product";
      const params = new URLSearchParams();

      if (categoryId) params.append("category_id", categoryId);
      if (minPrice) params.append("min_price", minPrice);
      if (maxPrice) params.append("max_price", maxPrice);

      url += `?${params.toString()}`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`Error en la solicitud: ${response.status}`);
      }

      const products = await response.json();
      productTableBody.innerHTML = "";

      if (products.length === 0) {
        productTableBody.innerHTML =
          "<tr><td colspan='5'>No hay productos disponibles.</td></tr>";
        return;
      }

      products.forEach((product) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${product.id}</td>
            <td>${product.name}</td>
            <td>${product.description}</td>
            <td>$${product.price}</td>
            <td>${product.category_name}</td>
          `;
        productTableBody.appendChild(row);
      });
    } catch (error) {
      showError("Error al cargar los productos.");
      console.error(error);
    } finally {
      showLoading(false);
    }
  }

  // Evento de filtro
  filterForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const selectedCategory = categorySelect.value;
    const minPrice = minPriceInput.value;
    const maxPrice = maxPriceInput.value;
    loadProducts(selectedCategory, minPrice, maxPrice);
  });

  // Inicializar
  loadCategories();
  loadProducts();
});
