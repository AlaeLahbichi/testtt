
        let currentEditingUser = null;
        let currentEditingProject = null;

        document.addEventListener('DOMContentLoaded', function() {
            updateStats();
            renderUsers();
            renderProjects();
        });

        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('sidebar-overlay');
            
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
        }

        function closeSidebar() {
            const sidebar = document.getElementById('sidebar');
            const overlay = document.getElementById('sidebar-overlay');
            
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        }

        function showSection(sectionName) {
            document.querySelectorAll('.content-section').forEach(section => {
                section.classList.add('hidden');
            });
            
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            
            document.getElementById(sectionName + '-section').classList.remove('hidden');
            
            event.target.closest('.nav-item').classList.add('active');
            
            if (window.innerWidth <= 767) {
                closeSidebar();
            }
        }

        window.addEventListener('resize', function() {
            if (window.innerWidth > 767) {
                closeSidebar();
            }
        });

        function showSection(sectionName) {
            document.querySelectorAll('.content-section').forEach(section => {
                section.classList.add('hidden');
            });
            
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            
            document.getElementById(sectionName + '-section').classList.remove('hidden');
            
            event.target.closest('.nav-item').classList.add('active');
        }

        function updateStats() {
            document.getElementById('total-users').textContent = users.length;
            document.getElementById('total-projects').textContent = projects.length;
            document.getElementById('active-users').textContent = users.filter(u => u.status === 'Actif').length;
            document.getElementById('completed-projects').textContent = projects.filter(p => p.status === 'Terminé').length;
        }

        function searchUsers(query) {
            const rows = document.querySelectorAll("#users-tbody tr");
            const lowerQuery = query.toLowerCase();
            rows.forEach(row => {
                const username = row.querySelector('.username')?.textContent.toLowerCase() || '';
                const match = [username].some(field => field.includes(lowerQuery));
                row.style.display = match ? '' : 'none';
            });
        }

        function closeUserModal() {
            document.getElementById('user-modal').style.display = 'none';
            currentEditingUser = null;
        }

        function searchProjects(query) {
            const rows = document.querySelectorAll("#projects-tbody tr");
            const lowerQuery = query.toLowerCase();
            rows.forEach(row => {
                const reference = row.querySelector('.reference')?.textContent.toLowerCase() || '';
                const reference_modcod = row.querySelector('.reference_modcod')?.textContent.toLowerCase() || '';
                const editeur = row.querySelector('.editeur')?.textContent.toLowerCase() || ''
                const match = [reference , reference_modcod , editeur].some(field => field.includes(lowerQuery));
                row.style.display = match ? '' : 'none';
            });
        }

        window.onclick = function(event) {
            const userModal = document.getElementById('user-modal');
            const projectModal = document.getElementById('project-modal');
            
            if (event.target == userModal) {
                closeUserModal();
            }
            if (event.target == projectModal) {
                closeProjectModal();
            }
        }