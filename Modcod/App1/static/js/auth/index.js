const toggles = document.querySelectorAll(".toggle-password");

toggles.forEach((icon) => {
    icon.addEventListener("click", () => {
        const input = icon.previousElementSibling; 
        if (input.type === "password") {
            input.type = "text";
            icon.classList.remove("fa-eye-slash");
            icon.classList.add("fa-eye");
        } else {
            input.type = "password";
            icon.classList.remove("fa-eye");
            icon.classList.add("fa-eye-slash");
        }
    });
});
