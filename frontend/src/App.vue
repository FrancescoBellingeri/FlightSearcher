<template>
  <div class="min-h-screen bg-slate-950 text-white font-sans">
    <!-- Header -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-40">
      <div class="max-w-5xl mx-auto px-6 py-4 flex items-center gap-3">
        <span class="text-2xl">✈️</span>
        <div>
          <h1 class="text-xl font-bold text-white tracking-tight">FlightSearcher</h1>
          <p class="text-xs text-slate-400">Powered by Kiwi.com</p>
        </div>
      </div>
    </header>

    <main class="max-w-5xl mx-auto px-4 sm:px-6 py-6 sm:py-10 space-y-8 sm:space-y-10">

      <!-- Search Card -->
      <section class="bg-slate-900 border border-slate-700 rounded-2xl p-5 sm:p-8 shadow-2xl">
        <h2 class="text-2xl font-bold mb-1 text-white">🔍 New Search</h2>
        <p class="text-slate-400 text-sm mb-8">Fill in the parameters and search all available flights for the month.</p>

        <form @submit.prevent="startSearch" class="space-y-6">

          <!-- Airports -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
            <AirportInput
              id="departure-airport"
              label="🛫 Departure Airport"
              placeholder="e.g. MXP — Milan Malpensa"
              v-model="form.departure_airport"
              v-model:displayLabel="form.departure_label"
            />
            <AirportInput
              id="arrival-airport"
              label="🛬 Arrival Airport"
              placeholder="e.g. IST — Istanbul"
              v-model="form.arrival_airport"
              v-model:displayLabel="form.arrival_label"
            />
          </div>

          <!-- Month, start day, duration -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6">
            <!-- Month -->
            <div>
              <label id="month-label" class="block text-sm font-semibold text-slate-300 mb-1">📅 Departure Month</label>

              <!-- Overlay to close the dropdown on outside click -->
              <div v-if="monthDropdownOpen" @click="monthDropdownOpen = false" class="fixed inset-0 z-40"></div>

              <div class="relative z-50">
                <button
                  type="button"
                  @click="monthDropdownOpen = !monthDropdownOpen"
                  aria-labelledby="month-label"
                  class="w-full px-4 py-3 rounded-xl bg-slate-800 border border-slate-600 text-white font-medium focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/30 transition-all duration-200 cursor-pointer flex justify-between items-center"
                >
                  <span>{{ currentMonthLabel }}</span>
                  <svg class="h-4 w-4 text-slate-400 transition-transform duration-200" :class="{ 'rotate-180': monthDropdownOpen }" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
                </button>

                <!-- Custom Dropdown List -->
                <div
                  v-if="monthDropdownOpen"
                  class="absolute top-full left-0 right-0 mt-2 bg-slate-800 border border-slate-600 rounded-xl shadow-2xl overflow-hidden"
                >
                  <ul class="max-h-[240px] overflow-y-auto divide-y divide-slate-700/50">
                    <li
                      v-for="m in nextMonths"
                      :key="m.value"
                      @click="selectMonth(m.value)"
                      class="px-4 py-3 hover:bg-slate-700 cursor-pointer transition-colors duration-150 flex items-center justify-between text-slate-300 hover:text-white"
                      :class="{ 'bg-sky-500/20 text-sky-400 font-bold': form.departure_month === m.value }"
                    >
                      <span>{{ m.fullLabel }}</span>
                      <span v-if="form.departure_month === m.value" class="text-sky-400 text-sm">✓</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- Start Day -->
            <div>
              <label for="start-day" class="block text-sm font-semibold text-slate-300 mb-1">📆 Search Start Day</label>
              <input
                id="start-day"
                type="number"
                v-model.number="form.start_day"
                min="1"
                max="31"
                required
                placeholder="e.g. 1"
                class="w-full px-4 py-3 rounded-xl bg-slate-800 border border-slate-600 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/30 transition-all duration-200"
              />
              <p class="mt-1 text-xs text-slate-500">The search will start from this day of the month</p>
            </div>

            <!-- Trip Duration -->
            <div>
              <label for="trip-duration" class="block text-sm font-semibold text-slate-300 mb-1">⏱️ Trip Duration (days)</label>
              <input
                id="trip-duration"
                type="number"
                v-model.number="form.trip_duration"
                min="1"
                required
                placeholder="e.g. 7"
                class="w-full px-4 py-3 rounded-xl bg-slate-800 border border-slate-600 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/30 transition-all duration-200"
              />
              <p class="mt-1 text-xs text-slate-500">Number of nights / days of stay</p>
            </div>
          </div>

          <!-- Weekend Requirement -->
          <div>
            <label class="block text-sm font-semibold text-slate-300 mb-3">🗓️ Weekend Requirements</label>
            <div class="grid grid-cols-3 gap-3">
              <label
                v-for="opt in weekendOptions"
                :key="opt.value"
                :for="`weekend-${opt.value}`"
                :class="[
                  'flex flex-col items-center gap-1 p-3 sm:p-4 rounded-xl border-2 cursor-pointer transition-all duration-200',
                  form.weekend_requirement === opt.value
                    ? 'border-sky-500 bg-sky-500/10 text-sky-400'
                    : 'border-slate-700 bg-slate-800 text-slate-400 hover:border-slate-500'
                ]"
              >
                <input
                  :id="`weekend-${opt.value}`"
                  type="radio"
                  :value="opt.value"
                  v-model="form.weekend_requirement"
                  class="sr-only"
                />
                <span class="text-2xl">{{ opt.icon }}</span>
                <span class="text-sm font-semibold">{{ opt.label }}</span>
                <span class="text-xs text-center leading-tight opacity-70">{{ opt.desc }}</span>
              </label>
            </div>
          </div>

          <!-- Advanced Filters -->
          <div class="border border-slate-700 rounded-xl p-5 space-y-5">
            <h3 class="text-sm font-semibold text-slate-300">⚙️ Advanced Filters</h3>

            <!-- Times -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
              <div>
                <label class="block text-xs font-semibold text-slate-400 mb-2">🛫 Outbound departure time</label>
                <div class="flex items-center gap-2">
                  <input type="number" v-model.number="form.out_dep_from" min="0" max="23" class="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-600 text-white text-sm focus:outline-none focus:border-sky-500" placeholder="From (0)" />
                  <span class="text-slate-500 shrink-0">—</span>
                  <input type="number" v-model.number="form.out_dep_to" min="1" max="24" class="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-600 text-white text-sm focus:outline-none focus:border-sky-500" placeholder="To (24)" />
                </div>
                <p class="mt-1 text-xs text-slate-500">Hours (0–24)</p>
              </div>
              <div>
                <label class="block text-xs font-semibold text-slate-400 mb-2">🛬 Return departure time</label>
                <div class="flex items-center gap-2">
                  <input type="number" v-model.number="form.ret_dep_from" min="0" max="23" class="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-600 text-white text-sm focus:outline-none focus:border-sky-500" placeholder="From (0)" />
                  <span class="text-slate-500 shrink-0">—</span>
                  <input type="number" v-model.number="form.ret_dep_to" min="1" max="24" class="w-full px-3 py-2 rounded-lg bg-slate-800 border border-slate-600 text-white text-sm focus:outline-none focus:border-sky-500" placeholder="To (24)" />
                </div>
                <p class="mt-1 text-xs text-slate-500">Hours (0–24)</p>
              </div>
            </div>

            <!-- Stops -->
            <div>
              <label class="block text-xs font-semibold text-slate-400 mb-2">🔀 Number of stops</label>
              <div class="grid grid-cols-2 md:flex gap-2 sm:gap-3">
                <label
                  v-for="opt in stopOptions"
                  :key="opt.value"
                  :class="[
                    'flex-1 flex flex-col items-center gap-1 p-2 sm:p-3 rounded-xl border-2 cursor-pointer transition-all duration-200 text-center',
                    form.stop_number === opt.value
                      ? 'border-sky-500 bg-sky-500/10 text-sky-400'
                      : 'border-slate-700 bg-slate-800 text-slate-400 hover:border-slate-500'
                  ]"
                >
                  <input type="radio" :value="opt.value" v-model="form.stop_number" class="sr-only" />
                  <span class="text-lg">{{ opt.icon }}</span>
                  <span class="text-xs font-semibold">{{ opt.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Submit + Progress -->
          <div class="flex flex-col sm:flex-row items-center gap-4 pt-2">
            <button
              type="submit"
              :disabled="loading"
              class="w-full sm:w-auto shrink-0 flex items-center justify-center gap-2 px-8 py-3 bg-sky-600 hover:bg-sky-500 disabled:bg-slate-700 disabled:text-slate-500 text-white font-semibold rounded-xl transition-all duration-200 shadow-lg hover:shadow-sky-500/25 disabled:cursor-not-allowed"
            >
              <span v-if="loading" class="animate-spin">⏳</span>
              <span v-else>🚀</span>
              {{ loading ? 'Searching...' : 'Start Search' }}
            </button>

            <!-- Progress Bar inline -->
            <div v-if="loading" class="w-full space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="text-xs text-slate-400 animate-pulse truncate pr-2">
                  {{ queued ? 'Waiting for another search to finish…' : searchingDate ? `Searching ${formatDate(searchingDate)}…` : 'Initializing…' }}
                </span>
                <span class="text-xs text-slate-500 font-mono tabular-nums shrink-0">
                  {{ total > 0 ? `${Math.round((progress / total) * 100)}%` : '0%' }}
                  <span v-if="results.length > 0" class="ml-1 text-emerald-400">· {{ results.length }} found</span>
                </span>
              </div>
              <div class="h-2 bg-slate-800 rounded-full overflow-hidden">
                <div
                  class="h-full bg-sky-500 rounded-full transition-all duration-500 ease-out"
                  :style="{ width: total > 0 ? `${Math.round((progress / total) * 100)}%` : '0%' }"
                ></div>
              </div>
            </div>
          </div>

        </form>
      </section>

      <!-- Error -->
      <div v-if="error" class="bg-red-950/50 border border-red-700 rounded-2xl p-6 flex items-start gap-4">
        <span class="text-2xl shrink-0">⚠️</span>
        <div>
          <p class="font-semibold text-red-400 mb-1">Search error</p>
          <p class="text-sm text-red-300">{{ error }}</p>
        </div>
      </div>

      <!-- Results -->
      <section v-if="results.length > 0">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-6 gap-3">
          <div>
            <h2 class="text-2xl font-bold text-white">📋 Results</h2>
            <p class="text-slate-400 text-sm mt-1">
              {{ results.length }} combination{{ results.length > 1 ? 's' : '' }} found
              <span v-if="!loading"> · sorted by price</span>
            </p>
          </div>
          <span
            class="w-full sm:w-auto text-center px-4 py-2 rounded-xl text-sm font-semibold border"
            :class="loading
              ? 'bg-sky-600/20 border-sky-600/40 text-sky-400'
              : 'bg-emerald-600/20 border-emerald-600/40 text-emerald-400'"
          >
            {{ loading ? '🔍 Search in progress…' : '✅ Search completed' }}
          </span>
        </div>

        <div class="space-y-4">
          <div
            v-for="(item, idx) in results"
            :key="idx"
            class="bg-slate-900 border border-slate-700 rounded-2xl overflow-hidden hover:border-slate-500 transition-all duration-200 group"
          >
            <!-- Result header -->
            <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between px-4 sm:px-6 py-4 border-b border-slate-700/50 bg-slate-800/30 gap-3 sm:gap-0">
              <div class="flex items-center gap-3 sm:gap-4 w-full">
                <span class="text-lg font-bold text-sky-400 bg-sky-500/10 border border-sky-500/30 rounded-lg px-3 py-1 shrink-0">#{{ idx + 1 }}</span>
                <div class="min-w-0 flex-1">
                  <p class="font-semibold text-white text-base sm:text-lg truncate flex flex-wrap items-center">
                    {{ formatDate(item.search_date.departure) }}
                    <span class="text-slate-400 font-normal mx-2">→</span>
                    {{ formatDate(item.search_date.return) }}
                  </p>
                  <p class="text-sm text-slate-400">{{ daysCount(item.search_date.departure, item.search_date.return) }} day trip</p>
                </div>
              </div>
            </div>

            <!-- Flights -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-0 divide-y md:divide-y-0 md:divide-x divide-slate-700/50">
              <!-- Best -->
              <div class="p-4 sm:p-6">
                <div class="flex items-center gap-2 mb-4">
                  <span class="text-yellow-400">⭐</span>
                  <span class="text-sm font-bold text-yellow-400 uppercase tracking-wide">Best Flight</span>
                  <span class="ml-auto text-xl font-bold text-white">€{{ item.best_flight.price.toFixed(2) }}</span>
                </div>
                <FlightCard :flight="item.best_flight" />
              </div>
              <!-- Cheapest -->
              <div class="p-4 sm:p-6">
                <div class="flex items-center gap-2 mb-4">
                  <span class="text-emerald-400">💰</span>
                  <span class="text-sm font-bold text-emerald-400 uppercase tracking-wide">Cheapest</span>
                  <span class="ml-auto text-xl font-bold text-white">€{{ item.cheapest_flight.price.toFixed(2) }}</span>
                </div>
                <FlightCard :flight="item.cheapest_flight" />
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Empty state -->
      <div v-else-if="!loading && !error" class="text-center py-10 sm:py-16 text-slate-600">
        <p class="text-5xl mb-4">🗺️</p>
        <p class="text-lg font-medium">No search performed yet</p>
        <p class="text-sm mt-1">Fill in the form above and press "Start Search"</p>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import AirportInput from './components/AirportInput.vue'
import FlightCard from './components/FlightCard.vue'

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'
const WS_BASE = API_BASE.replace(/^http/, 'ws')

const form = reactive({
  departure_airport: '',
  departure_label: '',
  arrival_airport: '',
  arrival_label: '',
  departure_month: new Date().toISOString().slice(0, 7),
  start_day: 1,
  trip_duration: 7,
  weekend_requirement: 'none',
  out_dep_from: null,
  out_dep_to: null,
  ret_dep_from: null,
  ret_dep_to: null,
  stop_number: null,
})

const stopOptions = [
  { value: null, icon: '🔀', label: 'Any' },
  { value: 0,    icon: '✈️', label: 'Direct' },
  { value: 1,    icon: '1️⃣', label: 'Max 1 stop' },
  { value: 2,    icon: '2️⃣', label: 'Max 2 stops' },
]

const weekendOptions = [
  { value: 'none', icon: '❌', label: 'None',         desc: 'No requirement' },
  { value: 'one',  icon: '📅', label: 'At least 1',  desc: 'At least one weekend day' },
  { value: 'full', icon: '🗓️', label: 'Full weekend', desc: 'Both Saturday and Sunday' },
]

const nextMonths = computed(() => {
  const months = []
  const today = new Date()
  let y = today.getFullYear()
  let m = today.getMonth()

  for (let i = 0; i < 24; i++) {
    const d = new Date(y, m + i, 1)
    const val = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
    const monthStr = d.toLocaleString('en-US', { month: 'long' })
    const yearStr = d.getFullYear().toString()
    months.push({ value: val, fullLabel: `${monthStr} ${yearStr}` })
  }
  return months
})

const monthDropdownOpen = ref(false)
const currentMonthLabel = computed(() => {
  const found = nextMonths.value.find(m => m.value === form.departure_month)
  return found ? found.fullLabel : 'Select Month'
})
function selectMonth(val) {
  form.departure_month = val
  monthDropdownOpen.value = false
}

const loading = ref(false)
const queued = ref(false)
const error = ref(null)
const results = ref([])
const progress = ref(0)
const total = ref(0)
const searchingDate = ref(null)

async function startSearch() {
  if (!form.departure_airport || !form.arrival_airport) {
    error.value = 'Please enter both a departure and an arrival airport.'
    return
  }

  loading.value = true
  queued.value = false
  error.value = null
  results.value = []
  progress.value = 0
  total.value = 0
  searchingDate.value = null

  const outFrom = form.out_dep_from ?? 0
  const outTo   = form.out_dep_to   ?? 24
  const retFrom = form.ret_dep_from ?? 0
  const retTo   = form.ret_dep_to   ?? 24
  const hasTimeFilter = form.out_dep_from !== null || form.out_dep_to !== null || form.ret_dep_from !== null || form.ret_dep_to !== null
  const times = hasTimeFilter ? `${outFrom}-${outTo}-0-24_${retFrom}-${retTo}-0-24` : null

  const params = {
    departure_airport: form.departure_airport,
    arrival_airport: form.arrival_airport,
    departure_month: form.departure_month,
    start_day: form.start_day,
    trip_duration: form.trip_duration,
    weekend_requirement: form.weekend_requirement,
    times,
    stop_number: form.stop_number,
  }

  try {
    const ws = new WebSocket(`${WS_BASE}/ws/search`)

    ws.onopen = () => ws.send(JSON.stringify(params))

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data)

      if (msg.type === 'queued') {
        queued.value = true

      } else if (msg.type === 'init') {
        queued.value = false
        total.value = msg.total

      } else if (msg.type === 'progress') {
        progress.value = msg.completed
        if (msg.current_date) searchingDate.value = msg.current_date

      } else if (msg.type === 'skip') {
        progress.value = msg.completed

      } else if (msg.type === 'result') {
        progress.value = msg.completed
        results.value.push(msg.data)

      } else if (msg.type === 'done') {
        results.value.sort((a, b) => a.cheapest_flight.price - b.cheapest_flight.price)
        if (results.value.length === 0) {
          error.value = 'No flights found for the selected parameters.'
        }
        loading.value = false
        searchingDate.value = null

      } else if (msg.type === 'error') {
        error.value = msg.message || 'Unknown error from backend.'
        loading.value = false
      }
    }

    ws.onerror = () => {
      error.value = 'Could not connect to backend.'
      loading.value = false
    }

    ws.onclose = () => {
      if (loading.value) {
        loading.value = false
      }
    }

  } catch (e) {
    error.value = `Could not connect to backend: ${e.message}`
    loading.value = false
  }
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const [y, m, d] = dateStr.split('-')
  const date = new Date(y, m - 1, d)
  return date.toLocaleDateString('en-US', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' })
}

function daysCount(dep, ret) {
  const d1 = new Date(dep)
  const d2 = new Date(ret)
  return Math.round((d2 - d1) / (1000 * 60 * 60 * 24))
}
</script>

<style>
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
