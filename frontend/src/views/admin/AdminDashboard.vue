<template>
  <div class="admin-page">
    <nav class="navbar navbar-dark bg-dark px-4">
      <span class="navbar-brand mb-0 h1">
        TMA Admin
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

    <div class="container-fluid">
      <div class="row">
        <div class="col-md-2 bg-light sidebar p-3">
          <h6 class="text-muted mb-3">
            MANAGEMENT
          </h6>

          <button
            class="btn w-100 text-start mb-2"
            :class="activeSection === 'dashboard'
              ? 'btn-dark'
              : 'btn-light'"
            @click="activeSection = 'dashboard'"
          >
            Dashboard
          </button>

          <button
            class="btn w-100 text-start mb-2"
            :class="activeSection === 'treks'
              ? 'btn-dark'
              : 'btn-light'"
            @click="openTreks"
          >
            Treks
          </button>

          <button
            class="btn w-100 text-start mb-2"
            :class="activeSection === 'staff'
              ? 'btn-dark'
              : 'btn-light'"
            @click="openStaff"
          >
            Trek Staff
          </button>

          <button
            class="btn w-100 text-start mb-2"
            :class="activeSection === 'users'
              ? 'btn-dark'
              : 'btn-light'"
            @click="openUsers"
          >
            Users
          </button>

          <button
            class="btn w-100 text-start mb-2"
            :class="activeSection === 'bookings'
              ? 'btn-dark'
              : 'btn-light'"
            @click="openBookings"
          >
            Bookings
          </button>
        </div>

        <main class="col-md-10 p-4">
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

          <!-- Dashboard -->
          <section v-if="activeSection === 'dashboard'">
            <h2 class="mb-4">Admin Dashboard</h2>

            <div class="row g-3">
              <div
                v-for="card in dashboardCards"
                :key="card.label"
                class="col-md-6 col-xl-4"
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

          <!-- Treks -->
          <section v-if="activeSection === 'treks'">
            <div
              class="d-flex justify-content-between
                     align-items-center mb-4"
            >
              <h2 class="mb-0">Manage Treks</h2>

              <button
                class="btn btn-success"
                @click="showCreateTrekForm"
              >
                Add New Trek
              </button>
            </div>

            <div
              v-if="showTrekForm"
              class="card shadow-sm mb-4"
            >
              <div class="card-body">
                <h4 class="mb-3">
                  {{ editingTrekId ? 'Edit Trek' : 'Create Trek' }}
                </h4>

                <form @submit.prevent="saveTrek">
                  <div class="row g-3">
                    <div class="col-md-6">
                      <label class="form-label">
                        Trek Name
                      </label>

                      <input
                        v-model.trim="trekForm.name"
                        class="form-control"
                        required
                      />
                    </div>

                    <div class="col-md-6">
                      <label class="form-label">
                        Location
                      </label>

                      <input
                        v-model.trim="trekForm.location"
                        class="form-control"
                        required
                      />
                    </div>

                    <div class="col-md-4">
                      <label class="form-label">
                        Difficulty
                      </label>

                      <select
                        v-model="trekForm.difficulty"
                        class="form-select"
                        required
                      >
                        <option value="">Select difficulty</option>
                        <option value="Easy">Easy</option>
                        <option value="Moderate">Moderate</option>
                        <option value="Hard">Hard</option>
                      </select>
                    </div>

                    <div class="col-md-4">
                      <label class="form-label">
                        Duration (days)
                      </label>

                      <input
                        v-model.number="trekForm.duration"
                        type="number"
                        min="1"
                        class="form-control"
                        required
                      />
                    </div>

                    <div class="col-md-4">
                      <label class="form-label">
                        Total Slots
                      </label>

                      <input
                        v-model.number="trekForm.total_slots"
                        type="number"
                        min="1"
                        class="form-control"
                        required
                      />
                    </div>

                    <div class="col-md-6">
                      <label class="form-label">
                        Start Date
                      </label>

                      <input
                        v-model="trekForm.start_date"
                        type="date"
                        class="form-control"
                        required
                      />
                    </div>

                    <div class="col-md-6">
                      <label class="form-label">
                        End Date
                      </label>

                      <input
                        v-model="trekForm.end_date"
                        type="date"
                        class="form-control"
                        required
                      />
                    </div>

                    <div class="col-md-4">
                      <label class="form-label">
                        Price
                      </label>

                      <input
                        v-model.number="trekForm.price"
                        type="number"
                        min="0"
                        class="form-control"
                      />
                    </div>

                    <div class="col-md-4">
                      <label class="form-label">
                        Altitude (feet)
                      </label>

                      <input
                        v-model.number="trekForm.altitude"
                        type="number"
                        min="0"
                        class="form-control"
                      />
                    </div>

                    <div
                      v-if="editingTrekId"
                      class="col-md-4"
                    >
                      <label class="form-label">
                        Status
                      </label>

                      <select
                        v-model="trekForm.status"
                        class="form-select"
                      >
                        <option value="Pending">Pending</option>
                        <option value="Approved">Approved</option>
                        <option value="Open">Open</option>
                        <option value="Closed">Closed</option>
                        <option value="Ongoing">Ongoing</option>
                        <option value="Completed">Completed</option>
                      </select>
                    </div>

                    <div class="col-12">
                      <label class="form-label">
                        Description
                      </label>

                      <textarea
                        v-model.trim="trekForm.description"
                        class="form-control"
                        rows="3"
                      ></textarea>
                    </div>
                  </div>

                  <div class="mt-3 d-flex gap-2">
                    <button
                      type="submit"
                      class="btn btn-primary"
                      :disabled="saving"
                    >
                      {{
                        saving
                          ? 'Saving...'
                          : editingTrekId
                            ? 'Update Trek'
                            : 'Create Trek'
                      }}
                    </button>

                    <button
                      type="button"
                      class="btn btn-secondary"
                      @click="cancelTrekForm"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            </div>

            <div class="card shadow-sm">
              <div class="card-body">
                <div class="row g-2 mb-3">
                  <div class="col-md-6">
                    <input
                      v-model.trim="trekSearch"
                      type="search"
                      class="form-control"
                      placeholder="Search by trek name or location"
                      @input="loadTreks"
                    />
                  </div>

                  <div class="col-md-3">
                    <select
                      v-model="difficultyFilter"
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
                    <select
                      v-model="statusFilter"
                      class="form-select"
                      @change="loadTreks"
                    >
                      <option value="">All statuses</option>
                      <option value="Pending">Pending</option>
                      <option value="Approved">Approved</option>
                      <option value="Open">Open</option>
                      <option value="Closed">Closed</option>
                      <option value="Ongoing">Ongoing</option>
                      <option value="Completed">Completed</option>
                    </select>
                  </div>
                </div>

                <div class="table-responsive">
                  <table class="table table-hover align-middle">
                    <thead>
                      <tr>
                        <th>ID</th>
                        <th>Trek</th>
                        <th>Difficulty</th>
                        <th>Slots</th>
                        <th>Staff</th>
                        <th>Status</th>
                        <th>Actions</th>
                      </tr>
                    </thead>

                    <tbody>
                      <tr
                        v-for="trek in treks"
                        :key="trek.id"
                      >
                        <td>{{ trek.id }}</td>

                        <td>
                          <strong>{{ trek.name }}</strong>
                          <div class="small text-muted">
                            {{ trek.location }}
                          </div>
                        </td>

                        <td>{{ trek.difficulty }}</td>

                        <td>
                          {{ trek.available_slots }}/{{ trek.total_slots }}
                        </td>

                        <td>
                          {{ trek.assigned_staff_name || 'Not assigned' }}
                        </td>

                        <td>
                          <span class="badge text-bg-secondary">
                            {{ trek.status }}
                          </span>
                        </td>

                        <td>
                          <div class="d-flex gap-2">
                            <button
                              class="btn btn-sm btn-outline-primary"
                              @click="editTrek(trek)"
                            >
                              Edit
                            </button>

                            <button
                              class="btn btn-sm btn-outline-danger"
                              @click="deleteTrek(trek)"
                            >
                              Delete
                            </button>
                          </div>
                        </td>
                      </tr>

                      <tr v-if="treks.length === 0">
                        <td
                          colspan="7"
                          class="text-center text-muted py-4"
                        >
                          No treks found.
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </section>

          <!-- Temporary placeholders -->
          <!-- <section v-if="activeSection === 'staff'">
            <h2>Trek Staff Management</h2>
            <p class="text-muted">
              Staff management UI will be added next.
            </p>
          </section> -->
          <section v-if="activeSection === 'staff'">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="mb-0">Trek Staff Management</h2>

        <button
        class="btn btn-success"
        @click="showStaffForm = !showStaffForm"
        >
        {{ showStaffForm ? 'Close Form' : 'Add Trek Staff' }}
        </button>
    </div>

    <div
        v-if="showStaffForm"
        class="card shadow-sm mb-4"
    >
        <div class="card-body">
        <h4 class="mb-3">Create Trek Staff</h4>

        <form @submit.prevent="createStaff">
            <div class="row g-3">
            <div class="col-md-6">
                <label class="form-label">
                Full Name
                </label>

                <input
                v-model.trim="staffForm.name"
                class="form-control"
                required
                />
            </div>

            <div class="col-md-6">
                <label class="form-label">
                Email
                </label>

                <input
                v-model.trim="staffForm.email"
                type="email"
                class="form-control"
                required
                />
            </div>

            <div class="col-md-6">
                <label class="form-label">
                Password
                </label>

                <input
                v-model="staffForm.password"
                type="password"
                minlength="6"
                class="form-control"
                required
                />
            </div>

            <div class="col-md-6">
                <label class="form-label">
                Phone
                </label>

                <input
                v-model.trim="staffForm.phone"
                class="form-control"
                />
            </div>

            <div class="col-md-6">
                <label class="form-label">
                Experience (years)
                </label>

                <input
                v-model.number="staffForm.experience_years"
                type="number"
                min="0"
                class="form-control"
                />
            </div>

            <div class="col-md-6">
                <label class="form-label">
                Specialization
                </label>

                <input
                v-model.trim="staffForm.specialization"
                class="form-control"
                placeholder="Example: Himalayan Treks"
                />
            </div>

            <div class="col-md-6">
                <label class="form-label">
                Emergency Contact
                </label>

                <input
                v-model.trim="staffForm.emergency_contact"
                class="form-control"
                />
            </div>

            <div class="col-12">
                <label class="form-label">
                Bio
                </label>

                <textarea
                v-model.trim="staffForm.bio"
                class="form-control"
                rows="3"
                ></textarea>
            </div>
            </div>

            <button
            type="submit"
            class="btn btn-primary mt-3"
            :disabled="saving"
            >
            {{ saving ? 'Creating...' : 'Create Staff' }}
            </button>
        </form>
        </div>
    </div>

    <div class="card shadow-sm">
        <div class="card-body">
        <input
            v-model.trim="staffSearch"
            type="search"
            class="form-control mb-3"
            placeholder="Search staff by name or email"
            @input="loadStaff"
        />

        <div class="table-responsive">
            <table class="table table-hover align-middle">
            <thead>
                <tr>
                <th>Staff</th>
                <th>Experience</th>
                <th>Specialization</th>
                <th>Assigned Treks</th>
                <th>Account</th>
                <th>Actions</th>
                </tr>
            </thead>

            <tbody>
                <tr
                v-for="staffMember in staffMembers"
                :key="staffMember.id"
                >
                <td>
                    <strong>{{ staffMember.name }}</strong>

                    <div class="small text-muted">
                    {{ staffMember.email }}
                    </div>
                </td>

                <td>
                    {{ staffMember.profile?.experience_years || 0 }} years
                </td>

                <td>
                    {{ staffMember.profile?.specialization || 'Not specified' }}
                </td>

                <td>
                    <div
                    v-if="staffMember.assigned_treks.length"
                    >
                    <span
                        v-for="trek in staffMember.assigned_treks"
                        :key="trek.id"
                        class="badge text-bg-info me-1 mb-1"
                    >
                        {{ trek.name }}
                    </span>
                    </div>

                    <span
                    v-else
                    class="text-muted"
                    >
                    None
                    </span>
                </td>

                <td>
                    <span
                    class="badge me-1"
                    :class="staffMember.is_active
                        ? 'text-bg-success'
                        : 'text-bg-secondary'"
                    >
                    {{ staffMember.is_active ? 'Active' : 'Inactive' }}
                    </span>

                    <span
                    v-if="staffMember.is_blacklisted"
                    class="badge text-bg-danger"
                    >
                    Blacklisted
                    </span>
                </td>

                <td>
                    <div class="d-flex flex-wrap gap-1">
                    <button
                        class="btn btn-sm btn-outline-secondary"
                        @click="toggleActive(staffMember)"
                    >
                        {{
                        staffMember.is_active
                            ? 'Deactivate'
                            : 'Activate'
                        }}
                    </button>

                    <button
                        class="btn btn-sm btn-outline-danger"
                        @click="toggleBlacklist(staffMember)"
                    >
                        {{
                        staffMember.is_blacklisted
                            ? 'Unblacklist'
                            : 'Blacklist'
                        }}
                    </button>
                    </div>
                </td>
                </tr>

                <tr v-if="staffMembers.length === 0">
                <td
                    colspan="6"
                    class="text-center text-muted py-4"
                >
                    No staff members found.
                </td>
                </tr>
            </tbody>
            </table>
        </div>
        </div>
    </div>

    <div class="card shadow-sm mt-4">
        <div class="card-body">
        <h4 class="mb-3">Assign Staff to Trek</h4>

        <form
            class="row g-3 align-items-end"
            @submit.prevent="assignStaff"
        >
            <div class="col-md-5">
            <label class="form-label">
                Trek
            </label>

            <select
                v-model="assignmentForm.trek_id"
                class="form-select"
                required
            >
                <option value="">Select trek</option>

                <option
                v-for="trek in allTreks"
                :key="trek.id"
                :value="trek.id"
                >
                {{ trek.name }}
                {{ trek.assigned_staff_name
                    ? `— ${trek.assigned_staff_name}`
                    : '— Not assigned' }}
                </option>
            </select>
            </div>

            <div class="col-md-5">
            <label class="form-label">
                Trek Staff
            </label>

            <select
                v-model="assignmentForm.staff_id"
                class="form-select"
                required
            >
                <option value="">Select staff</option>

                <option
                v-for="staffMember in availableStaff"
                :key="staffMember.id"
                :value="staffMember.id"
                >
                {{ staffMember.name }}
                </option>
            </select>
            </div>

            <div class="col-md-2">
            <button class="btn btn-primary w-100">
                Assign
            </button>
            </div>
        </form>
        </div>
    </div>
    </section>

          <!-- <section v-if="activeSection === 'users'">
            <h2>User Management</h2>
            <p class="text-muted">
              User management UI will be added next.
            </p>
          </section> -->
          <section v-if="activeSection === 'users'">
    <h2 class="mb-4">User Management</h2>

    <div class="card shadow-sm">
        <div class="card-body">
        <input
            v-model.trim="userSearch"
            type="search"
            class="form-control mb-3"
            placeholder="Search trekkers by name or email"
            @input="loadUsers"
        />

        <div class="table-responsive">
            <table class="table table-hover align-middle">
            <thead>
                <tr>
                <th>ID</th>
                <th>Trekker</th>
                <th>Phone</th>
                <th>Joined</th>
                <th>Account</th>
                <th>Actions</th>
                </tr>
            </thead>

            <tbody>
                <tr
                v-for="trekker in trekkers"
                :key="trekker.id"
                >
                <td>{{ trekker.id }}</td>

                <td>
                    <strong>{{ trekker.name }}</strong>

                    <div class="small text-muted">
                    {{ trekker.email }}
                    </div>
                </td>

                <td>{{ trekker.phone || 'Not provided' }}</td>

                <td>
                    {{ formatDate(trekker.created_at) }}
                </td>

                <td>
                    <span
                    class="badge me-1"
                    :class="trekker.is_active
                        ? 'text-bg-success'
                        : 'text-bg-secondary'"
                    >
                    {{ trekker.is_active ? 'Active' : 'Inactive' }}
                    </span>

                    <span
                    v-if="trekker.is_blacklisted"
                    class="badge text-bg-danger"
                    >
                    Blacklisted
                    </span>
                </td>

                <td>
                    <div class="d-flex flex-wrap gap-1">
                    <button
                        class="btn btn-sm btn-outline-secondary"
                        @click="toggleActive(trekker)"
                    >
                        {{
                        trekker.is_active
                            ? 'Deactivate'
                            : 'Activate'
                        }}
                    </button>

                    <button
                        class="btn btn-sm btn-outline-danger"
                        @click="toggleBlacklist(trekker)"
                    >
                        {{
                        trekker.is_blacklisted
                            ? 'Unblacklist'
                            : 'Blacklist'
                        }}
                    </button>
                    </div>
                </td>
                </tr>

                <tr v-if="trekkers.length === 0">
                <td
                    colspan="6"
                    class="text-center text-muted py-4"
                >
                    No trekkers found.
                </td>
                </tr>
            </tbody>
            </table>
        </div>
        </div>
    </div>
    </section>

          <!-- <section v-if="activeSection === 'bookings'">
            <h2>All Bookings</h2>
            <p class="text-muted">
              Booking records will appear here.
            </p>
          </section> -->
         <section v-if="activeSection === 'bookings'">
    <h2 class="mb-4">All Bookings & Trekking History</h2>

    <div class="card shadow-sm">
        <div class="card-body">
        <div class="row g-2 mb-3">
            <div class="col-md-8">
            <input
                v-model.trim="bookingSearch"
                type="search"
                class="form-control"
                placeholder="Search by trekker, email, trek or location"
                @input="loadBookings"
            />
            </div>

            <div class="col-md-4">
            <select
                v-model="bookingStatusFilter"
                class="form-select"
                @change="loadBookings"
            >
                <option value="">All booking statuses</option>
                <option value="Booked">Booked</option>
                <option value="Cancelled">Cancelled</option>
                <option value="Completed">Completed</option>
            </select>
            </div>
        </div>

        <div class="table-responsive">
            <table class="table table-hover align-middle">
            <thead>
                <tr>
                <th>ID</th>
                <th>Trekker</th>
                <th>Trek</th>
                <th>Location</th>
                <th>Booking Date</th>
                <th>Status</th>
                <th>Payment</th>
                </tr>
            </thead>

            <tbody>
                <tr
                v-for="booking in bookings"
                :key="booking.id"
                >
                <td>{{ booking.id }}</td>

                <td>
                    <strong>
                    {{ booking.user_name }}
                    </strong>

                    <div class="small text-muted">
                    User ID: {{ booking.user_id }}
                    </div>
                </td>

                <td>{{ booking.trek_name }}</td>

                <td>
                    {{ booking.location || '-' }}
                </td>

                <td>
                    {{ formatDate(booking.booking_date) }}
                </td>

                <td>
                    <span
                    class="badge"
                    :class="bookingStatusClass(booking.status)"
                    >
                    {{ booking.status }}
                    </span>
                </td>

                <td>
                    {{ booking.payment_status }}
                </td>
                </tr>

                <tr v-if="bookings.length === 0">
                <td
                    colspan="7"
                    class="text-center text-muted py-4"
                >
                    No booking records found.
                </td>
                </tr>
            </tbody>
            </table>
        </div>
        </div>
    </div>
    </section>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../services/api'

