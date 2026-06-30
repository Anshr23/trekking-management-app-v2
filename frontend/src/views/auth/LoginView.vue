<template>
  <div class="container min-vh-100 d-flex align-items-center justify-content-center">
    <div class="row justify-content-center w-100">
      <div class="col-md-6 col-lg-5">
        <div class="card shadow border-0">
          <div class="card-body p-4 p-md-5">
            <h2 class="text-center mb-2">Welcome Back</h2>
            <p class="text-center text-muted mb-4">
              Login to your trekking account
            </p>

            <div
              v-if="errorMessage"
              class="alert alert-danger"
            >
              {{ errorMessage }}
            </div>

            <form @submit.prevent="login">
              <div class="mb-3">
                <label for="email" class="form-label">
                  Email Address
                </label>

                <input
                  id="email"
                  v-model.trim="email"
                  type="email"
                  class="form-control"
                  required
                />
              </div>

              <div class="mb-4">
                <label for="password" class="form-label">
                  Password
                </label>

                <input
                  id="password"
                  v-model="password"
                  type="password"
                  class="form-control"
                  required
                />
              </div>

              <button
                type="submit"
                class="btn btn-primary w-100"
                :disabled="loading"
              >
                {{ loading ? 'Logging in...' : 'Login' }}
              </button>
            </form>

            <p class="text-center mt-4 mb-0">
              New trekker?
              <RouterLink to="/register">
                Create an account
              </RouterLink>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api'

export default {
  name: 'LoginView',

  data() {
    return {
      email: '',
      password: '',
      errorMessage: '',
      loading: false
    }
  },

  methods: {
    async login() {
      this.errorMessage = ''
      this.loading = true

      try {
        const response = await api.post('/auth/login', {
          email: this.email,
          password: this.password
        })

        const token = response.data.access_token
        const user = response.data.user

        localStorage.setItem('access_token', token)
        localStorage.setItem('user', JSON.stringify(user))

        if (user.role === 'admin') {
          this.$router.push('/admin/dashboard')
        } else if (user.role === 'staff') {
          this.$router.push('/staff/dashboard')
        } else {
          this.$router.push('/trekker/dashboard')
        }
      } catch (error) {
        this.errorMessage =
          error.response?.data?.message || 'Unable to login'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>