console.log("Material Master JS Loaded");

const API_BASE = "/material-master";
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

// ======================================================
// Edit Material
// ======================================================

document.querySelectorAll(".editMaterialBtn").forEach(button => {

    button.addEventListener("click", function () {

        console.log("Edit clicked");
        console.log(this.dataset);

        editingMaterialId = this.dataset.id;

        modalTitle.innerText = "Edit Material";

        saveMaterialBtn.innerText = "Update Material";

        document.getElementById("materialName").value =
            this.dataset.name;

        document.getElementById("categoryId").value =
            this.dataset.category;

        document.getElementById("subcategoryId").value =
            this.dataset.subcategory;

        document.getElementById("description").value =
            this.dataset.description;

        document.getElementById("defaultUnit").value =
            this.dataset.unit;

        document.getElementById("preferredBrand").value =
            this.dataset.brand;

        document.getElementById("gstPercentage").value =
            this.dataset.gst;

        document.getElementById("hsnCode").value =
            this.dataset.hsn;

        document.getElementById("isActive").checked =
            this.dataset.active === "true";

        materialModal.show();

    });

});

// ======================================================
// Build Material Payload
// ======================================================

function getMaterialPayload() {

    return {

        material_code: null,

        material_name:
            document
                .getElementById("materialName")
                .value
                .trim(),

        category_id:
            Number(
                document
                    .getElementById("categoryId")
                    .value
            ),

        subcategory_id:

            document
                .getElementById("subcategoryId")
                .value

                ?

                Number(

                    document
                        .getElementById("subcategoryId")
                        .value

                )

                :

                null,

        description:

            document
                .getElementById("description")
                .value
                .trim()

                ||

                null,

        default_unit:

            document
                .getElementById("defaultUnit")
                .value,

        preferred_brand:

            document
                .getElementById("preferredBrand")
                .value

                ||

                null,

        gst_percentage:

            document
                .getElementById("gstPercentage")
                .value

                ?

                Number(

                    document
                        .getElementById("gstPercentage")
                        .value

                )

                :

                null,

        hsn_code:

            document
                .getElementById("hsnCode")
                .value
                .trim()

                ||

                null,

        is_active:

            document
                .getElementById("isActive")
                .checked

    };

}

// ======================================================
// AJAX Create Material
// ======================================================

saveMaterialBtn.addEventListener("click", async function () {
    console.log("Save button clicked");

    if (!materialForm.checkValidity()) {
        materialForm.reportValidity();
        return;
    }

    saveMaterialBtn.disabled = true;
    saveMaterialBtn.innerHTML =
        '<span class="spinner-border spinner-border-sm"></span> Saving...';

    const payload = getMaterialPayload();

    try {

        const url = editingMaterialId
            ? `${API_BASE}/${editingMaterialId}`
            : `${API_BASE}/`;

        const method = editingMaterialId
            ? "PUT"
            : "POST";

        const response = await fetch(url, {

            method: method,

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(payload)

   });

        const data = await response.json();

        console.log("Response:", data);

        if (!response.ok) {

            console.error("Validation Error:", data);

            alert(JSON.stringify(data, null, 2));

            return;

        }

        alert(
            editingMaterialId
            ? "Material updated successfully."
            : "Material created successfully."
        );

        materialModal.hide();

        materialForm.reset();

        editingMaterialId = null;

        modalTitle.innerText = "Add Material";

        saveMaterialBtn.innerText = "Save Material";

        location.reload();

    }
    catch (error) {

        alert(error.message);

    }
    finally {

        saveMaterialBtn.disabled = false;

        saveMaterialBtn.innerHTML = "Save Material";

    }

});

console.log(document.querySelectorAll(".editMaterialBtn"));

// ======================================================
// Delete Material
// ======================================================

document.querySelectorAll(".deleteMaterialBtn").forEach(button => {

    button.addEventListener("click", async function () {

        console.log("Delete clicked");

        const materialId = this.dataset.id;
        const materialName = this.dataset.name;

        const confirmed = confirm(
            `Are you sure you want to delete "${materialName}"?`
        );

        if (!confirmed) {
            return;
        }

        try {

            const response = await fetch(
                `${API_BASE}/${materialId}`,
                {
                    method: "DELETE"
                }
            );

            const data = await response.json();

            if (!response.ok) {

                alert(data.detail || "Unable to delete material.");

                return;

            }

            alert(data.message);

            this.closest("tr").remove();

        }

        catch (error) {

            console.error(error);

            alert("Something went wrong while deleting.");

        }

    });

});