<template>
  <div class="container min-vh-100 d-flex align-items-center justify-content-center py-5">
    <div class="row justify-content-center w-100">
      <div class="col-md-7 col-lg-6">
        <div class="card shadow border-0">
          <div class="card-body p-4 p-md-5">
            <h2 class="text-center mb-2">Create Account</h2>
            <p class="text-center text-muted mb-4">
              Register as a trekker and start exploring
            </p>

            <div
              v-if="errorMessage"
              class="alert alert-danger"
            >
              {{ errorMessage }}
            </div>

            <form @submit.prevent="register">
              <div class="mb-3">
                <label for="name" class="form-label">
                  Full Name
                </label>

                <input
                  id="name"
                  v-model.trim="name"
                  type="text"
                  class="form-control"
                  required
                />
              </div>

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

              <div class="mb-3">
                <label for="phone" class="form-label">
                  Phone Number
                </label>

                <input
                  id="phone"
                  v-model.trim="phone"
                  type="tel"
                  class="form-control"
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
                  minlength="6"
                  required
                />

                <div class="form-text">
                  Password must be at least 6 characters.
                </div>
              </div>

              <button
                type="submit"
                class="btn btn-success w-100"
                :disabled="loading"
              >
                {{ loading ? 'Creating Account...' : 'Register' }}
              </button>
            </form>

            <p class="text-center mt-4 mb-0">
              Already have an account?
              <RouterLink to="/login">
                Login
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
  name: 'RegisterView',

  data() {
    return {
      name: '',
      email: '',
      phone: '',
      password: '',
      errorMessage: '',
      loading: false
    }
  },

  methods: {
    async register() {
      this.errorMessage = ''
      this.loading = true

      try {
        await api.post('/auth/register', {
          name: this.name,
          email: this.email,
          phone: this.phone,
          password: this.password
        })

        this.$router.push({
          path: '/login',
          query: {
            registered: 'true'
          }
        })
      } catch (error) {
        this.errorMessage =
          error.response?.data?.message || 'Unable to register'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>