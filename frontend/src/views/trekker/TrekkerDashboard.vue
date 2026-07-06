<template>
  <div class="trekker-page">
    <nav class="navbar navbar-dark bg-success px-4">
      <span class="navbar-brand mb-0 h1">
        Trekking Management
      </span>

      <div class="d-flex align-items-center gap-3">
        <span class="text-light">
          {{ user.name }}
        </span>

        <button
          class="btn btn-outline-light btn-sm"
          @click="logout"
        >
          Logout
        </button>
      </div>
    </nav>

    <div class="container py-4">
      <div
        v-if="message"
        class="alert alert-success alert-dismissible"
      >
        {{ message }}

        <button
          type="button"
          class="btn-close"
          @click="message = ''"
        ></button>
      </div>

      <div
        v-if="errorMessage"
        class="alert alert-danger alert-dismissible"
      >
        {{ errorMessage }}

        <button
          type="button"
          class="btn-close"
          @click="errorMessage = ''"
        ></button>
      </div>

      <div class="d-flex flex-wrap gap-2 mb-4">
        <button
          class="btn"
          :class="activeSection === 'dashboard'
            ? 'btn-success'
            : 'btn-outline-success'"
          @click="openDashboard"
        >
          Dashboard
        </button>

        <button
          class="btn"
          :class="activeSection === 'treks'
            ? 'btn-success'
            : 'btn-outline-success'"
          @click="openTreks"
        >
          Explore Treks
        </button>

        <button
          class="btn"
          :class="activeSection === 'bookings'
            ? 'btn-success'
            : 'btn-outline-success'"
          @click="openBookings"
        >
          My Bookings
        </button>

        <button
          class="btn"
          :class="activeSection === 'history'
            ? 'btn-success'
            : 'btn-outline-success'"
          @click="openHistory"
        >
          Trekking History
        </button>

        <button
          class="btn"
          :class="activeSection === 'profile'
            ? 'btn-success'
            : 'btn-outline-success'"
          @click="openProfile"
        >
          My Profile
        </button>
      </div>

      <!-- Dashboard -->
      <section v-if="activeSection === 'dashboard'">
        <div class="mb-4">
          <h2>Welcome, {{ user.name }}</h2>

          <p class="text-muted">
            Discover new treks and manage your adventures.
          </p>
        </div>

        <div class="row g-3">
          <div
            v-for="card in dashboardCards"
            :key="card.label"
            class="col-md-6 col-lg-3"
          >
            <div class="card shadow-sm border-0 h-100">
              <div class="card-body">
                <p class="text-muted mb-2">
                  {{ card.label }}
                </p>

                <h2 class="mb-0">
                  {{ card.value }}
                </h2>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Available Treks -->
      <section v-if="activeSection === 'treks'">
        <h2 class="mb-4">Explore Available Treks</h2>

        <div class="card shadow-sm mb-4">
          <div class="card-body">
            <div class="row g-2">
              <div class="col-md-4">
                <input
                  v-model.trim="filters.search"
                  type="search"
                  class="form-control"
                  placeholder="Search trek or location"
                  @input="loadTreks"
                />
              </div>

              <div class="col-md-3">
                <select
                  v-model="filters.difficulty"
                  class="form-select"
                  @change="loadTreks"
                >
                  <option value="">All difficulties</option>
                  <option value="Easy">Easy</option>
                  <option value="Moderate">Moderate</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>

              <div class="col-md-3">
                <input
                  v-model.trim="filters.location"
                  class="form-control"
                  placeholder="Filter by location"
                  @input="loadTreks"
                />
              </div>

              <div class="col-md-2">
                <input
                  v-model="filters.max_duration"
                  type="number"
                  min="1"
                  class="form-control"
                  placeholder="Max days"
                  @input="loadTreks"
                />
              </div>
            </div>
          </div>
        </div>

        <div class="row g-4">
          <div
            v-for="trek in treks"
            :key="trek.id"
            class="col-md-6 col-lg-4"
          >
            <div class="card shadow-sm h-100">
              <div class="card-body d-flex flex-column">
                <div
                  class="d-flex justify-content-between
                         align-items-start mb-2"
                >
                  <h4 class="card-title mb-0">
                    {{ trek.name }}
                  </h4>

                  <span class="badge text-bg-success">
                    {{ trek.status }}
                  </span>
                </div>

                <p class="text-muted mb-2">
                  {{ trek.location }}
                </p>

                <p class="card-text flex-grow-1">
                  {{
                    trek.description ||
                    'No description available.'
                  }}
                </p>

                <div class="small mb-3">
                  <div>
                    <strong>Difficulty:</strong>
                    {{ trek.difficulty }}
                  </div>

                  <div>
                    <strong>Duration:</strong>
                    {{ trek.duration }} days
                  </div>

                  <div>
                    <strong>Dates:</strong>
                    {{ formatDate(trek.start_date) }}
                    to
                    {{ formatDate(trek.end_date) }}
                  </div>

                  <div>
                    <strong>Available Slots:</strong>
                    {{ trek.available_slots }}
                  </div>

                  <div>
                    <strong>Price:</strong>
                    ₹{{ trek.price }}
                  </div>

                  <div v-if="trek.altitude">
                    <strong>Altitude:</strong>
                    {{ trek.altitude }} ft
                  </div>
                </div>

                <button
                  class="btn btn-success w-100"
                  :disabled="trek.available_slots <= 0"
                  @click="bookTrek(trek)"
                >
                  {{
                    trek.available_slots > 0
                      ? 'Book Trek'
                      : 'Fully Booked'
                  }}
                </button>
              </div>
            </div>
          </div>

          <div
            v-if="treks.length === 0"
            class="col-12"
          >
            <div class="alert alert-info">
              No open treks match your search.
            </div>
          </div>
        </div>
      </section>

      <!-- My Bookings -->
      <section v-if="activeSection === 'bookings'">
        <h2 class="mb-4">My Bookings</h2>

        <div class="card shadow-sm">
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover align-middle">
                <thead>
                  <tr>
                    <th>Trek</th>
                    <th>Location</th>
                    <th>Trek Dates</th>
                    <th>Booked On</th>
                    <th>Status</th>
                    <th>Payment</th>
                    <th>Action</th>
                  </tr>
                </thead>

                <tbody>
                  <tr
                    v-for="booking in activeBookings"
                    :key="booking.id"
                  >
                    <td>
                      <strong>{{ booking.trek_name }}</strong>
                    </td>

                    <td>{{ booking.location }}</td>

                    <td>
                      {{ formatDate(booking.start_date) }}
                      -
                      {{ formatDate(booking.end_date) }}
                    </td>

                    <td>
                      {{ formatDate(booking.booking_date) }}
                    </td>

                    <td>
                      <span class="badge text-bg-primary">
                        {{ booking.status }}
                      </span>
                    </td>

                    <td>
                      {{ booking.payment_status }}
                    </td>

                    <td>
                      <button
                        v-if="booking.status === 'Booked'"
                        class="btn btn-sm btn-outline-danger"
                        @click="cancelBooking(booking)"
                      >
                        Cancel
                      </button>
                    </td>
                  </tr>

                  <tr v-if="activeBookings.length === 0">
                    <td
                      colspan="7"
                      class="text-center text-muted py-4"
                    >
                      You have no active bookings.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      <!-- History -->
      <section v-if="activeSection === 'history'">
        <h2 class="mb-4">Trekking History</h2>

        <div class="card shadow-sm">
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover align-middle">
                <thead>
                  <tr>
                    <th>Trek</th>
                    <th>Location</th>
                    <th>Dates</th>
                    <th>Booking Status</th>
                  </tr>
                </thead>

                <tbody>
                  <tr
                    v-for="booking in history"
                    :key="booking.id"
                  >
                    <td>
                      <strong>{{ booking.trek_name }}</strong>
                    </td>

                    <td>{{ booking.location }}</td>

                    <td>
                      {{ formatDate(booking.start_date) }}
                      -
                      {{ formatDate(booking.end_date) }}
                    </td>

                    <td>
                      <span
                        class="badge"
                        :class="booking.status === 'Completed'
                          ? 'text-bg-success'
                          : 'text-bg-secondary'"
                      >
                        {{ booking.status }}
                      </span>
                    </td>
                  </tr>

                  <tr v-if="history.length === 0">
                    <td
                      colspan="4"
                      class="text-center text-muted py-4"
                    >
                      No trekking history yet.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      <!-- Profile -->
      <section v-if="activeSection === 'profile'">
        <h2 class="mb-4">My Profile</h2>

        <div class="card shadow-sm profile-card">
          <div class="card-body">
            <form @submit.prevent="updateProfile">
              <div class="mb-3">
                <label class="form-label">
                  Full Name
                </label>

                <input
                  v-model.trim="profileForm.name"
                  class="form-control"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">
                  Email
                </label>

                <input
                  :value="user.email"
                  class="form-control"
                  disabled
                />
              </div>

              <div class="mb-3">
                <label class="form-label">
                  Phone
                </label>

                <input
                  v-model.trim="profileForm.phone"
                  class="form-control"
                />
              </div>

              <button
                type="submit"
                class="btn btn-success"
                :disabled="saving"
              >
                {{
                  saving
                    ? 'Saving...'
                    : 'Update Profile'
                }}
              </button>
            </form>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import api from '../../services/api'

