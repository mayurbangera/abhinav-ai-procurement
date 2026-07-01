document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("requirementForm");

    if (form) {

        form.addEventListener(
            "submit",
            saveRequirement
        );

    }

});


async function saveRequirement(event) {

    event.preventDefault();

    const body = {

        project_name:
            document.getElementById("project_name").value,

        site_name:
            document.getElementById("site_name").value,

        requested_by:
            document.getElementById("requested_by").value,

        priority:
            document.getElementById("priority").value,

        required_date:
            document.getElementById("required_date").value,

        purpose:
            document.getElementById("purpose").value,

        remarks:
            document.getElementById("remarks").value

    };

    const response = await fetch(
        "/requirements/",
        {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify(body)

        }
    );

    if (response.ok) {

        alert("Requirement Created Successfully.");

        window.location.href =
            "/dashboard/requirements";

    }

    else {

        alert("Failed to create requirement.");

    }

}