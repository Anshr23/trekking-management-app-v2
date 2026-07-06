<template>
  <div class="staff-page">
    <nav class="navbar navbar-dark bg-primary px-4">
      <span class="navbar-brand mb-0 h1">
        TMA Trek Staff
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
            ? 'btn-primary'
            : 'btn-outline-primary'"
          @click="openDashboard"
        >
          Dashboard
        </button>

        <button
          class="btn"
          :class="activeSection === 'treks'
            ? 'btn-primary'
            : 'btn-outline-primary'"
          @click="openTreks"
        >
          My Assigned Treks
        </button>
      </div>

      <!-- Dashboard -->
      <section v-if="activeSection === 'dashboard'">
        <div class="mb-4">
          <h2>Welcome, {{ user.name }}</h2>

          <p class="text-muted">
            Manage your assigned treks and participants.
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

      <!-- Assigned Treks -->
      <section v-if="activeSection === 'treks'">
        <h2 class="mb-4">My Assigned Treks</h2>

        <div class="row g-4">
          <div
            v-for="trek in treks"
            :key="trek.id"
            class="col-lg-6"
          >
            <div class="card shadow-sm h-100">
              <div class="card-body">
                <div
                  class="d-flex justify-content-between
                         align-items-start mb-3"
                >
                  <div>
                    <h4 class="mb-1">
                      {{ trek.name }}
                    </h4>

                    <p class="text-muted mb-0">
                      {{ trek.location }}
                    </p>
                  </div>

                  <span
                    class="badge"
                    :class="statusBadgeClass(trek.status)"
                  >
                    {{ trek.status }}
                  </span>
                </div>

                <div class="row mb-3">
                  <div class="col-6">
                    <small class="text-muted">
                      Participants
                    </small>

                    <div class="fw-bold">
                      {{ trek.participant_count }}
                    </div>
                  </div>

                  <div class="col-6">
                    <small class="text-muted">
                      Available Slots
                    </small>

                    <div class="fw-bold">
                      {{ trek.available_slots }}
                      /
                      {{ trek.total_slots }}
                    </div>
                  </div>
                </div>

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
                    <strong>Start:</strong>
                    {{ formatDate(trek.start_date) }}
                  </div>

                  <div>
                    <strong>End:</strong>
                    {{ formatDate(trek.end_date) }}
                  </div>
                </div>

                <div class="mb-3">
                  <label class="form-label">
                    Update Total Slots
                  </label>

                  <div class="input-group">
                    <input
                      v-model.number="trek.slotInput"
                      type="number"
                      min="1"
                      class="form-control"
                    />

                    <button
                      class="btn btn-outline-primary"
                      @click="updateSlots(trek)"
                    >
                      Update
                    </button>
                  </div>
                </div>

                <div class="mb-3">
                  <label class="form-label">
                    Update Trek Status
                  </label>

                  <div class="input-group">
                    <select
                      v-model="trek.statusInput"
                      class="form-select"
                      :disabled="trek.status === 'Completed'"
                    >
                      <option value="Open">Open</option>
                      <option value="Closed">Closed</option>
                      <option value="Ongoing">Ongoing</option>
                      <option value="Completed">Completed</option>
                    </select>

                    <button
                      class="btn btn-outline-primary"
                      :disabled="trek.status === 'Completed'"
                      @click="updateStatus(trek)"
                    >
                      Update
                    </button>
                  </div>
                </div>

                <button
                  class="btn btn-primary w-100"
                  @click="viewParticipants(trek)"
                >
                  View Participants
                </button>
              </div>
            </div>
          </div>

          <div
            v-if="treks.length === 0"
            class="col-12"
          >
            <div class="alert alert-info">
              No treks have been assigned to you yet.
            </div>
          </div>
        </div>
      </section>

      <!-- Participants -->
      <section v-if="activeSection === 'participants'">
        <div
          class="d-flex justify-content-between
                 align-items-center mb-4"
        >
          <div>
            <h2 class="mb-1">
              Participants
            </h2>

            <p class="text-muted mb-0">
              {{ selectedTrek?.name }}
            </p>
          </div>

          <button
            class="btn btn-outline-primary"
            @click="openTreks"
          >
            Back to Treks
          </button>
        </div>

        <div class="card shadow-sm">
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover align-middle">
                <thead>
                  <tr>
                    <th>User ID</th>
                    <th>Participant</th>
                    <th>Phone</th>
                    <th>Booking Date</th>
                    <th>Status</th>
                    <th>Payment</th>
                  </tr>
                </thead>

                <tbody>
                  <tr
                    v-for="participant in participants"
                    :key="participant.booking_id"
                  >
                    <td>{{ participant.user_id }}</td>

                    <td>
                      <strong>
                        {{ participant.name }}
                      </strong>

                      <div class="small text-muted">
                        {{ participant.email }}
                      </div>
                    </td>

                    <td>
                      {{ participant.phone || 'Not provided' }}
                    </td>

                    <td>
                      {{ formatDate(participant.booking_date) }}
                    </td>

                    <td>
                      <span class="badge text-bg-primary">
                        {{ participant.booking_status }}
                      </span>
                    </td>

                    <td>
                      {{ participant.payment_status }}
                    </td>
                  </tr>

                  <tr v-if="participants.length === 0">
                    <td
                      colspan="6"
                      class="text-center text-muted py-4"
                    >
                      No registered participants for this trek.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import api from '../../services/api'

