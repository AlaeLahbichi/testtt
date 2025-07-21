    let currentRoleFilter = 'all';
    let currentSearchTerm = '';

    const membersGrid = document.getElementById('membersGrid');
    const searchInput = document.getElementById('searchInput');
    const roleButtons = document.querySelectorAll('.role-btn');
    const membersCount = document.getElementById('countText');
    const emptyState = document.getElementById('emptyState');
    const loading = document.getElementById('loading');

    function getMembersFromDOM() {
        const memberCards = Array.from(document.querySelectorAll('.member-card'));
        return memberCards.map(card => ({
            element: card,
            username: card.querySelector('.member-username').textContent.trim(),
            role: card.getAttribute('data-role').toLowerCase()
        }));
    }

    function renderMembers(filtered) {
        const allCards = document.querySelectorAll('.member-card');
        let count = 0;

        allCards.forEach(card => card.style.display = 'none');

        filtered.forEach(member => {
            member.element.style.display = 'block';
            count++;
        });

        if (count === 0) {
            membersGrid.style.display = 'none';
            emptyState.style.display = 'block';
        } else {
            membersGrid.style.display = 'grid';
            emptyState.style.display = 'none';
        }

        membersCount.textContent = `${count} membre${count !== 1 ? 's' : ''}`;
    }

    function filterMembers() {
        const members = getMembersFromDOM();
        const filtered = members.filter(member => {
            const matchesRole = currentRoleFilter === 'all' || member.role === currentRoleFilter;
            const matchesSearch = member.username.toLowerCase().includes(currentSearchTerm.toLowerCase());
            return matchesRole && matchesSearch;
        });

        loading.style.display = 'block';
        membersGrid.style.display = 'none';
        emptyState.style.display = 'none';

        setTimeout(() => {
            loading.style.display = 'none';
            renderMembers(filtered);
        }, 300);
    }

    roleButtons.forEach(button => {
        button.addEventListener('click', () => {
            roleButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            currentRoleFilter = button.dataset.role;
            filterMembers();
        });
    });

    searchInput.addEventListener('input', (e) => {
        currentSearchTerm = e.target.value;
        filterMembers();
    });

    document.addEventListener('DOMContentLoaded', () => {
        filterMembers();
    });