export default {
  name: 'TrekkerDashboard',

  data() {
    const savedUser =
      JSON.parse(localStorage.getItem('user')) || {}

    return {
      user: savedUser,

      activeSection: 'dashboard',

      stats: {
        available_treks: 0,
        total_bookings: 0,
        active_bookings: 0,
        completed_treks: 0
      },

      treks: [],

      filters: {
        search: '',
        difficulty: '',
        location: '',
        max_duration: ''
      },

      bookings: [],
      history: [],

      profileForm: {
        name: savedUser.name || '',
        phone: savedUser.phone || ''
      },

      saving: false,
      message: '',
      errorMessage: ''
    }
  },

  computed: {
    dashboardCards() {
      return [
        {
          label: 'Available Treks',
          value: this.stats.available_treks
        },
        {
          label: 'Total Bookings',
          value: this.stats.total_bookings
        },
        {
          label: 'Active Bookings',
          value: this.stats.active_bookings
        },
        {
          label: 'Completed Treks',
          value: this.stats.completed_treks
        }
      ]
    },

    activeBookings() {
      return this.bookings.filter((booking) => {
        return booking.status === 'Booked'
      })
    }
  },

  async mounted() {
    await this.loadDashboard()
  },

  methods: {
    clearMessages() {
      this.message = ''
      this.errorMessage = ''
    },

    async openDashboard() {
      this.activeSection = 'dashboard'
      await this.loadDashboard()
    },

    async loadDashboard() {
      try {
        const response = await api.get('/trekker/dashboard')
        this.stats = response.data
      } catch (error) {
        this.handleError(error)
      }
    },

    async openTreks() {
      this.activeSection = 'treks'
      await this.loadTreks()
    },

    async loadTreks() {
      try {
        const response = await api.get('/trekker/treks', {
          params: this.filters
        })

        this.treks = response.data.treks
      } catch (error) {
        this.handleError(error)
      }
    },

    async bookTrek(trek) {
      const confirmed = window.confirm(
        `Book "${trek.name}" for ₹${trek.price}?`
      )

      if (!confirmed) {
        return
      }

      this.clearMessages()

      try {
        const response = await api.post(
          `/trekker/treks/${trek.id}/book`
        )

        this.message = response.data.message

        await Promise.all([
          this.loadTreks(),
          this.loadDashboard()
        ])
      } catch (error) {
        this.handleError(error)
      }
    },

    async openBookings() {
      this.activeSection = 'bookings'
      await this.loadBookings()
    },

    async loadBookings() {
      try {
        const response = await api.get('/trekker/bookings')
        this.bookings = response.data.bookings
      } catch (error) {
        this.handleError(error)
      }
    },

    async cancelBooking(booking) {
      const confirmed = window.confirm(
        `Cancel your booking for "${booking.trek_name}"?`
      )

      if (!confirmed) {
        return
      }

      this.clearMessages()

      try {
        const response = await api.put(
          `/trekker/bookings/${booking.id}/cancel`
        )

        this.message = response.data.message

        await Promise.all([
          this.loadBookings(),
          this.loadDashboard()
        ])
      } catch (error) {
        this.handleError(error)
      }
    },

    async openHistory() {
      this.activeSection = 'history'
      await this.loadHistory()
    },

    async loadHistory() {
      try {
        const response = await api.get('/trekker/history')
        this.history = response.data.history
      } catch (error) {
        this.handleError(error)
      }
    },

    async openProfile() {
      this.activeSection = 'profile'

      try {
        const response = await api.get('/trekker/profile')

        this.user = response.data.user

        this.profileForm = {
          name: this.user.name,
          phone: this.user.phone || ''
        }
      } catch (error) {
        this.handleError(error)
      }
    },

    async updateProfile() {
      this.saving = true
      this.clearMessages()

      try {
        const response = await api.put(
          '/trekker/profile',
          this.profileForm
        )

        this.user = response.data.user

        localStorage.setItem(
          'user',
          JSON.stringify(this.user)
        )

        this.message = response.data.message
      } catch (error) {
        this.handleError(error)
      } finally {
        this.saving = false
      }
    },

    formatDate(dateValue) {
      if (!dateValue) {
        return '-'
      }

      return new Date(dateValue).toLocaleDateString()
    },

    handleError(error) {
      this.errorMessage =
        error.response?.data?.message ||
        error.response?.data?.msg ||
        'Something went wrong. Please try again.'
    },

    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')

      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.trekker-page {
  min-height: 100vh;
  background-color: #f5f7f5;
}

.profile-card {
  max-width: 650px;
}

.card {
  border: 0;
}
</style>