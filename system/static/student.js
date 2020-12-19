async function renderList() {
    let response = await fetch(`/api/student/list`);
    if (!response.ok) {
        console.error(response);
        return;
    }

    let data = await response.json();

    let tbodyEl = document.createElement("tbody");
    for (let item of data) {
        let trEl = document.createElement("tr");
        tbodyEl.append(trEl);

        let tdEl;
        tdEl = document.createElement("td");
        tdEl.innerText = item.stu_name;
        tdEl.className = "col-stu_name";
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "col-stu_no";
        tdEl.innerText = item.stu_no;
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "col-gender";
        tdEl.innerText = item.gender;
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "col-enrolled";
        tdEl.innerText = item.enrolled;
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "";
        trEl.append(tdEl);

        tdEl = document.createElement("td");
        tdEl.className = "ctrlbar";
        tdEl.append(renderRecordCtrlbar(item));
        trEl.append(tdEl);
    }

    let tableEl = document.querySelector("#student-table");
    document.querySelector("#student-table > tbody").remove();
    tableEl.append(tbodyEl);
}

function renderRecordCtrlbar(item) {
    let ctrlbarEl = document.createElement("div");

    let editBtn = document.createElement("a");
    editBtn.className = "btn";
    editBtn.innerText = "修改";
    editBtn.onclick = (e) => {
        openEditDialog(item);
    };
    ctrlbarEl.append(editBtn);

    let delBtn = document.createElement("a");
    delBtn.className = "btn";
    delBtn.innerText = "删除";
    delBtn.onclick = (e) => {
        openComfirmationDialog({
            message: `确定要删除“${item.stu_name}(#${item.stu_sn})”的信息？`,
            onOk: () => {
                (async () => {
                    let response = await fetch(`/api/student/${item.stu_sn}`, {
                        method: "DELETE",
                    });

                    if (!response.ok) {
                        console.error(response);
                    }

                    renderList();
                })();
            },
        });
    };
    ctrlbarEl.append(delBtn);

    return ctrlbarEl;
}

async function openEditDialog(item) {
    let dialog = document.querySelector(".student-editor");

    let dialogTitle = dialog.querySelector(".dialog-head");
    let form = dialog.querySelector("form");

    if (item) {
        dialogTitle.innerText = `修改学生信息 (#${item.stu_sn})`;
        form.elements.stu_sn.value = item.stu_sn ?? null;
        form.elements.stu_no.value = item.stu_no ?? "";
        form.elements.stu_name.value = item.stu_name ?? "";
        form.elements.gender.value = item.gender ?? "";
        form.elements.enrolled.value = item.enrolled ?? "";
    } else {
        dialogTitle.innerText = "新建学生信息";
        form.elements.stu_sn.value = null;
        form.elements.stu_no.value = "";
        form.elements.stu_name.value = "";
        form.elements.gender.value = "";
        form.elements.enrolled.value = "";
    }

    if (dialog.classList.contains("open")) {
        dialog.classList.remove("open");
    } else {
        dialog.classList.add("open");
    }
}

async function renderEditDialog() {
    let newStudentBtn = document.querySelector(".paper #new-btn");
    newStudentBtn.onclick = (e) => {
        openEditDialog();
    };

    let dialog = document.querySelector(".student-editor");

    let form = dialog.querySelector("form");

    let close_btn = dialog.querySelector("#close-btn");

    let closeDialog = () => {
        dialog.classList.remove("open");
    };

    close_btn.onclick = closeDialog;

    let save_btn = dialog.querySelector("#save-btn");
    save_btn.onclick = (e) => {
        let data = {
            stu_sn: form.elements.stu_sn.value,
            stu_no: form.elements.stu_no.value,
            stu_name: form.elements.stu_name.value,
            gender: form.elements.gender.value,
            enrolled: form.elements.enrolled.value,
        };

        if (!data.stu_sn) {
            // 异步执行POST请求操作
            (async () => {
                let response = await fetch("/api/student", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json;charset=utf-8",
                    },
                    body: JSON.stringify(data),
                });

                if (!response.ok) {
                    console.error(response);
                    return;
                }
                closeDialog();
                renderList();
            })();
        } else {
            // 异步执行PUT请求操作
            (async () => {
                let response = await fetch(`/api/student/${data.stu_sn}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json;charset=utf-8",
                    },
                    body: JSON.stringify(data),
                });

                if (!response.ok) {
                    console.error(response);
                    return;
                }
                closeDialog();
                renderList();
            })();
        }
    };
}

async function openComfirmationDialog({ message, onOk, onCancel }) {
    let dialog = document.querySelector(".comfirmation-dialog");

    let closeDialog = () => {
        dialog.classList.remove("open");
    };

    let okBtn = dialog.querySelector("#ok-btn");
    okBtn.onclick = (e) => {
        if (typeof onOk === "function") {
            onOk();
        }

        closeDialog();
    };

    let cancelBtn = dialog.querySelector("#cancel-btn");
    cancelBtn.onclick = (e) => {
        if (typeof onCancel === "function") {
            onCancel();
        }

        closeDialog();
    };

    let messageEl = dialog.querySelector("#message");
    messageEl.innerText = message;

    dialog.classList.add("open");
}

document.addEventListener("DOMContentLoaded", (e) => {
    renderList();
    renderEditDialog();
});
