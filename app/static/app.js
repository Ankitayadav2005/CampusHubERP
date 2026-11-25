
const configs = {
    students: {
        title: "Student Management",
        endpoint: "/students",
        id: "student_id",
        fields: [
            ["student_id", "Student ID", "text"],
            ["name", "Student Name", "text"],
            ["age", "Age", "number"],
            ["email", "Email", "email"],
            ["department", "Department", "text"]
        ],
        columns: ["student_id", "name", "age", "email", "department"],
        editFields: ["name"]
    },
    faculty: {
        title: "Faculty Management",
        endpoint: "/faculty",
        id: "faculty_id",
        fields: [
            ["faculty_id", "Faculty ID", "text"],
            ["name", "Faculty Name", "text"],
            ["age", "Age", "number"],
            ["email", "Email", "email"],
            ["department", "Department", "text"]
        ],
        columns: ["faculty_id", "name", "age", "email", "department"],
        editFields: ["name"]
    },
    courses: {
        title: "Course Management",
        endpoint: "/courses",
        id: "course_code",
        fields: [
            ["course_code", "Course Code", "text"],
            ["course_name", "Course Name", "text"],
            ["credits", "Credits", "number"]
        ],
        columns: ["course_code", "course_name", "credits"],
        editFields: ["course_name"]
    },
    enrollments: {
        title: "Enrollment Management",
        endpoint: "/enrollments",
        id: "enrollment_id",
        fields: [
            ["enrollment_id", "Enrollment ID", "text"],
            ["student_id", "Student ID", "text"],
            ["course_code", "Course Code", "text"]
        ],
        columns: ["enrollment_id", "student_id", "course_code"],
        editFields: ["student_id", "course_code"]
    }
};

let currentPage = "dashboard";
let records = [];
let editingRecord = null;

const $ = (id) => document.getElementById(id);

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[char]);
}

async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options.headers
        }
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.detail || data.message || "Something went wrong");
    }

    return data;
}

function showMessage(message, isError = false) {
    const box = $("message");
    box.textContent = message;
    box.style.color = isError ? "#d33b3b" : "#16834b";
}

function showPage(page) {
    currentPage = page;

    document.querySelectorAll(".nav-link").forEach(link => {
        link.classList.toggle("active", link.dataset.page === page);
    });

    $("dashboard-page").classList.toggle("hidden", page !== "dashboard");
    $("management-page").classList.toggle("hidden", page === "dashboard");

    if (page === "dashboard") {
        $("page-title").textContent = "Dashboard";
        loadDashboard();
        return;
    }

    const config = configs[page];

    if (!config) return;

    $("page-title").textContent = config.title;
    $("table-heading").textContent = config.title;
    $("add-button").textContent = "+ Add New";

    if ($("search-input")) {
        $("search-input").value = "";
    }

    loadRecords(page);
}

async function loadDashboard() {
    try {
        const [students, faculty, courses, enrollments] = await Promise.all([
            apiRequest("/students"),
            apiRequest("/faculty"),
            apiRequest("/courses"),
            apiRequest("/enrollments")
        ]);

        $("student-count").textContent = students.length;
        $("faculty-count").textContent = faculty.length;
        $("course-count").textContent = courses.length;
        $("enrollment-count").textContent = enrollments.length;

    } catch (error) {
        console.error("Dashboard error:", error);
    }
}

async function loadRecords(page) {
    const config = configs[page];

    try {
        records = await apiRequest(config.endpoint);
        renderTable(config);
        showMessage(`${records.length} records found.`);

    } catch (error) {
        $("table-body").innerHTML =
            `<tr><td colspan="10">Unable to load records.</td></tr>`;

        showMessage(error.message, true);
    }
}

// SEARCH AND FILTER TABLE
function renderTable(config) {
    $("table-head").innerHTML = `
        <tr>
            ${config.columns.map(column =>
                `<th>${escapeHTML(column.replaceAll("_", " ").toUpperCase())}</th>`
            ).join("")}
            <th>Actions</th>
        </tr>
    `;

    const searchText = $("search-input")
        ? $("search-input").value.toLowerCase().trim()
        : "";

    const filteredRecords = records
        .map((record, index) => ({ record, index }))
        .filter(item =>
            config.columns.some(column =>
                String(item.record[column] ?? "")
                    .toLowerCase()
                    .includes(searchText)
            )
        );

    if (filteredRecords.length === 0) {
        $("table-body").innerHTML = `
            <tr>
                <td colspan="${config.columns.length + 1}">
                    ${searchText ? "No matching records found." : "No records found."}
                </td>
            </tr>
        `;
        return;
    }

    $("table-body").innerHTML = filteredRecords.map(item => `
        <tr>
            ${config.columns.map(column =>
                `<td>${escapeHTML(item.record[column])}</td>`
            ).join("")}
            <td>
                <button class="edit-button" data-action="edit" data-index="${item.index}">
                    Edit
                </button>
                <button class="delete-button" data-action="delete" data-index="${item.index}">
                    Delete
                </button>
            </td>
        </tr>
    `).join("");
}

