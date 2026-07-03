console.log("Material Master JS Loaded");
// ======================================================
// Material Master
// ======================================================

let editingMaterialId = null;

const materialModalElement = document.getElementById("materialModal");

const materialModal = new bootstrap.Modal(
    materialModalElement
);

const materialForm = document.getElementById("materialForm");

const modalTitle = document.getElementById(
    "materialModalTitle"
);

const addMaterialBtn = document.getElementById(
    "addMaterialBtn"
);

const saveMaterialBtn = document.getElementById(
    "saveMaterialBtn"
);


// ======================================================
// Open Modal
// ======================================================

addMaterialBtn.addEventListener(
    "click",
    () => {

        editingMaterialId = null;

        modalTitle.innerText = "Add Material";

        materialForm.reset();

        materialModal.show();

    }
);


// ======================================================
// Reset Modal
// ======================================================

materialModalElement.addEventListener(
    "hidden.bs.modal",
    () => {

        editingMaterialId = null;

        modalTitle.innerText = "Add Material";

        materialForm.reset();

        document
            .getElementById("newCategoryDiv")
            .classList.add("d-none");

        document
            .getElementById("newSubcategoryDiv")
            .classList.add("d-none");

        document
            .getElementById("newUnitDiv")
            .classList.add("d-none");

        document
            .getElementById("newBrandDiv")
            .classList.add("d-none");

    }
);

console.log(addMaterialBtn);