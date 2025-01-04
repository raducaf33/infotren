<template>
  <div class="admin-dashboard">
    <h1>Admin Dashboard</h1>
    <div class="admin-actions">
      <button @click="navigateTo('add-route')" class="btn btn-primary">Adaugă Rute Noi</button>
      <button @click="navigateTo('add-train')" class="btn btn-primary">Adaugă Trenuri Noi</button>
      <button @click="navigateTo('manage-ticket-category')" class="btn btn-primary">Adaugă/Editează TicketCategory</button>
      <button @click="navigateTo('manage-seats')" class="btn btn-primary">Adaugă/Editează Locuri</button>
      <button @click="navigateTo('view-users-tickets')" class="btn btn-primary">Vezi Utilizatori/Bilete Cumpărate</button>
    </div>
  </div>
</template>
  
  <script>
  import { useRouter } from 'vue-router';
  
  export default {
    data() {
      return {
        user: {
          first_name: localStorage.getItem('first_name'),
          last_name: localStorage.getItem('last_name'),
        },
      };
    },
    setup() {
      const router = useRouter();
  
      const logout = () => {
        localStorage.clear();
        router.push('/login');
      };
  
      return { logout };
    },
  };
  </script>

<style scoped>
.admin-dashboard {
  text-align: center;
  margin-top: 50px;
}

.admin-actions {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}

.btn {
  width: 300px;
  padding: 10px 20px;
  font-size: 16px;
}
</style>
  