function emptyTrekForm() {
  return {
    name: '',
    location: '',
    description: '',
    difficulty: '',
    duration: 1,
    total_slots: 1,
    start_date: '',
    end_date: '',
    price: 0,
    altitude: '',
    status: 'Pending'
  }
}

export default {
  name: 'AdminDashboard',

  data() {
    return {
      user: JSON.parse(localStorage.getItem('user')) || {},
      activeSection: 'dashboard',

      stats: {
        total_treks: 0,
        total_users: 0,
        total_staff: 0,
        total_bookings: 0,
        active_treks: 0,
        completed_treks: 0
      },

      treks: [],
      trekSearch: '',
      difficultyFilter: '',
      statusFilter: '',

      showTrekForm: false,
      editingTrekId: null,
      trekForm: emptyTrekForm(),

      saving: false,
      message: '',
      errorMessage: '',
      staffMembers: [],
    staffSearch: '',
    showStaffForm: false,

    staffForm: {
    name: '',
    email: '',
    password: '',
    phone: '',
    experience_years: 0,
    specialization: '',
    emergency_contact: '',
    bio: ''
    },

    allTreks: [],

    assignmentForm: {
    trek_id: '',
    staff_id: ''
    },

    trekkers: [],
    userSearch: '',

    bookings: [],
    bookingSearch: '',
    bookingStatusFilter: '',
    }
  },

  computed: {
    dashboardCards() {
      return [
        {
          label: 'Total Treks',
          value: this.stats.total_treks
        },
        {
          label: 'Trekkers',
          value: this.stats.total_users
        },
        {
          label: 'Trek Staff',
          value: this.stats.total_staff
        },
        {
          label: 'Total Bookings',
          value: this.stats.total_bookings
        },
        {
          label: 'Active Treks',
          value: this.stats.active_treks
        },
        {
          label: 'Completed Treks',
          value: this.stats.completed_treks
        }
      ]
    },
    availableStaff() {
    return this.staffMembers.filter((staffMember) => {
        return (
        staffMember.is_active &&
        !staffMember.is_blacklisted
        )
    })
    }
  },

  async mounted() {
    await this.loadDashboard()
  },

  methods: {
    async loadDashboard() {
      try {
        const response = await api.get('/admin/dashboard')
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
        const response = await api.get('/admin/treks', {
          params: {
            search: this.trekSearch,
            difficulty: this.difficultyFilter,
            status: this.statusFilter
          }
        })

        this.treks = response.data.treks
      } catch (error) {
        this.handleError(error)
      }
    },

    showCreateTrekForm() {
      this.editingTrekId = null
      this.trekForm = emptyTrekForm()
      this.showTrekForm = true
    },

    editTrek(trek) {
      this.editingTrekId = trek.id

      this.trekForm = {
        name: trek.name,
        location: trek.location,
        description: trek.description || '',
        difficulty: trek.difficulty,
        duration: trek.duration,
        total_slots: trek.total_slots,
        start_date: trek.start_date,
        end_date: trek.end_date,
        price: trek.price,
        altitude: trek.altitude || '',
        status: trek.status
      }

      this.showTrekForm = true

      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      })
    },

    cancelTrekForm() {
      this.showTrekForm = false
      this.editingTrekId = null
      this.trekForm = emptyTrekForm()
    },

    async saveTrek() {
      this.saving = true
      this.message = ''
      this.errorMessage = ''

      try {
        if (this.editingTrekId) {
          await api.put(
            `/admin/treks/${this.editingTrekId}`,
            this.trekForm
          )

          this.message = 'Trek updated successfully.'
        } else {
          await api.post('/admin/treks', this.trekForm)

          this.message = 'Trek created successfully.'
        }

        this.cancelTrekForm()
        await this.loadTreks()
        await this.loadDashboard()
      } catch (error) {
        this.handleError(error)
      } finally {
        this.saving = false
      }
    },

    async deleteTrek(trek) {
      const confirmed = window.confirm(
        `Delete "${trek.name}"?`
      )

      if (!confirmed) {
        return
      }

      try {
        await api.delete(`/admin/treks/${trek.id}`)

        this.message = 'Trek deleted successfully.'

        await this.loadTreks()
        await this.loadDashboard()
      } catch (error) {
        this.handleError(error)
      }
    },
    async openStaff() {
    this.activeSection = 'staff'

    await Promise.all([
        this.loadStaff(),
        this.loadAllTreks()
    ])
    },

    async loadStaff() {
    try {
        const response = await api.get('/admin/staff', {
        params: {
            search: this.staffSearch
        }
        })

        this.staffMembers = response.data.staff
    } catch (error) {
        this.handleError(error)
    }
    },

    async createStaff() {
    this.saving = true
    this.message = ''
    this.errorMessage = ''

    try {
        await api.post('/admin/staff', this.staffForm)

        this.message = 'Trek staff created successfully.'
        this.showStaffForm = false

        this.staffForm = {
        name: '',
        email: '',
        password: '',
        phone: '',
        experience_years: 0,
        specialization: '',
        emergency_contact: '',
        bio: ''
        }

        await this.loadStaff()
        await this.loadDashboard()
    } catch (error) {
        this.handleError(error)
    } finally {
        this.saving = false
    }
    },

    async loadAllTreks() {
    try {
        const response = await api.get('/admin/treks')
        this.allTreks = response.data.treks
    } catch (error) {
        this.handleError(error)
    }
    },

    async assignStaff() {
    this.message = ''
    this.errorMessage = ''

    try {
        await api.put(
        `/admin/treks/${this.assignmentForm.trek_id}/assign-staff`,
        {
            staff_id: this.assignmentForm.staff_id
        }
        )

        this.message = 'Staff assigned to trek successfully.'

        this.assignmentForm = {
        trek_id: '',
        staff_id: ''
        }

        await Promise.all([
        this.loadStaff(),
        this.loadAllTreks()
        ])
    } catch (error) {
        this.handleError(error)
    }
    },

    async openUsers() {
    this.activeSection = 'users'
    await this.loadUsers()
    },

    async loadUsers() {
    try {
        const response = await api.get('/admin/users', {
        params: {
            search: this.userSearch
        }
        })

        this.trekkers = response.data.users
    } catch (error) {
        this.handleError(error)
    }
    },

    async toggleActive(user) {
    try {
        const response = await api.put(
        `/admin/users/${user.id}/toggle-active`
        )

        this.message = response.data.message

        if (user.role === 'staff') {
        await this.loadStaff()
        } else {
        await this.loadUsers()
        }

        await this.loadDashboard()
    } catch (error) {
        this.handleError(error)
    }
    },

    async toggleBlacklist(user) {
    try {
        const response = await api.put(
        `/admin/users/${user.id}/toggle-blacklist`
        )

        this.message = response.data.message

        if (user.role === 'staff') {
        await this.loadStaff()
        } else {
        await this.loadUsers()
        }
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
        const response = await api.get('/admin/bookings', {
        params: {
            search: this.bookingSearch,
            status: this.bookingStatusFilter
        }
        })

        this.bookings = response.data.bookings
    } catch (error) {
        this.handleError(error)
    }
    },

    bookingStatusClass(status) {
        if (status === 'Completed') {
            return 'text-bg-success'
        }

        if (status === 'Cancelled') {
            return 'text-bg-secondary'
        }

        return 'text-bg-primary'
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
.admin-page {
  min-height: 100vh;
  background-color: #f5f6f8;
}

.sidebar {
  min-height: calc(100vh - 56px);
  border-right: 1px solid #dee2e6;
}

@media (max-width: 767px) {
  .sidebar {
    min-height: auto;
    border-right: none;
    border-bottom: 1px solid #dee2e6;
  }
}
</style>