        const navbarToggle = document.getElementById('navbarToggle');
        const navbar = document.getElementById('navbar');
        const navbarOverlay = document.getElementById('navbarOverlay');
        const mainContent = document.getElementById('mainContent');

        navbarToggle.addEventListener('click', function() {
            navbar.classList.toggle('active');
            navbarOverlay.classList.toggle('active');
        });

        navbarOverlay.addEventListener('click', function() {
            navbar.classList.remove('active');
            navbarOverlay.classList.remove('active');
        });

        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                navLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
                
                if (window.innerWidth <= 768) {
                    navbar.classList.remove('active');
                    navbarOverlay.classList.remove('active');
                }
            });
        });

        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                navbar.classList.remove('active');
                navbarOverlay.classList.remove('active');
            }
        });