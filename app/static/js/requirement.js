document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("requirementForm");

    if (form) {

        form.addEventListener(
            "submit",
            createRequirement
        );

    }

});


async function createRequirement(event) {

    event.preventDefault();

    const data = {

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

            body: JSON.stringify(data)

        }

    );

    if (response.ok) {

        const requirement = await response.json();

        window.location.href =
            "/dashboard/requirements/" +
            requirement.id;

    }

    else {

        alert("Unable to create requirement.");

    }

}