export default {
  name: 'StaffDashboard',

  data() {
    return {
      user: JSON.parse(localStorage.getItem('user')) || {},

      activeSection: 'dashboard',

      stats: {
        assigned_treks: 0,
        total_participants: 0,
        ongoing_treks: 0,
        completed_treks: 0
      },

      treks: [],
      participants: [],
      selectedTrek: null,

      message: '',
      errorMessage: ''
    }
  },

  computed: {
    dashboardCards() {
      return [
        {
          label: 'Assigned Treks',
          value: this.stats.assigned_treks
        },
        {
          label: 'Total Participants',
          value: this.stats.total_participants
        },
        {
          label: 'Ongoing Treks',
          value: this.stats.ongoing_treks
        },
        {
          label: 'Completed Treks',
          value: this.stats.completed_treks
        }
      ]
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
        const response = await api.get('/staff/dashboard')
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
        const response = await api.get('/staff/treks')

        this.treks = response.data.treks.map((trek) => {
          return {
            ...trek,
            slotInput: trek.total_slots,
            statusInput: trek.status
          }
        })
      } catch (error) {
        this.handleError(error)
      }
    },

    async updateSlots(trek) {
      this.clearMessages()

      try {
        const response = await api.put(
          `/staff/treks/${trek.id}/slots`,
          {
            total_slots: trek.slotInput
          }
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

    async updateStatus(trek) {
      const confirmed = window.confirm(
        `Change "${trek.name}" status to ${trek.statusInput}?`
      )

      if (!confirmed) {
        return
      }

      this.clearMessages()

      try {
        const response = await api.put(
          `/staff/treks/${trek.id}/status`,
          {
            status: trek.statusInput
          }
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

    async viewParticipants(trek) {
      this.clearMessages()

      try {
        const response = await api.get(
          `/staff/treks/${trek.id}/participants`
        )

        this.selectedTrek = response.data.trek
        this.participants = response.data.participants
        this.activeSection = 'participants'
      } catch (error) {
        this.handleError(error)
      }
    },

    statusBadgeClass(status) {
      if (status === 'Open') {
        return 'text-bg-success'
      }

      if (status === 'Ongoing') {
        return 'text-bg-primary'
      }

      if (status === 'Completed') {
        return 'text-bg-dark'
      }

      return 'text-bg-secondary'
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
.staff-page {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.card {
  border: 0;
}
</style>