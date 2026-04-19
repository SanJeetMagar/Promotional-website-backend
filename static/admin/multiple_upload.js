document.addEventListener("DOMContentLoaded", function () {
    const input = document.querySelector("input[type='file'][name='image_url']");
    if (input) {
        input.setAttribute("multiple", "multiple");
    }
});