function openModal(record = null) {
    editingRecord = record;

    const config = configs[currentPage];
    const isEditing = Boolean(record);

    $("modal-title").textContent = isEditing ? "Edit Record" : "Add New Record";

    const fieldsToShow = isEditing
        ? config.editFields
        : config.fields.map(field => field[0]);

    $("form-fields").innerHTML = fieldsToShow.map(fieldName => {
        const field = config.fields.find(field => field[0] === fieldName);
        const value = isEditing ? record[fieldName] : "";
        const disabled = isEditing && fieldName === config.id;

        return `
            <label>
                ${escapeHTML(field[1])}
                <input
                    name="${escapeHTML(fieldName)}"
                    type="${field[2]}"
                    value="${escapeHTML(value)}"
                    ${disabled ? "disabled" : ""}
                    ${field[2] === "number" ? 'min="0"' : ""}
                    required
                >
            </label>
        `;
    }).join("");

    $("record-modal").classList.remove("hidden");
}

function closeModal() {
    $("record-modal").classList.add("hidden");
    $("record-form").reset();
    editingRecord = null;
}

async function saveRecord(event) {
    event.preventDefault();

    const config = configs[currentPage];
    const formData = new FormData($("record-form"));
    const data = Object.fromEntries(formData.entries());

    for (const field of config.fields) {
        if (field[2] === "number" && data[field[0]] !== undefined) {
            data[field[0]] = Number(data[field[0]]);
        }
    }

    try {
        if (editingRecord) {
            const recordId = encodeURIComponent(editingRecord[config.id]);

            await apiRequest(`${config.endpoint}/${recordId}`, {
                method: "PUT",
                body: JSON.stringify(data)
            });

            showMessage("Record updated successfully!");

        } else {
            await apiRequest(config.endpoint, {
                method: "POST",
                body: JSON.stringify(data)
            });

            showMessage("Record added successfully!");
        }

        closeModal();
        await loadRecords(currentPage);
        loadDashboard();

    } catch (error) {
        showMessage(error.message, true);
    }
}

async function deleteRecord(index) {
    const config = configs[currentPage];
    const record = records[index];

    if (!record) return;

    const recordId = record[config.id];

    if (!confirm(`Are you sure you want to delete ${recordId}?`)) {
        return;
    }

    try {
        await apiRequest(
            `${config.endpoint}/${encodeURIComponent(recordId)}`,
            { method: "DELETE" }
        );

        await loadRecords(currentPage);
        loadDashboard();
        showMessage("Record deleted successfully!");

    } catch (error) {
        showMessage(error.message, true);
    }
}

// SIDEBAR NAVIGATION
document.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", event => {
        event.preventDefault();
        showPage(link.dataset.page);
    });
});

// SEARCH INPUT EVENT
if ($("search-input")) {
    $("search-input").addEventListener("input", () => {
        const config = configs[currentPage];

        if (config) {
            renderTable(config);
        }
    });
}

// ADD NEW BUTTON
$("add-button").addEventListener("click", () => openModal());

$("close-modal").addEventListener("click", closeModal);

$("record-form").addEventListener("submit", saveRecord);

// EDIT AND DELETE BUTTONS
$("table-body").addEventListener("click", event => {
    const button = event.target.closest("button[data-action]");

    if (!button) return;

    const index = Number(button.dataset.index);

    if (button.dataset.action === "edit") {
        openModal(records[index]);
    }

    if (button.dataset.action === "delete") {
        deleteRecord(index);
    }
});

// CLOSE MODAL ON OUTSIDE CLICK
$("record-modal").addEventListener("click", event => {
    if (event.target === $("record-modal")) {
        closeModal();
    }
});

// START DASHBOARD
showPage("dashboard");

// CAMPUSHUB AUTHENTICATION

