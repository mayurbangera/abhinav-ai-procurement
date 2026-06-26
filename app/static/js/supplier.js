document.addEventListener("DOMContentLoaded", () => {

    const approveButton = document.getElementById("approve-btn");
    const rejectButton = document.getElementById("reject-btn");

    if (approveButton) {
        approveButton.addEventListener("click", approveSupplier);
    }

    if (rejectButton) {
        rejectButton.addEventListener("click", rejectSupplier);
    }

});


async function approveSupplier() {

    const confirmed = confirm(
        "Approve this supplier?"
    );

    if (!confirmed) {
        return;
    }

    const supplierId = window.location.pathname.split("/").pop();

    const response = await fetch(
        `/suppliers/${supplierId}/approve`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                remarks: "Approved from Dashboard"
            })
        }
    );

    if (response.ok) {

        alert("Supplier Approved Successfully.");

        window.location.href = "/dashboard/";

    } else {

        alert("Failed to approve supplier.");

    }

}


async function rejectSupplier() {

    const confirmed = confirm(
        "Reject this supplier?"
    );

    if (!confirmed) {
        return;
    }

    const supplierId = window.location.pathname.split("/").pop();

    const response = await fetch(
        `/suppliers/${supplierId}/reject`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                remarks: "Rejected from Dashboard"
            })
        }
    );

    if (response.ok) {

        alert("Supplier Rejected Successfully.");

        window.location.href = "/dashboard/";

    } else {

        alert("Failed to reject supplier.");

    }

}