<template>
  <div class="container py-5">
    <div class="card shadow-sm">
      <div class="card-body">
        <h1>Trek Staff Dashboard</h1>

        <p class="text-muted">
          Welcome, {{ user.name }}. You are logged in as Trek Staff.
        </p>

        <button
          class="btn btn-danger"
          @click="logout"
        >
          Logout
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StaffDashboard',

  data() {
    return {
      user: JSON.parse(localStorage.getItem('user')) || {}
    }
  },

  methods: {
    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')

      this.$router.push('/login')
    }
  }
}
</script>