const authApi = async (url, data) => {
    const response = await fetch(url, {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.detail || "Something went wrong");
    }

    return result;
};

function switchAuthPanel(panel) {
    ["login", "register", "forgot", "reset"].forEach(name => {
        document.getElementById(name + "-panel")
            .classList.toggle("hidden", name !== panel);
    });

    document.getElementById("auth-screen").classList.remove("hidden");
    document.getElementById("app-container").classList.add("hidden");
}

function authMessage(id, message, success = false) {
    const element = document.getElementById(id);
    element.textContent = message;
    element.classList.toggle("success", success);
}

// AUTH PANEL LINKS
document.getElementById("show-register").addEventListener("click", e => {
    e.preventDefault();
    switchAuthPanel("register");
});

document.getElementById("show-login").addEventListener("click", e => {
    e.preventDefault();
    switchAuthPanel("login");
});

document.getElementById("show-forgot").addEventListener("click", e => {
    e.preventDefault();
    switchAuthPanel("forgot");
});

document.getElementById("back-to-login").addEventListener("click", e => {
    e.preventDefault();
    switchAuthPanel("login");
});

document.getElementById("reset-back-login").addEventListener("click", e => {
    e.preventDefault();
    switchAuthPanel("login");
});

// REGISTER
document.getElementById("register-form").addEventListener("submit", async e => {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(e.target).entries());

    try {
        const result = await authApi("/auth/register", data);

        e.target.reset();
        switchAuthPanel("login");
        authMessage("login-message", result.message, true);

    } catch (error) {
        authMessage("register-message", error.message);
    }
});

// LOGIN
document.getElementById("login-form").addEventListener("submit", async e => {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(e.target).entries());

    try {
        const result = await authApi("/auth/login", data);

        document.getElementById("logged-user").textContent = result.name;
        document.getElementById("auth-screen").classList.add("hidden");
        document.getElementById("app-container").classList.remove("hidden");

        if (typeof showPage === "function") {
            showPage("dashboard");
        }

    } catch (error) {
        authMessage("login-message", error.message);
    }
});

// FORGOT PASSWORD
document.getElementById("forgot-form").addEventListener("submit", async e => {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(e.target).entries());

    try {
        const result = await authApi("/auth/forgot-password", data);
        authMessage("forgot-message", result.message, true);

    } catch (error) {
        authMessage("forgot-message", error.message);
    }
});

// RESET PASSWORD
document.getElementById("reset-form").addEventListener("submit", async e => {
    e.preventDefault();

    const token = new URLSearchParams(location.search).get("token");

    if (!token) {
        authMessage("reset-message", "Reset link is missing.");
        return;
    }

    const data = Object.fromEntries(new FormData(e.target).entries());
    data.token = token;

    try {
        const result = await authApi("/auth/reset-password", data);

        history.replaceState({}, document.title, location.pathname);
        switchAuthPanel("login");
        authMessage("login-message", result.message, true);

    } catch (error) {
        authMessage("reset-message", error.message);
    }
});

// LOGOUT
document.getElementById("logout-button").addEventListener("click", async () => {
    try {
        await fetch("/auth/logout", {
            method: "POST",
            credentials: "same-origin"
        });

        location.reload();

    } catch (error) {
        alert("Logout failed.");
    }
});

// CHECK LOGIN SESSION
async function checkAuthSession() {
    const token = new URLSearchParams(location.search).get("token");

    if (token) {
        switchAuthPanel("reset");
        return;
    }

    try {
        const response = await fetch("/auth/me", {
            credentials: "same-origin"
        });

        if (!response.ok) throw new Error("Not logged in");

        const user = await response.json();

        document.getElementById("logged-user").textContent = user.name;
        document.getElementById("auth-screen").classList.add("hidden");
        document.getElementById("app-container").classList.remove("hidden");

        if (typeof showPage === "function") {
            showPage("dashboard");
        }

    } catch {
        switchAuthPanel("login");
    }
}

checkAuthSession();

// DOWNLOAD PDF REPORT
document.getElementById("download-pdf-button").addEventListener("click", () => {
    if (!configs[currentPage]) {
        alert("Please open a management section first.");
        return;
    }

    window.location.href = `/reports/${currentPage}/pdf`;
});


// DOWNLOAD EXCEL REPORT
document.getElementById("download-excel-button").addEventListener("click", () => {
    if (!configs[currentPage]) {
        alert("Please open a management section first.");
        return;
    }

    window.location.href = `/reports/${currentPage}/excel`;
});
